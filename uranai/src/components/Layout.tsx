"use client";

import { useAppContext } from '../contexts/AppContext';
import Header from './Header';
import Navigation from './Navigation';
import { LogoIcon } from './Icons';
import StarBackground from './StarBackground';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const { state } = useAppContext();

  return (
    <>
      <LogoIcon />
      <StarBackground />
      {state.isLoggedIn && <Header />}
      <main id="app-container" className="relative">
        <div id="content-wrapper">
          {children}
        </div>
      </main>
      {state.isLoggedIn && <Navigation />}
    </>
  );
};

export default Layout;
