"""
数秘術アルゴリズム
外部設計書に基づく数秘術計算機能
numerology Pythonライブラリを使用
"""

from typing import Dict, Any, List
from datetime import datetime, date
import pykakasi
from numerology_temporal_engine import NumerologyTemporalEngine

class NumerologyCalculator:
    """数秘術計算クラス（numerologyライブラリ使用）"""
    
    def __init__(self):
        # 日本語をローマ字に変換するためのkakasiインスタンス
        self.kakasi = pykakasi.kakasi()
        self.kakasi.setMode('J', 'a')  # ひらがなをローマ字に
        self.kakasi.setMode('K', 'a')  # カタカナをローマ字に
        self.kakasi.setMode('H', 'a')  # 漢字をローマ字に
        self.converter = self.kakasi.getConverter()
        
        # 時間軸エンジンを初期化
        self.temporal_engine = NumerologyTemporalEngine()
        
        self.number_meanings = {
            1: "リーダーシップ、独立、創造性",
            2: "協調性、バランス、直感",
            3: "表現力、創造性、コミュニケーション",
            4: "安定、実用性、組織力",
            5: "自由、変化、冒険",
            6: "責任、愛情、調和",
            7: "精神性、分析、内省",
            8: "成功、権力、物質的達成",
            9: "完成、智慧、奉仕",
            11: "直感、啓示、スピリチュアル",
            22: "最高の職人、実現力、大いなる目的",
            33: "最高の教師、癒し、奉仕"
        }
    
    def _convert_japanese_to_english(self, japanese_name: str) -> str:
        """日本語名を英語（ローマ字）に変換"""
        try:
            # 日本語をローマ字に変換
            romaji = self.converter.do(japanese_name)
            # スペースを除去して小文字に変換
            english_name = romaji.replace(' ', '').lower()
            return english_name
        except Exception as e:
            print(f"Japanese to English conversion failed: {e}")
            # 変換に失敗した場合は元の名前をそのまま使用
            return japanese_name.lower()
    
    def get_numerology_reading(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """数秘術の総合的な読み取りを生成（numerologyライブラリ使用）"""
        try:
            # 日本語名を英語に変換
            japanese_name = profile_data.get('name_hiragana', '')
            english_name = self._convert_japanese_to_english(japanese_name)
            
            # numerologyライブラリを使用
            from numerology import Pythagorean
            
            # 生年月日をパース
            birth_date = profile_data.get('birth_date', '1990-01-01')
            birth_datetime = datetime.strptime(birth_date, '%Y-%m-%d')
            
            # Pythagorean数秘術計算
            # 日本語名（ひらがな）をスペースで分割
            japanese_parts = japanese_name.split()
            if len(japanese_parts) >= 2:
                # 前半部（名字）をLast name、後半部（名前）をFirst nameに
                last_name_jp = japanese_parts[0]  # 名字
                first_name_jp = ' '.join(japanese_parts[1:])  # 名前
                
                # それぞれを英語に変換
                last_name = self._convert_japanese_to_english(last_name_jp)
                first_name = self._convert_japanese_to_english(first_name_jp)
            else:
                # スペースで分割できない場合は全体をFirst nameとして使用
                first_name = english_name
                last_name = ''
            
            # 詳細出力を抑制
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                numerology = Pythagorean(
                    first_name=first_name,
                    last_name=last_name,
                    birthdate=birth_date,
                    verbose=False
                )
            finally:
                # 標準出力を復元
                sys.stdout = old_stdout
            
            return {
                'nickname': profile_data.get('nickname', 'あなた'),
                'life_path': {
                    'number': numerology.life_path_number,
                    'meaning': self.number_meanings.get(numerology.life_path_number, '')
                },
                'destiny': {
                    'number': numerology.destiny_number,
                    'meaning': self.number_meanings.get(numerology.destiny_number, '')
                },
                'soul': {
                    'number': numerology.hearth_desire_number,
                    'meaning': self.number_meanings.get(numerology.hearth_desire_number, '')
                },
                'personal': {
                    'number': numerology.personality_number,
                    'meaning': self.number_meanings.get(numerology.personality_number, '')
                },
                'birthday': {
                    'number': numerology.birthdate_day_num,
                    'meaning': self.number_meanings.get(numerology.birthdate_day_num, '')
                },
                'challenge': {
                    'number': numerology.power_number,
                    'meaning': self.number_meanings.get(numerology.power_number, '')
                },
                'maturity': {
                    'number': numerology.legacy_number,
                    'meaning': self.number_meanings.get(numerology.legacy_number, '')
                }
            }
            
        except Exception as e:
            print(f"Numerology library calculation failed: {e}")
            import traceback
            traceback.print_exc()
            # エラー時は空の結果を返す
            return {
                    'life_path': {'number': 0, 'meaning': '計算エラー'},
                    'destiny': {'number': 0, 'meaning': '計算エラー'},
                    'soul': {'number': 0, 'meaning': '計算エラー'},
                    'personal': {'number': 0, 'meaning': '計算エラー'},
                    'birthday': {'number': 0, 'meaning': '計算エラー'},
                    'challenge': {'number': 0, 'meaning': '計算エラー'},
                    'maturity': {'number': 0, 'meaning': '計算エラー'}
                }
    
    def calculate_temporal_fortune(self, profile_data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        特定時点の運勢を計算
        
        Args:
            profile_data: プロフィールデータ
            target_date: 占いたい日付 (YYYY-MM-DD形式)
            
        Returns:
            時間軸運勢の辞書
        """
        try:
            # 日付を変換
            target_date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
            
            # 時間軸エンジンを使用して計算
            temporal_result = self.temporal_engine.calculate_temporal_numbers(profile_data, target_date_obj)
            
            return {
                'target_date': target_date,
                'personal_year': {
                    'number': temporal_result['personal_year'],
                    'meaning': temporal_result['interpretations']['year']['description'],
                    'keywords': temporal_result['interpretations']['year']['keywords'],
                    'advice': temporal_result['interpretations']['year']['advice']
                },
                'personal_month': {
                    'number': temporal_result['personal_month'],
                    'meaning': temporal_result['interpretations']['month']['description'],
                    'keywords': temporal_result['interpretations']['month']['keywords'],
                    'advice': temporal_result['interpretations']['month']['advice']
                },
                'personal_day': {
                    'number': temporal_result['personal_day'],
                    'meaning': temporal_result['interpretations']['day']['description'],
                    'keywords': temporal_result['interpretations']['day']['keywords'],
                    'advice': temporal_result['interpretations']['day']['advice']
                }
            }
        except Exception as e:
            print(f"時間軸運勢計算エラー: {e}")
            import traceback
            traceback.print_exc()
            return {
                'target_date': target_date,
                'personal_year': {'number': 0, 'meaning': '計算エラー', 'keywords': [], 'advice': 'エラーが発生しました'},
                'personal_month': {'number': 0, 'meaning': '計算エラー', 'keywords': [], 'advice': 'エラーが発生しました'},
                'personal_day': {'number': 0, 'meaning': '計算エラー', 'keywords': [], 'advice': 'エラーが発生しました'}
            }
    
    def get_compatibility_analysis(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any]) -> Dict[str, Any]:
        """相性分析を生成"""
        try:
            print(f"Starting compatibility analysis for profiles:")
            print(f"Profile 1: {profile1_data}")
            print(f"Profile 2: {profile2_data}")
            
            reading1 = self.get_numerology_reading(profile1_data)
            print(f"Reading 1 generated: {reading1}")
            
            reading2 = self.get_numerology_reading(profile2_data)
            print(f"Reading 2 generated: {reading2}")
            
            # 相性スコアを計算（ライフパスナンバーの差が小さいほど相性が良い）
            life_path_diff = abs(reading1['life_path']['number'] - reading2['life_path']['number'])
            compatibility_score = max(0, 100 - (life_path_diff * 10))
            
            return {
                'person1': reading1,
                'person2': reading2,
                'person1_nickname': profile1_data.get('nickname', '人物1'),
                'person2_nickname': profile2_data.get('nickname', '人物2'),
                'compatibility_score': compatibility_score,
                'analysis': self._generate_compatibility_text(reading1, reading2, compatibility_score)
            }
            
        except Exception as e:
            print(f"Compatibility analysis error: {e}")
            return {
                'person1': {'life_path': {'number': 0, 'meaning': 'エラー'}},
                'person2': {'life_path': {'number': 0, 'meaning': 'エラー'}},
                'compatibility_score': 0,
                'analysis': '相性分析でエラーが発生しました'
            }
    
    def _generate_compatibility_text(self, reading1: Dict, reading2: Dict, score: int) -> str:
        """相性分析のテキストを生成"""
        if score >= 80:
            return "非常に相性の良い組み合わせです。お互いを高め合い、素晴らしい関係を築けるでしょう。"
        elif score >= 60:
            return "良い相性です。お互いの違いを理解し合えば、安定した関係を築けるでしょう。"
        elif score >= 40:
            return "中程度の相性です。お互いの努力次第で良い関係を築ける可能性があります。"
        else:
            return "相性に課題がありますが、お互いの理解を深めることで改善できるでしょう。"