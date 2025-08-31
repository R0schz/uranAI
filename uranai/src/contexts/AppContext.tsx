"use client";

import { createContext, useContext, ReactNode, useEffect } from 'react';
import { useError } from '../hooks/useError';
import { useLoading } from '../hooks/useLoading';
import { api } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import { create } from 'zustand';

// Personインターフェース (変更なし)
export interface Person {
  id: number;
  nickname: string;
  name: string;
  gender?: 'female' | 'male' | 'unknown';
  birthDate?: string;
  birthTime?: string;
  birthPlace?: string;
}

export type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson' | null;

export interface ModalData {
  personId?: number;
  message?: string;
}

// ========== ↓↓↓ ここからZustandの定義を修正 ↓↓↓ ==========

// 1. 「状態」のプロパティだけを定義するインターフェース
interface AppStateProperties {
  isAuthChecked: boolean;
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
}

// 2. 「アクション（状態を変更する関数）」だけを定義するインターフェース
interface AppStateActions {
  setAuthChecked: (isChecked: boolean) => void;
  setLoggedIn: (loggedIn: boolean) => void;
  setPremium: (premium: boolean) => void;
  setCurrentScreen: (screen: string) => void;
  setTickets: (tickets: number) => void;
  setFortunePurpose: (purpose: 'personal' | 'compatibility' | null) => void;
  setFortuneType: (type: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null) => void;
  setSelectedPeople: (people: number[]) => void;
  setPeople: (people: Person[]) => void;
  addPersonToState: (person: Person) => void;
  showModal: (type: ModalType, data?: ModalData | null) => void;
  hideModal: () => void;
}

// 3. 状態とアクションを結合してZustandストアを作成
export const useAppStore = create<AppStateProperties & AppStateActions>((set) => ({
  // --- 初期状態 ---
  isAuthChecked: false,
  isLoggedIn: false,
  isPremium: false,
  currentScreen: 'splash-screen',
  tickets: 5,
  fortunePurpose: null,
  fortuneType: null,
  selectedPeople: [],
  people: [],
  activeModal: null,
  modalData: null,
  // --- アクションの実装 ---
  setAuthChecked: (isChecked) => set({ isAuthChecked: isChecked }),
  setLoggedIn: (loggedIn) => set({ isLoggedIn: loggedIn }),
  setPremium: (premium) => set({ isPremium: premium }),
  setCurrentScreen: (screen) => set({ currentScreen: screen }),
  setTickets: (tickets) => set({ tickets }),
  setFortunePurpose: (purpose) => set({ fortunePurpose: purpose }),
  setFortuneType: (type) => set({ fortuneType: type }),
  setSelectedPeople: (people) => set({ selectedPeople: people }),
  setPeople: (people) => set({ people }),
  addPersonToState: (person) => set((state) => ({ people: [...state.people, person] })),
  showModal: (type, data = null) => set({ activeModal: type, modalData: data }),
  hideModal: () => set({ activeModal: null, modalData: null }),
}));

// ========== ↑↑↑ ここまでZustandの定義を修正 ↑↑↑ ==========


// Contextが提供する「副作用を伴う関数」の型定義
interface AppContextType {
  error: string | null;
  handleError: (error: string) => void;
  clearError: () => void;
  isLoading: boolean;
  withLoading: <T>(promise: Promise<T>) => Promise<T>;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  addPerson: (person: Omit<Person, 'id' | 'name'> & { name?: string }) => Promise<void>;
  updatePerson: (id: number, person: Partial<Person>) => Promise<void>;
  deletePerson: (id: number) => Promise<void>;
  getDivination: () => Promise<void>;
  askMoreQuestion: (question: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const { error, handleError, clearError } = useError();
  const { isLoading, withLoading } = useLoading();
  const { hideModal, addPersonToState } = useAppStore();

  const supabase = createPagesBrowserClient({
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
    supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_KEY!
  });

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
        const user = session?.user ?? null;
        useAppStore.getState().setLoggedIn(!!user);
        useAppStore.getState().setAuthChecked(true);

        if (user) {
            useAppStore.getState().setCurrentScreen('home-screen');
        } else {
            useAppStore.getState().setCurrentScreen('splash-screen');
        }
    });

    return () => {
        subscription.unsubscribe();
    };
  }, [supabase]);

  const handleSignIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) handleError(error.message);
    else hideModal();
  };

  const handleSignUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: { emailRedirectTo: `${location.origin}/auth/callback` },
    });
    if (error) handleError(error.message);
    else {
      alert('確認メールを送信しました。メールボックスをご確認ください。');
      hideModal();
    }
  };
  
  const addPerson = async (personData: Omit<Person, 'id' | 'name'> & { name?: string }) => {
    const personToSend = { ...personData, name: personData.name || '' };
    const result = await withLoading(api.person.addPerson(personToSend));

    if (result.error) {
      handleError(result.error);
      return;
    }
    
    if (result.data) {
      const newPerson: Person = { ...personToSend, id: result.data.id };
      addPersonToState(newPerson);
      hideModal();
    }
  };

  const updatePerson = async (id: number, person: Partial<Person>) => { /* ... */ };
  const deletePerson = async (id: number) => { /* ... */ };
  const getDivination = async () => { /* ... */ };
  const askMoreQuestion = async (question: string) => { /* ... */ };

  const contextValue: AppContextType = {
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
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
      {error && <ErrorMessage message={error} onClose={clearError} />}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === null) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}