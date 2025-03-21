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
- **Language**: Python 3.9+
- **Framework**: Flask
- **API**: RESTful endpoints
- **Containerization**: Docker
- **Deployment**: Docker/Docker Compose

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
- Python 3.9+ (for local development without Docker)
- Docker (recommended for deployment)
- Git

### Backend Setup

#### Using Docker (Recommended)

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

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app/main.py
   ```

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

3. Start the development server:
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
│   ├── DymensionInterface.tsx # Main CLI interface component
│   ├── LoadingSpinner.tsx # Loading indicator component
│   └── ThemeProvider.tsx # Theme context provider
├── lib/                  # Utility functions
│   └── utils.ts          # Common utilities
├── hooks/                # Custom React hooks
│   └── use-mobile.tsx    # Hook for responsive design
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
        "name": "Initialize RollApp",
        "description": "Initialize a new RollApp with configuration files",
        "example": "Initialize a new RollApp with ID myapp_12345-1",
        "category": "Setup"
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

### Interface Components

The Dymension CLI interface consists of the following components:

1. **Command Input**: A text input field at the bottom of the interface where you enter natural language commands
2. **Command History**: A list of previously executed commands and their outputs
3. **Command Output**: A formatted display of the results from executed commands
4. **Help Button**: Access to information about available commands and their syntax

### Common Commands

#### Environment Setup
- "Install essential dependencies for running Dymension"
- "Install Go version 1.23.0 on my system"
- "Install the Roller CLI on my system"

#### RollApp Creation and Management
- "Initialize a new RollApp with ID myapp_12345-1"
- "Create a new RollApp with ID myapp_12345-1 and chain-id dymension_1100-1"
- "Register my RollApp myapp_12345-1 on the Dymension hub"
- "Update endpoints for my RollApp myapp_12345-1"

#### Sequencer Operations
- "Setup sequencer for my RollApp with ID myapp_12345-1"
- "Start the sequencer for my RollApp"
- "Check status of my RollApp sequencer"
- "Increase the bond amount for my sequencer by 10 DYM"

#### Wallet Management
- "Create a new wallet named mywallet"
- "Recover wallet using my mnemonic phrase"
- "Check balance of my wallet mywallet"
- "Transfer 10 DYM from mywallet to targetwallet"

## Development Guide

### Adding New Features

#### Backend
1. Create new utility functions in `backend/app/utils/`
2. Add new route handlers in `backend/app/routes/api.py`
3. Update the command processing logic in the Dymension CLI handler
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

#### Docker Container Not Starting
- Check if port 5000 is already in use by another application
- Verify Docker is running properly on your system
- Check the container logs for errors: `docker logs dymension-backend`

#### Command Execution Errors
- Ensure the Dymension CLI is properly installed and accessible
- Check file permissions for executing CLI commands
- Verify environment variables are set correctly

### Frontend Issues

#### Development Server Not Starting
- Check for Node.js version compatibility (18.0+)
- Verify all dependencies are installed: `npm install` or `yarn install`
- Check for TypeScript or ESLint errors

#### API Connection Errors
- Ensure the backend server is running and accessible
- Check the API URL configuration in the frontend
- Verify network connectivity between frontend and backend

#### UI Rendering Issues
- Clear browser cache and reload the page
- Check browser console for JavaScript errors
- Verify CSS is loading correctly

## System Diagrams

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

The home page provides an overview of the Dymension RollApp CLI Platform and offers a direct link to the CLI interface.

**Main Components:**
- Header with the platform title and navigation
- Card with information about the Dymension RollApp CLI
- Button to access the CLI interface

### Dymension CLI Interface

The Dymension CLI interface is the main interaction point for users to issue commands and view results.

**Main Components:**
- Command input field
- Command history display
- Response output area
- Help information

### Command Categories

Commands in the Dymension CLI are organized into categories:

1. **Setup** - Environment and prerequisite installation
2. **RollApp** - RollApp creation and management
3. **Sequencer** - Sequencer operations and management
4. **SequencerMgmt** - Advanced sequencer management
5. **Relayer** - IBC relayer setup and management
6. **eIBC** - Ethereum IBC client operations
7. **Node** - Full node operations
8. **Explorer** - Block explorer deployment
9. **Wallet** - Wallet management operations

### Screenshots

#### Home Page
![Home Page](placeholder-for-homepage-screenshot.png)

#### Dymension CLI Interface
![CLI Interface](placeholder-for-cli-interface-screenshot.png)

#### Command Execution
![Command Execution](placeholder-for-command-execution-screenshot.png)

#### Help Information
![Help Information](placeholder-for-help-information-screenshot.png) 