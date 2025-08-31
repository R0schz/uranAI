"use client";

import { useState } from 'react';
import { useAppContext, useAppStore } from '../../contexts/AppContext';
import Modal from './Modal';

const LoginModal = () => {
  // 関数はContextから、状態はZustandから取得
  const { login } = useAppContext();
  const { showModal, hideModal } = useAppStore();
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      alert('メールアドレスとパスワードを入力してください。');
      return;
    }
    await login(email, password);
  };

  const handleShowRegister = () => {
    showModal('register');
  };

  return (
    <Modal onClose={hideModal}>
      <h2 className="font-serif-special text-2xl text-center mb-6">ログイン</h2>
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
        <p className="text-center text-sm text-gray-400">
          アカウントをお持ちでない方は
          <button
            onClick={handleShowRegister}
            className="text-purple-400 hover:text-purple-300 ml-1"
          >
            新規登録
          </button>
        </p>
      </div>
    </Modal>
  );
};

export default LoginModal;