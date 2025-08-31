"use client";

import { useAppContext } from '../contexts/AppContext';

const SplashScreen = () => {
  const { state, showModal } = useAppContext();

  if (state.currentScreen !== 'splash-screen') return null;

  const handleStartClick = () => {
    showModal('login');
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-md mx-auto">
        <div className="text-center card p-8 md:p-12">
          <div className="flex flex-col items-center gap-4 mb-8">
            <svg width="100" height="100" className="glow-filter">
              <use href="#logo-icon"></use>
            </svg>
            <span className="font-serif-special text-5xl">
              uran<span className="gradient-text font-bold">AI</span>
            </span>
          </div>
          <p className="text-gray-400 mb-10 px-4">
            あなたの未来を、<br />AIがそっと照らし出します。
          </p>
          <button
            onClick={handleStartClick}
            className="btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg"
          >
            占いを始める
          </button>
        </div>
      </div>
    </section>
  );
};

export default SplashScreen;
