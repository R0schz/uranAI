"use client";

import { createContext, useContext, ReactNode, useEffect, useCallback } from 'react';
import { useError } from '../hooks/useError';
import { useLoading } from '../hooks/useLoading';
import { api } from '../lib/api';
import ErrorMessage from '../components/ErrorMessage';
import { createBrowserClient } from '@supabase/ssr';
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// Profileインターフェース（外部設計書に合わせて修正）
export interface Profile {
  profile_id: number;
  nickname: string;
  name_hiragana: string;
  gender?: 'female' | 'male' | 'unknown';
  birth_date?: string;
  birth_time?: string;
  birth_location_json?: any;  // 出生地の詳細情報
  is_self_flag?: boolean;     // 自分自身のプロフィールかどうか
}

export type ModalType = 'login' | 'register' | 'premium' | 'ticket' | 'addPerson' | 'confirmPerson' | null;

export interface ModalData {
  personId?: number;
  message?: string;
}

// 状態の型定義
interface AppStateProperties {
  isAuthChecked: boolean;
  isLoggedIn: boolean;
  isPremium: boolean;
  currentScreen: string;
  tickets: number;
  fortunePurpose: 'personal' | 'compatibility' | null;
  fortuneType: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null;
  selectedPeople: number[];
  profiles: Profile[];
  consultation: string;
  activeModal: ModalType;
  modalData: ModalData | null;
}

// アクションの型定義
interface AppStateActions {
  setAuthChecked: (isChecked: boolean) => void;
  setLoggedIn: (loggedIn: boolean) => void;
  setPremium: (premium: boolean) => void;
  setCurrentScreen: (screen: string) => void;
  setTickets: (tickets: number) => void;
  setFortunePurpose: (purpose: 'personal' | 'compatibility' | null) => void;
  setFortuneType: (type: 'numerology' | 'horoscope' | 'tarot' | 'comprehensive' | null) => void;
  setSelectedPeople: (people: number[]) => void;
  setProfiles: (profiles: Profile[]) => void;
  addProfileToState: (profile: Profile) => void;
  setConsultation: (consultation: string) => void;
  showModal: (type: ModalType, data?: ModalData | null) => void;
  hideModal: () => void;
}

// Zustandストアの作成（永続化機能付き）
export const useAppStore = create<AppStateProperties & AppStateActions>()(
  persist(
    (set, get) => ({
      isAuthChecked: false,
      isLoggedIn: false,
      isPremium: false,
      currentScreen: 'splash-screen',
      tickets: 5,
      fortunePurpose: null,
      fortuneType: null,
      selectedPeople: [],
      profiles: [],
      consultation: '',
      activeModal: null,
      modalData: null,
      setAuthChecked: (isChecked) => {
        console.log('setAuthChecked called with:', isChecked);
        set({ isAuthChecked: isChecked });
        console.log('isAuthChecked after set:', get().isAuthChecked);
      },
      setLoggedIn: (loggedIn) => set({ isLoggedIn: loggedIn }),
      setPremium: (premium) => set({ isPremium: premium }),
      setCurrentScreen: (screen) => {
        console.log('setCurrentScreen called with:', screen);
        set({ currentScreen: screen });
        console.log('currentScreen after set:', get().currentScreen);
      },
      setTickets: (tickets) => set({ tickets }),
      setFortunePurpose: (purpose) => set({ fortunePurpose: purpose }),
      setFortuneType: (type) => set({ fortuneType: type }),
      setSelectedPeople: (people) => set({ selectedPeople: people }),
      setProfiles: (profiles) => set({ profiles }),
      addProfileToState: (profile) => set((state) => ({ profiles: [...state.profiles, profile] })),
      setConsultation: (consultation) => set({ consultation }),
      showModal: (type, data = null) => set({ activeModal: type, modalData: data }),
      hideModal: () => set({ activeModal: null, modalData: null }),
    }),
    {
      name: 'uranai-app-storage', // ローカルストレージのキー名
      storage: createJSONStorage(() => localStorage),
      // 永続化する項目を指定（isAuthCheckedは永続化しない）
      partialize: (state) => ({
        isLoggedIn: state.isLoggedIn,
        isPremium: state.isPremium,
        currentScreen: state.currentScreen,
        tickets: state.tickets,
        profiles: state.profiles,
        fortunePurpose: state.fortunePurpose,
        fortuneType: state.fortuneType,
        selectedPeople: state.selectedPeople,
        consultation: state.consultation,
        // isAuthCheckedは永続化しない（常にfalseから開始）
      }),
      // 復元時の処理
      onRehydrateStorage: () => (state) => {
        if (state) {
          console.log('App state restored from storage:', {
            isLoggedIn: state.isLoggedIn,
            currentScreen: state.currentScreen,
            profilesCount: state.profiles.length
          });
        }
      },
    }
  )
);

