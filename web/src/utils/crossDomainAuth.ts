import { signIn } from "next-auth/react";

interface SharedAuthData {
  id: string;
  username: string;
  token: string;
  locale: string;
  temporary_pwd: boolean;
  enable_otp: boolean;
  qrcode: boolean;
  provider?: string;
  wechatOpenId?: string;
  wechatUnionId?: string;
  wechatWorkId?: string;
  timestamp: number;
  expires: number;
}

const AUTH_EXPIRY_HOURS = 24;
const STORAGE_KEY = 'bk_shared_auth';

/**
 * Get base identifier (for cross-port/subdomain sharing)
 */
function getBaseIdentifier(): string {
  const hostname = window.location.hostname;
  
  // IP address: return IP (ignore port)
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) {
    return hostname;
  }
  
  // localhost: return localhost (ignore port)
  if (hostname === 'localhost') {
    return 'localhost';
  }
  
  // Domain: extract root domain
  const parts = hostname.split('.');
  if (parts.length >= 2) {
    return parts.slice(-2).join('.'); // e.g.: canway.net
  }
  
  return hostname;
}

/**
 * Generate storage key (based on base identifier)
 */
function getStorageKey(): string {
  const baseId = getBaseIdentifier();
  return `${STORAGE_KEY}_${baseId.replace(/\./g, '_')}`;
}

/**
 * Set cross-domain/cross-port cookie
 */
function setCrossDomainCookie(name: string, value: string, hours: number = AUTH_EXPIRY_HOURS): void {
  const hostname = window.location.hostname;
  const expires = new Date();
  expires.setTime(expires.getTime() + (hours * 60 * 60 * 1000));
  
  const cookieOptions = `expires=${expires.toUTCString()}; path=/; SameSite=Lax`;
  
  // IP address or localhost: can only set to current domain
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname) || hostname === 'localhost') {
    document.cookie = `${name}=${value}; ${cookieOptions}`;
    return;
  }
  
  // Domain: try to set to root domain to support subdomain sharing
  const baseId = getBaseIdentifier();
  if (baseId.includes('.') && hostname !== baseId) {
    // Set to root domain (support subdomain sharing)
    document.cookie = `${name}=${value}; ${cookieOptions}; domain=.${baseId}`;
  }
  
  // Always set to current domain
  document.cookie = `${name}=${value}; ${cookieOptions}`;
}

/**
 * Get cookie value
 */
function getCookie(name: string): string | null {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  return null;
}

/**
 * Delete cross-domain/cross-port cookie
 */
function deleteCrossDomainCookie(name: string): void {
  const hostname = window.location.hostname;
  const pastDate = 'Thu, 01 Jan 1970 00:00:00 UTC';
  
  // Delete current domain cookie
  document.cookie = `${name}=; expires=${pastDate}; path=/`;
  
  // If it's a domain, also delete root domain cookie
  if (!(/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) && hostname !== 'localhost') {
    const baseId = getBaseIdentifier();
    if (baseId.includes('.') && hostname !== baseId) {
      document.cookie = `${name}=; expires=${pastDate}; path=/; domain=.${baseId}`;
    }
  }
}

/**
 * Cross-port storage (for IP+port and localhost+port scenarios)
 */
function setCrossPortStorage(key: string, value: string): void {
  const hostname = window.location.hostname;
  
  // Only use cross-port storage for IP addresses and localhost
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname) || hostname === 'localhost') {
    try {
      // Use hostname-based key
      const crossPortKey = `${key}_${hostname}`;
      localStorage.setItem(crossPortKey, value);
      
      // Broadcast to other ports on same host (via BroadcastChannel)
      if (typeof BroadcastChannel !== 'undefined') {
        const channel = new BroadcastChannel('bk_auth_sync');
        channel.postMessage({
          type: 'AUTH_UPDATE',
          key: crossPortKey,
          value: value,
          hostname: hostname
        });
        channel.close();
      }
    } catch (error) {
      console.warn('Failed to set cross-port storage:', error);
    }
  }
}

/**
 * Get cross-port storage data
 */
function getCrossPortStorage(key: string): string | null {
  const hostname = window.location.hostname;
  
  // Only try cross-port retrieval for IP addresses and localhost
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname) || hostname === 'localhost') {
    try {
      const crossPortKey = `${key}_${hostname}`;
      return localStorage.getItem(crossPortKey);
    } catch (error) {
      console.warn('Failed to get cross-port storage:', error);
      return null;
    }
  }
  
  return null;
}

/**
 * Clear cross-port storage data
 */
function clearCrossPortStorage(key: string): void {
  const hostname = window.location.hostname;
  
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname) || hostname === 'localhost') {
    try {
      const crossPortKey = `${key}_${hostname}`;
      localStorage.removeItem(crossPortKey);
      
      // Broadcast clear message
      if (typeof BroadcastChannel !== 'undefined') {
        const channel = new BroadcastChannel('bk_auth_sync');
        channel.postMessage({
          type: 'AUTH_CLEAR',
          key: crossPortKey,
          hostname: hostname
        });
        channel.close();
      }
    } catch (error) {
      console.warn('Failed to clear cross-port storage:', error);
    }
  }
}

/**
 * Set up cross-port listener (listen for auth data sync from other ports)
 */
