"use client";

import { useEffect } from 'react';

const StarBackground = () => {
  useEffect(() => {
    const starsContainer = document.getElementById('stars-container');
    if (!starsContainer) return;

    for (let i = 0; i < 100; i++) {
      const star = document.createElement('div');
      star.className = 'star';
      const size = Math.random() * 3 + 1;
      star.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        top: ${Math.random() * 100}%;
        left: ${Math.random() * 100}%;
        animation-delay: ${Math.random() * 5}s;
        animation-duration: ${Math.random() * 3 + 4}s;
      `;
      starsContainer.appendChild(star);
    }
  }, []);

  return <div className="stars-bg" id="stars-container" />;
};

export default StarBackground;
