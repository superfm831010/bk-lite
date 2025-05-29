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
 * Get host identifier (hostname + port for cross-port scenarios)
 */
function getHostIdentifier(): string {
  const hostname = window.location.hostname;
  const port = window.location.port;
  
  // Include port if it exists and is not default
  if (port && port !== '80' && port !== '443') {
    return `${hostname}:${port}`;
  }
  
  return hostname;
}

/**
 * Check if cross-port sharing should be enabled
 */
function shouldUseCrossPortSharing(): boolean {
  const hostname = window.location.hostname;
  const port = window.location.port;
  
  // Enable cross-port for IP addresses, localhost, or domains with non-standard ports
  return (
    /^\d+\.\d+\.\d+\.\d+$/.test(hostname) || 
    hostname === 'localhost' || 
    (!!port && port !== '80' && port !== '443')
  );
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
 * Cross-port storage (enhanced for all cross-port scenarios)
 */
function setCrossPortStorage(key: string, value: string): void {
  if (!shouldUseCrossPortSharing()) {
    return;
  }
  
  try {
    const baseId = getBaseIdentifier();
    const hostId = getHostIdentifier();
    
    // Use base identifier for cross-port key to enable sharing across ports
    const crossPortKey = `${key}_${baseId}`;
    localStorage.setItem(crossPortKey, value);
    
    // Broadcast to other ports on same base domain (via BroadcastChannel)
    if (typeof BroadcastChannel !== 'undefined') {
      const channel = new BroadcastChannel('bk_auth_sync');
      channel.postMessage({
        type: 'AUTH_UPDATE',
        key: crossPortKey,
        value: value,
        baseId: baseId,
        hostId: hostId
      });
      channel.close();
    }
  } catch (error) {
    console.warn('Failed to set cross-port storage:', error);
  }
}

/**
 * Get cross-port storage data (enhanced for all cross-port scenarios)
 */
function getCrossPortStorage(key: string): string | null {
  if (!shouldUseCrossPortSharing()) {
    return null;
  }
  
  try {
    const baseId = getBaseIdentifier();
    const crossPortKey = `${key}_${baseId}`;
    return localStorage.getItem(crossPortKey);
  } catch (error) {
    console.warn('Failed to get cross-port storage:', error);
    return null;
  }
}

/**
 * Clear cross-port storage data (enhanced for all cross-port scenarios)
 */
function clearCrossPortStorage(key: string): void {
  if (!shouldUseCrossPortSharing()) {
    return;
  }
  
  try {
    const baseId = getBaseIdentifier();
    const hostId = getHostIdentifier();
    const crossPortKey = `${key}_${baseId}`;
    
    localStorage.removeItem(crossPortKey);
    
    // Broadcast clear message
    if (typeof BroadcastChannel !== 'undefined') {
      const channel = new BroadcastChannel('bk_auth_sync');
      channel.postMessage({
        type: 'AUTH_CLEAR',
        key: crossPortKey,
        baseId: baseId,
        hostId: hostId
      });
      channel.close();
    }
  } catch (error) {
    console.warn('Failed to clear cross-port storage:', error);
  }
}

/**
 * Set up cross-port listener (enhanced for all cross-port scenarios)
 */
function setupCrossPortListener(): void {
  if (typeof window === 'undefined' || typeof BroadcastChannel === 'undefined') {
    return;
  }
  
  const channel = new BroadcastChannel('bk_auth_sync');
  const baseId = getBaseIdentifier();
  
  channel.addEventListener('message', (event) => {
    const { type, key, value, baseId: senderBaseId, hostId: senderHostId, storageKeyPrefix } = event.data;
    
    // Only handle messages from same base domain (allows cross-port communication)
    if (senderBaseId !== baseId) return;
    
    try {
      if (type === 'AUTH_UPDATE') {
        localStorage.setItem(key, value);
        console.log('Cross-port auth data synced:', key, 'from:', senderHostId);
      } else if (type === 'AUTH_CLEAR') {
        localStorage.removeItem(key);
        console.log('Cross-port auth data cleared:', key, 'from:', senderHostId);
      } else if (type === 'AUTH_CLEAR_ALL') {
        // Clear all related storage keys for comprehensive logout
        const storageKeys = [];
        for (let i = 0; i < localStorage.length; i++) {
          const storageKey = localStorage.key(i);
          if (storageKey && storageKey.includes(`${storageKeyPrefix}_`) && 
              (storageKey.endsWith(`_${baseId}`) || storageKey.includes(`_${baseId}_`))) {
            storageKeys.push(storageKey);
          }
        }
        
        storageKeys.forEach(storageKey => {
          localStorage.removeItem(storageKey);
          console.log('Cross-port auth data cleared (all):', storageKey, 'from:', senderHostId);
        });
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
 * Clear all related domain storage keys (for comprehensive logout)
 */
function clearAllRelatedStorageKeys(): void {
  const baseId = getBaseIdentifier();
  const hostname = window.location.hostname;
  
  try {
    // Get all localStorage keys that might be related to this domain
    const storageKeys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(STORAGE_KEY)) {
        storageKeys.push(key);
      }
    }
    
    // Filter keys that are related to current domain
    const relatedKeys = storageKeys.filter(key => {
      // Extract domain part from key (remove STORAGE_KEY prefix and underscore replacement)
      const keyDomain = key.replace(`${STORAGE_KEY}_`, '').replace(/_/g, '.');
      
      // Check if this key is related to current domain
      if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname) || hostname === 'localhost') {
        // For IP/localhost, only clear exact matches
        return keyDomain === hostname;
      } else {
        // For domains, clear both root domain and subdomains
        return keyDomain === baseId || keyDomain.endsWith(`.${baseId}`) || baseId.endsWith(`.${keyDomain}`);
      }
    });
    
    // Clear all related keys
    relatedKeys.forEach(key => {
      localStorage.removeItem(key);
      console.log('Cleared related storage key:', key);
    });
    
  } catch (error) {
    console.warn('Failed to clear related storage keys:', error);
  }
}

/**
 * Clear all related domain cookies (for comprehensive logout)
 */
function clearAllRelatedCookies(): void {
  const hostname = window.location.hostname;
  const baseId = getBaseIdentifier();
  const pastDate = 'Thu, 01 Jan 1970 00:00:00 UTC';
  
  // Get all cookies and find related ones
  const cookies = document.cookie.split(';');
  const relatedCookieNames = [];
  
  for (const cookie of cookies) {
    const [name] = cookie.trim().split('=');
    if (name && name.startsWith(STORAGE_KEY)) {
      relatedCookieNames.push(name);
    }
  }
  
  // Clear all related cookies
  relatedCookieNames.forEach(cookieName => {
    // Clear for current domain
    document.cookie = `${cookieName}=; expires=${pastDate}; path=/`;
    
    // For non-IP/localhost domains, also clear root domain cookies
    if (!(/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) && hostname !== 'localhost') {
      if (baseId.includes('.') && hostname !== baseId) {
        document.cookie = `${cookieName}=; expires=${pastDate}; path=/; domain=.${baseId}`;
      }
    }
    
    console.log('Cleared related cookie:', cookieName);
  });
}

/**
 * Broadcast subdomain logout to clear next-auth sessions across subdomains
 */
function broadcastSubdomainLogout(): void {
  if (typeof window === 'undefined' || typeof BroadcastChannel === 'undefined') {
    return;
  }
  
  const baseId = getBaseIdentifier();
  const hostId = getHostIdentifier();
  
  try {
    // Use a dedicated channel for subdomain logout notifications
    const channel = new BroadcastChannel('bk_subdomain_logout');
    channel.postMessage({
      type: 'SUBDOMAIN_LOGOUT',
      baseId: baseId,
      hostId: hostId,
      timestamp: Date.now()
    });
    channel.close();
    
    console.log('Broadcasted subdomain logout from:', hostId);
  } catch (error) {
    console.warn('Failed to broadcast subdomain logout:', error);
  }
}

/**
 * Set up subdomain logout listener
 */
function setupSubdomainLogoutListener(): void {
  if (typeof window === 'undefined' || typeof BroadcastChannel === 'undefined') {
    return;
  }
  
  const channel = new BroadcastChannel('bk_subdomain_logout');
  const baseId = getBaseIdentifier();
  const hostId = getHostIdentifier();
  
  channel.addEventListener('message', (event) => {
    const { type, baseId: senderBaseId, hostId: senderHostId } = event.data;
    
    // Only handle logout messages from same base domain but different hosts
    if (type === 'SUBDOMAIN_LOGOUT' && senderBaseId === baseId && senderHostId !== hostId) {
      console.log('Received subdomain logout notification from:', senderHostId);
      
      try {
        // Clear local storage data
        const storageKey = getStorageKey();
        localStorage.removeItem(storageKey);
        
        // Clear all related storage keys
        clearAllRelatedStorageKeys();
        
        // Clear local cookies (current subdomain)
        clearAllRelatedCookies();
        
        // Clear cross-port storage if applicable
        clearAllCrossPortStorage();
        
        // Trigger next-auth signOut to clear session
        if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
          // Import signOut dynamically to avoid circular dependencies
          import('next-auth/react').then(({ signOut }) => {
            signOut({ redirect: false }).catch(console.error);
          }).catch(console.error);
        }
        
        console.log('Local auth data cleared due to subdomain logout');
      } catch (error) {
        console.warn('Failed to handle subdomain logout:', error);
      }
    }
  });
  
  // Close channel on page unload
  window.addEventListener('beforeunload', () => {
    channel.close();
  });
}

/**
 * Clear all cross-port storage data (enhanced for comprehensive logout)
 */
function clearAllCrossPortStorage(): void {
  const baseId = getBaseIdentifier();
  const hostId = getHostIdentifier();
  
  if (!shouldUseCrossPortSharing()) {
    return;
  }
  
  try {
    // Get all localStorage keys and find cross-port related ones
    const storageKeys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.includes(`${STORAGE_KEY}_`) && 
          (key.endsWith(`_${baseId}`) || key.includes(`_${baseId}_`))) {
        storageKeys.push(key);
      }
    }
    
    // Clear all related cross-port keys
    storageKeys.forEach(key => {
      localStorage.removeItem(key);
      console.log('Cleared cross-port storage key:', key);
    });
    
    // Broadcast clear message to all ports on same base domain
    if (typeof BroadcastChannel !== 'undefined') {
      const channel = new BroadcastChannel('bk_auth_sync');
      channel.postMessage({
        type: 'AUTH_CLEAR_ALL',
        baseId: baseId,
        hostId: hostId,
        storageKeyPrefix: STORAGE_KEY
      });
      channel.close();
    }
    
  } catch (error) {
    console.warn('Failed to clear cross-port storage:', error);
  }
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
 * Clear shared authentication state data (enhanced for comprehensive logout)
 */
