import NextAuth from "next-auth";
import { getAuthOptions } from "@/constants/authOptions";

const handler = NextAuth(await getAuthOptions());

export { handler as GET, handler as POST };