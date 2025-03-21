from app import create_app
import logging
import os

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO if os.environ.get('FLASK_ENV') == 'production' else logging.DEBUG)
    app.logger.info('Starting Dymension CLI application')
    app.logger.info(f'Registered routes: {[r.rule for r in app.url_map.iter_rules()]}')
    
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'  # Bind to all interfaces
    
    app.run(host=host, port=port, debug=os.environ.get('DEBUG', 'True').lower() == 'true')