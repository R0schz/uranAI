"use client";

import { useEffect } from 'react';

interface TarotShuffleProps {
  onComplete: () => void;
  cardBackUrl?: string;
}

const TarotShuffle = ({ onComplete, cardBackUrl }: TarotShuffleProps) => {
  useEffect(() => {
    const container = document.querySelector('.tarot-shuffle-container');
    if (!container) {
      console.error('TarotShuffle: Container not found');
      return;
    }

    // Clear existing cards
    container.innerHTML = '';

    // Use the tarot back image if no cardBackUrl is provided
    const backImageUrl = cardBackUrl || '/images/tarot_back/tarot_back.png';
    console.log('TarotShuffle: Using image URL:', backImageUrl);

    // Create new cards with enhanced effects
    for (let i = 0; i < 10; i++) {
      const card = document.createElement('div');
      card.className = 'tarot-shuffle-card';
      card.style.animationDelay = `${i * 0.08}s`;
      card.style.backgroundImage = `url(${backImageUrl})`;
      card.style.backgroundSize = 'cover';
      card.style.backgroundPosition = 'center';
      card.style.backgroundRepeat = 'no-repeat';
      
      // 追加のスタイル設定
      card.style.filter = 'brightness(1.1) contrast(1.1)';
      card.style.backfaceVisibility = 'hidden';
      card.style.perspective = '1000px';
      
      container.appendChild(card);
    }

    console.log('TarotShuffle: Created', container.children.length, 'cards');

    // Set timeout to trigger completion (アニメーション時間に合わせて調整)
    const timer = setTimeout(() => {
      console.log('TarotShuffle: Animation complete, calling onComplete');
      onComplete();
    }, 4500); // 4.5秒（アニメーション4秒 + 余裕0.5秒）

    return () => {
      console.log('TarotShuffle: Cleanup');
      clearTimeout(timer);
    };
  }, [onComplete, cardBackUrl]);

  return (
    <div className="page-content flex flex-col items-center justify-center">
      <div className="tarot-shuffle-container"></div>
      <p className="font-serif-special text-xl text-gray-200 mt-16 animate-pulse">
        カードに触れて運命を読み解いています...
      </p>
      <p className="text-sm text-gray-400 mt-4 animate-bounce">
        占いたいことについて考えながらカードに触れてください
      </p>
    </div>
  );
};

export default TarotShuffle;
