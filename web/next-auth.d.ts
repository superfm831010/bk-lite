import { JWT } from "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    accessToken?: string;
    error?: string;
    locale?: string;
    username?: string;
    roles?: string[];
    zoneinfo?: string;
    user?: {
      id: string;
      username?: string;
      locale?: string;
      token?: string;
    };
  }

  interface User {
    id: string;
    username?: string;
    locale?: string;
    token?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    idToken?: string;
    accessToken?: string;
    refreshToken?: string;
    expiresAt?: number;
    locale?: string;
    error?: string;
    username?: string;
    roles?: string[];
    zoneinfo?: string;
    id?: string;
    token?: string;
  }
}