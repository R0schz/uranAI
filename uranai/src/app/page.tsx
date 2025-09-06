"use client";

import { useAppStore } from '../contexts/AppContext';
import Layout from '../components/Layout';
import SplashScreen from '../components/SplashScreen';
import ModalContainer from '../components/modals/ModalContainer';
import HomeScreen from '../components/HomeScreen';
import PersonSelectScreen from '../components/PersonSelectScreen';
import DivinationSelectScreen from '../components/DivinationSelectScreen';
import InformationInputScreen from '../components/InformationInputScreen';
import TarotTouchScreen from '../components/TarotTouchScreen';
import LoadingScreen from '../components/LoadingScreen';
import ResultScreen from '../components/ResultScreen';
import MyPage from '../components/MyPage';

export default function App() {
  // Zustandストアから直接、必要な状態を取得
  const { currentScreen, activeModal, isAuthChecked } = useAppStore();
  
  // デバッグ用: 現在の状態をコンソールに出力
  console.log('App - currentScreen:', currentScreen, 'isAuthChecked:', isAuthChecked);

  // 認証チェックが完了するまでスプラッシュ画面を表示
  if (!isAuthChecked) {
    console.log('Auth not checked yet, showing splash screen');
    return (
      <Layout>
        <SplashScreen />
      </Layout>
    );
  }
  
  console.log('Auth checked, currentScreen:', currentScreen);

  const getCurrentScreen = () => {
    console.log('getCurrentScreen called with currentScreen:', currentScreen);
    console.log('getCurrentScreen - currentScreen type:', typeof currentScreen);
    console.log('getCurrentScreen - currentScreen value:', JSON.stringify(currentScreen));
    
    // currentScreenがnullやundefinedの場合はスプラッシュ画面を表示
    if (!currentScreen) {
      console.log('currentScreen is null/undefined, returning SplashScreen');
      return <SplashScreen />;
    }
    
    switch (currentScreen) {
      case 'splash-screen':
        console.log('Returning SplashScreen');
        return <SplashScreen />;
      case 'home-screen':
        console.log('Returning HomeScreen');
        return <HomeScreen />;
      case 'person-select-screen':
        console.log('Returning PersonSelectScreen');
        return <PersonSelectScreen />;
      case 'fortune-type-screen':
        console.log('Returning DivinationSelectScreen');
        return <DivinationSelectScreen />;
      case 'input-screen':
        console.log('Returning InformationInputScreen');
        return <InformationInputScreen />;
      case 'tarot-touch-screen':
        console.log('Returning TarotTouchScreen');
        return <TarotTouchScreen />;
      case 'tarot-loading-screen':
      case 'horoscope-loading-screen':
      case 'numerology-loading-screen':
        console.log('Returning LoadingScreen');
        return <LoadingScreen />;
      case 'result-screen':
        console.log('Returning ResultScreen');
        return <ResultScreen />;
      case 'mypage-screen':
        console.log('Returning MyPage');
        return <MyPage />;
      default:
        // 認証済みだが画面が確定しない場合はホームを表示
        console.log('Default case: Returning HomeScreen');
        console.log('Default case - currentScreen was:', currentScreen);
        return <HomeScreen />;
    }
  };

  return (
    <Layout>
      {getCurrentScreen()}
      <ModalContainer activeModal={activeModal} />
    </Layout>
  );
}