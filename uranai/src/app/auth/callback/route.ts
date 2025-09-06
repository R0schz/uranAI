import { createSupabaseServerClient } from '@/lib/supabase/server';
import { NextRequest, NextResponse } from 'next/server';

/**
 * Supabaseの認証コールバックを処理するルートハンドラ
 * @param request NextRequest
 * @returns NextResponse
 */
export async function GET(request: NextRequest) {
  // リクエストURLからクエリパラメータを取得
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  // nextはSupabaseのOAuthプロバイダ設定で指定したリダイレクト先
  const next = searchParams.get('next') ?? '/';

  // 認証コードがあればセッションと交換
  if (code) {
    const supabase = await createSupabaseServerClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (!error) {
      // 成功した場合、指定されたページ（デフォルトはホームページ）にリダイレクト
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  // エラーが発生した場合やコードがない場合は、エラーページにリダイレクト
  // ここではシンプルにホームページに戻しています
  console.error('Authentication callback error');
  return NextResponse.redirect(`${origin}/auth/auth-code-error`);
}