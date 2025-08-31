"use client";

import { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';
import { useError } from '../hooks/useError';
import { useLoading } from '../hooks/useLoading';
// 独自のモーダル管理を使用するため、useModalフックは削除
import { api } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import { create } from 'zustand';

export interface Person {
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
  fortuneType: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null;
  selectedPeople: number[];
  people: Person[];
  activeModal: ModalType;
  modalData: ModalData | null;
  setLoggedIn: (loggedIn: boolean) => void;
  setPremium: (premium: boolean) => void;
  setCurrentScreen: (screen: string) => void;
  setTickets: (tickets: number) => void;
  setFortunePurpose: (purpose: 'personal' | 'compatibility' | null) => void;
  setFortuneType: (type: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null) => void;
  setSelectedPeople: (people: number[]) => void;
  setPeople: (people: Person[]) => void;
  showModal: (type: ModalType) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isLoggedIn: false,
  isPremium: false,
  currentScreen: 'splash-screen',
  tickets: 5,
  fortunePurpose: null,
  fortuneType: null,
  selectedPeople: [],
  people: [], // Initialize people array
  activeModal: null, // Add activeModal to Zustand
  modalData: null, // Add modalData to Zustand
  setLoggedIn: (loggedIn) => set({ isLoggedIn: loggedIn }),
  setPremium: (premium) => set({ isPremium: premium }),
  setCurrentScreen: (screen) => set({ currentScreen: screen }),
  setTickets: (tickets) => set({ tickets }),
  setFortunePurpose: (purpose) => set({ fortunePurpose: purpose }),
  setFortuneType: (type) => set({ fortuneType: type }),
  setSelectedPeople: (people) => set({ selectedPeople: people }),
  setPeople: (people) => set({ people }), // Add setPeople to Zustand
  showModal: (type) => set({ activeModal: type, modalData: null }),
}));

export type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson' | null;

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
  setCurrentScreen: (screen: string) => void;
}

const initialState: AppState = {
  isLoggedIn: false,
  isPremium: false,
  currentScreen: 'splash-screen',
  tickets: 5,
  fortunePurpose: null,
  fortuneType: null,
  selectedPeople: [],
  people: [], // Initialize people array
  activeModal: null, // Add activeModal to initial state
  modalData: null, // Add modalData to initial state
  setLoggedIn: (loggedIn) => {},
  setPremium: (premium) => {},
  setCurrentScreen: (screen) => {},
  setTickets: (tickets) => {},
  setFortunePurpose: (purpose) => {},
  setFortuneType: (type) => {},
  setSelectedPeople: (people) => {},
  setPeople: (people) => {}, // Add setPeople to initial state
  showModal: (type) => {},
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
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
      useAppStore.getState().setLoggedIn(true);
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
    useAppStore.getState().setLoggedIn(true);
    hideModal();
  };

  const handleSignIn = async (email: string, password: string) => {
    await supabase.auth.signInWithPassword({
      email,
      password,
    });
    useAppStore.getState().setLoggedIn(true);
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
    // This part of the state management is now handled by Zustand
    // setState(prev => ({
    //   ...prev,
    //   people: [...prev.people, { ...person, id: result.data!.id }],
    //   nextPersonId: prev.nextPersonId + 1
    // }));
    hideModal();
  };

  const updatePerson = async (id: number, person: Partial<Person>) => {
    const result = await withLoading(api.person.updatePerson(id, person));
    if (result.error) {
      handleError(result.error);
      return;
    }
    // This part of the state management is now handled by Zustand
    // setState(prev => ({
    //   ...prev,
    //   people: prev.people.map(p => p.id === id ? { ...p, ...person } : p)
    // }));
  };

  const deletePerson = async (id: number) => {
    const result = await withLoading(api.person.deletePerson(id));
    if (result.error) {
      handleError(result.error);
      return;
    }
    // This part of the state management is now handled by Zustand
    // setState(prev => ({
    //   ...prev,
    //   people: prev.people.filter(p => p.id !== id)
    // }));
  };

  const getDivination = async () => {
    const state = useAppStore.getState();
    if (!state.fortuneType || state.selectedPeople.length === 0) return;

    const people = state.selectedPeople.map((id: number) => {
      const person = state.people.find((p: Person) => p.id === id);
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
        type: state.fortuneType!, // Assert non-null
        people
      })
    );

    if (result.error) {
      handleError(result.error);
      return;
    }

    // 結果を表示
    state.setCurrentScreen('result-screen');
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
        state: useAppStore.getState(), // Expose Zustand state
        setState: useAppStore.getState, // Expose Zustand setState
        activeModal,
        modalData,
        showModal,
        hideModal,
        error,
        handleError,
        clearError,
        isLoading,
        withLoading,
        login: handleSignIn,
        register: handleSignUp,
        addPerson,
        updatePerson,
        deletePerson,
        getDivination,
        askMoreQuestion,
        setCurrentScreen: useAppStore.getState().setCurrentScreen,
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