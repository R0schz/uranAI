import React from 'react';

const ResultScreen: React.FC = () => {
  return (
    <section className="page p-4">
      <div className="page-content max-w-2xl mx-auto">
        <div className="card p-6 md:p-8">
          <p className="text-xs text-center text-gray-500 mb-6">
            免責事項: 本占いはエンターテイメントを目的としたものであり、<br />その結果を保証するものではありません。
          </p>
          <h2 id="result-title" className="font-serif-special text-3xl text-center mb-6 border-b border-gray-700 pb-4">
            星からの神託
          </h2>
          <div id="visual-result-area" className="mb-8">
            {/* Visual results will be dynamically generated here */}
          </div>
          <h3 className="font-serif-special text-xl mb-4 text-purple-300">AIによる鑑定文</h3>
          <div id="ai-result-text" className="text-gray-300 leading-relaxed space-y-4 bg-black bg-opacity-20 p-4 rounded-lg">
            <p>
              星々の配置が示すところによると、<br />あなたの進む道には新たな光が差し込んでいます。
            </p>
            <p>
              特に人間関係において、予期せぬ出会いが訪れる兆し。<br />それはまるで夜空に流れる星のように一瞬の輝きかもしれませんが、あなたの心に深い印象を残すでしょう。
            </p>
          </div>
          <div className="mt-8 flex flex-col md:flex-row gap-4 justify-center">
            <button data-action="share-result" className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center">
              <i data-lucide="share-2" className="w-5 h-5 mr-2"></i> 結果を共有する
            </button>
            <button data-action="ask-ai-more" className="bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center">
              <i data-lucide="message-circle" className="w-5 h-5 mr-2"></i> AIに追加質問する
            </button>
          </div>
          <div className="mt-8 text-center">
            <button data-action="back-to-home" className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-full transition duration-300">
              ホームに戻る
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResultScreen;
