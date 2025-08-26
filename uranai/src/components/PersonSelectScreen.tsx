import React from 'react';

const PersonSelectScreen: React.FC = () => {
  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-4">人物を選択</h2>
        <p id="person-select-description" className="text-center text-gray-400 mb-8">
          鑑定したい人物を選択してください。
        </p>
        <div id="person-list" className="space-y-4 mb-6">
          {/* Person cards will be dynamically generated here */}
        </div>
        <div className="text-center">
          <button data-action="show-add-person-from-select" className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center mx-auto">
            <i data-lucide="plus" className="w-5 h-5 mr-2"></i> 新しい人物を追加
          </button>
        </div>
        <div className="mt-10 text-center">
          <button data-action="confirm-person-selection" className="btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg opacity-50" disabled>
            次へ
          </button>
        </div>
      </div>
    </section>
  );
};

export default PersonSelectScreen;
