import { NextRequest, NextResponse } from 'next/server';

// WeChat login callback route - process callback and store in NextAuth JWT
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  
  console.log("[WeChat Callback] Received callback with code:", code ? "Present" : "Missing");
  console.log("[WeChat Callback] Request URL:", request.url);
  console.log("[WeChat Callback] Origin:", new URL(request.url).origin);
  
  if (!code) {
    console.error("[WeChat Callback] No authorization code received");
    return NextResponse.redirect(new URL('/auth/signin?error=wechat_auth_failed', request.url));
  }
  
  try {
    // Parse state parameter to get callbackUrl
    let callbackUrl = '/';
    if (state) {
      try {
        const stateData = JSON.parse(decodeURIComponent(state));
        callbackUrl = stateData.callbackUrl || '/';
        console.log("[WeChat Callback] Parsed callbackUrl from state:", callbackUrl);
      } catch (e) {
        console.warn("[WeChat Callback] Failed to parse state parameter:", e);
      }
    }
    
    // Get WeChat configuration
    const configResponse = await fetch(`${process.env.NEXTAPI_URL}/api/v1/core/api/get_wechat_settings/`, {
      method: "GET",
      headers: { 
        "Content-Type": "application/json",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
      },
      cache: "no-store"
    });
    
    const configData = await configResponse.json();
    
    if (!configResponse.ok || !configData.result) {
      console.error("[WeChat Callback] Failed to get WeChat settings:", configData);
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_config_error', request.url));
    }
    
    const wechatConfig = configData.data;
    console.log("[WeChat Callback] WeChat config loaded successfully");
    
    // Get access_token
    const tokenUrl = new URL("https://api.weixin.qq.com/sns/oauth2/access_token");
    tokenUrl.searchParams.set("appid", wechatConfig.app_id);
    tokenUrl.searchParams.set("secret", wechatConfig.app_secret);
    tokenUrl.searchParams.set("code", code);
    tokenUrl.searchParams.set("grant_type", "authorization_code");

    console.log("[WeChat Callback] Requesting access token");

    const tokenResponse = await fetch(tokenUrl.toString());
    const tokenData = await tokenResponse.json();

    if (tokenData.errcode) {
      console.error("[WeChat Callback] Token request failed:", tokenData);
      return NextResponse.redirect(new URL(`${wechatConfig.redirect_uri}/auth/signin?error=wechat_token_error`, request.url));
    }

    console.log("[WeChat Callback] Access token received successfully");

    // Get user information
    const userinfoUrl = new URL("https://api.weixin.qq.com/sns/userinfo");
    userinfoUrl.searchParams.set("access_token", tokenData.access_token);
    userinfoUrl.searchParams.set("openid", tokenData.openid);
    userinfoUrl.searchParams.set("lang", "zh_CN");

    console.log("[WeChat Callback] Requesting user info");

    const userinfoResponse = await fetch(userinfoUrl.toString());
    const profile = await userinfoResponse.json();

    if (profile.errcode) {
      console.error("[WeChat Callback] Userinfo request failed:", profile);
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_userinfo_error', request.url));
    }

    console.log("[WeChat Callback] Processing profile:", {
      openid: profile.openid || "Not received",
      nickname: profile.nickname || "Not received",
      unionid: profile.unionid ? "Set" : "Not set"
    });

    // Call backend registration API
    const registerResponse = await fetch(`${process.env.NEXTAPI_URL}/api/v1/core/api/wechat_user_register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: profile.openid,
        nick_name: profile.nickname || profile.openid
      }),
    });

    const registerData = await registerResponse.json();
    console.log("[WeChat Callback] Register API response status:", registerResponse.status);
    console.log("[WeChat Callback] Register API response:", registerData);

    if (!registerResponse.ok || !registerData.result) {
      console.error("[WeChat Callback] Register API failed:", registerData);
      return NextResponse.redirect(new URL(`${wechatConfig.redirect_uri}/auth/signin?error=wechat_register_failed`, request.url));
    }

    const userData = registerData.data;
    console.log("[WeChat Callback] User registration successful, user ID:", userData.id);
    
    // Build user data including WeChat information for NextAuth
    const userDataForAuth = {
      id: userData.id.toString(),
      username: userData.username,
      token: userData.token,
      locale: userData.locale || 'zh',
      temporary_pwd: false,
      enable_otp: false,
      qrcode: false,
      provider: 'wechat',  // 重要：标记为微信登录
      wechatOpenId: profile.openid,     // 存储微信 OpenID
      wechatUnionId: profile.unionid,   // 存储微信 UnionID
      wechatNickname: profile.nickname, // 存储微信昵称
      wechatHeadImg: profile.headimgurl, // 存储微信头像
    };

    console.log("[WeChat Callback] Prepared user data for NextAuth:", {
      provider: userDataForAuth.provider,
      wechatOpenId: userDataForAuth.wechatOpenId ? "Set" : "Not set",
      wechatUnionId: userDataForAuth.wechatUnionId ? "Set" : "Not set",
    });

    // Save auth token to cookie for immediate access
    if (userData.token) {
      console.log("[WeChat Callback] User token received, setting cookies and redirecting", userData);
      const response = NextResponse.redirect(new URL(`${wechatConfig.redirect_uri}/auth/signin?wechat_success=true`, request.url));
      
      // Set user data in cookie for client-side NextAuth authentication
      response.cookies.set('wechat_user_data', JSON.stringify(userDataForAuth), {
        httpOnly: false, // Allow client-side access
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 300, // 5 minutes
        path: '/'
      });
      
      response.cookies.set('wechat_callback_url', callbackUrl, {
        httpOnly: false,
        secure: process.env.NODE_ENV === 'production', 
        sameSite: 'lax',
        maxAge: 300, // 5 minutes
        path: '/'
      });
      
      console.log("[WeChat Callback] Redirecting to signin page with user data in cookie");
      return response;
    } else {
      console.error("[WeChat Callback] No token received from registration");
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_token_missing', request.url));
    }
    
  } catch (error) {
    console.error("[WeChat Callback] Error processing callback:", error);
    console.error("[WeChat Callback] Error stack:", error instanceof Error ? error.stack : 'No stack trace');
    return NextResponse.redirect(new URL('/auth/signin?error=wechat_callback_error', request.url));
  }
}