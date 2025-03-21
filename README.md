# Dymension RollApp CLI Platform

This platform provides a natural language interface for creating and managing Dymension RollApps. The system allows developers to easily interact with the Dymension network through a simple conversational interface, handling complex CLI commands through an intuitive Next.js frontend and Flask backend.

## Project Structure

```
dymension-cli/
├── frontend/                 # Next.js application
│   ├── app/                  # Pages and routes (home, dymension, about)
│   ├── components/           # UI components (DymensionInterface, UI components)
│   └── public/               # Static assets and images
├── backend/                  # Flask API server
│   ├── app/                  # Core application
│   │   ├── routes/           # API endpoints for Dymension CLI commands
│   │   └── utils/            # Dymension CLI utilities
│   └── Dockerfile            # Docker configuration for backend
└── README.md                 # Project documentation     
```

## Features

- Natural language command interface for Dymension CLI operations
- Support for RollApp initialization and configuration 
- Sequencer and relayer management capabilities
- Full node deployment and monitoring tools
- Wallet management for Dymension operations

## Installation

1. Clone this repository and navigate into it:

```bash
git clone https://github.com/yourusername/dymension-cli-platform
cd dymension-cli-platform
```

### Backend Setup

2. Using Docker (recommended):

```bash
cd backend
docker-compose up -d
```

Or manually:

```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

### Frontend Setup

3. Install dependencies:

```bash
cd frontend
npm install
```

4. Setup environment variables:
- Create `.env.local` file
- Add `NEXT_PUBLIC_API_URL=http://localhost:5000/api` to the file

5. Run the Next.js app:

```bash
npm run dev
```

Visit `http://localhost:3000` in your web browser to access the application.

## Usage

1. Navigate to the Dymension CLI page
2. Enter commands in natural language (e.g., "Create a new wallet named mywallet")
3. View the command output and execution status

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
