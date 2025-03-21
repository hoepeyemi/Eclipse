from flask import Flask
from flask_cors import CORS
from app.routes.api import api_bp

def create_app(test_config=None):
    """Create and configure the Flask application instance"""
    
    # Initialize Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # Apply CORS to the app
    CORS(app)
    
    # Configure settings
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True
    )
    
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Define root route
    @app.route('/')
    def home():
        # List of available endpoints for documentation
        endpoints = [
            {'path': '/api/ping', 'method': 'GET', 'description': 'Health check endpoint'},
            {'path': '/api/dymension/command', 'method': 'POST', 'description': 'Execute Dymension CLI commands'},
            {'path': '/api/dymension/help', 'method': 'GET', 'description': 'Get help for Dymension CLI commands'},
        ]
        
        # Create HTML response
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Tradi-App Backend API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                ul { list-style-type: none; padding: 0; }
                li { margin-bottom: 10px; padding: 10px; background-color: #f4f4f4; border-radius: 5px; }
                .method { display: inline-block; width: 60px; font-weight: bold; }
                .path { color: #0066cc; font-family: monospace; }
            </style>
        </head>
        <body>
            <h1>Tradi-App Backend API</h1>
            <p>Welcome to the Tradi-App Backend API. The following endpoints are available:</p>
            <ul>
        """
        
        # Add each endpoint to the HTML
        for endpoint in endpoints:
            html += f"""
                <li>
                    <span class="method">{endpoint['method']}</span>
                    <span class="path">{endpoint['path']}</span>
                    <p>{endpoint['description']}</p>
                </li>
            """
        
        html += """
            </ul>
            <p>For more information, please refer to the documentation.</p>
        </body>
        </html>
        """
        
        return html
    
    return app