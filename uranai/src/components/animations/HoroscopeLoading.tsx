"use client";

import { useEffect, useRef } from 'react';

interface HoroscopeLoadingProps {
  onComplete: () => void;
}

const HoroscopeLoading = ({ onComplete }: HoroscopeLoadingProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameIdRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    canvas.width = 300;
    canvas.height = 300;

    const stars: Array<{
      x: number;
      y: number;
      radius: number;
      arcRadius: number;
      angle: number;
      speed: number;
    }> = [];

    const numStars = 200;
    for (let i = 0; i < numStars; i++) {
      stars.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        radius: Math.random() * 1.5 + 0.5,
        arcRadius: Math.random() * (canvas.width / 2 - 10) + 10,
        angle: Math.random() * Math.PI * 2,
        speed: (Math.random() - 0.5) * 0.04
      });
    }

    function draw() {
      if (!ctx || !canvas) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      stars.forEach(star => {
        const currentX = canvas.width / 2 + Math.cos(star.angle) * star.arcRadius;
        const currentY = canvas.height / 2 + Math.sin(star.angle) * star.arcRadius;

        ctx.beginPath();
        ctx.arc(currentX, currentY, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.5 + 0.5})`;
        ctx.shadowColor = 'white';
        ctx.shadowBlur = 10;
        ctx.fill();

        star.angle += star.speed;
      });

      animationFrameIdRef.current = requestAnimationFrame(draw);
    }

    draw();

    const timer = setTimeout(onComplete, 5000);

    return () => {
      if (animationFrameIdRef.current) {
        cancelAnimationFrame(animationFrameIdRef.current);
      }
      clearTimeout(timer);
    };
  }, [onComplete]);

  return (
    <div className="page-content flex flex-col items-center justify-center">
      <canvas id="star-trail-canvas" className="loading-canvas" ref={canvasRef}></canvas>
      <p className="font-serif-special text-xl text-gray-200 mt-12 animate-pulse">
        星々の配置を計算しています...
      </p>
    </div>
  );
};

export default HoroscopeLoading;
