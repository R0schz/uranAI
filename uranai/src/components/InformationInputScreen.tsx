import React from 'react';

const InformationInputScreen: React.FC = () => {
  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 id="input-title" className="font-serif-special text-3xl text-center mb-8">情報入力</h2>
        <div id="input-fields" className="space-y-6">
          {/* Input fields will be dynamically generated here based on the selected divination */}
        </div>
        <div className="mt-10 text-center">
          <button data-action="get-fortune" className="btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg">
            鑑定する
          </button>
        </div>
      </div>
    </section>
  );
};

export default InformationInputScreen;
