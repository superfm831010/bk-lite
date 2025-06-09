import NextAuth from "next-auth";
import { getAuthOptions } from "../constants/authOptions";

// Create NextAuth instance with dynamic auth options
const createNextAuth = async () => {
  const authOptions = await getAuthOptions();
  return NextAuth(authOptions);
};

// Export async versions of the auth functions
export const getAuth = async () => {
  const nextAuth = await createNextAuth();
  return nextAuth.auth;
};

export const getSignIn = async () => {
  const nextAuth = await createNextAuth();
  return nextAuth.signIn;
};

export const getSignOut = async () => {
  const nextAuth = await createNextAuth();
  return nextAuth.signOut;
};

// Export a simplified handler for direct usage in API routes
export async function handler(req: Request) {
  const nextAuth = await createNextAuth();
  const handlers = nextAuth.handlers;
  
  // Determine which method to use based on the request
  if (req.method === "GET" && handlers?.GET) {
    return handlers.GET(req);
  } else if (handlers?.POST) {
    return handlers.POST(req);
  }
  
  // Fallback response
  return new Response("Method not allowed", { status: 405 });
}
