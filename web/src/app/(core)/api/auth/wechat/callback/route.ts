import { NextRequest, NextResponse } from 'next/server';

// WeChat login callback route - directly complete NextAuth authentication
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  
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
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_token_error', request.url));
    }

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
    console.log("[WeChat Callback] Register API response:", registerData);

    if (!registerResponse.ok || !registerData.result) {
      console.error("[WeChat Callback] Register API failed:", registerData);
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_register_failed', request.url));
    }

    const userData = registerData.data;
    
    // Build user data for NextAuth
    const userDataForAuth = {
      id: userData.id.toString(),
      username: userData.username,
      token: userData.token,
      locale: userData.locale || 'zh',
      temporary_pwd: false,
      enable_otp: false,
      qrcode: false,
      provider: 'wechat',
      wechatOpenId: profile.openid,
      wechatUnionId: profile.unionid,
    };

    // Directly create NextAuth session - through internal API call
    const authUrl = new URL('/api/auth/callback/credentials', request.url);
    const formData = new URLSearchParams();
    formData.append('username', userDataForAuth.username || '');
    formData.append('password', ''); // WeChat login does not require password
    formData.append('skipValidation', 'true');
    formData.append('userData', JSON.stringify(userDataForAuth));
    formData.append('callbackUrl', callbackUrl);
    formData.append('redirect', 'false');

    const authResponse = await fetch(authUrl.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': request.headers.get('cookie') || '',
      },
      body: formData.toString(),
    });

    console.log("[WeChat Callback] Auth response status:", authResponse.status);

    if (authResponse.ok) {
      // Get authentication response cookies
      const setCookieHeaders = authResponse.headers.getSetCookie();
      
      // Create redirect response
      const redirectResponse = NextResponse.redirect(new URL(callbackUrl, request.url));
      
      // Forward NextAuth cookies to client
      setCookieHeaders.forEach(cookie => {
        const [nameValue, ...attributes] = cookie.split(';');
        const [name, value] = nameValue.split('=');
        
        redirectResponse.cookies.set({
          name: name.trim(),
          value: value || '',
          ...parseCookieAttributes(attributes)
        });
      });
      
      console.log("[WeChat Callback] Authentication successful, redirecting to:", callbackUrl);
      return redirectResponse;
    } else {
      console.error("[WeChat Callback] Authentication failed");
      return NextResponse.redirect(new URL('/auth/signin?error=wechat_auth_failed', request.url));
    }
    
  } catch (error) {
    console.error("[WeChat Callback] Error processing callback:", error);
    return NextResponse.redirect(new URL('/auth/signin?error=wechat_callback_error', request.url));
  }
}

// Helper function: parse Cookie attributes
function parseCookieAttributes(attributes: string[]) {
  const result: any = {};
  
  attributes.forEach(attr => {
    const [key, value] = attr.trim().split('=');
    switch (key.toLowerCase()) {
      case 'httponly':
        result.httpOnly = true;
        break;
      case 'secure':
        result.secure = true;
        break;
      case 'samesite':
        result.sameSite = value || 'lax';
        break;
      case 'path':
        result.path = value;
        break;
      case 'max-age':
        result.maxAge = parseInt(value);
        break;
      case 'expires':
        result.expires = new Date(value);
        break;
    }
  });
  
  return result;
}