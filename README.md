# Dymension RollApp CLI Platform

A modern web application providing a natural language interface for creating and managing Dymension RollApps.

## Overview

This platform simplifies the process of working with Dymension CLI tools by providing an intuitive user interface that accepts natural language commands. It's designed to help blockchain developers create, deploy, and manage Dymension RollApps with ease.

## Project Structure

```
├── backend/                # Flask-based backend server
│   ├── app/                # Application code
│   │   ├── routes/         # API endpoints
│   │   └── utils/          # Utility functions for CLI operations
│   ├── Dockerfile          # Backend container definition
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend application
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   │   └── ui/             # UI component library
│   ├── lib/                # Utility functions
│   └── public/             # Static assets
└── README.md               # Project documentation
```

## Features

- **Dymension CLI Operations**: Execute Dymension CLI commands using natural language
- **RollApp Management**: Create, configure, and deploy RollApps
- **Sequencer Operations**: Manage sequencers for your RollApps
- **Relayer Management**: Configure and monitor IBC relayers
- **Wallet Management**: Create and manage wallets for Dymension operations

## Installation

### Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Using Docker (recommended)
docker-compose up -d

# Or for local development
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

### Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev
# or
yarn dev
```

## Usage

1. Start both the backend and frontend servers
2. Navigate to `http://localhost:3000` in your browser
3. Click on "Open RollApp CLI" to access the CLI interface
4. Enter commands in natural language, such as:
   - "Create a new RollApp with ID myapp_12345-1"
   - "Start the sequencer for my RollApp"
   - "Setup IBC connection for my RollApp"

## API Endpoints

The backend provides the following main API endpoints:

- `/api/ping`: Health check endpoint
- `/api/dymension/command`: Execute Dymension CLI commands
- `/api/dymension/help`: Get help information for Dymension CLI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


