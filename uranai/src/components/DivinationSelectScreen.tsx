import React from 'react';

const DivinationSelectScreen: React.FC = () => {
  return (
    <section className="page p-4">
      <div className="page-content max-w-2xl mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-10">占術を選択</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div data-action="select-fortune-type" data-type="numerology" className="card p-6 text-center cursor-pointer hover:border-purple-400 transition">
            <i data-lucide="binary" className="w-12 h-12 mx-auto mb-3 text-purple-300"></i>
            <h3 className="font-serif-special text-xl mb-1">数秘術</h3>
            <p className="text-sm text-gray-400">生年月日と名前から<br />運命を解読</p>
          </div>
          <div data-action="select-fortune-type" data-type="horoscope" className="card p-6 text-center cursor-pointer hover:border-cyan-400 transition">
            <i data-lucide="orbit" className="w-12 h-12 mx-auto mb-3 text-cyan-300"></i>
            <h3 className="font-serif-special text-xl mb-1">西洋占星術</h3>
            <p className="text-sm text-gray-400">星々の配置が示す<br />あなたの全て</p>
          </div>
          <div data-action="select-fortune-type" data-type="tarot" className="card p-6 text-center cursor-pointer hover:border-yellow-400 transition">
            <i data-lucide="layout-template" className="w-12 h-12 mx-auto mb-3 text-yellow-300"></i>
            <h3 className="font-serif-special text-xl mb-1">タロット</h3>
            <p className="text-sm text-gray-400">カードが導く<br />未来へのメッセージ</p>
          </div>
          <div data-action="select-fortune-type" data-type="comprehensive" className="card p-6 text-center cursor-pointer transition relative overflow-hidden" data-premium="true">
            <div className="absolute top-2 right-2 bg-yellow-500 text-black text-xs font-bold px-2 py-1 rounded-full flex items-center">
              <i data-lucide="gem" className="w-3 h-3 mr-1"></i> PREMIUM
            </div>
            <i data-lucide="sparkles" className="w-12 h-12 mx-auto mb-3 text-yellow-300"></i>
            <h3 className="font-serif-special text-xl mb-1">総合占い</h3>
            <p className="text-sm text-gray-400">全ての占術で<br />多角的に鑑定</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DivinationSelectScreen;
