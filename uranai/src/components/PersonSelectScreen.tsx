"use client";

import { useAppStore, Profile } from '../contexts/AppContext';

const PersonSelectScreen = () => {
  // Zustandストアから直接状態と更新関数を取得
  const {
    currentScreen,
    fortunePurpose,
    selectedPeople,
    profiles,
    isPremium,
    setCurrentScreen,
    setSelectedPeople,
    showModal,
  } = useAppStore();

  if (currentScreen !== 'person-select-screen') return null;

  const handlePersonSelect = (id: number) => {
    const maxSelection = fortunePurpose === 'personal' ? 1 : 2;
    let newSelectedPeople: number[];

    if (selectedPeople.includes(id)) {
      newSelectedPeople = selectedPeople.filter((personId: number) => personId !== id);
    } else {
      if (selectedPeople.length < maxSelection) {
        newSelectedPeople = [...selectedPeople, id];
      } else if (maxSelection === 1) {
        newSelectedPeople = [id];
      } else {
        return;
      }
    }
    setSelectedPeople(newSelectedPeople);
  };

  const handleConfirm = () => {
    setCurrentScreen('fortune-type-screen');
  };

  const handleAddPerson = () => {
    if (!isPremium && profiles.length >= 3) {
      showModal('premium');
      return;
    }
    showModal('addPerson');
  };

  const handleBack = () => {
    setSelectedPeople([]);
    setCurrentScreen('home-screen');
  };

  const description = fortunePurpose === 'personal'
    ? '鑑定したい人物を1人選択してください。'
    : `鑑定したい人物を2人選択してください。(${selectedPeople.length}/2)`;

  const isConfirmEnabled = fortunePurpose === 'personal'
    ? selectedPeople.length === 1
    : selectedPeople.length === 2;

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-4">人物を選択</h2>
        <p className="text-center text-gray-400 mb-8">{description}</p>
        <div className="space-y-4 mb-6">
          {profiles.map((profile: Profile) => (
            <div
              key={profile.profile_id}
              onClick={() => handlePersonSelect(profile.profile_id)}
              className={`person-card card p-4 flex items-center justify-between cursor-pointer transition ${
                selectedPeople.includes(profile.profile_id) ? 'border-purple-400' : ''
              }`}
            >
              <div className="flex items-center">
                <div className="w-12 h-12 rounded-full bg-purple-900 flex items-center justify-center mr-4">
                  <span className="text-xl font-bold">{profile.nickname.charAt(0)}</span>
                </div>
                <div>
                  <p className="font-bold text-lg">{profile.nickname}</p>
                  <p className="text-sm text-gray-400">{profile.birth_date || '生年月日未登録'}</p>
                </div>
              </div>
              <div className={`select-indicator w-6 h-6 rounded-full border-2 ${
                selectedPeople.includes(profile.profile_id)
                  ? 'bg-purple-500 border-purple-400'
                  : 'border-gray-500'
              }`}></div>
            </div>
          ))}
        </div>
        <div className="text-center">
          <button
            onClick={handleAddPerson}
            className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center mx-auto"
          >
            新しい人物を追加
          </button>
        </div>
        <div className="mt-10 text-center">
          <button
            onClick={handleConfirm}
            disabled={!isConfirmEnabled}
            className={`btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg mx-auto ${
              !isConfirmEnabled ? 'opacity-50' : ''
            }`}
          >
            次へ
          </button>
        </div>
        <div className="mt-8 text-center">
          <button
            onClick={handleBack}
            className="text-gray-400 hover:text-white text-sm underline mx-auto"
          >
            ← ホームに戻る
          </button>
        </div>
      </div>
    </section>
  );
};

export default PersonSelectScreen;