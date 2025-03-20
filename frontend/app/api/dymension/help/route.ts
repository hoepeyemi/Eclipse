import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'http://localhost:5000';

export async function GET(req: NextRequest) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/dymension/help`);
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching help from backend:', error);
    return NextResponse.json(
      { 
        status: 'error', 
        error: 'Failed to connect to backend server. Please ensure the backend is running.' 
      },
      { status: 500 }
    );
  }
} 