import { NextResponse } from 'next/server';

// Get WeChat configuration dynamically
export async function GET() {
  try {
    // Fetch WeChat configuration from backend
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
      console.error("Failed to get WeChat settings:", configData);
      return NextResponse.json(
        { 
          result: false, 
          message: "WeChat configuration not available",
          data: { enabled: false }
        },
        { status: 200 }
      );
    }
    
    // Return configuration with enabled flag
    return NextResponse.json({
      result: true,
      data: {
        enabled: true,
        ...configData.data
      }
    });
    
  } catch (error) {
    console.error("Error fetching WeChat configuration:", error);
    return NextResponse.json(
      { 
        result: false, 
        message: "Failed to fetch WeChat configuration",
        data: { enabled: false }
      },
      { status: 500 }
    );
  }
}