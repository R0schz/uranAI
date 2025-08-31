"use client";

import { useAppStore } from '../contexts/AppContext'; // useAppContextを削除し、useAppStoreをインポート
import Header from './Header';
import Navigation from './Navigation';
import { LogoIcon } from './Icons';
import StarBackground from './StarBackground';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  // Zustandストアから直接isLoggedInの状態を取得
  const { isLoggedIn } = useAppStore();

  return (
    <>
      <LogoIcon />
      <StarBackground />
      {/* 取得したisLoggedInを直接使用 */}
      {isLoggedIn && <Header />}
      <main id="app-container" className="relative">
        <div id="content-wrapper">
          {children}
        </div>
      </main>
      {isLoggedIn && <Navigation />}
    </>
  );
};

export default Layout;