'use client'

import { createClient } from '../../lib/supabase'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  // クライアントコンポーネント用のSupabaseクライアントを作成
  const supabase = createClient()

  const handleSignUp = async () => {
    await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${location.origin}/auth/callback`,
      },
    })
    alert('確認メールを送信しました。メールボックスをご確認ください。')
    router.refresh()
  }

  const handleSignIn = async () => {
    await supabase.auth.signInWithPassword({
      email,
      password,
    })
    router.push('/') // トップページにリダイレクト
  }

  const handleOAuthSignIn = async (provider: 'google' | 'twitter' | 'facebook') => {
    await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${location.origin}/auth/callback`,
      },
    })
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2 bg-gray-50">
      <div className="p-8 bg-white border rounded-lg shadow-lg w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">ログイン</h1>
        <div className="space-y-4">
          <input
            type="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="メールアドレス"
            className="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 transition"
          />
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="パスワード"
            className="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 transition"
          />
        </div>
        <div className="mt-6 space-y-2">
          <button onClick={handleSignIn} className="w-full p-3 text-white bg-blue-600 rounded-md hover:bg-blue-700 font-semibold transition">
            ログイン
          </button>
          <button onClick={handleSignUp} className="w-full p-3 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 font-semibold transition">
            新規登録
          </button>
        </div>
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">または</span>
          </div>
        </div>
        <div className="space-y-3">
          <button onClick={() => handleOAuthSignIn('google')} className="w-full flex justify-center items-center p-3 border rounded-md hover:bg-gray-50 font-semibold transition">
            {/* ここにGoogleのSVGアイコンなどを入れると見栄えが良くなります */}
            <span className="ml-2">Googleでログイン</span>
          </button>
        </div>
      </div>
    </div>
  )
}