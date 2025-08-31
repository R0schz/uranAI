"use client";

import { useAppContext } from '../contexts/AppContext';

const PersonSelectScreen = () => {
  const { state, setState } = useAppContext();

  if (state.currentScreen !== 'person-select-screen') return null;

  const handlePersonSelect = (id: number) => {
    const maxSelection = state.fortunePurpose === 'personal' ? 1 : 2;
    let newSelectedPeople: number[];

    if (state.selectedPeople.includes(id)) {
      newSelectedPeople = state.selectedPeople.filter(personId => personId !== id);
    } else {
      if (state.selectedPeople.length < maxSelection) {
        newSelectedPeople = [...state.selectedPeople, id];
      } else if (maxSelection === 1) {
        newSelectedPeople = [id];
      } else {
        return; // Cannot select more than max
      }
    }

    setState(prev => ({
      ...prev,
      selectedPeople: newSelectedPeople
    }));
  };

  const handleConfirm = () => {
    setState(prev => ({
      ...prev,
      currentScreen: 'fortune-type-screen'
    }));
  };

  const handleAddPerson = () => {
    if (!state.isPremium && state.people.length >= 3) {
      // Show premium modal
      return;
    }
    // Show add person modal
  };

  const description = state.fortunePurpose === 'personal'
    ? '鑑定したい人物を1人選択してください。'
    : `鑑定したい人物を2人選択してください。(${state.selectedPeople.length}/2)`;

  const isConfirmEnabled = state.fortunePurpose === 'personal'
    ? state.selectedPeople.length === 1
    : state.selectedPeople.length === 2;

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-4">人物を選択</h2>
        <p className="text-center text-gray-400 mb-8">{description}</p>
        <div className="space-y-4 mb-6">
          {state.people.map(person => (
            <div
              key={person.id}
              onClick={() => handlePersonSelect(person.id)}
              className={`person-card card p-4 flex items-center justify-between cursor-pointer transition ${
                state.selectedPeople.includes(person.id) ? 'border-purple-400' : ''
              }`}
            >
              <div className="flex items-center">
                <div className="w-12 h-12 rounded-full bg-purple-900 flex items-center justify-center mr-4">
                  <span className="text-xl font-bold">{person.nickname.charAt(0)}</span>
                </div>
                <div>
                  <p className="font-bold text-lg">{person.nickname}</p>
                  <p className="text-sm text-gray-400">{person.birthDate || '生年月日未登録'}</p>
                </div>
              </div>
              <div className={`select-indicator w-6 h-6 rounded-full border-2 ${
                state.selectedPeople.includes(person.id)
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
            <i data-lucide="plus" className="w-5 h-5 mr-2"></i>
            新しい人物を追加
          </button>
        </div>
        <div className="mt-10 text-center">
          <button
            onClick={handleConfirm}
            disabled={!isConfirmEnabled}
            className={`btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg ${
              !isConfirmEnabled ? 'opacity-50' : ''
            }`}
          >
            次へ
          </button>
        </div>
      </div>
    </section>
  );
};

export default PersonSelectScreen;