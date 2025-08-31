"use client";

import { useAppContext } from '../contexts/AppContext';
import TarotShuffle from './animations/TarotShuffle';
import HoroscopeLoading from './animations/HoroscopeLoading';
import NumerologyLoading from './animations/NumerologyLoading';

const LoadingScreen = () => {
  const { state, setState } = useAppContext();

  if (!state.currentScreen.endsWith('-loading-screen')) return null;

  const handleComplete = () => {
    setState(prev => ({ ...prev, currentScreen: 'result-screen' }));
  };

  const renderLoadingAnimation = () => {
    switch (state.fortuneType) {
      case 'tarot':
        return (
          <TarotShuffle
            onComplete={handleComplete}
            cardBackUrl="https://placehold.co/100/176/1a1a2e/c850c0?text=uranAI"
          />
        );
      case 'horoscope':
        return <HoroscopeLoading onComplete={handleComplete} />;
      case 'numerology':
        return <NumerologyLoading onComplete={handleComplete} />;
      default:
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
