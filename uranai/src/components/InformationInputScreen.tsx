"use client";

import { useState } from 'react';
import { useAppStore, Profile } from '../contexts/AppContext';

interface InputField {
  name: string;
  label: string;
  type: string;
  placeholder: string;
  defaultValue: string;
}

const InformationInputScreen = () => {
  const {
    currentScreen,
    fortuneType,
    fortunePurpose,
    selectedPeople,
    profiles,
    setCurrentScreen,
    setConsultation,
  } = useAppStore();

  // フォームの状態管理
  const [formData, setFormData] = useState<Record<string, string>>({});

  if (currentScreen !== 'input-screen') return null;

  const profile1 = profiles.find((p: Profile) => p.profile_id === selectedPeople[0]);
  if (!profile1) return null;

  const getInputFields = (): InputField[] => {
    const fields: InputField[] = [];
    
    switch (fortuneType) {
      case 'numerology':
        fields.push(
          { name: 'nickname1', label: 'ニックネーム', type: 'text', placeholder: 'はなこ', defaultValue: profile1.nickname || '' },
          { name: 'name1', label: '名前(ひらがな)', type: 'text', placeholder: 'やまだ はなこ（名字 名前の順でスペース区切り）', defaultValue: profile1.name_hiragana || '' },
          { name: 'birthDate1', label: '生年月日', type: 'date', placeholder: '', defaultValue: profile1.birth_date || '' }
        );
        if (fortunePurpose === 'compatibility') {
          const profile2 = profiles.find((p: Profile) => p.profile_id === selectedPeople[1]);
          fields.push(
            { name: 'nickname2', label: '相手のニックネーム', type: 'text', placeholder: 'たろう', defaultValue: profile2?.nickname || '' },
            { name: 'name2', label: '相手の名前(ひらがな)', type: 'text', placeholder: 'すずき たろう（名字 名前の順でスペース区切り）', defaultValue: profile2?.name_hiragana || '' },
            { name: 'birthDate2', label: '相手の生年月日', type: 'date', placeholder: '', defaultValue: profile2?.birth_date || '' }
          );
        }
        // 相談内容は最後に追加（個人・相性共通）
        fields.push(
          { name: 'consultation', label: '相談内容', type: 'textarea', placeholder: '何かご相談があればお聞かせください（空欄の場合は今日の運勢を占います）', defaultValue: '' }
        );
        break;
      case 'horoscope':
        fields.push(
          { name: 'nickname1', label: 'ニックネーム', type: 'text', placeholder: 'はなこ', defaultValue: profile1.nickname || '' },
          { name: 'birthDate1', label: '出生年月日', type: 'date', placeholder: '', defaultValue: profile1.birth_date || '' },
          { name: 'birthTime1', label: '出生時刻', type: 'time', placeholder: '', defaultValue: profile1.birth_time || '' },
          { name: 'birthPlace1', label: '出生場所', type: 'text', placeholder: '例: 東京都中央区', defaultValue: profile1.birth_location_json?.place || '' }
        );
        if (fortunePurpose === 'compatibility') {
          const profile2 = profiles.find((p: Profile) => p.profile_id === selectedPeople[1]);
          fields.push(
            { name: 'nickname2', label: '相手のニックネーム', type: 'text', placeholder: 'たろう', defaultValue: profile2?.nickname || '' },
            { name: 'birthDate2', label: '相手の出生年月日', type: 'date', placeholder: '', defaultValue: profile2?.birth_date || '' },
            { name: 'birthTime2', label: '相手の出生時刻', type: 'time', placeholder: '', defaultValue: profile2?.birth_time || '' },
            { name: 'birthPlace2', label: '相手の出生場所', type: 'text', placeholder: '例: 東京都中央区', defaultValue: profile2?.birth_location_json?.place || '' }
          );
        }
        // 相談内容は最後に追加（個人・相性共通）
        fields.push(
          { name: 'consultation', label: '相談内容', type: 'textarea', placeholder: '何かご相談があればお聞かせください（空欄の場合は今日の運勢を占います）', defaultValue: '' }
        );
        break;
      case 'tarot':
        fields.push(
          { name: 'nickname1', label: 'ニックネーム', type: 'text', placeholder: 'はなこ', defaultValue: profile1.nickname || '' }
        );
        if (fortunePurpose === 'compatibility') {
          const profile2 = profiles.find((p: Profile) => p.profile_id === selectedPeople[1]);
          fields.push(
            { name: 'nickname2', label: '相手のニックネーム', type: 'text', placeholder: 'たろう', defaultValue: profile2?.nickname || '' }
          );
        }
        // 相談内容は最後に追加（個人・相性共通）
        fields.push(
          { name: 'consultation', label: '相談内容', type: 'textarea', placeholder: '何かご相談があればお聞かせください（空欄の場合は今日の運勢を占います）', defaultValue: '' }
        );
        break;
    }

    return fields;
  };

  const handleInputChange = (name: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGetFortune = () => {
    // 相談内容を保存
    const consultation = formData.consultation || '';
    console.log('Form data:', formData);
    console.log('Consultation from form:', consultation);
    setConsultation(consultation);
    
    // タロットの場合はタッチ画面に遷移、その他はローディング画面に遷移
    if (fortuneType === 'tarot') {
      setCurrentScreen('tarot-touch-screen');
    } else {
      setCurrentScreen(`${fortuneType}-loading-screen`);
    }
  };

  const handleBack = () => {
    setCurrentScreen('person-select-screen');
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
              {field.type === 'textarea' ? (
                <textarea
                  name={field.name}
                  placeholder={field.placeholder}
                  defaultValue={field.defaultValue}
                  onChange={(e) => handleInputChange(field.name, e.target.value)}
                  className="form-textarea w-full p-3 h-32 resize-none"
                />
              ) : (
                <input
                  name={field.name}
                  type={field.type}
                  placeholder={field.placeholder}
                  defaultValue={field.defaultValue}
                  onChange={(e) => handleInputChange(field.name, e.target.value)}
                  className="form-input w-full p-3"
                />
              )}
            </div>
          ))}
        </div>
        <div className="mt-10 text-center">
          <button
            onClick={handleGetFortune}
            className="btn-primary text-white font-bold py-3 px-10 rounded-full text-lg shadow-lg flex items-center justify-center mx-auto"
          >
            鑑定する
          </button>
        </div>
        <div className="mt-8 text-center">
          <button
            onClick={handleBack}
            className="text-gray-400 hover:text-white text-sm underline mx-auto"
          >
            ← 人物選択に戻る
          </button>
        </div>
      </div>
    </section>
  );
};

export default InformationInputScreen;