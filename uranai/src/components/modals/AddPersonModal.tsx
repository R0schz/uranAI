"use client";

import React, { useState } from 'react';
import { useAppContext, useAppStore } from '../../contexts/AppContext';
import Modal from './Modal';

const AddPersonModal = () => {
  const { addPerson } = useAppContext();
  // Zustandストアからモーダルを閉じる関数を取得
  const { hideModal } = useAppStore();
  
  const [nickname, setNickname] = useState('');
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [birthPlace, setBirthPlace] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!nickname.trim()) {
      setError('ニックネームは必須です');
      return;
    }
    
    // addPerson関数を呼び出す。成功すればAppContext内でモーダルが閉じられる。
    await addPerson({
      nickname,
      name,
      birthDate,
      birthTime,
      birthPlace,
    });
  };

  return (
    <Modal onClose={hideModal}>
      <h2 className="font-serif-special text-2xl text-center mb-6">新しい人物を登録</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">
            ニックネーム <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            placeholder="例: はなこ"
            className="form-input w-full p-3"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">
            名前（ひらがな）
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="例: やまだ はなこ"
            className="form-input w-full p-3"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">
            生年月日
          </label>
          <input
            type="date"
            value={birthDate}
            onChange={(e) => setBirthDate(e.target.value)}
            className="form-input w-full p-3"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">
            出生時刻
          </label>
          <input
            type="time"
            value={birthTime}
            onChange={(e) => setBirthTime(e.target.value)}
            className="form-input w-full p-3"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">
            出生地
          </label>
          <input
            type="text"
            value={birthPlace}
            onChange={(e) => setBirthPlace(e.target.value)}
            placeholder="例: 東京都渋谷区"
            className="form-input w-full p-3"
          />
        </div>
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <div className="pt-4">
          <button
            type="submit"
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-full transition"
          >
            登録する
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default AddPersonModal;