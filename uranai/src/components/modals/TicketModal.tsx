"use client";

import React from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Modal from './Modal';

const TicketModal = () => {
  const { hideModal, showModal } = useAppContext();

  const handleWatchAd = () => {
    // TODO: 広告視聴ロジックを実装
    hideModal();
  };

  const handleShowPremium = () => {
    showModal('premium');
  };

  return (
    <Modal onClose={hideModal}>
      <div className="text-center">
        <i data-lucide="ticket" className="w-12 h-12 mx-auto mb-4 text-yellow-300"></i>
        <h2 className="font-serif-special text-2xl mb-4">チケットが不足しています</h2>
        <p className="text-gray-300 mb-8">
          この機能を利用するには<br />チケットが1枚必要です
        </p>
        <div className="space-y-4">
          <button
            onClick={handleWatchAd}
            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded-full transition flex items-center justify-center"
          >
            <i data-lucide="play-circle" className="w-5 h-5 mr-2"></i>
            広告を視聴してチケット獲得
          </button>
          <button
            onClick={handleShowPremium}
            className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-3 rounded-full transition flex items-center justify-center"
          >
            <i data-lucide="gem" className="w-5 h-5 mr-2"></i>
            プレミアムプランに登録
          </button>
          <button
            onClick={hideModal}
            className="text-sm text-gray-400 hover:text-gray-300"
          >
            また後で
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default TicketModal;