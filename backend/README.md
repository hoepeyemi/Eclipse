# Dymension RollApp CLI Backend

This is the backend service for the Dymension RollApp CLI Platform, providing API endpoints for executing Dymension CLI operations through a REST API.

## Features

- Natural language processing for Dymension CLI commands
- Execution of Dymension CLI commands with formatted output
- Extensive command help and documentation
- Health check endpoint for service monitoring

## Requirements

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Deployment with Docker

### Running with Docker (Recommended)

The simplest way to deploy the backend is using Docker directly:

```bash
# Navigate to the backend directory
cd backend

# Build the Docker image
docker build -t dymension-cli-backend .

# Run the container
docker run -p 5000:5000 dymension-cli-backend
```

See the [Docker Guide](DOCKER-GUIDE.md) for more detailed instructions and options.

### Building and running with Docker Compose

If you prefer to use Docker Compose:

```bash
# Build and start the backend service
docker compose up -d

# View logs
docker compose logs -f

# Stop the service
docker compose down
```

## Environment Variables

You can configure the application using the following environment variables:

- `FLASK_ENV`: Set to `production` for production deployment or `development` for development
- `DEBUG`: Set to `True` to enable debug mode or `False` for production
- `SECRET_KEY`: Secret key for session security
- `PORT`: Port to run the Flask application (default: 5000)

## API Endpoints

The backend provides the following RESTful API endpoints:

### Health Check

- **URL**: `/api/ping`
- **Method**: `GET`
- **Description**: Simple health check endpoint to verify the service is running
- **Response**: 
  ```json
  {
    "status": "ok",
    "timestamp": "2023-05-20T12:00:00Z",
    "version": "1.0.0"
  }
  ```

### Execute Dymension Command

- **URL**: `/api/dymension/command`
- **Method**: `POST`
- **Description**: Executes a Dymension CLI command based on natural language input
- **Request Body**:
  ```json
  {
    "command": "Create a new RollApp with ID myapp_12345-1"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "output": "RollApp successfully created with ID myapp_12345-1",
    "raw_output": "[detailed command output]"
  }
  ```

### Get Dymension CLI Help

- **URL**: `/api/dymension/help`
- **Method**: `GET`
- **Description**: Provides help information for available Dymension CLI commands
- **Response**:
  ```json
  {
    "status": "success",
    "commands": [
      {
        "name": "Initialize RollApp",
        "description": "Initialize a new RollApp with configuration files",
        "example": "Initialize a new RollApp with ID myapp_12345-1",
        "category": "Setup"
      },
      ...
    ]
  }
  ```

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

The server will be available at `https://eclipse-511z.onrender.com`.

## Project Structure

```
backend/
├── app/                # Application code
│   ├── __init__.py     # Application factory
│   ├── routes/         # API endpoints
│   │   └── api.py      # API route definitions
│   └── utils/          # Utility functions
│       └── dymension_cli.py  # Dymension CLI handler
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── config.py           # Configuration settings
└── main.py             # Application entry point
```

## Common Issues

- **Command execution errors**: Ensure the Dymension CLI is properly installed and accessible to the application
- **Permission issues**: When running inside Docker, ensure proper permissions for executing CLI commands

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
