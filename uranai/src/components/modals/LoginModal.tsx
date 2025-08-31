"use client";

import { useState } from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Modal from './Modal';

const LoginModal = () => {
  const { state, showModal, hideModal, login, setCurrentScreen } = useAppContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  if (state.isLoggedIn) return null;

  const handleLogin = async () => {
    if (!email || !password) {
      alert('メールアドレスとパスワードを入力してください。');
      return;
    }
    try {
      await login(email, password);
      hideModal();
      setCurrentScreen('home-screen');
    } catch (error) {
      alert('ログインに失敗しました。');
    }
  };

  const handleShowRegister = () => {
    showModal('register');
  };

  return (
    <Modal onClose={hideModal}>
      <div className="bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-sm mx-auto fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 p-8">
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
          <button
            onClick={handleLogin}
            className="btn-primary w-full text-white font-bold py-3 rounded-full"
          >
            ログイン
          </button>
          <p className="text-center text-sm text-gray-400">または</p>
          <button
            onClick={handleShowRegister}
            className="w-full bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 rounded-full"
          >
            新規登録
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default LoginModal;