function setupCrossPortListener(): void {
  if (typeof window === 'undefined' || typeof BroadcastChannel === 'undefined') {
    return;
  }
  
  const channel = new BroadcastChannel('bk_auth_sync');
  const hostname = window.location.hostname;
  
  channel.addEventListener('message', (event) => {
    const { type, key, value, hostname: senderHostname } = event.data;
    
    // Only handle messages from same host
    if (senderHostname !== hostname) return;
    
    try {
      if (type === 'AUTH_UPDATE') {
        localStorage.setItem(key, value);
        console.log('Cross-port auth data synced:', key);
      } else if (type === 'AUTH_CLEAR') {
        localStorage.removeItem(key);
        console.log('Cross-port auth data cleared:', key);
      }
    } catch (error) {
      console.warn('Failed to sync cross-port auth data:', error);
    }
  });
  
  // Close channel on page unload
  window.addEventListener('beforeunload', () => {
    channel.close();
  });
}

// Initialize cross-port listener
if (typeof window !== 'undefined') {
  setupCrossPortListener();
}

/**
 * Save shared authentication state
 */
export function saveSharedAuthData(userData: Omit<SharedAuthData, 'timestamp' | 'expires'>): void {
  const now = Date.now();
  const expires = now + (AUTH_EXPIRY_HOURS * 60 * 60 * 1000);
  const storageKey = getStorageKey();
  
  const authData: SharedAuthData = {
    ...userData,
    timestamp: now,
    expires
  };
  
  const authDataStr = JSON.stringify(authData);
  
  try {
    // 1. Save to cookie (support subdomain sharing)
    setCrossDomainCookie(storageKey, authDataStr, AUTH_EXPIRY_HOURS);
    
    // 2. Save to localStorage (local domain backup)
    localStorage.setItem(storageKey, authDataStr);
    
    // 3. Cross-port storage (IP+port and localhost+port scenarios)
    setCrossPortStorage(storageKey, authDataStr);
    
    console.log('Shared auth data saved successfully for:', getBaseIdentifier());
  } catch (error) {
    console.error('Failed to save shared auth data:', error);
  }
}

/**
 * Get shared authentication state data
 */
export function getSharedAuthData(): SharedAuthData | null {
  const storageKey = getStorageKey();
  
  try {
    // 1. Prefer getting from cookie (support cross-subdomain)
    let authDataStr = getCookie(storageKey);
    
    // 2. If no cookie, try localStorage
    if (!authDataStr) {
      authDataStr = localStorage.getItem(storageKey);
    }
    
    // 3. If still none, try cross-port retrieval (IP+port scenario)
    if (!authDataStr) {
      authDataStr = getCrossPortStorage(storageKey);
    }
    
    if (!authDataStr) {
      return null;
    }
    
    const authData: SharedAuthData = JSON.parse(authDataStr);
    
    // Check if expired
    if (Date.now() > authData.expires) {
      clearSharedAuthData();
      return null;
    }
    
    return authData;
  } catch (error) {
    console.error('Failed to get shared auth data:', error);
    return null;
  }
}

/**
 * Clear shared authentication state data
 */
export function clearSharedAuthData(): void {
  const storageKey = getStorageKey();
  
  try {
    // 1. Clear cookie
    deleteCrossDomainCookie(storageKey);
    
    // 2. Clear localStorage
    localStorage.removeItem(storageKey);
    
    // 3. Clear cross-port storage
    clearCrossPortStorage(storageKey);
    
    console.log('Shared auth data cleared for:', getBaseIdentifier());
  } catch (error) {
    console.error('Failed to clear shared auth data:', error);
  }
}

/**
 * Check and auto sign-in (if there is valid shared authentication state)
 */
export async function autoSignInFromSharedAuth(callbackUrl?: string): Promise<boolean> {
  const sharedAuth = getSharedAuthData();
  
  if (!sharedAuth) {
    return false;
  }
  
  try {
    console.log('Found shared auth data, attempting auto sign-in for:', getBaseIdentifier());
    
    const result = await signIn("credentials", {
      redirect: false,
      username: sharedAuth.username,
      password: '',
      skipValidation: 'true',
      userData: JSON.stringify(sharedAuth),
      callbackUrl: callbackUrl || "/",
    });
    
    if (result?.ok) {
      console.log('Auto sign-in successful');
      return true;
    } else {
      console.error('Auto sign-in failed:', result?.error);
      clearSharedAuthData();
      return false;
    }
  } catch (error) {
    console.error('Error during auto sign-in:', error);
    clearSharedAuthData();
    return false;
  }
}

/**
 * Validate shared authentication token
 */
export async function validateSharedAuthToken(token: string): Promise<boolean> {
  try {
    const response = await fetch('/api/proxy/core/api/validate_token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ token })
    });
    
    const data = await response.json();
    return response.ok && data.result;
  } catch (error) {
    console.error('Token validation failed:', error);
    return false;
  }
}

/**
 * Get current configuration information (for debugging)
 */
export function getAuthConfig() {
  return {
    baseIdentifier: getBaseIdentifier(),
    storageKey: getStorageKey(),
    hostname: window.location.hostname,
    port: window.location.port,
    isIP: /^\d+\.\d+\.\d+\.\d+$/.test(window.location.hostname),
    isLocalhost: window.location.hostname === 'localhost',
    supportsBroadcastChannel: typeof BroadcastChannel !== 'undefined'
  };
}