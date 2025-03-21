# Dymension RollApp CLI Frontend

This is the frontend application for the Dymension RollApp CLI Platform, built with Next.js and modern React techniques to provide an intuitive interface for Dymension CLI operations.

## Features

- Natural language interface for issuing Dymension CLI commands
- Real-time command execution and response display
- Command history and session management
- Responsive design for desktop and mobile usage
- Dark and light theme support

## Technology Stack

- **Next.js 15**: For server-side rendering and routing
- **React 19**: For component-based UI architecture
- **TypeScript**: For type safety and improved developer experience
- **Tailwind CSS**: For utility-first styling
- **Radix UI**: For accessible UI components
- **Shadcn/UI**: Component library built on Radix UI
- **Lucide Icons**: For beautiful SVG icons

## Project Structure

```
frontend/
├── app/                  # Next.js app directory
│   ├── page.tsx          # Home page
│   ├── dymension/        # Dymension CLI interface page
│   ├── about/            # About page
│   ├── api/              # API client utilities
│   ├── globals.css       # Global styles
│   └── layout.tsx        # Root layout component
├── components/           # Shared React components
│   ├── ui/               # UI component library (shadcn/ui)
│   ├── Navbar.tsx        # Navigation component
│   ├── LoadingSpinner.tsx # Loading indicator component
│   └── ThemeProvider.tsx # Theme context provider
├── lib/                  # Utility functions
│   └── utils.ts          # Common utilities
├── hooks/                # Custom React hooks
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 18.0 or later
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
```

### Development

```bash
# Start development server
npm run dev
# or
yarn dev
```

The development server will be available at `http://localhost:3000`.

### Building for Production

```bash
# Build the application
npm run build
# or
yarn build

# Start production server
npm start
# or
yarn start
```

## API Integration

The frontend communicates with the backend server through a REST API. The API base URL can be configured via the `NEXT_PUBLIC_API_URL` environment variable.

Key API endpoints used:
- `GET /api/ping`: Health check endpoint
- `POST /api/dymension/command`: Execute Dymension CLI commands
- `GET /api/dymension/help`: Get help information for Dymension CLI

## Components

### `DymensionCLI`

The main component for the Dymension CLI interface, featuring:
- Command input field with natural language processing
- Response display with formatted output
- Command history tracking
- Error handling and status indicators

### `CommandInput`

A specialized input component for entering natural language commands with:
- Command history navigation (up/down arrows)
- Command validation
- Auto-focus functionality

### `CommandOutput`

Displays the output of executed commands with:
- Syntax highlighting for code blocks
- Error formatting
- Loading state indicators

## Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of the backend API (default: 'https://eclipse-511z.onrender.com/api')

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 