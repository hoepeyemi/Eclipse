from flask import Blueprint, jsonify, request
import traceback
from flask_cors import cross_origin
from datetime import datetime
# Import Dymension CLI utilities
from app.utils.dymension_cli import DymensionCLI, format_output

# Create a Blueprint for the API routes
api_bp = Blueprint('api', __name__)

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
                "name": "Register relayer",
                "description": "Register a relayer for your RollApp",
                "example": "Register relayer for my RollApp",
                "category": "Relayer"
            },
            {
                "name": "Start relayer",
                "description": "Start the IBC relayer service",
                "example": "Start relayer for my RollApp",
                "category": "Relayer"
            },
            {
                "name": "Check relayer status",
                "description": "View the status of the IBC relayer",
                "example": "Check relayer status for my RollApp",
                "category": "Relayer"
            },
            {
                "name": "Update relayer keys",
                "description": "Update the keys used by the relayer",
                "example": "Update relayer keys for my RollApp",
                "category": "Relayer"
            },
            
            # eIBC Client Operations
            {
                "name": "Setup eIBC client",
                "description": "Setup an Ethereum IBC (eIBC) client for bridging with EVM chains",
                "example": "Setup eIBC client for my RollApp",
                "category": "eIBC"
            },
            {
                "name": "Configure eIBC endpoints",
                "description": "Configure endpoints for eIBC client",
                "example": "Configure eIBC endpoints for my RollApp",
                "category": "eIBC"
            },
            {
                "name": "Start eIBC client",
                "description": "Start the eIBC client for bridging",
                "example": "Start eIBC client for my RollApp",
                "category": "eIBC"
            },
            {
                "name": "Check eIBC status",
                "description": "View the status of the eIBC client",
                "example": "Check eIBC status for my RollApp",
                "category": "eIBC"
            },
            
            # Full Node Operations
            {
                "name": "Setup full node",
                "description": "Setup a full node for your RollApp",
                "example": "Setup full node for my RollApp",
                "category": "Node"
            },
            {
                "name": "Start full node",
                "description": "Start the RollApp full node",
                "example": "Start full node for my RollApp",
                "category": "Node"
            },
            {
                "name": "Check node status",
                "description": "View the status of the RollApp node",
                "example": "Check node status for my RollApp",
                "category": "Node"
            },
            {
                "name": "Update node configuration",
                "description": "Update the configuration of your RollApp node",
                "example": "Update node configuration for my RollApp",
                "category": "Node"
            },
            
            # Block Explorer
            {
                "name": "Deploy block explorer",
                "description": "Deploy a block explorer for your RollApp",
                "example": "Deploy block explorer for my RollApp",
                "category": "Explorer"
            },
            {
                "name": "Configure block explorer",
                "description": "Configure the RollApp block explorer",
                "example": "Configure block explorer for my RollApp",
                "category": "Explorer"
            },
            {
                "name": "Start block explorer",
                "description": "Start the RollApp block explorer service",
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
    """Global exception handler for API routes"""
    return jsonify({
        "status": "error",
        "message": str(e),
        "traceback": traceback.format_exc()
    }), 500