import type { OAuthConfig, OAuthUserConfig } from "next-auth/providers/oauth";

export interface WechatProfile {
  openid: string;
  nickname?: string;
  sex?: string;
  province?: string;
  city?: string;
  country?: string;
  headimgurl?: string;
  privilege?: string[];
  unionid?: string;
  access_token?: string;
}

export default function WeChatProvider<P extends WechatProfile>(
  options: OAuthUserConfig<P> & { redirectUri: string }
): OAuthConfig<P> {
  console.log("[WeChat OAuth] Initializing WeChat Provider with options:", {
    clientId: options.clientId ? "Set" : "Not set",
    clientSecret: options.clientSecret ? "Set" : "Not set",
    redirectUri: options.redirectUri,
  });

  return {
    id: "wechat",
    name: "WeChat",
    type: "oauth",
    version: "2.0",
    wellKnown: undefined,
    authorization: {
      url: "https://open.weixin.qq.com/connect/qrconnect",
      params: {
        appid: options.clientId,
        response_type: "code",
        scope: "snsapi_login",
        redirect_uri: options.redirectUri
      }
    },
    token: {
      url: "https://api.weixin.qq.com/sns/oauth2/access_token",
      params: {
        grant_type: "authorization_code",
        appid: options.clientId,
        secret: options.clientSecret,
      }
    },
    userinfo: {
      url: "https://api.weixin.qq.com/sns/userinfo",
      params: {
        openid: { param: "openid" },
        access_token: { param: "access_token" },
        lang: "zh_CN"
      }
    },
    profile(profile) {
      console.log("[WeChat OAuth] Processing profile:", profile, {
        openid: profile.openid || "Not received",
        nickname: profile.nickname || "Not received",
        unionid: profile.unionid ? "Set" : "Not set"
      });

      return {
        id: profile.openid,
        name: profile.nickname || profile.openid,
        image: profile.headimgurl,
        email: null,
        username: profile.nickname || profile.openid,
        token: profile.access_token,
        wechatOpenId: profile.openid,
        wechatUnionId: profile.unionid
      };
    },
    clientId: options.clientId || "",
    clientSecret: options.clientSecret || ""
  };
}
