"use client";

import { useState } from 'react';
import { useAppContext } from '../contexts/AppContext';

const LoginModal = () => {
  const { state, setState, login, register } = useAppContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      await login(email, password);
    } catch (err) {
      setError('ログインに失敗しました。');
    }
  };

  const handleRegister = async () => {
    try {
      await register(email, password);
    } catch (err) {
      setError('新規登録に失敗しました。');
    }
  };

  if (!state.isLoggedIn && state.currentScreen === 'login-modal') {
    return (
      <div className="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div className="bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-sm mx-auto p-8">
          <h2 className="font-serif-special text-2xl text-center mb-6">ログイン/新規登録</h2>
          <div className="space-y-4">
            <input
              className="form-input w-full p-3"
              type="email"
              placeholder="メールアドレス"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              className="form-input w-full p-3"
              type="password"
              placeholder="パスワード"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button
              className="btn-primary w-full text-white font-bold py-3 rounded-full"
              onClick={handleLogin}
            >
              ログイン
            </button>
            <p className="text-center text-sm text-gray-400">または</p>
            <button
              className="w-full bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 rounded-full"
              onClick={handleRegister}
            >
              新規登録
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default LoginModal;