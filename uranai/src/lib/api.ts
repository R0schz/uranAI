const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  password: string;
  nickname?: string;
}

interface DivinationRequest {
  type: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive';
  people: {
    id: number;
    name: string;
    birthDate: string;
    birthTime?: string;
    birthPlace?: string;
  }[];
  question?: string;
}

interface DivinationResult {
  type: string;
  visualData: any;
  aiMessage: string;
}

async function handleResponse<T>(response: Response): Promise<ApiResponse<T>> {
  if (!response.ok) {
    if (response.status === 401) {
      return { error: '認証エラー: ログインが必要です。' };
    }
    if (response.status === 403) {
      return { error: 'アクセス権限がありません。' };
    }
    if (response.status === 429) {
      return { error: 'リクエスト制限を超えました。しばらく待ってから再試行してください。' };
    }
    try {
      const errorData = await response.json();
      return { error: errorData.detail || '予期せぬエラーが発生しました。' };
    } catch {
      return { error: '予期せぬエラーが発生しました。' };
    }
  }
  const data = await response.json();
  return { data };
}

export const api = {
  auth: {
    login: async (credentials: LoginRequest): Promise<ApiResponse<{ token: string }>> => {
      try {
        const response = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },

    register: async (data: RegisterRequest): Promise<ApiResponse<{ token: string }>> => {
      try {
        const response = await fetch(`${API_URL}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },
  },

  divination: {
    getDivination: async (request: DivinationRequest): Promise<ApiResponse<DivinationResult>> => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/divination`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(request),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },

    askMore: async (questionId: string, question: string): Promise<ApiResponse<{ answer: string }>> => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/divination/${questionId}/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ question }),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },
  },

  person: {
    addPerson: async (person: {
      nickname: string;
      name?: string;
      birthDate?: string;
      birthTime?: string;
      birthPlace?: string;
    }): Promise<ApiResponse<{ id: number }>> => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/person`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(person),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },

    updatePerson: async (id: number, person: {
      nickname?: string;
      name?: string;
      birthDate?: string;
      birthTime?: string;
      birthPlace?: string;
    }): Promise<ApiResponse<void>> => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/person/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(person),
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },

    deletePerson: async (id: number): Promise<ApiResponse<void>> => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_URL}/person/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        return handleResponse(response);
      } catch (error) {
        return { error: 'ネットワークエラー: サーバーに接続できません。' };
      }
    },
  },
};
