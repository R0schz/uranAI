"use client";

import React, { useState } from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Modal from './Modal';

const RegisterModal = () => {
  const { hideModal, showModal, register } = useAppContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async () => {
    setError('');
    if (password !== confirmPassword) {
      setError('パスワードが一致しません');
      return;
    }
    try {
      await register(email, password);
      hideModal();
    } catch (err: any) {
      setError(err.message || '登録に失敗しました');
    }
  };

  const handleShowLogin = () => {
    showModal('login');
  };

  return (
    <Modal onClose={hideModal}>
      <h2 className="font-serif-special text-2xl text-center mb-6">新規登録</h2>
      <div className="space-y-4">
        <input
          type="email"
          placeholder="メールアドレス"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="form-input w-full p-3"
        />
        <input
          type="password"
          placeholder="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="form-input w-full p-3"
        />
        <input
          type="password"
          placeholder="パスワード（確認）"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="form-input w-full p-3"
        />
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <button
          onClick={handleRegister}
          className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-full transition"
        >
          登録する
        </button>
        <p className="text-center text-sm text-gray-400">
          すでにアカウントをお持ちの方は
          <button
            onClick={handleShowLogin}
            className="text-purple-400 hover:text-purple-300 ml-1"
          >
            ログイン
          </button>
        </p>
      </div>
    </Modal>
  );
};

export default RegisterModal;
