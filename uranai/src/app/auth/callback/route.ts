import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

import type { NextRequest } from 'next/server'

export const dynamic = 'force-dynamic';

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const cookieStore = cookies()
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          get(name: string) {
            return cookieStore.get(name)?.value
          },
          set(name: string, value: string, options: Record<string, any>) {
            cookieStore.set({ name, value, ...options })
          },
          remove(name: string, options: Record<string, any>) {
            cookieStore.set({ name, value: '', ...options })
          },
        },
      }
    )
    await supabase.auth.exchangeCodeForSession(code)
  }

  // 認証後のリダイレクト先URL
  return NextResponse.redirect(requestUrl.origin)
}