export function clearSharedAuthData(): void {
  const storageKey = getStorageKey();
  
  try {
    // 1. Clear current domain cookie
    deleteCrossDomainCookie(storageKey);
    
    // 2. Clear current domain localStorage
    localStorage.removeItem(storageKey);
    
    // 3. Clear current domain cross-port storage
    clearCrossPortStorage(storageKey);
    
    // 4. Enhanced: Clear all related domain storage keys
    clearAllRelatedStorageKeys();
    
    // 5. Enhanced: Clear all related domain cookies
    clearAllRelatedCookies();
    
    // 6. Enhanced: Clear all cross-port storage data
    clearAllCrossPortStorage();
    
    // 7. NEW: Broadcast logout to all subdomains to clear their next-auth sessions
    broadcastSubdomainLogout();
    
    console.log('All shared auth data cleared for domain and subdomains:', getBaseIdentifier());
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
 * Get current configuration information (enhanced for debugging)
 */
export function getAuthConfig() {
  return {
    baseIdentifier: getBaseIdentifier(),
    hostIdentifier: getHostIdentifier(),
    storageKey: getStorageKey(),
    hostname: window.location.hostname,
    port: window.location.port,
    isIP: /^\d+\.\d+\.\d+\.\d+$/.test(window.location.hostname),
    isLocalhost: window.location.hostname === 'localhost',
    shouldUseCrossPortSharing: shouldUseCrossPortSharing(),
    supportsBroadcastChannel: typeof BroadcastChannel !== 'undefined',
    currentUrl: window.location.href,
    scenarios: {
      'IP + Port': /^\d+\.\d+\.\d+\.\d+$/.test(window.location.hostname) && window.location.port,
      'Domain + Subdomain': !(/^\d+\.\d+\.\d+\.\d+$/.test(window.location.hostname)) && 
                             window.location.hostname !== 'localhost' && 
                             !window.location.port,
      'Domain + Port': !(/^\d+\.\d+\.\d+\.\d+$/.test(window.location.hostname)) && 
                       window.location.hostname !== 'localhost' && 
                       window.location.port && 
                       window.location.port !== '80' && 
                       window.location.port !== '443',
      'Localhost + Port': window.location.hostname === 'localhost' && window.location.port
    }
  };
}

// Initialize subdomain logout listener
if (typeof window !== 'undefined') {
  setupSubdomainLogoutListener();
}