import { createBrowserClient, createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

// 環境変数を検証する関数
function getSupabaseConfig() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  
  // 環境変数が設定されていない場合はデフォルト値を使用
  return { supabaseUrl, supabaseKey };
}

// ブラウザ用のSupabaseクライアント
export function createClient() {
  // ブラウザ環境でのみ実行
  if (typeof window === 'undefined') {
    return null;
  }
  
  const { supabaseUrl, supabaseKey } = getSupabaseConfig();
  
  return createBrowserClient({
    supabaseUrl,
    supabaseKey,
  });
}

// サーバー用のSupabaseクライアント
export function createServerSupabaseClient() {
  const { supabaseUrl, supabaseKey } = getSupabaseConfig();
  const cookieStore = cookies();
  
  return createServerClient(
    supabaseUrl,
    supabaseKey,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: Record<string, any>) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: Record<string, any>) {
          cookieStore.set({ name, value: '', ...options });
        },
      },
    }
  );
}
