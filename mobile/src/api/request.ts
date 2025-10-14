/**
 * API 客户端工具
 * 用于 Tauri 移动应用直接调用后端 API
 */

// 获取 API 基础 URL
const getApiBaseUrl = (): string => {
  // 开发环境：使用开发代理（避免 CORS）
  if (process.env.NODE_ENV === 'development') {
    return '/dev-proxy';
  }

  return process.env.NEXT_PUBLIC_API_URL || 'https://bklite.canway.net';
};

const API_BASE_URL = getApiBaseUrl();

/**
 * 创建带有默认配置的 fetch 请求
 */
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  console.log(`[API Request] ${options.method || 'GET'} ${url}`);

  // 从 localStorage 获取 token
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  // 合并默认配置
  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }), // 添加 token
      ...options.headers,
    },
    mode: 'cors', // 显式设置 CORS 模式
    credentials: 'include', // 发送 cookies
  };

  try {
    const response = await fetch(url, config);
    
    console.log(`[API Response] ${url} - Status: ${response.status}`);

    // 检查响应状态
    if (!response.ok) {
      let errorText = '';
      try {
        errorText = await response.text();
      } catch (e) {
        errorText = 'Unable to parse error response';
      }
      console.error(`[API Error] ${url} - ${response.status}: ${errorText}`);
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    // 尝试解析 JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }

    // 返回文本响应
    return await response.text() as any;
  } catch (error) {
    console.error(`[API Request Failed] ${url}:`, error);
    throw error;
  }
}

/**
 * GET 请求
 */
export async function apiGet<T = any>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'GET',
  });
}

/**
 * POST 请求
 */
export async function apiPost<T = any>(
  endpoint: string,
  data?: any,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  });
}

/**
 * PUT 请求
 */
export async function apiPut<T = any>(
  endpoint: string,
  data?: any,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  });
}

/**
 * DELETE 请求
 */
export async function apiDelete<T = any>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'DELETE',
  });
}

/**
 * PATCH 请求
 */
export async function apiPatch<T = any>(
  endpoint: string,
  data?: any,
  options?: RequestInit
): Promise<T> {
  return apiRequest<T>(endpoint, {
    ...options,
    method: 'PATCH',
    body: data ? JSON.stringify(data) : undefined,
  });
}

// 导出 API 基础 URL 供其他模块使用
export { API_BASE_URL };
