"use client";

import React from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Modal from './Modal';

interface Person {
  id: number;
  nickname: string;
  name?: string;
  birthDate?: string;
  birthTime?: string;
  birthPlace?: string;
}

const ConfirmPersonModal = () => {
  const { hideModal, showModal, state } = useAppContext();
  const selectedPerson = state.people.find(p => p.id === state.modalData?.personId);

  if (!selectedPerson) {
    hideModal();
    return null;
  }

  const handleEdit = () => {
    // TODO: 編集モーダルを実装
    hideModal();
  };

  const handleDelete = () => {
    // TODO: 削除確認モーダルを実装
    hideModal();
  };

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return '未設定';
    return new Date(dateStr).toLocaleDateString('ja-JP');
  };

  return (
    <Modal onClose={hideModal}>
      <div className="text-center">
        <div className="w-20 h-20 rounded-full bg-purple-900 flex items-center justify-center mx-auto mb-4">
          <span className="text-3xl font-bold">{selectedPerson.nickname.charAt(0)}</span>
        </div>
        <h2 className="font-serif-special text-2xl mb-6">{selectedPerson.nickname}</h2>
        <div className="space-y-4 mb-8">
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <p className="text-sm text-gray-400">名前（ひらがな）</p>
            <p className="text-lg">{selectedPerson.name || '未設定'}</p>
          </div>
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <p className="text-sm text-gray-400">生年月日</p>
            <p className="text-lg">{formatDate(selectedPerson.birthDate)}</p>
          </div>
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <p className="text-sm text-gray-400">出生時刻</p>
            <p className="text-lg">{selectedPerson.birthTime || '未設定'}</p>
          </div>
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <p className="text-sm text-gray-400">出生地</p>
            <p className="text-lg">{selectedPerson.birthPlace || '未設定'}</p>
          </div>
        </div>
        <div className="space-y-3">
          <button
            onClick={handleEdit}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-full transition flex items-center justify-center"
          >
            <i data-lucide="edit" className="w-5 h-5 mr-2"></i>
            編集する
          </button>
          <button
            onClick={handleDelete}
            className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-3 rounded-full transition flex items-center justify-center"
          >
            <i data-lucide="trash-2" className="w-5 h-5 mr-2"></i>
            削除する
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default ConfirmPersonModal;
