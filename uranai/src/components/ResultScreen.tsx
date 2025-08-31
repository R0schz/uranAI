"use client";

import { useAppContext } from '../contexts/AppContext';

const ResultScreen = () => {
  const { state, setState } = useAppContext();

  if (state.currentScreen !== 'result-screen') return null;

  const handleShare = () => {
    if (state.tickets > 0) {
      setState(prev => ({ ...prev, tickets: prev.tickets - 1 }));
      alert('共有しました。(チケットを1枚消費しました)');
    } else {
      // Show ticket prompt modal
    }
  };

  const handleAskMore = () => {
    if (state.tickets > 0) {
      setState(prev => ({ ...prev, tickets: prev.tickets - 1 }));
      alert('追加質問しました。(チケットを1枚消費しました)');
    } else {
      // Show ticket prompt modal
    }
  };

  const handleBackToHome = () => {
    setState(prev => ({
      ...prev,
      currentScreen: 'home-screen',
      selectedPeople: [],
      fortunePurpose: null,
      fortuneType: null
    }));
  };

  const renderVisualResult = () => {
    switch (state.fortuneType) {
      case 'numerology':
        return (
          <>
            <h3 className="font-serif-special text-xl mb-6 text-purple-300 text-center">
              あなたのナンバー
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
              {['ライフパス', 'ディスティニー', 'ソウル', 'パーソナル', 'バースデー', 'マチュリティー'].map(
                (name, index) => (
                  <div key={index} className="bg-black bg-opacity-20 p-4 rounded-lg">
                    <p className="text-sm text-gray-400">{name}</p>
                    <p className="font-serif-special text-3xl font-bold">
                      {Math.floor(Math.random() * 9) + 1}
                    </p>
                  </div>
                )
              )}
            </div>
          </>
        );
      case 'horoscope':
        return (
          <>
            <h3 className="font-serif-special text-xl mb-4 text-cyan-300 text-center">
              ホロスコープチャート
            </h3>
            <img
              src="https://placehold.co/400x400/1a1a2e/e3e3e3?text=Horoscope+Chart"
              alt="Horoscope Chart"
              className="mx-auto rounded-full"
            />
          </>
        );
      case 'tarot':
        return (
          <>
            <h3 className="font-serif-special text-xl mb-6 text-yellow-300 text-center">
              ケルト十字スプレッド
            </h3>
            <div className="grid grid-cols-3 sm:grid-cols-4 gap-2 justify-items-center">
              {Array.from({ length: 10 }).map((_, i) => (
                <div key={i} className="w-20">
                  <img
                    src={`https://placehold.co/100x170/4158d0/ffffff?text=Card${i + 1}`}
                    alt={`Card ${i + 1}`}
                    className={`rounded-md ${i % 3 === 0 ? 'transform rotate-90' : ''}`}
                  />
                </div>
              ))}
            </div>
          </>
        );
      default:
        return (
          <div className="text-center text-gray-400">
            複数の占術結果を統合しています...
          </div>
        );
    }
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-2xl mx-auto">
        <div className="card p-6 md:p-8">
          <p className="text-xs text-center text-gray-500 mb-6">
            免責事項: 本占いはエンターテイメントを目的としたものであり、<br />
            その結果を保証するものではありません。
          </p>
          <h2 className="font-serif-special text-3xl text-center mb-6 border-b border-gray-700 pb-4">
            {state.fortuneType === 'numerology'
              ? '数秘術の鑑定結果'
              : state.fortuneType === 'horoscope'
              ? '西洋占星術の鑑定結果'
              : state.fortuneType === 'tarot'
              ? 'タロット占いの結果'
              : '総合鑑定結果'}
          </h2>
          <div className="mb-8">{renderVisualResult()}</div>
          <h3 className="font-serif-special text-xl mb-4 text-purple-300">AIによる鑑定文</h3>
          <div className="text-gray-300 leading-relaxed space-y-4 bg-black bg-opacity-20 p-4 rounded-lg">
            <p>
              星々の配置が示すところによると、<br />
              あなたの進む道には新たな光が差し込んでいます。
            </p>
            <p>
              特に人間関係において、予期せぬ出会いが訪れる兆し。<br />
              それはまるで夜空に流れる星のように一瞬の輝きかもしれませんが、あなたの心に深い印象を残すでしょう。
            </p>
          </div>
          <div className="mt-8 flex flex-col md:flex-row gap-4 justify-center">
            <button
              onClick={handleShare}
              className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center"
            >
              <i data-lucide="share-2" className="w-5 h-5 mr-2"></i>
              結果を共有する
            </button>
            <button
              onClick={handleAskMore}
              className="bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center"
            >
              <i data-lucide="message-circle" className="w-5 h-5 mr-2"></i>
              AIに追加質問する
            </button>
          </div>
          <div className="mt-8 text-center">
            <button
              onClick={handleBackToHome}
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-full transition duration-300"
            >
              ホームに戻る
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResultScreen;