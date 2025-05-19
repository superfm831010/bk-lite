import { getToken } from 'next-auth/jwt';
import { NextRequest, NextResponse } from 'next/server';

// Handle the actual logout API
export const POST = async (req: NextRequest) => {
  try {
    console.log('Received POST request for logout.');

    // Attempt to get the JWT from the request
    const token = await getToken({ req });
    if (!token) {
      console.warn('No token found in the session.');
      return NextResponse.json(
        { message: 'No session found', error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Return success with the signIn URL for redirection
    const signInUrl = '/auth/signin';
    return NextResponse.json({ 
      success: true, 
      url: signInUrl 
    }, { status: 200 });
  } catch (error) {
    console.error('Logout error:', error);
    return NextResponse.json(
      { message: 'Logout processing failed' },
      { status: 500 }
    );
  }
};

// Optional: Handle GET requests for debugging or consistency
export const GET = async () => {
  return NextResponse.json({ 
    success: true, 
    url: '/auth/signin' 
  }, { status: 200 });
};

// Export to force dynamic behavior
export const dynamic = 'force-dynamic';
