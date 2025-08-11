import CredentialsProvider from "next-auth/providers/credentials";
import { AuthOptions } from "next-auth";

// Basic authentication configuration - does not fetch WeChat config on startup
export async function getAuthOptions(): Promise<AuthOptions> {
  const providers = [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
        domain: { label: "Domain", type: "text" },
        skipValidation: { label: "Skip Validation", type: "text" },
        userData: { label: "User Data", type: "text" },
      },
      async authorize(credentials) {
        if (!credentials) {
          console.error("No credentials provided");
          return null;
        }

        try {
          // If skipValidation is true, use the provided userData directly
          if (credentials.skipValidation === 'true' && credentials.userData) {
            const userData = JSON.parse(credentials.userData);
            console.log("[Credentials] Using provided userData:", userData);
            
            if (!userData.id && !userData.username) {
              console.error("Invalid userData: missing id and username");
              return null;
            }
            
            return {
              id: userData.id || userData.username,
              username: userData.username,
              token: userData.token,
              locale: userData.locale || 'en',
              temporary_pwd: userData.temporary_pwd || false,
              enable_otp: userData.enable_otp || false,
              qrcode: userData.qrcode || false,
              provider: userData.provider,
              wechatOpenId: userData.wechatOpenId,
              wechatUnionId: userData.wechatUnionId,
              wechatWorkId: userData.wechatWorkId,
            };
          }

          // Otherwise, perform normal login validation
          const response = await fetch(`${process.env.NEXTAPI_URL}/api/v1/core/api/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: credentials.username,
              password: credentials.password,
              domain: credentials.domain,
            }),
          });
          
          const responseData = await response.json();
          
          if (!response.ok || !responseData.result) {
            console.error("Authentication failed:", responseData);
            return null;
          }
          
          if (responseData.result) {
            const user = responseData.data;
            return {
              id: user.id || user.username,
              username: user.username,
              token: user.token,
              locale: user.locale || 'en',
              temporary_pwd: user.temporary_pwd || false,
              enable_otp: user.enable_otp || false,
              qrcode: user.qrcode || false,
            };
          }
        } catch (error) {
          console.error("Error during authentication:", error);
          return null;
        }
        
        return null;
      },
    }),
  ];
  
  return {
    providers,
    pages: {
      signIn: '/auth/signin',
      signOut: '/auth/signout',
    },
    session: {
      strategy: "jwt",
      maxAge: 60 * 60 * 24,
    },
    callbacks: {
      async jwt({ token, user, account }) {
        if (user) {
          // Store all user information in JWT token
          token.id = user.id;
          token.username = user.username || user.name || '';
          token.locale = user.locale || 'en';
          token.token = user.token;
          token.temporary_pwd = user.temporary_pwd;
          token.enable_otp = user.enable_otp;
          token.qrcode = user.qrcode;
          token.provider = user.provider || account?.provider;
          
          // Store WeChat-specific information if available
          if (user.wechatOpenId || user.wechatUnionId || user.provider === 'wechat') {
            token.wechatOpenId = user.wechatOpenId;
            token.wechatUnionId = user.wechatUnionId;
            token.wechatWorkId = user.wechatWorkId;
            
            console.log("[JWT Callback] WeChat user data stored in JWT:", {
              provider: token.provider,
              wechatOpenId: token.wechatOpenId ? "Set" : "Not set",
              wechatUnionId: token.wechatUnionId ? "Set" : "Not set",
            });
          }
        }
        return token;
      },
      async session({ session, token }) {
        // Pass all JWT data to session
        session.user = {
          id: token.id || '',
          username: token.username,
          locale: token.locale,
          token: token.token,
          temporary_pwd: token.temporary_pwd,
          enable_otp: token.enable_otp,
          qrcode: token.qrcode,
          provider: token.provider,
          wechatOpenId: token.wechatOpenId,
          wechatUnionId: token.wechatUnionId,
          wechatWorkId: token.wechatWorkId,
        };
        return session;
      },
    },
  };
}

// Default configuration for backward compatibility
export const authOptions: AuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
        domain: { label: "Domain", type: "text" },
        skipValidation: { label: "Skip Validation", type: "text" },
        userData: { label: "User Data", type: "text" },
      },
      async authorize(credentials) {
        if (!credentials) {
          console.error("No credentials provided");
          return null;
        }

        try {
          if (credentials.skipValidation === 'true' && credentials.userData) {
            const userData = JSON.parse(credentials.userData);
            
            if (!userData.id && !userData.username) {
              console.error("Invalid userData: missing id and username");
              return null;
            }
            
            return {
              id: userData.id || userData.username,
              username: userData.username,
              token: userData.token,
              locale: userData.locale || 'en',
              temporary_pwd: userData.temporary_pwd || false,
              enable_otp: userData.enable_otp || false,
              qrcode: userData.qrcode || false,
              provider: userData.provider,
              wechatOpenId: userData.wechatOpenId,
              wechatUnionId: userData.wechatUnionId,
              wechatWorkId: userData.wechatWorkId,
            };
          }

          const response = await fetch(`${process.env.NEXTAPI_URL}/api/v1/core/api/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              username: credentials.username,
              password: credentials.password,
              domain: credentials.domain,
            }),
          });
          
          const responseData = await response.json();
          
          if (!response.ok || !responseData.result) {
            console.error("Authentication failed:", responseData);
            return null;
          }
          
          if (responseData.result) {
            const user = responseData.data;
            return {
              id: user.id || user.username,
              username: user.username,
              token: user.token,
              locale: user.locale || 'en',
              temporary_pwd: user.temporary_pwd || false,
              enable_otp: user.enable_otp || false,
              qrcode: user.qrcode || false,
            };
          }
        } catch (error) {
          console.error("Error during authentication:", error);
          return null;
        }
        
        return null;
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
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id;
        token.username = user.username || user.name || '';
        token.locale = user.locale || 'en';
        token.token = user.token;
        token.temporary_pwd = user.temporary_pwd;
        token.enable_otp = user.enable_otp;
        token.qrcode = user.qrcode;
        token.provider = account?.provider;
        token.wechatOpenId = user.wechatOpenId;
        token.wechatUnionId = user.wechatUnionId;
        token.wechatWorkId = user.wechatWorkId;
      }
      return token;
    },
    async session({ session, token }) {
      session.user = {
        id: token.id || '',
        username: token.username,
        locale: token.locale,
        token: token.token,
        temporary_pwd: token.temporary_pwd,
        enable_otp: token.enable_otp,
        qrcode: token.qrcode,
        provider: token.provider,
        wechatOpenId: token.wechatOpenId,
        wechatUnionId: token.wechatUnionId,
        wechatWorkId: token.wechatWorkId,
      };
      return session;
    },
  },
};