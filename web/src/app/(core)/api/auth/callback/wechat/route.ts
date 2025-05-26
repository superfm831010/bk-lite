import { NextRequest, NextResponse } from "next/server";
import { handler } from "@/lib/auth";

// Handle GET requests
export async function GET(request: NextRequest) {
  try {
    // Extract the code and state from the URL
    const searchParams = request.nextUrl.searchParams;
    const code = searchParams.get("code");
    const state = searchParams.get("state");
    
    // Create a new request with the provider and callback parameters
    const callbackUrl = new URL(request.url);
    callbackUrl.searchParams.set("provider", "wechat");
    
    // Create a modified request to pass to NextAuth
    const nextAuthRequest = new Request(callbackUrl, {
      method: "POST",
      headers: request.headers,
      body: JSON.stringify({ code, state, provider: "wechat" }),
      credentials: "include"
    });
    
    console.log("[WeChat Callback] Processing callback with params:", { code, state });
    
    // Pass control to NextAuth handler
    return await handler(nextAuthRequest);
  } catch (error) {
    console.error("[WeChat Callback] Error processing GET request:", error);
    return NextResponse.json({ error: "Authentication callback failed" }, { status: 500 });
  }
}

// Handle POST requests (in case NextAuth redirects here with POST)
export async function POST(request: NextRequest) {
  try {
    console.log("[WeChat Callback] Received POST request");
    return await handler(request);
  } catch (error) {
    console.error("[WeChat Callback] Error processing POST request:", error);
    return NextResponse.json({ error: "Authentication callback failed" }, { status: 500 });
  }
}