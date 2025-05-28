import NextAuth from "next-auth";
import { authOptions } from "../constants/authOptions";

// Create NextAuth instance
const nextAuth = NextAuth(authOptions);

// Safely extract exports
export const auth = nextAuth.auth;
export const signIn = nextAuth.signIn;
export const signOut = nextAuth.signOut;

// Safely extract handlers
const handlers = nextAuth.handlers;
export const GET = handlers?.GET;
export const POST = handlers?.POST;

// Export a simplified handler for direct usage in API routes
export async function handler(req: Request) {
  // Determine which method to use based on the request
  if (req.method === "GET" && GET) {
    return GET(req);
  } else if (POST) {
    return POST(req);
  }
  
  // Fallback response
  return new Response("Method not allowed", { status: 405 });
}
