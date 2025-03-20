import os
import pandas as pd
from dotenv import load_dotenv
import json
import asyncio
from datetime import datetime
from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret

load_dotenv()

class SecretChatAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get API key from environment variable
        # SECRET_API_KEY already set in .env file
        # Initialize Secret client
        self.secret_client = Secret()
        
        # Get available models
        self.models = self.secret_client.get_models()
        
        if not self.models:
            raise ValueError("No Secret AI models available")
        
        # Get model URLs
        self.model_urls = self.secret_client.get_urls(model=self.models[0])
        
        if not self.model_urls:
            raise ValueError(f"No URLs available for model {self.models[0]}")
        
        # Initialize the LLM client
        self.llm = ChatSecret(
            base_url=self.model_urls[0],
            model=self.models[0],
            temperature=0.7
        )

        # Initialize conversation histories
        self.conversations = {}
        # Initialize token context
        self.token_contexts = {}

    def generate_chart_analysis(self, symbol: str, signals: pd.DataFrame) -> str:
        """Generate analysis of trading signals using Secret AI."""
        try:
            # Calculate metrics
            total_trades = len(signals[signals['positions'] != 0])
            buy_signals = len(signals[signals['positions'] == 1.0])
            sell_signals = len(signals[signals['positions'] == -1.0])
            price_change = ((signals['price'].iloc[-1] - signals['price'].iloc[0]) / 
                        signals['price'].iloc[0] * 100)

            messages = [
                ("system", "You are a professional stock market analyst."),
                ("human", f"""
                Analyze this trading data for {symbol}:
                - Total number of trades: {total_trades}
                - Buy signals: {buy_signals}
                - Sell signals: {sell_signals}
                - Price change: {price_change:.2f}%
                - Current price trend relative to moving averages: 
                  Last price: {signals['price'].iloc[-1]:.2f}
                  Short MA: {signals['short_mavg'].iloc[-1]:.2f}
                  Long MA: {signals['long_mavg'].iloc[-1]:.2f}

                Provide a brief trading analysis and recommendation.
                """)
            ]

            response = self.llm.invoke(messages, stream=False)
            return response.content
        except Exception as e:
            return f"Could not generate analysis: {str(e)}"

    def add_token_context(self, session_id: str, symbol: str, analysis_result: str):
        """Add token analysis context to the session"""
        self.token_contexts[session_id] = {
            "symbol": symbol,
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add the analysis to the conversation history
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            
        # Add system message with the analysis context
        self.conversations[session_id].append(
            ("system", f"Initial analysis for {symbol}: {analysis_result}\n\nThe user may ask follow-up questions about {symbol}.")
        )

    async def get_response(self, message, session_id="default"):
        """Get response from Secret AI."""
        try:
            # Initialize conversation history for new sessions
            if session_id not in self.conversations:
                self.conversations[session_id] = []

            # Add user message to conversation history
            self.conversations[session_id].append(("human", message))

            # Build system message with token context if available
            system_message = """You are a helpful AI assistant. Help the user with trading analysis and predictions.
            When providing answers, be concise and informative."""
            
            # Add token context if available
            token_context = self.token_contexts.get(session_id)
            if token_context:
                system_message += f"\n\nRecently analyzed token: {token_context['symbol']}\nAnalysis summary: {token_context['analysis']}\n\nRefer to this analysis when the user asks about {token_context['symbol']} and suggest trading actions based on this analysis."

            # Prepare messages for Secret AI
            messages = [("system", system_message)]
            messages.extend(self.conversations[session_id])

            # Get response from Secret AI
            response = await asyncio.to_thread(
                self.llm.invoke,
                messages=messages,
                stream=False
            )

            bot_message = response.content
            self.conversations[session_id].append(("assistant", bot_message))

            return {
                "response": bot_message,
                "session_id": session_id
            }

        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}. How else can I help you?"
            return {
                "response": error_response,
                "session_id": session_id,
            }

    async def analyze_chart(self, symbol: str, signals: pd.DataFrame, session_id: str = None):
        """Analyze chart data and initialize conversation"""
        try:
            if session_id is None:
                session_id = f"analysis_{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Generate analysis
            analysis_result = self.generate_chart_analysis(symbol, signals)
            
            # Add analysis to token context for the session
            self.add_token_context(session_id, symbol, analysis_result)
            
            return {
                "response": analysis_result,
                "session_id": session_id,
                "symbol": symbol
            }
        except Exception as e:
            return {
                "error": str(e),
                "response": f"I apologize, but I encountered an error analyzing the chart data: {str(e)}",
            }

    def clear_history(self, session_id="default"):
        """Clear conversation history for a specific session."""
        if session_id in self.conversations:
            self.conversations[session_id].clear()
        if session_id in self.token_contexts:
            del self.token_contexts[session_id]

    def get_history(self, session_id="default"):
        """Get conversation history for a specific session."""
        return self.conversations.get(session_id, [])

    def get_token_context(self, session_id="default"):
        """Get token context for a specific session."""
        return self.token_contexts.get(session_id)
    
    __all__ = ["SecretChatAgent"]