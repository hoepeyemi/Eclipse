FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_ENV=production \
    DEBUG=False \
    SECRET_KEY=bWFzdGVyQHNjcnRsYWJzLmNvbTpTZWNyZXROZXR3b3JrTWFzdGVyS2V5X18yMDI1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    tar \
    jq \
    libssl-dev \
    pkg-config \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app/ /app/app/
COPY backend/main.py /app/
COPY backend/config.py /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]

# ------------------------------------------------------------------------------
# To build and run this container directly without Docker Compose:
# 1. Navigate to the backend directory:
#    cd backend
#
# 2. Build the Docker image:
#    docker build -t dymension-cli-backend .
#
# 3. Run the container:
#    docker run -p 5000:5000 dymension-cli-backend
#
# 4. Access the API at:
#    https://eclipse-511z.onrender.com
# ------------------------------------------------------------------------------ 