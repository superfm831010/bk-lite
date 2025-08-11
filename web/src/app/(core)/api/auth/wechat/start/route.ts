import { NextRequest, NextResponse } from 'next/server';

// WeChat login start route - dynamically fetch config
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const callbackUrl = searchParams.get('callbackUrl') || '/';
  
  try {
    // Dynamically fetch WeChat configuration only when needed
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
    
    if (!configResponse.ok || !configData.result || !configData.data.app_id) {
      console.error("WeChat configuration not available:", configData);
      return NextResponse.redirect(new URL(`/auth/signin?error=wechat_config_unavailable&callbackUrl=${encodeURIComponent(callbackUrl)}`, request.url));
    }
    
    const wechatConfig = configData.data;
    
    // Build WeChat authorization URL
    const state = encodeURIComponent(JSON.stringify({ callbackUrl }));
    
    // Use current request origin instead of backend configured redirect_uri
    const currentOrigin = new URL(request.url).origin;
    const redirectUri = `${currentOrigin}/api/auth/wechat/callback`;
    
    const wechatAuthUrl = new URL('https://open.weixin.qq.com/connect/qrconnect');
    wechatAuthUrl.searchParams.set('appid', wechatConfig.app_id);
    wechatAuthUrl.searchParams.set('redirect_uri', redirectUri);
    wechatAuthUrl.searchParams.set('response_type', 'code');
    wechatAuthUrl.searchParams.set('scope', 'snsapi_login');
    wechatAuthUrl.searchParams.set('state', state);
    
    console.log("[WeChat Login] Current origin:", currentOrigin);
    console.log("[WeChat Login] Redirect URI:", redirectUri);
    console.log("[WeChat Login] Redirecting to:", wechatAuthUrl.toString());
    
    return NextResponse.redirect(wechatAuthUrl.toString());
    
  } catch (error) {
    console.error("Error starting WeChat login:", error);
    return NextResponse.redirect(new URL(`/auth/signin?error=wechat_login_failed&callbackUrl=${encodeURIComponent(callbackUrl)}`, request.url));
  }
}