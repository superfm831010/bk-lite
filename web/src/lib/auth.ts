import NextAuth from "next-auth";
import { authOptions } from "../constants/authOptions";

// Export the NextAuth handler
export const { handlers: { GET, POST }, auth, signIn, signOut } = NextAuth(authOptions);

// Export a simplified handler for direct usage in API routes
export async function handler(req: Request) {
  // Determine which method to use based on the request
  if (req.method === "GET") {
    return GET(req);
  } else {
    return POST(req);
  }
}