// Contextが提供する「副作用を伴う関数」の型定義
interface AppContextType {
  error: string | null;
  handleError: (error: string) => void;
  clearError: () => void;
  isLoading: boolean;
  withLoading: <T>(promise: Promise<T>) => Promise<T>;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  addProfile: (profile: Omit<Profile, 'profile_id' | 'name_hiragana'> & { name_hiragana?: string }) => Promise<void>;
  updateProfile: (id: number, profile: Partial<Profile>) => Promise<void>;
  deleteProfile: (id: number) => Promise<void>;
  getDivination: () => Promise<void>;
  askMoreQuestion: (question: string) => Promise<void>;
}

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const { error, handleError, clearError } = useError();
  const { isLoading, withLoading } = useLoading();
  const { hideModal, addProfileToState, setProfiles } = useAppStore();
  
// ▼▼▼ 環境変数を明示的に渡すように修正 ▼▼▼
console.log('Supabase URL:', process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log('Supabase Key exists:', !!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

const supabase = createBrowserClient({
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
});

  // プロフィールデータをデータベースから取得する関数
  const loadProfiles = useCallback(async () => {
    try {
      console.log('Loading profiles from API...');
      const profiles = await withLoading(api.profile.getAll());
      console.log('Profiles loaded:', profiles);
      console.log('Number of profiles:', profiles.length);
      setProfiles(profiles);
    } catch (error) {
      console.error('Failed to load profiles:', error);
      console.error('Error details:', error);
      // エラーが発生してもアプリケーションを停止させない
    }
  }, [withLoading, setProfiles]);

  useEffect(() => {
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
        console.log('Auth state changed:', event, session?.user?.id);
        const user = session?.user ?? null;
        const currentScreen = useAppStore.getState().currentScreen;
        const isLoggedIn = useAppStore.getState().isLoggedIn;
        
        // 既にログイン済みの場合は重複処理を避ける
        if (user && isLoggedIn && event === 'SIGNED_IN') {
            console.log('Already logged in, skipping duplicate auth state change');
            return;
        }
        
        useAppStore.getState().setLoggedIn(!!user);
        useAppStore.getState().setAuthChecked(true);

        if (user) {
            console.log('User logged in, loading profiles...');
            console.log('Current screen:', currentScreen);
            console.log('Auth event:', event);
            // 認証後にプロフィールデータを読み込み
            await loadProfiles();
            
            // 初回ログイン時（スプラッシュ画面から）のみホーム画面に遷移
            if (event === 'SIGNED_IN' && currentScreen === 'splash-screen') {
                console.log('Navigating to home screen from splash screen');
                useAppStore.getState().setCurrentScreen('home-screen');
            }
        } else {
            console.log('User logged out, clearing profiles...');
            useAppStore.getState().setCurrentScreen('splash-screen');
            // ログアウト時にプロフィールデータをクリア
            setProfiles([]);
            // ローカルストレージからセッション情報を削除
            localStorage.removeItem('supabase_session');
            localStorage.removeItem('uranai-app-storage');
        }
    });

    // 初回ロード時に現在のセッションをチェック
    const checkInitialSession = async () => {
      console.log('Checking initial session...');
      console.log('Starting checkInitialSession function');
      
      try {
        // 既にローカルストレージから状態が復元されているかチェック
        const currentState = useAppStore.getState();
        console.log('Current state from store:', {
          isLoggedIn: currentState.isLoggedIn,
          currentScreen: currentState.currentScreen,
          profilesCount: currentState.profiles.length
        });
        
        // 既にログイン状態が復元されている場合は、プロフィールを読み込んで認証チェックを完了
        if (currentState.isLoggedIn && currentState.profiles.length > 0) {
          console.log('User already logged in with profiles, completing auth check');
          useAppStore.getState().setAuthChecked(true);
          console.log('setAuthChecked(true) called - already logged in');
          return;
        }
        
        // ローカルストレージからセッション情報を確認
        console.log('Checking localStorage for saved session...');
        const savedSession = localStorage.getItem('supabase_session');
        console.log('Saved session found:', !!savedSession);
        
        if (savedSession) {
          try {
            const sessionData = JSON.parse(savedSession);
            const now = Math.floor(Date.now() / 1000);
            
            // セッションの有効期限をチェック
            if (sessionData.expires_at && sessionData.expires_at > now) {
              console.log('Valid saved session found, restoring...');
              useAppStore.getState().setLoggedIn(true);
              
              // プロフィールを読み込む（エラーが発生しても続行）
              try {
                await loadProfiles();
                console.log('loadProfiles completed successfully');
              } catch (error) {
                console.error('Error in loadProfiles:', error);
              }
              
              // 保存された画面状態を復元
              const savedScreen = useAppStore.getState().currentScreen;
              console.log('Saved screen from storage:', savedScreen);
              if (savedScreen && savedScreen !== 'splash-screen') {
                console.log('Restoring saved screen:', savedScreen);
                useAppStore.getState().setCurrentScreen(savedScreen);
              } else {
                console.log('Setting screen to home-screen');
                useAppStore.getState().setCurrentScreen('home-screen');
              }
              console.log('Final currentScreen after auth check:', useAppStore.getState().currentScreen);
              useAppStore.getState().setAuthChecked(true);
              console.log('setAuthChecked(true) called - saved session');
              return;
            } else {
              console.log('Saved session expired, clearing...');
              localStorage.removeItem('supabase_session');
            }
          } catch (error) {
            console.error('Error parsing saved session:', error);
            localStorage.removeItem('supabase_session');
          }
        }
        
        // ローカルストレージにセッションがない場合でも、Supabaseのセッションチェックを実行
        if (!savedSession) {
          console.log('No saved session, but checking Supabase session...');
        }
        
        // Supabaseのセッションをチェック（タイムアウト付き）
        console.log('Checking Supabase session...');
        let session = null;
        
        try {
          // タイムアウト付きでセッション取得（タイムアウト時間を2秒に短縮）
          const sessionPromise = supabase.auth.getSession();
          const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Session check timeout')), 2000)
          );
          
          const { data: { session: sessionData }, error } = await Promise.race([sessionPromise, timeoutPromise]) as any;
          
          if (error) {
            console.error('Error getting session:', error);
            session = null;
          } else {
            session = sessionData;
          }
          console.log('Initial session:', session?.user?.id);
          console.log('Session exists:', !!session);
        } catch (sessionError) {
          console.error('Exception getting session:', sessionError);
          // セッション取得に失敗した場合は、セッションなしとして処理
          session = null;
          // タイムアウトエラーの場合は警告のみ表示
          if (sessionError instanceof Error && sessionError.message === 'Session check timeout') {
            console.warn('Session check timed out, continuing without session');
          }
        }
        
        if (session?.user) {
          console.log('Initial session found, loading profiles...');
          useAppStore.getState().setLoggedIn(true);
          console.log('About to call loadProfiles...');
          try {
            await loadProfiles();
            console.log('loadProfiles completed successfully');
          } catch (error) {
            console.error('Error in loadProfiles:', error);
          }
          
          // 保存された画面状態を復元
          const savedScreen = useAppStore.getState().currentScreen;
          console.log('Saved screen from storage (initial session):', savedScreen);
          if (savedScreen && savedScreen !== 'splash-screen') {
            console.log('Restoring saved screen:', savedScreen);
            useAppStore.getState().setCurrentScreen(savedScreen);
          } else {
            console.log('Setting screen to home-screen (initial session)');
            useAppStore.getState().setCurrentScreen('home-screen');
          }
          console.log('Final currentScreen after initial session check:', useAppStore.getState().currentScreen);
        } else {
          console.log('No initial session found');
          // セッションがない場合は保存された状態をクリア
          useAppStore.getState().setLoggedIn(false);
          // セッションがない場合はスプラッシュ画面のまま
          useAppStore.getState().setCurrentScreen('splash-screen');
          setProfiles([]);
        }
        
        // 認証チェック完了を確実に設定
        console.log('Setting auth checked to true - final step');
        useAppStore.getState().setAuthChecked(true);
        console.log('Auth check completed, isAuthChecked:', useAppStore.getState().isAuthChecked);
        console.log('checkInitialSession function completed');
        
      } catch (error) {
        console.error('Error in checkInitialSession:', error);
        // エラーが発生した場合でも認証チェックを完了させる
        useAppStore.getState().setAuthChecked(true);
      }
    };

    console.log('About to call checkInitialSession...');
    
    // タイムアウトを設定して、認証チェックが確実に完了するようにする
    const authCheckTimeout = setTimeout(() => {
      console.log('Auth check timeout - forcing auth check completion');
      useAppStore.getState().setAuthChecked(true);
    }, 5000); // 5秒でタイムアウト
    
    checkInitialSession().then(() => {
      console.log('checkInitialSession promise resolved');
      clearTimeout(authCheckTimeout);
    }).catch((error) => {
      console.error('checkInitialSession promise rejected:', error);
      clearTimeout(authCheckTimeout);
      // エラーが発生した場合でも認証チェックを完了させる
      useAppStore.getState().setAuthChecked(true);
    });

    return () => {
        subscription.unsubscribe();
    };
  }, [supabase, loadProfiles]);



  const handleSignIn = async (email: string, password: string) => {
    console.log('handleSignIn called with:', email);
    try {
      const { data, error } = await supabase.auth.signInWithPassword({ 
        email, 
        password 
      });
      console.log('SignIn response:', { data, error });
      
      if (error) {
        console.log('Login error:', error.message);
        handleError(error.message);
      } else {
        console.log('Login successful, hiding modal and navigating to home');
        console.log('User data:', data.user);
        console.log('Current modal state before hide:', useAppStore.getState().activeModal);
        hideModal();
        console.log('Current screen before navigation:', useAppStore.getState().currentScreen);
        useAppStore.getState().setCurrentScreen('home-screen');
        console.log('Current screen after navigation:', useAppStore.getState().currentScreen);
        
        // セッション情報をローカルストレージに保存
        if (data.session) {
          localStorage.setItem('supabase_session', JSON.stringify({
            access_token: data.session.access_token,
            refresh_token: data.session.refresh_token,
            expires_at: data.session.expires_at,
            user_id: data.user.id
          }));
        }
      }
    } catch (err) {
      console.error('Unexpected error during login:', err);
      handleError('ログイン中に予期しないエラーが発生しました');
    }
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
  
  const addProfile = async (profileData: Omit<Profile, 'profile_id' | 'name_hiragana'> & { name_hiragana?: string }) => {
    try {
      const profileToSend = { 
        nickname: profileData.nickname,
        name_hiragana: profileData.name_hiragana || '',
        gender: profileData.gender,
        birth_date: profileData.birth_date,
        birth_time: profileData.birth_time,
        birth_location_json: profileData.birth_location_json,
        is_self_flag: profileData.is_self_flag || false
      };
      
      const result = await withLoading(api.profile.create(profileToSend));
      
      if (result && result.profile) {
        const newProfile: Profile = { 
          profile_id: result.profile.profile_id,
          nickname: result.profile.nickname,
          name_hiragana: result.profile.name_hiragana,
          gender: result.profile.gender,
          birth_date: result.profile.birth_date,
          birth_time: result.profile.birth_time,
          birth_location_json: result.profile.birth_location_json,
          is_self_flag: result.profile.is_self_flag
        };
        addProfileToState(newProfile);
        hideModal();
      } else {
        handleError('プロフィールの追加に失敗しました');
      }
    } catch (error) {
      handleError(error instanceof Error ? error.message : 'プロフィールの追加に失敗しました');
    }
  };

  const updateProfile = async (id: number, profile: Partial<Profile>) => {
    try {
      const profileToUpdate = {
        nickname: profile.nickname,
        name_hiragana: profile.name_hiragana,
        gender: profile.gender,
        birth_date: profile.birth_date,
        birth_time: profile.birth_time,
        birth_location_json: profile.birth_location_json,
        is_self_flag: profile.is_self_flag
      };
      
      await withLoading(api.profile.update(id, profileToUpdate));
    } catch (error) {
      handleError(error instanceof Error ? error.message : 'プロフィールの更新に失敗しました');
    }
  };

  const deleteProfile = async (id: number) => {
    try {
      await withLoading(api.profile.delete(id));
      // フロントエンドの状態からも削除
      const currentProfiles = useAppStore.getState().profiles;
      setProfiles(currentProfiles.filter(p => p.profile_id !== id));
    } catch (error) {
      handleError(error instanceof Error ? error.message : 'プロフィールの削除に失敗しました');
    }
  };

  const getDivination = async () => {
    try {
      const { fortuneType, selectedPeople, profiles } = useAppStore.getState();
      
      if (!fortuneType || selectedPeople.length === 0) return;

      const profilesData = selectedPeople.map(id => {
          const profile = profiles.find(p => p.profile_id === id);
          if (!profile) throw new Error('Selected profile not found');
          return {
              profile_id: profile.profile_id,
              name_hiragana: profile.name_hiragana,
              birth_date: profile.birth_date || '',
              birth_time: profile.birth_time,
              birth_location_json: profile.birth_location_json
          };
      });

      const resultData = {
        fortune_type: fortuneType,
        request_data: {
          type: fortuneType,
          profiles: profilesData
        },
        visual_result: {},
        ai_text: "占い結果のテキスト"
      };

      const result = await withLoading(api.divination.create(resultData));

      if (result.result_id) {
        // 占い結果の処理
        console.log('占い結果が保存されました:', result.result_id);
        useAppStore.getState().setCurrentScreen('result-screen');
      }
    } catch (error) {
      handleError(error instanceof Error ? error.message : '占いの実行に失敗しました');
    }
  };

  const askMoreQuestion = async (question: string) => {
    // (実装は省略)
  };

  const handleLogout = async () => {
    try {
      console.log('Logging out user...');
      const { error } = await supabase.auth.signOut();
      
      if (error) {
        console.error('Logout error:', error);
        handleError('ログアウト中にエラーが発生しました');
      } else {
        console.log('Logout successful');
        // ローカルストレージをクリア
        localStorage.removeItem('supabase_session');
        localStorage.removeItem('uranai-app-storage');
        
        // 状態をリセット
        useAppStore.getState().setLoggedIn(false);
        useAppStore.getState().setCurrentScreen('splash-screen');
        setProfiles([]);
        hideModal();
      }
    } catch (err) {
      console.error('Unexpected error during logout:', err);
      handleError('ログアウト中に予期しないエラーが発生しました');
    }
  };

  const contextValue: AppContextType = {
    error,
    handleError,
    clearError,
    isLoading,
    withLoading,
    login: handleSignIn,
    register: handleSignUp,
    logout: handleLogout,
    addProfile,
    updateProfile,
    deleteProfile,
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