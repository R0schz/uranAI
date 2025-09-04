"use client";

import { useState } from 'react';
import { useAppStore } from '../contexts/AppContext';

const TarotTouchScreen = () => {
  const { setCurrentScreen } = useAppStore();
  const [isTouched, setIsTouched] = useState(false);

  const handleCardTouch = () => {
    if (!isTouched) {
      setIsTouched(true);
      // タッチされたらローディング画面に遷移
      setTimeout(() => {
        setCurrentScreen('tarot-loading-screen');
      }, 500);
    }
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto flex flex-col items-center justify-center min-h-[60vh]">
        <div className="text-center mb-8">
          <h2 className="font-serif-special text-3xl mb-4">タロットカードに触れる</h2>
          <p className="text-lg text-gray-300 mb-6">
            占いたいことについて考えながら<br />
            カードに触れてください
          </p>
        </div>
        
        <div className="relative">
          {/* タロットカードの裏面 */}
          <div
            onClick={handleCardTouch}
            className={`w-48 h-72 mx-auto cursor-pointer transition-all duration-500 ${
              isTouched 
                ? 'scale-110 rotate-3 shadow-2xl' 
                : 'hover:scale-105 hover:shadow-xl'
            }`}
            style={{
              backgroundImage: 'url(/images/tarot_back/tarot_back.png)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat',
              borderRadius: '12px',
              border: '2px solid #8b5cf6',
              boxShadow: isTouched 
                ? '0 25px 50px -12px rgba(139, 92, 246, 0.5)' 
                : '0 10px 25px -5px rgba(0, 0, 0, 0.3)'
            }}
          >
            {/* タッチ時のエフェクト */}
            {isTouched && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-16 h-16 bg-purple-500 rounded-full opacity-80 animate-ping"></div>
              </div>
            )}
          </div>
          

        </div>

        {/* タッチ後のメッセージ */}
        {isTouched && (
          <div className="mt-8 text-center">
            <p className="text-purple-300 font-medium animate-pulse">
              カードがあなたのエネルギーを感じ取っています...
            </p>
          </div>
        )}
      </div>
    </section>
  );
};

export default TarotTouchScreen;
