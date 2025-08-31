"use client";

import { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';
import { useError } from '../hooks/useError';
import { useLoading } from '../hooks/useLoading';
import { api } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import { create } from 'zustand';
import { User } from '@supabase/supabase-js';

// Personインターフェース
export interface Person {
  id: number;
  nickname: string;
  name: string;
  gender?: 'female' | 'male' | 'unknown';
  birthDate?: string;
  birthTime?: string;
  birthPlace?: string;
}

// AppStateインターフェース (Zustandで管理する状態)
interface AppState {
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
  setAuthChecked: (isChecked: boolean) => void;
  setLoggedIn: (loggedIn: boolean) => void;
  setPremium: (premium: boolean) => void;
  setCurrentScreen: (screen: string) => void;
  setTickets: (tickets: number) => void;
  setFortunePurpose: (purpose: 'personal' | 'compatibility' | null) => void;
  setFortuneType: (type: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null) => void;
  setSelectedPeople: (people: number[]) => void;
  setPeople: (people: Person[]) => void;
  showModal: (type: ModalType, data?: ModalData | null) => void;
  hideModal: () => void;
}

// Zustandストアの作成
export const useAppStore = create<AppState>((set) => ({
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
  setAuthChecked: (isChecked) => set({ isAuthChecked: isChecked }),
  setLoggedIn: (loggedIn) => set({ isLoggedIn: loggedIn }),
  setPremium: (premium) => set({ isPremium: premium }),
  setCurrentScreen: (screen) => set({ currentScreen: screen }),
  setTickets: (tickets) => set({ tickets }),
  setFortunePurpose: (purpose) => set({ fortunePurpose: purpose }),
  setFortuneType: (type) => set({ fortuneType: type }),
  setSelectedPeople: (people) => set({ selectedPeople: people }),
  setPeople: (people) => set({ people }),
  showModal: (type, data = null) => set({ activeModal: type, modalData: data }),
  hideModal: () => set({ activeModal: null, modalData: null }),
}));

export type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson' | null;

interface ModalData {
  personId?: number;
  message?: string;
}

// Contextが提供する「関数」の型定義
interface AppContextType {
  error: string | null;
  handleError: (error: string) => void;
  clearError: () => void;
  isLoading: boolean;
  withLoading: <T>(promise: Promise<T>) => Promise<T>;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  addPerson: (person: Omit<Person, 'id'>) => Promise<void>;
  updatePerson: (id: number, person: Partial<Person>) => Promise<void>;
  deletePerson: (id: number) => Promise<void>;
  getDivination: () => Promise<void>;
  askMoreQuestion: (question: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const { error, handleError, clearError } = useError();
  const { isLoading, withLoading } = useLoading();
  const { showModal, hideModal } = useAppStore();

  const supabase = createPagesBrowserClient({
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
    supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_KEY!
  });

  // Supabaseの認証状態を監視し、Zustandストアを更新する
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

  const addPerson = async (person: Omit<Person, 'id'>) => {
    const result = await withLoading(api.person.addPerson(person));
    if (result.error) handleError(result.error);
    else hideModal();
  };

  const updatePerson = async (id: number, person: Partial<Person>) => {
    const result = await withLoading(api.person.updatePerson(id, person));
    if (result.error) handleError(result.error);
  };

  const deletePerson = async (id: number) => {
    const result = await withLoading(api.person.deletePerson(id));
    if (result.error) handleError(result.error);
  };

  const getDivination = async () => {
    // (実装は省略)
  };

  const askMoreQuestion = async (question: string) => {
    // (実装は省略)
  };

  // Contextに渡す関数のセット
  const contextValue = {
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

// 関数を取得するためのカスタムフック
export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}