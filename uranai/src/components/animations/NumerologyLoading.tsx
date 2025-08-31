"use client";

import { useEffect, useRef } from 'react';

interface NumerologyLoadingProps {
  onComplete: () => void;
}

const NumerologyLoading = ({ onComplete }: NumerologyLoadingProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const intervalIdRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = 300;
    canvas.height = 300;

    const letters = '0123456789';
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = Array.from({ length: Math.floor(columns) }).map(() =>
      1 + Math.floor(Math.random() * 250)
    );

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#c850c0';
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i++) {
        const text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    intervalIdRef.current = setInterval(draw, 33);

    const timer = setTimeout(onComplete, 3500);

    return () => {
      if (intervalIdRef.current) {
        clearInterval(intervalIdRef.current);
      }
      clearTimeout(timer);
    };
  }, [onComplete]);

  return (
    <div className="page-content flex flex-col items-center justify-center">
      <canvas id="matrix-canvas" className="loading-canvas" ref={canvasRef}></canvas>
      <p className="font-serif-special text-xl text-gray-200 mt-12 animate-pulse">
        運命数を算出しています...
      </p>
    </div>
  );
};

export default NumerologyLoading;
