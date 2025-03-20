from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import traceback
from flask_cors import cross_origin
import traceback
from datetime import datetime
# Import utility functions
from app.utils.trading_strategy import fetch_stock_data
from app.utils.trading_strategy import momentum_trading_strategy
# Import models
from app.models.model_instance import sk_model, sk_model_trained
from app.models.model_instance import reset_model
from app.utils.ai_utils import SecretChatAgent
from app.utils.json_utils import clean_for_json
# Import Dymension CLI utilities
from app.utils.dymension_cli import DymensionCLI, format_output

# Import model from model_instance instead of app.config
from app.models.model_instance import sk_model, sk_model_trained
# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__)
# Initialize chat agent
agent = SecretChatAgent()

# Initialize Dymension CLI handler
dym_cli = DymensionCLI()

@api_bp.route("/ping", methods=["GET"])
@cross_origin()
def ping():
    """Health check endpoint"""
    return jsonify({
        "status": "ok", 
        "timestamp": datetime.now().isoformat(), 
        "version": "1.0.0"
    })

@api_bp.route("/stock-data", methods=["POST"])
@cross_origin()
def stock_data_endpoint():
    """Endpoint to fetch stock data and prepare it for the frontend chart"""
    try:
        if request.is_json:
            # Get data from JSON body
            data = request.get_json()
            symbol = data.get('symbol', 'NVDA')
            timeframe = data.get('timeframe', '1Y') 
            interval = data.get('interval', 'day')
        else: 
            symbol = request.args.get('symbol', 'NVDA')
            timeframe = request.args.get('timeframe', '1Y')
            interval = request.args.get('interval', 'day')
        print(f"Fetching stock data for {symbol} - {timeframe} - {interval}")
        
        # Fetch data using your existing functions
        data = fetch_stock_data(symbol, timeframe, interval)
        signals = momentum_trading_strategy(data)
        
        # Create response with the exact field names expected by frontend
        response = {
            'symbol': symbol,
            'timeframe': timeframe,
            'interval': interval,
            'price': data['Close'].tolist(),          
            'dates': data.index.strftime('%Y-%m-%d').tolist(), 
            'short_mavg': signals['short_mavg'].tolist(), 
            'long_mavg': signals['long_mavg'].tolist(),  
            'positions': signals['positions'].tolist()  
        }
        
        # Clean any NaN or non-JSON serializable values
        clean_for_json(response)
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'message': 'Failed to fetch stock data'
        }), 500


@api_bp.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict_endpoint():
    """API endpoint for price predictions"""
    try:
        reset_model()
        # Get parameters based on request method
        if request.method == "POST":
            if request.is_json:
                # Get data from JSON body
                data = request.get_json()
                symbol = data.get('symbol', 'NVDA')
                timeframe = data.get('timeframe', '1Y') 
                interval = data.get('interval', 'day')
                model_type = data.get('model', 'default')
            else:
                # Form data
                symbol = request.form.get('symbol', 'NVDA')
                timeframe = request.form.get('timeframe', '1Y')
                interval = request.form.get('interval', 'day')
                model_type = request.form.get('model', 'default')
        else:
            # GET request - get from query parameters
            symbol = request.args.get('symbol', 'NVDA')
            timeframe = request.args.get('timeframe', '1Y')
            interval = request.args.get('interval', 'day')
            model_type = request.args.get('model', 'default')
            
        print(f"Generating predictions for {symbol} ({timeframe}, {interval}) using model: {model_type}")

        # Fetch data
        data = fetch_stock_data(symbol, timeframe, interval)
        # Train model if not already trained
        global sk_model, sk_model_trained
        if not sk_model_trained:
            print("Training model on data shape:", data.shape)
            metrics = sk_model.train(data)
            sk_model_trained = True
        
        # Get performance metrics
        performance = sk_model.evaluate(data)
        
        # Make predictions
        predictions = sk_model.predict(data)
        current_price = float(data['Close'].iloc[-1])
        
        # Convert any NumPy types to Python native types for JSON serialization
        def convert_to_native_types(obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return [float(x) for x in obj]
            elif isinstance(obj, dict):
                return {k: convert_to_native_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native_types(x) for x in obj]
            return obj
            
        clean_predictions = convert_to_native_types(predictions)
        clean_performance = convert_to_native_types(performance)
        
        print(f"Predictions complete: {clean_predictions}")
        
        return jsonify({
            'symbol': symbol,
            'current_price': current_price,
            'predictions': clean_predictions,
            'performance': clean_performance,
            'status': 'success'
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'message': 'Failed to generate predictions',
            'status': 'error'
        }), 500

@api_bp.route("/reset-model", methods=["POST"])
@cross_origin()
def reset_model_endpoint():
    """Reset the model"""
    try:
        result = reset_model()
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'message': 'Failed to reset model'
        }), 500

