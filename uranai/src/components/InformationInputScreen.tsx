"use client";

import { useAppContext } from '../contexts/AppContext';

interface InputField {
  name: string;
  label: string;
  type: string;
  placeholder: string;
  value?: string;
}

const InformationInputScreen = () => {
  const { state, setState } = useAppContext();

  if (state.currentScreen !== 'input-screen') return null;

  const person1 = state.people.find(p => p.id === state.selectedPeople[0]);
  if (!person1) return null;

  const getInputFields = (): InputField[] => {
    const fields: InputField[] = [];
    
    switch (state.fortuneType) {
      case 'numerology':
        fields.push(
          { name: 'name1', label: '名前(ひらがな)', type: 'text', placeholder: 'てすと はなこ', value: person1.name },
          { name: 'birthDate1', label: '生年月日', type: 'date', placeholder: '', value: person1.birthDate }
        );
        if (state.fortunePurpose === 'compatibility') {
          const person2 = state.people.find(p => p.id === state.selectedPeople[1]);
          fields.push(
            { name: 'name2', label: '相手の名前(ひらがな)', type: 'text', placeholder: 'てすと たろう', value: person2?.name },
            { name: 'birthDate2', label: '相手の生年月日', type: 'date', placeholder: '', value: person2?.birthDate }
          );
        }
        break;
      case 'horoscope':
        fields.push(
          { name: 'name1', label: '名前(ひらがな)', type: 'text', placeholder: 'てすと はなこ', value: person1.name },
          { name: 'birthDate1', label: '出生年月日', type: 'date', placeholder: '', value: person1.birthDate },
          { name: 'birthTime1', label: '出生時刻', type: 'time', placeholder: '', value: person1.birthTime },
          { name: 'birthPlace1', label: '出生場所', type: 'text', placeholder: '例: 東京都中央区', value: person1.birthPlace }
        );
        break;
      case 'tarot':
        break;
    }

    return fields;
  };

  const handleGetFortune = () => {
    if (state.fortuneType === 'tarot') {
      setState(prev => ({ ...prev, currentScreen: 'tarot-touch-screen' }));
    } else {
      setState(prev => ({ ...prev, currentScreen: 'result-screen' }));
    }
  };

  const fields = getInputFields();

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 id="input-title" className="font-serif-special text-3xl text-center mb-8">
          情報入力
        </h2>
        <div id="input-fields" className="space-y-6">
          {fields.map((field, index) => (
            <div key={index}>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                {field.label}
              </label>
              <input
                name={field.name}
                type={field.type}
                placeholder={field.placeholder}
                value={field.value}
                className="form-input w-full p-3"
              />
            </div>
          ))}
          {state.fortuneType !== 'tarot' && (
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                相談内容 (任意)
              </label>
              <textarea
                name="question"
                placeholder="今年の運勢は？"
                className="form-textarea w-full p-3 h-32 resize-none"
              ></textarea>
            </div>
          )}
        </div>
        <div className="mt-10 text-center">
          <button
            onClick={handleGetFortune}
            className="btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg"
          >
            鑑定する
          </button>
        </div>
      </div>
    </section>
  );
};

export default InformationInputScreen;