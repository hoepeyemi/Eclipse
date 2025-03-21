// API handlers for the backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://eclipse-511z.onrender.com/api';

export interface CommandParams {
  command: string;
}

export interface CommandResult {
  status: string;
  output: string;
  raw_output?: string;
  error?: string;
}

export interface Command {
  name: string;
  description: string;
  example: string;
  category: string;
}

// Health check endpoint
export const ping = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/ping`);
    
    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

