"use client";

import { useAppStore, Person } from '../contexts/AppContext';

const PersonSelectScreen = () => {
  const {
    currentScreen,
    fortunePurpose,
    selectedPeople,
    people,
    isPremium,
    setCurrentScreen,
    setSelectedPeople,
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
        return; // Cannot select more than max
      }
    }

    setSelectedPeople(newSelectedPeople);
  };

  const handleConfirm = () => {
    setCurrentScreen('fortune-type-screen');
  };

  const handleAddPerson = () => {
    if (!isPremium && people.length >= 3) {
      // Show premium modal
      return;
    }
    // Show add person modal
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
          {people.map((person: Person) => (
            <div
              key={person.id}
              onClick={() => handlePersonSelect(person.id)}
              className={`person-card card p-4 flex items-center justify-between cursor-pointer transition ${
                selectedPeople.includes(person.id) ? 'border-purple-400' : ''
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
                selectedPeople.includes(person.id)
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