@api_bp.route("/chart-analysis", methods=["POST"])
@cross_origin()
def chart_analysis_endpoint():
    """Endpoint to analyze chart data and initialize conversation"""
        
    try:
        if request.is_json:
            # Get data from JSON body
            data = request.get_json()
            symbol = data.get('symbol', 'NVDA')
            timeframe = data.get('timeframe', '1Y') 
            interval = data.get('interval', 'day')
        else: 
            symbol = request.args.get('symbol', 'NVDA')
            timeframe = request.args.get('timeframe', '1Y')
            interval = request.args.get('interval', 'day')
      
        if not data or "symbol" not in data:
            return jsonify({
                "error": "Missing symbol",
                "response": "Please provide a symbol for analysis."
            }), 400
        data = fetch_stock_data(symbol, timeframe, interval)

        # Convert signals to DataFrame properly
        signals = momentum_trading_strategy(data)
        session_id = data.get("session_id", f"analysis_{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        
        # Check if signals DataFrame is empty
        if signals.empty:
            return jsonify({
                "error": "Empty data",
                "response": f"No valid data available for {symbol}."
            }), 400
            
        # Generate analysis
        analysis_result = agent.generate_chart_analysis(symbol, signals)
        
        return jsonify({
            "response": analysis_result,
            "session_id": session_id,
            "symbol": symbol
        })
        
    except Exception as e:
        print(f"Error in chart analysis: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "response": f"Error analyzing chart: {str(e)}"
        }), 500


@api_bp.route("/chat", methods=["POST"])
@cross_origin()
def chat_endpoint():
    """Main chat endpoint"""
    if not request.is_json:
        return jsonify({
            "error": "Invalid request format",
            "response": "Request must be in JSON format"
        }), 400
        
    data = request.get_json()
    try:
        if not data or "message" not in data:
            return jsonify({
                "error": "No message provided",
                "response": "Please provide a message to continue our conversation.",
                "session_id": data.get("session_id", "default"),
                "agent_id": data.get("agent_id", "default"),
                "agent_key": data.get("agent_key", "default"),
                "environment": data.get("environment", "testnet"),
            }), 400

        session_id = data.get("session_id", "default")
        private_key = data.get("agent_key", "default")
        agent_id = data.get("agent_id", "default")
        environment = data.get("environment", "testnet")
        
        # Create a separate thread to run the async function
        import threading
        response_container = [None]
        
        def run_async_chat():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response_container[0] = loop.run_until_complete(
                agent.get_response(data["message"], session_id, private_key, agent_id, environment)
            )
            loop.close()
            
        thread = threading.Thread(target=run_async_chat)
        thread.start()
        thread.join()
        
        response = response_container[0]
        if response is None:
            return jsonify({
                "error": "Failed to get response",
                "response": "An error occurred while processing your request.",
                "session_id": session_id
            }), 500

        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "response": "I apologize, but I encountered an error. Please try again.",
            "session_id": data.get("session_id", "default"),
        }), 500

@api_bp.route("/history", methods=["GET"])
@cross_origin()
def history_endpoint():
    """Get chat history endpoint"""
    session_id = request.args.get("session_id", "default")
    return jsonify({
        "history": agent.get_history(session_id),
        "token_context": agent.get_token_context(session_id)
    })
    
@api_bp.route("/clear", methods=["POST"])
@cross_origin()
def clear_endpoint():
    """Clear chat history endpoint"""
    session_id = request.args.get("session_id", "default")
    agent.clear_history(session_id)
    return jsonify({"status": "success"})
