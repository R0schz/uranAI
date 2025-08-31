"use client";

import { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';
import { useError } from '../hooks/useError';
import { useLoading } from '../hooks/useLoading';
// 独自のモーダル管理を使用するため、useModalフックは削除
import { api } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';

interface Person {
  id: number;
  nickname: string;
  name: string;
  gender?: 'female' | 'male' | 'unknown';
  birthDate?: string;
  birthTime?: string;
  birthPlace?: string;
}

interface AppState {
  isLoggedIn: boolean;
  isPremium: boolean;
  currentScreen: string;
  tickets: number;
  fortunePurpose: 'personal' | 'compatibility' | null;
  selectedPeople: number[];
  fortuneType: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null;
  people: Person[];
  nextPersonId: number;
}

type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson' | null;

interface ModalData {
  personId?: number;
  message?: string;
}

interface AppContextType {
  state: AppState;
  setState: React.Dispatch<React.SetStateAction<AppState>>;
  activeModal: ModalType;
  modalData: ModalData | null;
  showModal: (type: ModalType, data?: ModalData) => void;
  hideModal: () => void;
  error: string | null;
  handleError: (error: string) => void;
  clearError: () => void;
  isLoading: boolean;
  withLoading: <T>(promise: Promise<T>) => Promise<T>;
  // 既に上部で定義済みのため削除
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  addPerson: (person: Omit<Person, 'id'>) => Promise<void>;
  updatePerson: (id: number, person: Partial<Person>) => Promise<void>;
  deletePerson: (id: number) => Promise<void>;
  getDivination: () => Promise<void>;
  askMoreQuestion: (question: string) => Promise<void>;
}

const initialState: AppState = {
  isLoggedIn: false,
  isPremium: false,
  currentScreen: 'splash-screen',
  tickets: 5,
  fortunePurpose: null,
  selectedPeople: [],
  fortuneType: null,
  people: [
    {
      id: 1,
      nickname: 'あなた',
      name: 'てすと はなこ',
      gender: 'female',
      birthDate: '1998-11-10',
      birthTime: '14:30',
      birthPlace: '東京都渋谷区'
    }
  ],
  nextPersonId: 2,
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AppState>(initialState);
  const [activeModal, setActiveModal] = useState<ModalType>(null);
  const [modalData, setModalData] = useState<ModalData | null>(null);
  const { error, handleError, clearError } = useError();
  const { isLoading, withLoading } = useLoading();

  const supabase = createPagesBrowserClient({
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
    supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_KEY!
  });

  // トークンの復元
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setState(prev => ({ ...prev, isLoggedIn: true }));
    }
  }, []);

  const handleSignUp = async (email: string, password: string) => {
    await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${location.origin}/auth/callback`,
      },
    });
    alert('確認メールを送信しました。メールボックスをご確認ください。');
    setState(prev => ({ ...prev, isLoggedIn: true }));
    hideModal();
  };

  const handleSignIn = async (email: string, password: string) => {
    await supabase.auth.signInWithPassword({
      email,
      password,
    });
    setState(prev => ({ ...prev, isLoggedIn: true, currentScreen: 'home-screen' }));
    hideModal();
  };

  const handleOAuthSignIn = async (provider: 'google' | 'twitter' | 'facebook') => {
    await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${location.origin}/auth/callback`,
      },
    });
  };

  const addPerson = async (person: Omit<Person, 'id'>) => {
    const result = await withLoading(api.person.addPerson(person));
    if (result.error) {
      handleError(result.error);
      return;
    }
    setState(prev => ({
      ...prev,
      people: [...prev.people, { ...person, id: result.data!.id }],
      nextPersonId: prev.nextPersonId + 1
    }));
    hideModal();
  };

  const updatePerson = async (id: number, person: Partial<Person>) => {
    const result = await withLoading(api.person.updatePerson(id, person));
    if (result.error) {
      handleError(result.error);
      return;
    }
    setState(prev => ({
      ...prev,
      people: prev.people.map(p => p.id === id ? { ...p, ...person } : p)
    }));
  };

  const deletePerson = async (id: number) => {
    const result = await withLoading(api.person.deletePerson(id));
    if (result.error) {
      handleError(result.error);
      return;
    }
    setState(prev => ({
      ...prev,
      people: prev.people.filter(p => p.id !== id)
    }));
  };

  const getDivination = async () => {
    if (!state.fortuneType || state.selectedPeople.length === 0) return;

    const people = state.selectedPeople.map(id => {
      const person = state.people.find(p => p.id === id);
      if (!person) throw new Error('Selected person not found');
      return {
        id: person.id,
        name: person.name,
        birthDate: person.birthDate || '',
        birthTime: person.birthTime,
        birthPlace: person.birthPlace
      };
    });

    const result = await withLoading(
      api.divination.getDivination({
        type: state.fortuneType,
        people
      })
    );

    if (result.error) {
      handleError(result.error);
      return;
    }

    // 結果を表示
    setState(prev => ({
      ...prev,
      currentScreen: 'result-screen'
    }));
  };

  const askMoreQuestion = async (question: string) => {
    // TODO: 実装
  };

  const showModal = useCallback((type: ModalType, data: ModalData | null = null) => {
    setActiveModal(type);
    setModalData(data);
  }, []);

  const hideModal = useCallback(() => {
    setActiveModal(null);
    setModalData(null);
  }, []);

  return (
    <AppContext.Provider
      value={{
        state,
        setState,
        activeModal,
        modalData,
        showModal,
        hideModal,
        error,
        handleError,
        clearError,
        isLoading,
        withLoading,
        // 既に上部で定義済みのため削除
        login: handleSignIn,
        register: handleSignUp,
        addPerson,
        updatePerson,
        deletePerson,
        getDivination,
        askMoreQuestion
      }}
    >
      {children}
      {error && <ErrorMessage message={error} onClose={clearError} />}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}