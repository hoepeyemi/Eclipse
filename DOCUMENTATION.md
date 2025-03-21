# Dymension RollApp CLI Platform Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Features](#features)
4. [Technology Stack](#technology-stack)
5. [Setting Up the Application](#setting-up-the-application)
   - [Prerequisites](#prerequisites)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
6. [Application Structure](#application-structure)
   - [Backend Structure](#backend-structure)
   - [Frontend Structure](#frontend-structure)
7. [API Reference](#api-reference)
8. [Usage Guide](#usage-guide)
9. [Development Guide](#development-guide)
10. [Troubleshooting](#troubleshooting)
11. [System Diagrams](#system-diagrams)
12. [UI Reference](#ui-reference)

## Introduction

The Dymension RollApp CLI Platform is a web-based application that provides a natural language interface for creating and managing Dymension RollApps. It simplifies the complex command-line operations required for Dymension blockchain development by offering an intuitive interface that processes natural language commands and executes the corresponding Dymension CLI operations.

The platform aims to make blockchain development more accessible by abstracting away the complexity of command-line interfaces while providing all the functionality developers need to create, deploy, and manage their RollApps on the Dymension network.

## Architecture Overview

The application follows a client-server architecture with a clear separation between the frontend and backend:

```
┌─────────────┐                 ┌─────────────┐                 ┌─────────────┐
│             │                 │             │                 │             │
│  Frontend   │◄───REST API────►│   Backend   │◄────Execute────►│ Dymension   │
│  (Next.js)  │                 │   (Flask)   │                 │    CLI      │
│             │                 │             │                 │             │
└─────────────┘                 └─────────────┘                 └─────────────┘
```

- **Frontend**: A Next.js application that provides the user interface for interacting with the Dymension CLI. It handles user input in natural language and displays command outputs in a user-friendly format.

- **Backend**: A Flask-based REST API that processes natural language commands, translates them into Dymension CLI commands, executes them, and returns formatted results.

- **Dymension CLI**: The underlying command-line interface for Dymension operations that the backend interacts with.

### Command Processing Flow

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ User enters   │     │ Frontend sends│     │ Backend       │     │ Dymension CLI │
│ natural       │────►│ command to    │────►│ processes and │────►│ executes the  │
│ language      │     │ backend API   │     │ translates    │     │ command       │
│ command       │     │               │     │ command       │     │               │
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
                                                                         │
┌───────────────┐     ┌───────────────┐     ┌───────────────┐           │
│ Frontend      │     │ Frontend      │     │ Backend       │           │
│ displays      │◄────│ receives      │◄────│ formats and   │◄──────────┘
│ result to     │     │ response from │     │ returns       │
│ user          │     │ backend       │     │ result        │
└───────────────┘     └───────────────┘     └───────────────┘
```

## Features

The Dymension RollApp CLI Platform offers the following key features:

### RollApp Management
- Create and initialize new RollApps with custom configurations
- Register RollApps on the Dymension hub
- Update RollApp metadata and endpoints
- Configure custom parameters for RollApps

### Sequencer Operations
- Setup and initialize sequencers for RollApps
- Start and monitor sequencer services
- Manage sequencer bonds (increase, decrease, unbond)
- Check sequencer health and penalty points
- Export and update sequencer metadata

### Relayer Management
- Setup IBC connections between Dymension hub and RollApps
- Register and manage relayers
- Start and monitor relayer services
- Update relayer keys and configurations

### Wallet Management
- Create and recover wallets for Dymension operations
- List available wallets and check balances
- Transfer tokens between wallets
- Manage wallet keys and security

### Node Operations
- Setup and configure full nodes
- Start and monitor node services
- Check node status and update configurations

### Block Explorer
- Deploy and configure block explorers for RollApps
- Start and monitor explorer services

### Natural Language Interface
- Process commands in natural language format
- Convert natural language to Dymension CLI operations
- Provide descriptive output for easier understanding

## Technology Stack

### Backend
- **Language**: Python 3.12
- **Framework**: Flask
- **API**: RESTful endpoints
- **Containerization**: Docker
- **Deployment**: Render.com

### Frontend
- **Language**: TypeScript
- **Framework**: Next.js 15.2+, React 19.0+
- **UI Components**: Shadcn/UI (built on Radix UI)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

## Setting Up the Application

### Prerequisites

Before setting up the application, ensure you have the following installed:

- Node.js 18.0+ and npm/yarn
- Python 3.12+ (for local development without Docker)
- Docker (optional, for containerized deployment)
- Git

### Backend Setup

#### Using Docker (Optional)

1. Clone the repository and navigate to the backend directory:
   ```bash
   git clone https://github.com/your-username/dymension-rollapp-cli.git
   cd dymension-rollapp-cli/backend
   ```

2. Build the Docker image:
   ```bash
   docker build -t dymension-cli-backend .
   ```

3. Run the container:
   ```bash
   docker run -p 5000:5000 dymension-cli-backend
   ```

The backend API will be accessible at `http://localhost:5000`.

#### Local Development Setup

1. Navigate to the backend directory:
   ```bash
   cd dymension-rollapp-cli/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

#### Deployment with Render.com

The backend is currently deployed on Render.com and accessible at:

```
https://eclipse-511z.onrender.com
```

For deploying your own instance:

1. Push your code to GitHub
2. Connect the repository to Render.com
3. Setup a Web Service with the following settings:
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && python main.py`
   - Environment variables:
     - `PORT`: Set by Render
     - `FLASK_ENV`: `production`
     - `DEBUG`: `False`
     - `SECRET_KEY`: Generate a secure key

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd dymension-rollapp-cli/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set the backend URL in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=https://eclipse-511z.onrender.com/api
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The frontend will be accessible at `http://localhost:3000`.

## Application Structure

### Backend Structure

```
backend/
├── app/                # Application code
│   ├── __init__.py     # Application factory
│   ├── main.py         # Application configuration  
│   ├── routes/         # API endpoints
│   │   ├── __init__.py # Routes initialization
│   │   └── api.py      # API route definitions
│   ├── models/         # Data models (minimal for this app)
│   │   └── __init__.py # Models initialization
│   └── utils/          # Utility functions
│       ├── __init__.py # Utils initialization
│       ├── dymension_cli.py  # Dymension CLI handler
│       └── json_utils.py     # JSON processing utilities
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── config.py           # Configuration settings
└── main.py             # Application entry point
```

### Frontend Structure

```
frontend/
├── app/                  # Next.js app directory
│   ├── page.tsx          # Home page
│   ├── dymension/        # Dymension CLI interface page
│   │   └── page.tsx      # Dymension command interface
│   ├── about/            # About page
│   │   └── page.tsx      # About page content
│   ├── api/              # API client utilities
│   │   └── index.ts      # API functions for backend communication
│   ├── globals.css       # Global styles
│   └── layout.tsx        # Root layout component
├── components/           # Shared React components
│   ├── ui/               # UI component library (shadcn/ui)
│   ├── Navbar.tsx        # Navigation component
│   ├── LoadingSpinner.tsx # Loading indicator component
│   ├── ThemeSelector.tsx  # Theme selection component
│   └── ThemeProvider.tsx  # Theme context provider
├── lib/                  # Utility functions
│   └── utils.ts          # Common utilities
├── hooks/                # Custom React hooks
│   ├── use-mobile.tsx    # Hook for responsive design
│   └── use-toast.ts      # Toast notification hook
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## API Reference

The backend provides the following RESTful API endpoints:

### Health Check
- **Endpoint**: `/api/ping`
- **Method**: GET
- **Description**: Simple health check endpoint
- **Response Example**:
  ```json
  {
    "status": "ok", 
    "timestamp": "2023-05-24T15:30:45Z", 
    "version": "1.0.0"
  }
  ```

### Execute Dymension Command
- **Endpoint**: `/api/dymension/command`
- **Method**: POST
- **Description**: Execute a Dymension CLI command
- **Request Body**:
  ```json
  {
    "command": "Create a new RollApp with ID myapp_12345-1"
  }
  ```
- **Response Example**:
  ```json
  {
    "status": "success",
    "output": "RollApp successfully created with ID myapp_12345-1",
    "raw_output": "[detailed command output]"
  }
  ```

### Get Dymension Help
- **Endpoint**: `/api/dymension/help`
- **Method**: GET
- **Description**: Get help information for Dymension CLI commands
- **Response Example**: 
  ```json
  {
    "status": "success",
    "commands": [
      {
        "name": "Create wallet",
        "description": "Create a new wallet for Dymension operations",
        "example": "Create a new wallet named mywallet",
        "category": "Wallet"
      },
      {
        "name": "Check balance",
        "description": "Check the token balance of a wallet",
        "example": "Check balance of my wallet mywallet",
        "category": "Wallet"
      },
      // More commands...
    ]
  }
  ```

## Usage Guide

### Accessing the Application

1. Ensure both the backend and frontend servers are running
2. Open your browser and navigate to `http://localhost:3000`
3. You'll see the home page with information about the Dymension RollApp CLI Platform
4. Click on "Open RollApp CLI" to access the command interface

### Using the Dymension CLI Interface

1. The CLI interface has a command input field where you can type natural language commands
2. Enter commands like:
   - "Create a new RollApp with ID myapp_12345-1"
   - "Setup sequencer for my RollApp with ID myapp_12345-1"
   - "Start the sequencer for my RollApp"
   - "Check sequencer status for my RollApp"
3. Press Enter or click the Submit button to execute the command
4. The command output will be displayed in the response section
5. You can view command history and access previously executed commands

### Common Commands

#### Wallet Management
- "Create a new wallet named mywallet"
- "Recover wallet using my mnemonic phrase"
- "Check balance of my wallet mywallet"
- "Transfer 10 DYM from mywallet to targetwallet"

#### RollApp Creation and Management
- "Create a new RollApp with ID myapp_12345-1 and chain-id dymension_1100-1"
- "Register my RollApp myapp_12345-1 on the Dymension hub"
- "Query information about RollApp myapp_12345-1"
- "List all registered RollApps"

#### Sequencer Operations
- "Register sequencer for RollApp myapp_12345-1"
- "Query sequencers for RollApp myapp_12345-1"
- "Submit a batch for RollApp myapp_12345-1"
- "Claim settlement for settlement ID 12345"

#### Relayer Management
- "Update whitelisted relayers for my RollApp"

## Development Guide

### Adding New Features

#### Backend
1. Create new utility functions in `backend/app/utils/`
2. Add new route handlers in `backend/app/routes/api.py`
3. Update the command processing logic in the `DymensionCLI` class
4. Test the new endpoints with API testing tools like Postman or curl

#### Frontend
1. Create new components in `frontend/components/`
2. Add new pages in `frontend/app/` if needed
3. Update the API client utilities in `frontend/app/api/`
4. Test the new features in the user interface

### Styling Guidelines
- Use Tailwind CSS utility classes for styling
- Follow the Shadcn/UI component patterns for consistency
- Ensure responsive design for all screen sizes
- Maintain dark/light theme compatibility

## Troubleshooting

### Backend Issues

#### Deployment Errors
- Check the path structure in your Dockerfile or deployment configuration
- Ensure your `main.py` file is at the correct location
- Verify port configuration and environment variables
- Check Render.com logs for specific error messages

#### Command Execution Errors
- Ensure the Dymension CLI is properly installed and accessible
- Check that the `DymensionCLI` class can find the required binaries
- Verify file permissions for executing CLI commands
- Check for proper error handling in the command execution process

### Frontend Issues

#### API Connection Errors
- Ensure the backend server is running and accessible
- Verify the `NEXT_PUBLIC_API_URL` in your environment variables points to the correct backend URL
- Check network connectivity between frontend and backend
- Examine browser network tab for specific API errors

#### UI Rendering Issues
- Clear browser cache and reload the page
- Check browser console for JavaScript errors
- Verify CSS is loading correctly
- Test with different browsers to isolate browser-specific issues

## System Diagrams

### Application Components

```
┌─────────────────────────────────────────┐
│               Frontend                   │
│                                          │
│  ┌─────────────┐      ┌─────────────┐   │
│  │  UI         │      │  API        │   │
│  │  Components │      │  Client     │   │
│  └─────────────┘      └─────────────┘   │
│                                          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│               Backend                    │
│                                          │
│  ┌─────────────┐      ┌─────────────┐   │
│  │  API        │      │  Dymension  │   │
│  │  Routes     │      │  CLI Utils  │   │
│  └─────────────┘      └─────────────┘   │
│                                          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Dymension CLI Commands           │
└─────────────────────────────────────────┘
```

### User Workflow

```
Start
  │
  ▼
┌─────────────┐
│ Access Web  │
│ Interface   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Navigate to │
│ Dymension   │
│ CLI Page    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Enter       │
│ Natural     │
│ Language    │
│ Command     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Command     │
│ Processed   │
│ by Backend  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ View        │
│ Command     │
│ Result      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Execute     │
│ Additional  │◄───┐
│ Commands    │    │
└──────┬──────┘    │
       │           │
       ▼           │
   Decision        │
  /       \        │
Yes/       \No     │
  /         \      │
 ▼           ▼     │
Continue?    End   │
  │                │
  └────────────────┘
```

## UI Reference

### Home Page
The home page provides an introduction to the Dymension RollApp CLI Platform and a button to access the CLI interface.

### Dymension CLI Interface
The CLI interface includes:
- A command input field
- A results display area
- Command history
- Help and reference section

### About Page
Information about the platform, its features, and technology stack.

*Note: Screenshots will be added in a future update.*

