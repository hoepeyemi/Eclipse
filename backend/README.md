# Tradi Backend

This is the backend service for the Tradi application, providing API endpoints for stock data analysis, predictions, and Dymension CLI operations.

## Requirements

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Deployment with Docker

### Building and running with Docker Compose

The simplest way to deploy the backend is using Docker Compose:

```bash
# Build and start the backend service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Building and running with Docker directly

You can also build and run the Docker container directly:

```bash
# Build the Docker image
docker build -t tradi-backend .

# Run the container
docker run -p 5000:5000 -d --name tradi-backend tradi-backend
```

## Environment Variables

You can configure the application using the following environment variables:

- `FLASK_ENV`: Set to `production` for production deployment or `development` for development
- `DEBUG`: Set to `True` to enable debug mode or `False` for production
- `SECRET_KEY`: Secret key for session security
- `PORT`: Port to run the Flask application (default: 5000)

## API Endpoints

The backend provides the following main API endpoints:

- `/api/ping`: Health check endpoint
- `/api/stock-data`: Get stock data for analysis
- `/api/predict`: Generate price predictions using ML models
- `/api/chart-analysis`: Analyze chart patterns
- `/api/dymension/command`: Execute Dymension CLI commands
- `/api/dymension/help`: Get help information for Dymension CLI

## Local Development

For local development without Docker:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py
```

The server will be available at `http://localhost:5000`.
