import React from 'react';

// 星座シンボルのHTMLコンポーネント
export const ZodiacSymbols = {
  // 完全な英語名
  Aries: () => <span className="zodiac-symbol">♈</span>,
  Taurus: () => <span className="zodiac-symbol">♉</span>,
  Gemini: () => <span className="zodiac-symbol">♊</span>,
  Cancer: () => <span className="zodiac-symbol">♋</span>,
  Leo: () => <span className="zodiac-symbol">♌</span>,
  Virgo: () => <span className="zodiac-symbol">♍</span>,
  Libra: () => <span className="zodiac-symbol">♎</span>,
  Scorpio: () => <span className="zodiac-symbol">♏</span>,
  Sagittarius: () => <span className="zodiac-symbol">♐</span>,
  Capricorn: () => <span className="zodiac-symbol">♑</span>,
  Aquarius: () => <span className="zodiac-symbol">♒</span>,
  Pisces: () => <span className="zodiac-symbol">♓</span>,
  
  // 短縮形（kerykeionライブラリの形式）
  Ari: () => <span className="zodiac-symbol">♈</span>,
  Tau: () => <span className="zodiac-symbol">♉</span>,
  Gem: () => <span className="zodiac-symbol">♊</span>,
  Can: () => <span className="zodiac-symbol">♋</span>,
  Vir: () => <span className="zodiac-symbol">♍</span>,
  Lib: () => <span className="zodiac-symbol">♎</span>,
  Sco: () => <span className="zodiac-symbol">♏</span>,
  Sag: () => <span className="zodiac-symbol">♐</span>,
  Cap: () => <span className="zodiac-symbol">♑</span>,
  Aqu: () => <span className="zodiac-symbol">♒</span>,
  Pis: () => <span className="zodiac-symbol">♓</span>,
};

// 星座シンボルを取得するヘルパー関数
export const getZodiacSymbol = (sign: string): React.ReactElement => {
  const SymbolComponent = ZodiacSymbols[sign as keyof typeof ZodiacSymbols];
  return SymbolComponent ? <SymbolComponent /> : <span className="zodiac-symbol">?</span>;
};

// 星座シンボルの文字列版（従来の互換性のため）
export const getZodiacSymbolString = (sign: string): string => {
  const symbolMap: { [key: string]: string } = {
    // 完全な英語名
    'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
    'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
    'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓',
    // 短縮形（kerykeionライブラリの形式）
    'Ari': '♈', 'Tau': '♉', 'Gem': '♊', 'Can': '♋',
    'Vir': '♍', 'Lib': '♎', 'Sco': '♏',
    'Sag': '♐', 'Cap': '♑', 'Aqu': '♒', 'Pis': '♓'
  };
  return symbolMap[sign] || '?';
};

// 星座名からシンボルを除いた日本語名を取得
export const getJapaneseSignName = (signWithSymbol: string): string => {
  if (!signWithSymbol) return '?';
  const parts = signWithSymbol.split(' ');
  return parts.length > 1 ? parts[1] : signWithSymbol;
};

// 星座シンボルのCSSスタイル
export const zodiacSymbolStyles = `
  .zodiac-symbol {
    font-family: 'Times New Roman', serif;
    font-size: inherit;
    line-height: 1;
    display: inline-block;
  }
`;
