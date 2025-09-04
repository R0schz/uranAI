import { createBrowserClient } from '@supabase/ssr';

const supabase = createBrowserClient({
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://kkbhpbbjudjbwxnwpieg.supabase.co',
  supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrYmhwYmJqdWRqYnd4bndwaWVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5NzQ4NzQsImV4cCI6MjA1MDU1MDg3NH0.placeholder',
});

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// JWTトークンを取得する関数（自動更新機能付き）
async function getAuthToken(): Promise<string | null> {
  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    
    if (error) {
      console.error('Session error:', error);
      return null;
    }
    
    if (!session) {
      console.log('No active session found');
      return null;
    }
    
    // トークンの有効期限をチェック（5分前に更新）
    const now = Math.floor(Date.now() / 1000);
    const expiresAt = session.expires_at || 0;
    const timeUntilExpiry = expiresAt - now;
    
    if (timeUntilExpiry < 300) { // 5分未満の場合
      console.log('Token expires soon, refreshing...');
      const { data: refreshData, error: refreshError } = await supabase.auth.refreshSession();
      
      if (refreshError) {
        console.error('Token refresh failed:', refreshError);
        return null;
      }
      
      if (refreshData.session) {
        console.log('Token refreshed successfully');
        return refreshData.session.access_token;
      }
    }
    
    console.log('Using current token');
    return session.access_token;
  } catch (error) {
    console.error('Error getting auth token:', error);
    return null;
  }
}

// 認証ヘッダー付きのAPIリクエストを実行する関数
async function authenticatedRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = await getAuthToken();
  
  if (!token) {
    console.error('Authentication token not found');
    throw new Error('Authentication token not found');
  }

  console.log('Making authenticated request to:', `${API_BASE_URL}${endpoint}`);
  console.log('Token (first 20 chars):', token.substring(0, 20) + '...');
  console.log('Request options:', options);
  
  // リクエストボディの内容をログ出力
  if (options.body && typeof options.body === 'string') {
    try {
      const bodyData = JSON.parse(options.body);
      console.log('Request body data:', bodyData);
    } catch (e) {
      console.log('Request body (raw):', options.body);
    }
  }

  // タイムアウト設定（45秒）
  const controller = new AbortController();
  const timeoutId = setTimeout(() => {
    console.log('Request timeout after 45 seconds');
    controller.abort();
  }, 45000);

  try {
    console.log('Making fetch request to:', `${API_BASE_URL}${endpoint}`);
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    
    console.log('Response status:', response.status);
    console.log('Response headers:', Object.fromEntries(response.headers.entries()));
    console.log('Response ok:', response.ok);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('API request failed:', response.status, errorData);
      throw new Error(errorData.detail || `API request failed: ${response.status}`);
    }

    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    console.error('Request error:', error);
    console.error('Error type:', typeof error);
    console.error('Error name:', error instanceof Error ? error.name : 'Unknown');
    console.error('Error message:', error instanceof Error ? error.message : 'Unknown');
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('Request timeout - 占いの処理に時間がかかりすぎています。しばらく待ってから再度お試しください。');
    }
    throw error;
  }
}

// APIクライアント
export const api = {
  // ユーザー管理
  user: {
    create: async (userData: any) => {
      const response = await authenticatedRequest('/users/', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
      return response.json();
    },

    getCurrent: async () => {
      const response = await authenticatedRequest('/users/me');
      return response.json();
    },
  },

          // プロフィール管理
        profile: {
          create: async (profileData: any) => {
            const response = await authenticatedRequest('/profiles/', {
              method: 'POST',
              body: JSON.stringify(profileData),
            });
            return response.json();
          },

          getAll: async () => {
            console.log('Making API request to /profiles/');
            const response = await authenticatedRequest('/profiles/');
            console.log('API response received:', response.status);
            const data = await response.json();
            console.log('API response data:', data);
            return data;
          },

          update: async (id: number, profileData: any) => {
            const response = await authenticatedRequest(`/profiles/${id}`, {
              method: 'PUT',
              body: JSON.stringify(profileData),
            });
            return response.json();
          },

          delete: async (id: number) => {
            const response = await authenticatedRequest(`/profiles/${id}`, {
              method: 'DELETE',
            });
            return response.json();
          },
        },

  // 占い結果管理
  divination: {
    create: async (resultData: any) => {
      console.log('API divination.create called with:', resultData);
      const response = await authenticatedRequest('/divination-results/', {
        method: 'POST',
        body: JSON.stringify(resultData),
      });
      console.log('API divination.create response received:', response);
      const jsonData = await response.json();
      console.log('API divination.create json data:', jsonData);
      return jsonData;
    },

    getAll: async () => {
      const response = await authenticatedRequest('/divination-results/');
      return response.json();
    },

    getById: async (id: number) => {
      const response = await authenticatedRequest(`/divination-results/${id}`);
      return response.json();
    },
  },
};