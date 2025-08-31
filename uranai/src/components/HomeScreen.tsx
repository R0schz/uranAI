"use client";

import { useAppContext } from '../contexts/AppContext';

const HomeScreen = () => {
  const { state, setState } = useAppContext();

  if (state.currentScreen !== 'home-screen') return null;

  const handlePurposeSelect = (purpose: 'personal' | 'compatibility') => {
    setState(prev => ({
      ...prev,
      fortunePurpose: purpose,
      selectedPeople: [],
      currentScreen: 'person-select-screen'
    }));
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-10">占いの目的を選択</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            onClick={() => handlePurposeSelect('personal')}
            className="card p-8 text-center cursor-pointer hover:border-purple-400 transition"
          >
            <i data-lucide="user" className="w-16 h-16 mx-auto mb-4 text-purple-300"></i>
            <h3 className="font-serif-special text-2xl mb-2">パーソナル鑑定</h3>
            <p className="text-gray-400">
              あなた自身を<br />深く占います
            </p>
          </div>
          <div
            onClick={() => handlePurposeSelect('compatibility')}
            className="card p-8 text-center cursor-pointer hover:border-cyan-400 transition"
          >
            <i data-lucide="users" className="w-16 h-16 mx-auto mb-4 text-cyan-300"></i>
            <h3 className="font-serif-special text-2xl mb-2">相性占い</h3>
            <p className="text-gray-400">
              特定の人との相性を<br />占います
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HomeScreen;