"use client";

import { useEffect } from 'react';

interface TarotShuffleProps {
  onComplete: () => void;
  cardBackUrl: string;
}

const TarotShuffle = ({ onComplete, cardBackUrl }: TarotShuffleProps) => {
  useEffect(() => {
    const container = document.querySelector('.tarot-shuffle-container');
    if (!container) return;

    // Clear existing cards
    container.innerHTML = '';

    // Create new cards
    for (let i = 0; i < 8; i++) {
      const card = document.createElement('div');
      card.className = 'tarot-shuffle-card';
      card.style.animationDelay = `${i * 0.1}s`;
      card.style.backgroundImage = `url(${cardBackUrl})`;
      container.appendChild(card);
    }

    // Set timeout to trigger completion
    const timer = setTimeout(onComplete, 3500);

    return () => clearTimeout(timer);
  }, [onComplete, cardBackUrl]);

  return (
    <div className="page-content flex flex-col items-center justify-center">
      <div className="tarot-shuffle-container"></div>
      <p className="font-serif-special text-xl text-gray-200 mt-12 animate-pulse">
        運命を読み解いています...
      </p>
    </div>
  );
};

export default TarotShuffle;
