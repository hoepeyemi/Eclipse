# Docker Guide for Dymension RollApp CLI Backend

This guide provides detailed instructions for running the Dymension RollApp CLI Backend using Docker, without requiring Docker Compose.

## Prerequisites

- Docker installed on your system
  - [Install Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install Docker for macOS](https://docs.docker.com/desktop/install/mac-install/)
  - [Install Docker for Linux](https://docs.docker.com/engine/install/)

## Running the Backend with Docker

### Step 1: Navigate to the Backend Directory

```bash
cd backend
```

Make sure you're in the directory containing the `Dockerfile` and `requirements.txt`.

### Step 2: Build the Docker Image

```bash
docker build -t dymension-cli-backend .
```

This command builds a Docker image named `dymension-cli-backend` using the current directory (`.`) as the build context.

### Step 3: Run the Container

```bash
docker run -p 5000:5000 dymension-cli-backend
```

This command runs the container and maps port 5000 of the container to port 5000 on your host machine.

#### Additional Options

To run the container in detached mode (in the background):

```bash
docker run -d -p 5000:5000 dymension-cli-backend
```

To give the container a specific name for easier management:

```bash
docker run -d -p 5000:5000 --name dymension-backend dymension-cli-backend
```

### Step 4: Verify the Container is Running

```bash
docker ps
```

You should see the container running in the list.

### Step 5: Access the API

The API is now accessible at:

```
https://eclipse-511z.onrender.com
```

You can test it with:

```bash
curl https://eclipse-511z.onrender.com/api/ping
```

## Managing the Container

### Stop the Container

```bash
docker stop dymension-backend
```

### Restart the Container

```bash
docker start dymension-backend
```

### View Container Logs

```bash
docker logs dymension-backend
```

To follow the logs in real-time:

```bash
docker logs -f dymension-backend
```

### Remove the Container

```bash
docker rm dymension-backend
```

Note: The container must be stopped before it can be removed.

### Remove the Image

```bash
docker rmi dymension-cli-backend
```

## Troubleshooting

### Port Conflicts

If port 5000 is already in use on your system, you can map to a different port:

```bash
docker run -p 8080:5000 dymension-cli-backend
```

This maps port 5000 in the container to port 8080 on your host.

### Container Crashes

If the container crashes or exits unexpectedly, check the logs:

```bash
docker logs dymension-backend
```

### Permission Issues

If you encounter permission issues with the command:

```bash
sudo docker build -t dymension-cli-backend .
sudo docker run -p 5000:5000 dymension-cli-backend
```

## Environment Variables

You can customize the container behavior with environment variables:

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e DEBUG=True \
  -e SECRET_KEY=your_custom_secret_key \
  dymension-cli-backend
```

## Volume Mounting for Development

For development purposes, you can mount your local code into the container:

```bash
docker run -p 5000:5000 \
  -v $(pwd)/app:/app/app \
  dymension-cli-backend
```

This allows you to make changes to your code without rebuilding the image.

## Using Docker for Frontend and Backend

For running both services, you can:

1. Run the backend container as described above
2. Run your frontend pointing to the backend API URL (https://eclipse-511z.onrender.com/api) 