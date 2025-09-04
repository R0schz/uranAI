"use client";

import { useAppStore } from '../contexts/AppContext';
import TarotShuffle from './animations/TarotShuffle';
import HoroscopeLoading from './animations/HoroscopeLoading';
import NumerologyLoading from './animations/NumerologyLoading';

const LoadingScreen = () => {
  const {
    currentScreen,
    fortuneType,
    setCurrentScreen,
  } = useAppStore();

  console.log('LoadingScreen: currentScreen =', currentScreen, 'fortuneType =', fortuneType);

  if (!currentScreen.endsWith('-loading-screen')) {
    console.log('LoadingScreen: Not a loading screen, returning null');
    return null;
  }

  const handleComplete = () => {
    console.log('LoadingScreen: handleComplete called, setting screen to result-screen');
    setCurrentScreen('result-screen');
  };

  const renderLoadingAnimation = () => {
    console.log('LoadingScreen: renderLoadingAnimation called for fortuneType =', fortuneType);
    switch (fortuneType) {
      case 'tarot':
        console.log('LoadingScreen: Rendering TarotShuffle');
        return (
          <TarotShuffle
            onComplete={handleComplete}
          />
        );
      case 'horoscope':
        console.log('LoadingScreen: Rendering HoroscopeLoading');
        return <HoroscopeLoading onComplete={handleComplete} />;
      case 'numerology':
        console.log('LoadingScreen: Rendering NumerologyLoading');
        return <NumerologyLoading onComplete={handleComplete} />;
      default:
        console.log('LoadingScreen: Rendering default loading');
        return (
          <div className="page-content flex flex-col items-center justify-center">
            <p className="font-serif-special text-xl text-gray-200 animate-pulse">
              占いの準備をしています...
            </p>
          </div>
        );
    }
  };

  return <section className="page p-4">{renderLoadingAnimation()}</section>;
};

export default LoadingScreen;
