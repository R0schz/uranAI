"use client";

import { useAppStore } from '../contexts/AppContext';
import Layout from '../components/Layout';
import SplashScreen from '../components/SplashScreen';
import ModalContainer from '../components/modals/ModalContainer';
import HomeScreen from '../components/HomeScreen';
import PersonSelectScreen from '../components/PersonSelectScreen';
import DivinationSelectScreen from '../components/DivinationSelectScreen';
import InformationInputScreen from '../components/InformationInputScreen';
import LoadingScreen from '../components/LoadingScreen';
import ResultScreen from '../components/ResultScreen';
import MyPage from '../components/MyPage';

export default function App() {
  const {
    currentScreen,
    activeModal,
  } = useAppStore();

  // 現在のスクリーンに基づいて表示するコンポーネントを決定
  const getCurrentScreen = () => {
    switch (currentScreen) {
      case 'splash-screen':
        return <SplashScreen />;
      case 'home-screen':
        return <HomeScreen />;
      case 'person-select-screen':
        return <PersonSelectScreen />;
      case 'fortune-type-screen':
        return <DivinationSelectScreen />;
      case 'input-screen':
        return <InformationInputScreen />;
      case 'tarot-loading-screen':
      case 'horoscope-loading-screen':
      case 'numerology-loading-screen':
        return <LoadingScreen />;
      case 'result-screen':
        return <ResultScreen />;
      case 'mypage-screen':
        return <MyPage />;
      default:
        return null;
    }
  };

  return (
    <Layout>
      {getCurrentScreen()}
      <ModalContainer activeModal={activeModal} />
    </Layout>
  );
}