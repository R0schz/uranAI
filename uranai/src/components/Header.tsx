"use client";

import { useAppStore } from '../contexts/AppContext';

const Header = () => {
  // 状態をZustandから取得
  const { isLoggedIn, isPremium, tickets, setCurrentScreen } = useAppStore();

  if (!isLoggedIn) return null;

  return (
    <header id="app-header" className="fixed top-0 left-0 right-0 z-40 flex items-center justify-between px-4">
      <div
        data-action="back-to-home"
        className="flex items-center gap-2 cursor-pointer transition-opacity hover:opacity-80"
        onClick={() => setCurrentScreen('home-screen')}
      >
        <svg width="32" height="32" className="glow-filter">
          <use href="#logo-icon"></use>
        </svg>
        <span className="font-serif-special text-2xl">
          uran<span className="gradient-text font-bold">AI</span>
        </span>
      </div>
      <div id="header-user-status">
        {isPremium ? (
          <div id="premium-user-header">
            <div className="flex items-center gap-2 premium-text-glow">
              <i data-lucide="gem" className="w-5 h-5"></i>
              <span className="text-lg">Premium</span>
            </div>
          </div>
        ) : (
          <div id="free-user-header" className="flex items-center gap-4">
            <div className="flex items-center gap-1 text-yellow-300">
              <i data-lucide="ticket" className="w-5 h-5"></i>
              <span id="header-ticket-count" className="font-bold text-lg">
                {tickets}
              </span>
            </div>
            <button
              data-action="show-premium-modal"
              className="bg-yellow-500/20 text-yellow-300 text-xs font-bold px-3 py-1 rounded-full border border-yellow-500/50 hover:bg-yellow-500/40 transition"
            >
              プレミアム
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;