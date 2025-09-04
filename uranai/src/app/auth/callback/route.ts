import { createServerSupabaseClient } from '../../lib/supabase'
import { NextResponse } from 'next/server'

import type { NextRequest } from 'next/server'

export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = createServerSupabaseClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // 認証後のリダイレクト先URL
  return NextResponse.redirect(requestUrl.origin)
}