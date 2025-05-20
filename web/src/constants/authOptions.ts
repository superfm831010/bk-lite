import CredentialsProvider from "next-auth/providers/credentials";
import { AuthOptions } from "next-auth";

// Function to automatically detect the top-level domain for cookie sharing
const getTopLevelDomain = () => {
  if (typeof window === 'undefined') {
    return undefined;
  }

  const hostname = window.location.hostname;
  
  // Don't set domain for localhost or IP addresses
  if (hostname === 'localhost' || /^\d+\.\d+\.\d+\.\d+$/.test(hostname)) {
    return undefined;
  }
  
  // Extract the top-level domain (e.g., example.com from subdomain.example.com)
  const parts = hostname.split('.');
  if (parts.length >= 2) {
    return `.${parts.slice(-2).join('.')}`;
  }
  
  return undefined;
};

// Get the cookie domain at initialization time
const cookieDomain = typeof window !== 'undefined' 
  ? getTopLevelDomain() 
  : undefined;

export const authOptions: AuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials) return null;

        try {
          const response = await fetch(`${process.env.NEXTAPI_URL}/core/api/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: credentials.username,
              password: credentials.password,
            }),
          });
          console.log("Response status:", response.status);
          
          const responseData = await response.json();
          console.log("Response data:", JSON.stringify(responseData, null, 2));
          
          if (!response.ok) {
            console.error("Authentication failed:", responseData);
            throw new Error("Invalid credentials");
          }
          
          console.log("User authenticated successfully:", responseData);
          if (responseData.result) {
            const user = responseData.data;
            return user;
          }
        } catch (error) {
          console.error("Error during authentication:", error);
          return null;
        }
      },
    }),
  ],
  pages: {
    signIn: '/auth/signin',
    signOut: '/auth/signout',
  },
  session: {
    strategy: "jwt",
    maxAge: 60 * 60 * 24,
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.username = user.username;
        token.locale = user.locale || 'en';
        token.token = user.token;
      }
      
      return token;
    },
    async session({ session, token }) {
      session.user = {
        id: token.id || '',
        username: token.username,
        locale: token.locale,
        token: token.token,
      };
      return session;
    },
  },
  // Configure cookies to enable session sharing across subdomains
  cookies: {
    sessionToken: {
      name: `next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        domain: cookieDomain
      }
    },
    callbackUrl: {
      name: `next-auth.callback-url`,
      options: {
        sameSite: 'lax',
        path: '/',
        domain: cookieDomain
      }
    },
    csrfToken: {
      name: `next-auth.csrf-token`,
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        domain: cookieDomain
      }
    }
  },
};
