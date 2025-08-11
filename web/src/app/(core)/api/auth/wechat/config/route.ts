import { NextResponse } from 'next/server';

// API for checking WeChat configuration availability
export async function GET() {
  try {
    // Get WeChat configuration
    const response = await fetch(`${process.env.NEXTAPI_URL}/api/v1/core/api/get_wechat_settings/`, {
      method: "GET",
      headers: { 
        "Content-Type": "application/json",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
      },
      cache: "no-store"
    });
    
    const responseData = await response.json();
    
    if (!response.ok || !responseData.result) {
      console.log("WeChat settings not available:", responseData);
      return NextResponse.json({
        available: false,
        message: "WeChat login is not configured"
      });
    }
    
    const wechatConfig = responseData.data;
    
    // Check if required configuration exists
    if (!wechatConfig.app_id || !wechatConfig.app_secret) {
      return NextResponse.json({
        available: false,
        message: "WeChat configuration is incomplete"
      });
    }
    
    // Return configuration availability status without sensitive information
    return NextResponse.json({
      available: true,
      redirectUri: wechatConfig.redirect_uri,
      message: "WeChat login is available"
    });
    
  } catch (error) {
    console.error("Error checking WeChat configuration:", error);
    return NextResponse.json({
      available: false,
      message: "Unable to check WeChat configuration"
    }, { status: 500 });
  }
}