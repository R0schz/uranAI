"use client";

import { useAppStore } from '../contexts/AppContext';

const Navigation = () => {
  const {
    isLoggedIn,
    currentScreen,
    setCurrentScreen,
  } = useAppStore();

  if (!isLoggedIn) return null;

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen);
  };

  return (
    <nav id="nav-bar" className="fixed bottom-0 left-0 right-0 nav-bar flex justify-around items-center z-40">
      <div
        onClick={() => handleNavigate('home-screen')}
        className={`nav-item text-center text-gray-400 cursor-pointer ${
          currentScreen === 'home-screen' ? 'active' : ''
        }`}
      >
        <i data-lucide="home" className="w-7 h-7 mx-auto"></i>
        <span className="text-xs">ホーム</span>
      </div>
      <div
        onClick={() => handleNavigate('mypage-screen')}
        className={`nav-item text-center text-gray-400 cursor-pointer ${
          currentScreen === 'mypage-screen' ? 'active' : ''
        }`}
      >
        <i data-lucide="user-circle" className="w-7 h-7 mx-auto"></i>
        <span className="text-xs">マイページ</span>
      </div>
    </nav>
  );
};

export default Navigation;
