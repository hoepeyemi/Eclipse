import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = 'https://eclipse-511z.onrender.com';

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

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    const response = await fetch(`${BACKEND_URL}/api/dymension/command`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error sending command to backend:', error);
    return NextResponse.json(
      { 
        status: 'error', 
        error: 'Failed to connect to backend server. Please ensure the backend is running.' 
      },
      { status: 500 }
    );
  }
} 