@api_bp.route('/train', methods=['POST'])
def train_model():
    """Train the ML model using provided data."""
    try:
        # Get training data from request
        data = request.get_json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data['price_history'])
        
        # Train the model
        global sk_model, sk_model_trained
        metrics = sk_model.train(df)
        sk_model_trained = True
        
        return jsonify({
            'status': 'success',
            'message': 'Model trained successfully',
            'metrics': {k: float(v) if isinstance(v, np.float64) else v 
                        for k, v in metrics.items() if k != 'feature_importance'}
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Make predictions using trained model."""
    try:
        if request.is_json:
            # Get data from JSON body
            data = request.get_json()
            symbol = data.get('symbol', 'NVDA')
            timeframe = data.get('timeframe', '1Y') 
            interval = data.get('interval', 'day')
        else: 
            symbol = request.args.get('symbol', 'NVDA')
            timeframe = request.args.get('timeframe', '1Y')
            interval = request.args.get('interval', 'day')
      
        if not data or "symbol" not in data:
            return jsonify({
                "error": "Missing symbol",
                "response": "Please provide a symbol for analysis."
            }), 400
        data = fetch_stock_data(symbol, timeframe, interval)
        
        # Train model if not already trained (per chart)
        if not sk_model_trained:
            metrics = sk_model.train(data)
            sk_model_trained = True
        
        # Get performance metrics
        performance = sk_model.evaluate(data)
        
        # Make predictions
        predictions = sk_model.predict(data)
        current_price = float(data['Close'].iloc[-1])
        
        return jsonify({
            'status': 'success',
            'current_price': current_price,
            'predictions': predictions,
            'performance': performance
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

@api_bp.route("/dymension/command", methods=["POST"])
@cross_origin()
def dymension_command():
    """Execute Dymension CLI commands based on natural language description."""
    try:
        if not request.is_json:
            return jsonify({
                "status": "error",
                "output": "",
                "error": "Request must be in JSON format"
            }), 400
            
        data = request.get_json()
        
        if "command" not in data:
            return jsonify({
                "status": "error", 
                "output": "",
                "error": "Missing 'command' parameter"
            }), 400
            
        command_text = data["command"]
        
        # Parse and execute the command
        result = dym_cli.parse_command(command_text)
        
        # Format the output for better display
        formatted_output = format_output(result)
        
        # Return the result
        return jsonify({
            "status": result["status"],
            "output": formatted_output,
            "raw_output": result["output"],
            "error": result["error"]
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "output": "",
            "error": str(e)
        }), 500

@api_bp.route("/dymension/help", methods=["GET"])
@cross_origin()
def dymension_help():
    """Provide help information for Dymension CLI commands."""
    try:
        # List of available commands with descriptions and examples
        commands = [
            # Environment Setup
            {
                "name": "Install essentials",
                "description": "Install essential dependencies for running Dymension",
                "example": "Install essential dependencies for running Dymension on my system",
                "category": "Setup"
            },
            {
                "name": "Install Go",
                "description": "Install Go programming language required for Dymension",
                "example": "Install Go version 1.23.0 on my system",
                "category": "Setup"
            },
            {
                "name": "Install Roller",
                "description": "Install the Roller CLI for managing Dymension RollApps",
                "example": "Install the Roller CLI on my system",
                "category": "Setup"
            },
            
            # RollApp Initialization
            {
                "name": "Initialize RollApp",
                "description": "Initialize a new RollApp with configuration files",
                "example": "Initialize a new RollApp with ID myapp_12345-1",
                "category": "Setup"
            },
            {
                "name": "Setup RollApp endpoints",
                "description": "Configure endpoints for a RollApp using telebit",
                "example": "Setup endpoints for my RollApp using telebit",
                "category": "Setup"
            },
            
            # Sequencer Operations
            {
                "name": "Setup sequencer",
                "description": "Setup a RollApp sequencer for processing transactions and creating blocks",
                "example": "Setup sequencer for my RollApp with ID myapp_12345-1",
                "category": "Sequencer"
            },
            {
                "name": "Start sequencer",
                "description": "Start the RollApp sequencer to process transactions",
                "example": "Start the sequencer for my RollApp",
                "category": "Sequencer"
            },
            {
                "name": "Start DA light client",
                "description": "Start the Data Availability light client",
                "example": "Start DA light client for my RollApp",
                "category": "Sequencer"
            },
            {
                "name": "Check sequencer status",
                "description": "View the status of the RollApp sequencer",
                "example": "Check status of my RollApp sequencer",
                "category": "Sequencer"
            },
            {
                "name": "Load sequencer services",
                "description": "Load the RollApp services for systemd/launchd",
                "example": "Load sequencer services for my RollApp",
                "category": "Sequencer"
            },
            {
                "name": "Start sequencer services",
                "description": "Start RollApp services in the background",
                "example": "Start sequencer services for my RollApp in the background",
                "category": "Sequencer"
            },
            
            # Sequencer Management
            {
                "name": "Export sequencer metadata",
                "description": "Export the current sequencer metadata for your RollApp",
                "example": "Export sequencer metadata for my RollApp",
                "category": "SequencerMgmt"
            },
            {
                "name": "Update sequencer metadata",
                "description": "Update the sequencer metadata for your RollApp",
                "example": "Update sequencer metadata for my RollApp",
                "category": "SequencerMgmt"
            },
            {
                "name": "Get sequencer bond",
                "description": "Get the current bond amount for your sequencer",
                "example": "Get the current bond amount for my sequencer",
                "category": "SequencerMgmt"
            },
            {
                "name": "Increase sequencer bond",
                "description": "Increase the bond amount for your sequencer",
                "example": "Increase the bond amount for my sequencer by 10 DYM",
                "category": "SequencerMgmt"
            },
            {
                "name": "Decrease sequencer bond",
                "description": "Decrease the bond amount for your sequencer",
                "example": "Decrease the bond amount for my sequencer by 5 DYM",
                "category": "SequencerMgmt"
            },
            {
                "name": "Unbond sequencer",
                "description": "Unbond your sequencer from the RollApp",
                "example": "Unbond my sequencer from RollApp myapp_12345-1",
                "category": "SequencerMgmt"
            },
            {
                "name": "Check sequencer penalty points",
                "description": "Check accumulated penalty points for a sequencer",
                "example": "Check penalty points for sequencer on RollApp myapp_12345-1",
                "category": "SequencerMgmt"
            },
            {
                "name": "Kick sequencer",
                "description": "Remove a sequencer with excessive penalty points",
                "example": "Kick sequencer with address dym1xrqph4kuyf9et20zh6m5a9tc3gljvwn2p7ezqn from my RollApp",
                "category": "SequencerMgmt"
            },
            {
                "name": "Update reward address",
                "description": "Update the address where sequencer rewards are sent",
                "example": "Update reward address to ethm1lhk5cnfrhgh26w5r6qft36qerg4dclfev9nprc for my sequencer",
                "category": "SequencerMgmt"
            },
            {
                "name": "Update minimum gas prices",
                "description": "Update the minimum gas prices for transactions on your RollApp",
                "example": "Update minimum gas prices for my RollApp",
                "category": "SequencerMgmt"
            },
            {
                "name": "Setup sequencer metrics",
                "description": "Configure metrics reporting for your sequencer",
                "example": "Setup metrics for my sequencer",
                "category": "SequencerMgmt"
            },
            {
                "name": "Check sequencer health",
                "description": "Perform a health check on your sequencer",
                "example": "Check health status of my sequencer",
                "category": "SequencerMgmt"
            },
            {
                "name": "Update whitelisted relayer",
                "description": "Update the list of whitelisted relayers for gas-free IBC transactions",
                "example": "Add dym123... to whitelisted relayers for my RollApp",
                "category": "SequencerMgmt"
            },
            
            # Relayer Operations
            {
                "name": "Setup IBC connection",
                "description": "Setup an IBC connection between Dymension hub and RollApp",
                "example": "Setup IBC connection for my RollApp with ID myapp_12345-1",
                "category": "Relayer"
            },
            {
                "name": "Start relayer",
                "description": "Start the relayer to facilitate token transfers",
                "example": "Start relayer for my RollApp",
                "category": "Relayer"
            },
            {
                "name": "Load relayer services",
                "description": "Load relayer services for systemd/launchd",
                "example": "Load relayer services for my RollApp",
                "category": "Relayer"
            },
            {
                "name": "Start relayer services",
                "description": "Start relayer services in the background",
                "example": "Start relayer services for my RollApp in the background",
                "category": "Relayer"
            },
            
            # eIBC Client Operations
            {
                "name": "Initialize eIBC client",
                "description": "Initialize eIBC client to process withdrawals from RollApps",
                "example": "Initialize eIBC client for my RollApp",
                "category": "eIBC"
            },
            {
                "name": "Configure eIBC client",
                "description": "Configure the eIBC client with RollApp whitelist",
                "example": "Add myapp_12345-1 to whitelist in eIBC client configuration",
                "category": "eIBC"
            },
            {
                "name": "Start eIBC client",
                "description": "Start the eIBC client for processing withdrawals",
                "example": "Start eIBC client for processing withdrawals",
                "category": "eIBC"
            },
            {
                "name": "Load eIBC services",
                "description": "Load eIBC services for systemd/launchd",
                "example": "Load eIBC services for my system",
                "category": "eIBC"
            },
            {
                "name": "Start eIBC services",
                "description": "Start eIBC services in the background",
                "example": "Start eIBC services in the background",
                "category": "eIBC"
            },
            
            # Full Node Operations
            {
                "name": "Setup full node",
                "description": "Setup a full node to verify the Sequencer state transitions",
                "example": "Setup full node for my RollApp with ID myapp_12345-1",
                "category": "Node"
            },
            {
                "name": "Start full node",
                "description": "Start the full node to verify transactions",
                "example": "Start full node for my RollApp",
                "category": "Node"
            },
            {
                "name": "Load full node services",
                "description": "Load full node services for systemd/launchd",
                "example": "Load full node services for my RollApp",
                "category": "Node"
            },
            {
                "name": "Start full node services",
                "description": "Start full node services in the background",
                "example": "Start full node services for my RollApp in the background",
                "category": "Node"
            },
            
            # Block Explorer Operations
            {
                "name": "Setup block explorer",
                "description": "Setup a block explorer for your RollApp",
                "example": "Setup block explorer for my RollApp with ID myapp_12345-1",
                "category": "Explorer"
            },
            {
                "name": "Start block explorer",
                "description": "Start the block explorer service",
                "example": "Start block explorer for my RollApp",
                "category": "Explorer"
            },
            
            # Wallet Management
            {
                "name": "Create wallet",
                "description": "Create a new wallet for Dymension operations",
                "example": "Create a new wallet named mywallet",
                "category": "Wallet"
            },
            {
                "name": "Recover wallet",
                "description": "Recover a wallet using mnemonic phrase",
                "example": "Recover wallet using my mnemonic phrase",
                "category": "Wallet"
            },
            {
                "name": "List wallets",
                "description": "List all available wallets",
                "example": "List all wallets",
                "category": "Wallet"
            },
            {
                "name": "Check balance",
                "description": "Check the token balance of a wallet",
                "example": "Check balance of my wallet mywallet",
                "category": "Wallet"
            },
            {
                "name": "Transfer tokens",
                "description": "Transfer tokens between wallets",
                "example": "Transfer 10 DYM from mywallet to targetwallet",
                "category": "Wallet"
            },
            
            # RollApp Management
            {
                "name": "Create RollApp",
                "description": "Create a new RollApp with specified parameters",
                "example": "Create a new RollApp with ID myapp_12345-1 and chain-id dymension_1100-1",
                "category": "RollApp"
            },
            {
                "name": "Register RollApp",
                "description": "Register a RollApp on the Dymension hub",
                "example": "Register my RollApp myapp_12345-1 on the Dymension hub",
                "category": "RollApp"
            },
            {
                "name": "Update RollApp metadata",
                "description": "Update RollApp metadata like endpoints or properties",
                "example": "Update endpoints for my RollApp myapp_12345-1",
                "category": "RollApp"
            }
        ]
        
        return jsonify({
            "status": "success",
            "commands": commands
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

@api_bp.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions in API routes"""
    return jsonify({
        "error": str(e),
        "traceback": traceback.format_exc()
    }), 500