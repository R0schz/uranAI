"use client";

import { useAppStore } from '../contexts/AppContext';
import { useState, useEffect, useRef } from 'react';
import { api } from '../lib/api';

interface DivinationResult {
  fortune_type: string;
  purpose: string;
  numerology_data?: any;
  temporal_fortune?: any;
  horoscope_data?: any;
  tarot_data?: any;
  compatibility_data?: any;
  ai_analysis: string;
  visual_result: any;
}

const ResultScreen = () => {
  const { 
    currentScreen, 
    tickets, 
    fortuneType, 
    selectedPeople, 
    fortunePurpose,
    profiles,
    consultation,
    setCurrentScreen,
    setSelectedPeople,
    setFortunePurpose,
    setFortuneType,
    setTickets
  } = useAppStore();

  const [divinationResult, setDivinationResult] = useState<DivinationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const hasFetchedRef = useRef(false);
  
  // 画面が変わったらhasFetchedをリセット
  useEffect(() => {
    if (currentScreen !== 'result-screen') {
      hasFetchedRef.current = false;
      setDivinationResult(null);
      setIsLoading(false);
    }
  }, [currentScreen]);

  // 占い結果を取得
  useEffect(() => {
    const fetchDivinationResult = async () => {
      // console.log('ResultScreen useEffect triggered:', {
      //   currentScreen,
      //   fortuneType,
      //   selectedPeople,
      //   profilesLength: profiles.length,
      //   hasFetched,
      //   fetchKey
      // });
      
      if (currentScreen === 'result-screen' && fortuneType && selectedPeople.length > 0 && !hasFetchedRef.current) {
        console.log('Starting divination result fetch...', { 
          currentScreen, 
          fortuneType, 
          selectedPeople, 
          fortunePurpose,
          profilesLength: profiles.length,
          hasFetched: hasFetchedRef.current
        });
        
        // プロファイルが読み込まれていない場合は待機
        if (profiles.length === 0) {
          console.log('Profiles not loaded yet, waiting...');
          return;
        }
        
        setIsLoading(true);
        hasFetchedRef.current = true;
        try {
          const profilesData = selectedPeople.map(id => {
            const profile = profiles.find(p => p.profile_id === id);
            if (!profile) {
              console.error(`Profile not found for ID: ${id}`);
              console.error('Available profiles:', profiles.map(p => ({ id: p.profile_id, nickname: p.nickname })));
              throw new Error(`Selected profile not found for ID: ${id}`);
            }
            return {
              profile_id: profile.profile_id,
              nickname: profile.nickname,
              name_hiragana: profile.name_hiragana,
              birth_date: profile.birth_date || '',
              birth_time: profile.birth_time,
              birth_location_json: profile.birth_location_json
            };
          });
          
          console.log('Profiles data prepared:', profilesData);

          const resultData = {
            fortune_type: fortuneType,
            request_data: {
              type: fortuneType,
              purpose: fortunePurpose,
              profiles: profilesData,
              consultation: consultation
            },
            visual_result: {},
            ai_text: ""
          };

          console.log('Sending result data:', resultData);
          console.log('Request data details:', {
            fortune_type: resultData.fortune_type,
            purpose: resultData.request_data.purpose,
            profiles_count: resultData.request_data.profiles.length,
            profiles: resultData.request_data.profiles.map(p => ({ id: p.profile_id, nickname: p.nickname })),
            consultation: consultation
          });
          
          console.log('About to call api.divination.create...');
          const result = await api.divination.create(resultData);
          console.log('Received result:', result);
          console.log('Result type:', typeof result);
          console.log('Result keys:', Object.keys(result));
          
          if (result.divination_result) {
            console.log('Setting divination result:', result.divination_result);
            console.log('Divination result keys:', Object.keys(result.divination_result));
            console.log('Fortune type:', result.divination_result.fortune_type);
            console.log('Tarot data present:', !!result.divination_result.tarot_data);
            setDivinationResult(result.divination_result);
          } else {
            console.log('No divination_result in response');
            console.log('Full result:', result);
          }
        } catch (error) {
          console.error('占い結果の取得に失敗しました:', error);
          console.error('Error details:', error);
          console.error('Error name:', error instanceof Error ? error.name : 'Unknown');
          console.error('Error message:', error instanceof Error ? error.message : 'Unknown');
          // エラー時はホーム画面に戻る
          setCurrentScreen('home-screen');
        } finally {
          console.log('Setting isLoading to false');
          setIsLoading(false);
        }
      }
    };

    if (currentScreen === 'result-screen' && fortuneType && selectedPeople.length > 0 && !hasFetchedRef.current) {
      fetchDivinationResult();
    }
  }, [currentScreen, fortuneType, selectedPeople, fortunePurpose, profiles]);

  if (currentScreen !== 'result-screen') return null;

  const handleShare = () => {
    if (tickets > 0) {
      setTickets(tickets - 1);
      alert('共有しました。(チケットを1枚消費しました)');
    } else {
      // Show ticket prompt modal
    }
  };

  const handleAskMore = () => {
    if (tickets > 0) {
      setTickets(tickets - 1);
      alert('追加質問しました。(チケットを1枚消費しました)');
    } else {
      // Show ticket prompt modal
    }
  };

  const handleBackToHome = () => {
    setCurrentScreen('home-screen');
    setSelectedPeople([]);
    setFortunePurpose(null);
    setFortuneType(null);
  };

  const renderVisualResult = () => {
    if (isLoading) {
      return (
        <div className="bg-black bg-opacity-20 p-6 rounded-lg text-center">
          <div className="text-6xl mb-4 animate-pulse">🔮</div>
          <div className="text-lg text-white mb-2">占い結果を生成中...</div>
          <div className="text-sm text-white opacity-75 mb-4">占いアルゴリズムの計算とAI分析を行っています</div>
          <div className="w-full rounded-full h-2">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full animate-pulse"></div>
          </div>
        </div>
      );
    }

    if (!divinationResult) {
      return (
        <div className="bg-black bg-opacity-20 p-6 rounded-lg text-center">
          <div className="text-6xl mb-4">❌</div>
          <div className="text-lg text-white">占い結果の取得に失敗しました</div>
        </div>
      );
    }

    switch (fortuneType) {
      case 'numerology':
        if (fortunePurpose === 'compatibility') {
          const compatibilityData = divinationResult.compatibility_data;
          return (
            <>
              <div className="mb-8">
                <h3 className="font-serif-special text-xl mb-6 text-purple-300 text-center">
                  あなたのナンバー
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
                  {[
                    { name: 'ライフパス', value: compatibilityData?.person1?.life_path?.number || '?' },
                    { name: 'ディスティニー', value: compatibilityData?.person1?.destiny?.number || '?' },
                    { name: 'ソウル', value: compatibilityData?.person1?.soul?.number || '?' },
                    { name: 'パーソナル', value: compatibilityData?.person1?.personal?.number || '?' },
                    { name: 'バースデー', value: compatibilityData?.person1?.birthday?.number || '?' },
                    { name: 'マチュリティー', value: compatibilityData?.person1?.maturity?.number || '?' }
                  ].map((item, index) => (
                    <div key={index} className="bg-black bg-opacity-20 p-4 rounded-lg">
                      <p className="text-sm text-gray-400">{item.name}</p>
                      <p className="font-serif-special text-3xl font-bold">{item.value}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="font-serif-special text-xl mb-6 text-pink-300 text-center">
                  相手のナンバー
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
                  {[
                    { name: 'ライフパス', value: compatibilityData?.person2?.life_path?.number || '?' },
                    { name: 'ディスティニー', value: compatibilityData?.person2?.destiny?.number || '?' },
                    { name: 'ソウル', value: compatibilityData?.person2?.soul?.number || '?' },
                    { name: 'パーソナル', value: compatibilityData?.person2?.personal?.number || '?' },
                    { name: 'バースデー', value: compatibilityData?.person2?.birthday?.number || '?' },
                    { name: 'マチュリティー', value: compatibilityData?.person2?.maturity?.number || '?' }
                  ].map((item, index) => (
                    <div key={index} className="bg-black bg-opacity-20 p-4 rounded-lg">
                      <p className="text-sm text-gray-400">{item.name}</p>
                      <p className="font-serif-special text-3xl font-bold">{item.value}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="mt-8 text-center">
                <h3 className="font-serif-special text-xl mb-4 text-yellow-300">相性スコア</h3>
                <div className="text-4xl font-bold text-white">
                  {compatibilityData?.compatibility_score || 0}/100
                </div>
              </div>
            </>
          );
        } else {
          const numerologyData = divinationResult.numerology_data;
          const temporalFortune = divinationResult.temporal_fortune;
          console.log('Numerology data for display:', numerologyData);
          console.log('Temporal fortune for display:', temporalFortune);
        return (
          <>
            <h3 className="font-serif-special text-xl mb-6 text-purple-300 text-center">
              あなたのナンバー
            </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-center mb-8">
                {[
                  { name: 'ライフパス', value: numerologyData?.life_path?.number || '?' },
                  { name: 'ディスティニー', value: numerologyData?.destiny?.number || '?' },
                  { name: 'ソウル', value: numerologyData?.soul?.number || '?' },
                  { name: 'パーソナル', value: numerologyData?.personal?.number || '?' },
                  { name: 'バースデー', value: numerologyData?.birthday?.number || '?' },
                  { name: 'マチュリティー', value: numerologyData?.maturity?.number || '?' }
                ].map((item, index) => (
                  <div key={index} className="bg-black bg-opacity-20 p-4 rounded-lg">
                    <p className="text-sm text-gray-400">{item.name}</p>
                    <p className="font-serif-special text-3xl font-bold">{item.value}</p>
                  </div>
                ))}
              </div>
              
              {/* 今日の運勢 */}
              {temporalFortune && (
                <div className="mt-8">
                  <h3 className="font-serif-special text-xl mb-6 text-yellow-300 text-center">
                    今日の運勢
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-lg">
                      <h4 className="text-lg font-bold text-white mb-2">パーソナルイヤー</h4>
                      <p className="text-4xl font-bold text-yellow-300 mb-2">
                        {temporalFortune.personal_year?.number || '?'}
                      </p>
                      <p className="text-sm text-purple-200">
                        {temporalFortune.personal_year?.description || '計算中...'}
                      </p>
                    </div>
                    <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-lg">
                      <h4 className="text-lg font-bold text-white mb-2">パーソナルマンス</h4>
                      <p className="text-4xl font-bold text-yellow-300 mb-2">
                        {temporalFortune.personal_month?.number || '?'}
                      </p>
                      <p className="text-sm text-blue-200">
                        {temporalFortune.personal_month?.description || '計算中...'}
                      </p>
                    </div>
                    <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-lg">
                      <h4 className="text-lg font-bold text-white mb-2">パーソナルデイ</h4>
                      <p className="text-4xl font-bold text-yellow-300 mb-2">
                        {temporalFortune.personal_day?.number || '?'}
                      </p>
                      <p className="text-sm text-green-200">
                        {temporalFortune.personal_day?.description || '計算中...'}
                      </p>
                    </div>
                  </div>
                </div>
              )}
          </>
        );
        }
      case 'horoscope':
        if (fortunePurpose === 'compatibility') {
          const compatibilityData = divinationResult.compatibility_data;
        return (
          <>
              {/* シナストリーチャートの表示 */}
              {compatibilityData?.synastry_chart && (
                <div className="mb-8 w-full">
                  <div className="bg-gray-800/50 rounded-lg p-4 w-full">
                    <h3 className="font-serif-special text-xl mb-4 text-purple-300 text-center">
                      シナストリーチャート
                    </h3>
                    <div className="w-full flex justify-center">
                      <div className="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 aspect-square">
                        {/* 円形のマスクコンテナ */}
                        <div className="absolute inset-0 rounded-full overflow-hidden shadow-2xl border-4 border-purple-300/30 bg-gradient-to-br from-purple-100/20 to-pink-100/20">
                          <img 
                            src={compatibilityData.synastry_chart} 
                            alt="シナストリーチャート"
                            className="absolute inset-0 object-contain object-center"
                            style={{ 
                              clipPath: 'circle(50% at 50% 50%)',
                              WebkitClipPath: 'circle(50% at 50% 50%)',
                              aspectRatio: '1 / 1'
                            }}
                          />
                        </div>
                        {/* 装飾的な枠線 */}
                        <div className="absolute inset-0 rounded-full border-2 border-purple-400/50 pointer-events-none"></div>
                        <div className="absolute inset-1 rounded-full border border-purple-200/30 pointer-events-none"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              

              {/* 相性スコア */}
              <div className="text-center">
                <h3 className="font-serif-special text-xl mb-4 text-yellow-300">相性スコア</h3>
                <div className="text-4xl font-bold text-white mb-2">
                  {compatibilityData?.compatibility_score || 0}/100
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-3 rounded-full transition-all duration-1000"
                    style={{ width: `${compatibilityData?.compatibility_score || 0}%` }}
                  ></div>
                </div>
              </div>
            </>
          );
        } else {
          const horoscopeData = divinationResult.horoscope_data;
          const isTransit = horoscopeData?.calculation_type === 'transit';
          return (
            <>
              <h3 className="font-serif-special text-xl mb-6 text-cyan-300 text-center">
                {isTransit ? `トランジット分析 - ${horoscopeData?.target_date}` : 'あなたのホロスコープ'}
              </h3>
              
              {/* ホイールチャートの表示 */}
              {horoscopeData?.wheel_chart && (
                <div className="mb-8 w-full">
                  <div className="bg-gray-800/50 rounded-lg p-4 w-full">
                    <h4 className="font-serif-special text-lg mb-4 text-yellow-300 text-center">
                      {isTransit ? 'トランジットチャート' : '出生図'}
                    </h4>
                    <div className="w-full flex justify-center">
                      <div className="relative w-64 h-64 md:w-80 md:h-80 lg:w-96 lg:h-96 aspect-square">
                        {/* 円形のマスクコンテナ */}
                        <div className="absolute inset-0 rounded-full overflow-hidden shadow-2xl border-4 border-yellow-300/30 bg-gradient-to-br from-yellow-100/20 to-amber-100/20">
                          <img 
                            src={horoscopeData.wheel_chart} 
                            alt={isTransit ? 'トランジットチャート' : '出生図'}
                            className="absolute inset-0 object-contain object-center"
                            style={{ 
                              clipPath: 'circle(50% at 50% 50%)',
                              WebkitClipPath: 'circle(50% at 50% 50%)',
                              aspectRatio: '1 / 1'
                            }}
                          />
                        </div>
                        {/* 装飾的な枠線 */}
                        <div className="absolute inset-0 rounded-full border-2 border-yellow-400/50 pointer-events-none"></div>
                        <div className="absolute inset-1 rounded-full border border-yellow-200/30 pointer-events-none"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* 惑星位置の詳細表示 */}
              <div className="bg-gray-800/50 rounded-lg p-4">
                <h4 className="font-serif-special text-lg mb-4 text-yellow-300 text-center">
                  {isTransit ? '出生時とトランジット惑星位置' : '惑星位置'}
                </h4>
                
                {isTransit ? (
                  // トランジット法の表示
                  <div className="space-y-6">
                    {/* 出生時の惑星位置 */}
                    <div>
                      <h5 className="text-md mb-3 text-cyan-300 text-center">出生時の惑星位置</h5>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                        {horoscopeData?.natal_planets && Object.entries(horoscopeData.natal_planets).map(([planet, data]: [string, any]) => (
                          <div key={planet} className="flex justify-between items-center bg-gray-700/30 rounded px-3 py-2">
                            <span className="text-gray-300 capitalize">{planet}</span>
                            <div className="text-right">
                              <div className="text-white font-medium">{getJapaneseSignName(data.sign_jp) || data.sign}</div>
                              <div className="text-gray-400 text-xs">{data.degree?.toFixed(1)}°</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    {/* トランジット惑星位置 */}
                    <div>
                      <h5 className="text-md mb-3 text-orange-300 text-center">トランジット惑星位置</h5>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                        {horoscopeData?.transit_planets && Object.entries(horoscopeData.transit_planets).map(([planet, data]: [string, any]) => (
                          <div key={planet} className="flex justify-between items-center bg-orange-900/30 rounded px-3 py-2">
                            <span className="text-gray-300 capitalize">{planet}</span>
                            <div className="text-right">
                              <div className="text-white font-medium">{getJapaneseSignName(data.sign_jp) || data.sign}</div>
                              <div className="text-gray-400 text-xs">{data.degree?.toFixed(1)}°</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    {/* アスペクト */}
                    {horoscopeData?.aspects && horoscopeData.aspects.length > 0 && (
                      <div>
                        <h5 className="text-md mb-3 text-purple-300 text-center">重要なアスペクト</h5>
                        <div className="space-y-2">
                          {horoscopeData.aspects.map((aspect: any, index: number) => (
                            <div key={index} className="bg-purple-900/30 rounded px-3 py-2 text-sm">
                              <div className="text-white font-medium">{aspect.description}</div>
                              <div className="text-gray-400 text-xs">角度: {aspect.angle?.toFixed(1)}° (許容範囲: {aspect.orb?.toFixed(1)}°)</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  // 通常のホロスコープ表示
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                    {horoscopeData?.planets && Object.entries(horoscopeData.planets).map(([planet, data]: [string, any]) => (
                      <div key={planet} className="flex justify-between items-center bg-gray-700/30 rounded px-3 py-2">
                        <span className="text-gray-300 capitalize">{planet}</span>
                        <div className="text-right">
                          <div className="text-white font-medium">{getJapaneseSignName(data.sign_jp) || data.sign}</div>
                          <div className="text-gray-400 text-xs">{data.degree?.toFixed(1)}°</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
          </>
        );
        }
      case 'tarot':
        if (fortunePurpose === 'compatibility') {
          const compatibilityData = divinationResult.compatibility_data;
        return (
          <>
            <h3 className="font-serif-special text-xl mb-6 text-yellow-300 text-center">
                タロット相性占い
            </h3>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                {compatibilityData?.drawn_cards?.map((card: any, index: number) => (
                  <div key={index} className="text-center">
                    <div className="relative mb-2">
                      <img
                        src={card.card_image_path || '/images/tarot/CardBacks.jpg'}
                        alt={card.card_name}
                        className={`w-24 h-36 object-cover rounded-lg shadow-lg ${
                          card.is_reversed ? 'transform rotate-180' : ''
                        }`}
                        onError={(e) => {
                          e.currentTarget.src = '/images/tarot/CardBacks.jpg';
                        }}
                      />
                      {card.is_reversed && (
                        <div className="absolute top-1 right-1 bg-red-500 text-white text-xs px-1 rounded">
                          逆
                        </div>
                      )}
                    </div>
                    <div className="text-sm font-bold text-white">{card.card_name}</div>
                    <div className="text-xs text-gray-300">{card.position_name}</div>
                  </div>
                ))}
              </div>
              <div className="text-center">
                <h3 className="font-serif-special text-xl mb-4 text-yellow-300">相性スコア</h3>
                <div className="text-4xl font-bold text-white mb-2">
                  {compatibilityData?.compatibility_score || 0}/100
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-3 rounded-full transition-all duration-1000"
                    style={{ width: `${compatibilityData?.compatibility_score || 0}%` }}
                  ></div>
                </div>
              </div>
            </>
          );
        } else {
          const tarotData = divinationResult.tarot_data;
          console.log('Rendering tarot result, tarotData:', tarotData);
          console.log('Tarot cards count:', tarotData?.drawn_cards?.length || 0);
          return (
            <>
              <h3 className="font-serif-special text-xl mb-6 text-yellow-300 text-center">
                {tarotData?.spread_name || 'タロット占い'}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {tarotData?.drawn_cards?.map((card: any, index: number) => (
                  <div key={index} className="text-center">
                    <div className="relative mb-3">
                      <img
                        src={card.card_image_path || '/images/tarot/CardBacks.jpg'}
                        alt={card.card_name}
                        className={`w-32 h-48 object-cover rounded-lg shadow-lg mx-auto ${
                          card.is_reversed ? 'transform rotate-180' : ''
                        }`}
                        onError={(e) => {
                          e.currentTarget.src = '/images/tarot/CardBacks.jpg';
                        }}
                      />
                      {card.is_reversed && (
                        <div className="absolute top-2 right-2 bg-red-500 text-white text-sm px-2 py-1 rounded">
                          逆位置
                        </div>
                      )}
                    </div>
                    <div className="text-lg font-bold text-white mb-1">{card.card_name}</div>
                    <div className="text-sm text-gray-300 mb-2">{card.position_name}</div>
                    <div className="text-xs text-gray-400 bg-gray-800 p-2 rounded">
                      {card.card_description}
                    </div>
                    {card.is_reversed && card.reversed_meaning && (
                      <div className="text-xs text-red-300 bg-red-900 bg-opacity-30 p-2 rounded mt-2">
                        逆位置: {card.reversed_meaning}
                      </div>
                    )}
                </div>
              ))}
            </div>
          </>
        );
        }
      default:
        return (
          <div className="text-center text-gray-400">
            複数の占術結果を統合しています...
          </div>
        );
    }
  };

  const getSignImagePath = (sign: string) => {
    const imagePaths: { [key: string]: string } = {
      // 完全な英語名
      'Aries': '/images/zodiac/aries.png',
      'Taurus': '/images/zodiac/taurus.png',
      'Gemini': '/images/zodiac/gemini.png',
      'Cancer': '/images/zodiac/cancer.png',
      'Leo': '/images/zodiac/leo.png',
      'Virgo': '/images/zodiac/virgo.png',
      'Libra': '/images/zodiac/libra.png',
      'Scorpio': '/images/zodiac/scorpio.png',
      'Sagittarius': '/images/zodiac/sagittarius.png',
      'Capricorn': '/images/zodiac/capricorn.png',
      'Aquarius': '/images/zodiac/aquarius.png',
      'Pisces': '/images/zodiac/pisces.png',
      // 短縮形（kerykeionライブラリの形式）
      'Ari': '/images/zodiac/aries.png',
      'Tau': '/images/zodiac/taurus.png',
      'Gem': '/images/zodiac/gemini.png',
      'Can': '/images/zodiac/cancer.png',
      'Vir': '/images/zodiac/virgo.png',
      'Lib': '/images/zodiac/libra.png',
      'Sco': '/images/zodiac/scorpio.png',
      'Sag': '/images/zodiac/sagittarius.png',
      'Cap': '/images/zodiac/capricorn.png',
      'Aqu': '/images/zodiac/aquarius.png',
      'Pis': '/images/zodiac/pisces.png'
    };
    return imagePaths[sign] || null;
  };

  const getJapaneseSignName = (signWithSymbol: string) => {
    // "♈ 牡羊座" から "牡羊座" を抽出
    if (!signWithSymbol) return '?';
    const parts = signWithSymbol.split(' ');
    return parts.length > 1 ? parts[1] : signWithSymbol;
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-2xl mx-auto">
        <div className="card p-6 md:p-8">
          <p className="text-xs text-center text-gray-500 mb-6">
            免責事項: 本占いはエンターテイメントを目的としたものであり、<br />
            その結果を保証するものではありません。
          </p>
          <h2 className="font-serif-special text-3xl text-center mb-6 border-b border-gray-700 pb-4">
            {fortuneType === 'numerology'
              ? fortunePurpose === 'compatibility' 
                ? '数秘術相性占いの結果'
                : '数秘術の鑑定結果'
              : fortuneType === 'horoscope'
              ? fortunePurpose === 'compatibility'
                ? 'ホロスコープ相性占いの結果'
                : '西洋占星術の鑑定結果'
              : fortuneType === 'tarot'
              ? 'タロット占いの結果'
              : '総合鑑定結果'}
          </h2>
          <div className="mb-8">{renderVisualResult()}</div>
          <h3 className="font-serif-special text-xl mb-4 text-purple-300">AIによる鑑定文</h3>
          <div className="text-gray-300 leading-relaxed space-y-4 bg-black bg-opacity-20 p-4 rounded-lg">
            {divinationResult?.ai_analysis ? (
              <div 
                className="prose prose-invert max-w-none whitespace-pre-wrap"
                dangerouslySetInnerHTML={{
                  __html: (() => {
                      let text = divinationResult.ai_analysis;
                      // 1. 全体のテキストに対して、先にインライン要素の**を<strong>に変換
                      text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                      // 2. テキストを空行（2つ以上の連続した改行）でブロックに分割
                      const blocks = text.split(/\n\s*\n/).filter(block => block.trim() !== '');
                      // 3. 各ブロックを段落かリストか判断して処理
                      const processedBlocks = blocks.map(block => {
                          const trimmedBlock = block.trim(); 
                          // リストブロック（行頭が'* 'で始まる）の場合
                          if (trimmedBlock.startsWith('* ')) {
                              const listItems = trimmedBlock.split('\n')
                                  .map(item => `<li>${item.replace(/^\* /, '').trim()}</li>`)
                                  .join('');
                              return `<ul>${listItems}</ul>`;
                          } 
                          // それ以外の文章ブロックは段落として処理
                          else {
                              // 段落内の改行は<br>に変換
                              const paragraphContent = trimmedBlock.replace(/\n/g, '<br>');
                              // <p>タグで囲み、CSSで字下げ（text-indent）を適用
                              return `<p style="text-indent: 1em;">${paragraphContent}</p>`;
                          }
                      });
                      // 4. 処理した全ブロックを結合して最終的なHTMLを生成
                      return processedBlocks.join('<br>');
                  })()
                }}
              />
            ) : (
              <p className="text-gray-400">鑑定文を生成中...</p>
            )}
          </div>
          <div className="mt-8 flex flex-col md:flex-row gap-4 justify-center">
            <button
              onClick={handleShare}
              className="bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center"
            >
              結果を共有する
            </button>
            <button
              onClick={handleAskMore}
              className="bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 px-6 rounded-full transition duration-300 flex items-center justify-center"
            >
              AIに追加質問する
            </button>
          </div>
          <div className="mt-8 text-center">
            <button
              onClick={handleBackToHome}
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-6 rounded-full transition duration-300"
            >
              ホームに戻る
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResultScreen;