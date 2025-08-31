"use client";

import React from 'react';
import { useAppContext } from '../../contexts/AppContext';
import Modal from './Modal';

const PremiumModal = () => {
  const { hideModal } = useAppContext();

  const handleSubscribe = () => {
    // TODO: Stripe決済フローを実装
    hideModal();
  };

  return (
    <Modal onClose={hideModal} className="border-2 premium-glow">
      <div className="text-center">
        <i data-lucide="gem" className="w-12 h-12 mx-auto mb-4 text-yellow-300"></i>
        <h2 className="font-serif-special text-2xl mb-6">プレミアムプラン</h2>
        <div className="space-y-4 mb-8">
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <h3 className="text-lg font-bold text-yellow-300 mb-2">無制限の占い</h3>
            <p className="text-gray-300">チケットを気にせず、好きなだけ占えます</p>
          </div>
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <h3 className="text-lg font-bold text-yellow-300 mb-2">総合占い機能</h3>
            <p className="text-gray-300">全ての占術を組み合わせた詳細な鑑定が可能に</p>
          </div>
          <div className="bg-black bg-opacity-20 p-4 rounded-lg">
            <h3 className="text-lg font-bold text-yellow-300 mb-2">広告非表示</h3>
            <p className="text-gray-300">快適な占い体験をお楽しみいただけます</p>
          </div>
        </div>
        <div className="text-center mb-8">
          <p className="text-3xl font-bold">
            ¥980 <span className="text-sm font-normal text-gray-400">/ 月</span>
          </p>
          <p className="text-sm text-gray-400">いつでもキャンセル可能</p>
        </div>
        <button
          onClick={handleSubscribe}
          className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-3 rounded-full transition mb-4"
        >
          プレミアムプランに登録
        </button>
        <button
          onClick={hideModal}
          className="text-sm text-gray-400 hover:text-gray-300"
        >
          また後で
        </button>
      </div>
    </Modal>
  );
};

export default PremiumModal;