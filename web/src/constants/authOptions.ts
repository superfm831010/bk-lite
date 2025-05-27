import CredentialsProvider from "next-auth/providers/credentials";
import { AuthOptions } from "next-auth";
import WeChatProvider from "../lib/wechatProvider";

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
    WeChatProvider({
      clientId: process.env.WECHAT_APP_ID || "",
      clientSecret: process.env.WECHAT_APP_SECRET || "",
      redirectUri: `${process.env.WECHAT_APP_REDIRECT_URI}/api/auth/callback/wechat`,
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
        provider: token.provider,
        wechatOpenId: token.wechatOpenId,
        wechatUnionId: token.wechatUnionId,
        wechatWorkId: token.wechatWorkId,
      };
      return session;
    },
  },
};
