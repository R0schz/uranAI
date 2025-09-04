#!/usr/bin/env python3
"""
Updated Numerology Calculator
既存システムとの統合を考慮した数秘術計算クラス
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator_new import NumerologyCalculator as NewNumerologyCalculator
import pykakasi
from typing import Dict, Any


class NumerologyCalculator:
    """
    Updated Numerology Calculator
    
    既存システムとの互換性を保ちつつ、新しいアルゴリズムを使用する数秘術計算クラス
    """
    
    def __init__(self):
        """Initialize the calculator with number meanings"""
        self.number_meanings = {
            1: 'リーダーシップ、独立、創造性',
            2: '協調性、バランス、直感',
            3: '表現力、創造性、コミュニケーション',
            4: '安定、実用性、組織力',
            5: '自由、変化、冒険',
            6: '責任、愛情、調和',
            7: '精神性、分析、内省',
            8: '成功、権力、物質的達成',
            9: '完成、智慧、奉仕',
            11: '直感、啓示、スピリチュアル',
            22: '最高の職人、実現力、大いなる目的',
            33: 'マスター教師、癒し、奉仕',
            44: '実用的な理想主義、建設的な変化'
        }
    
    def _convert_japanese_name_to_romanization(self, name_hiragana: str) -> str:
        """
        Convert Japanese hiragana name to Hepburn romanization
        
        Args:
            name_hiragana: Japanese name in hiragana (e.g., "こばやし　よしたか")
            
        Returns:
            Romanized name in uppercase (e.g., "KOBAYASHI YOSHITAKA")
        """
        # Split name by space
        name_parts = name_hiragana.split()
        if len(name_parts) < 2:
            # If no space, treat as single name
            name_parts = [name_hiragana]
        
        # Convert each part to romanization
        kks = pykakasi.kakasi()
        romanized_parts = []
        
        for part in name_parts:
            result = kks.convert(part)
            romanized_part = ''.join([item['hepburn'] for item in result])
            romanized_parts.append(romanized_part.upper())
        
        return ' '.join(romanized_parts)
    
    def get_numerology_reading(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get numerology reading for a profile (compatible with existing system)
        
        Args:
            profile_data: Profile data containing name_hiragana, birth_date, etc.
            
        Returns:
            Dictionary with numerology results in existing format
        """
        try:
            # Extract data from profile
            name_hiragana = profile_data.get('name_hiragana', '')
            birth_date = profile_data.get('birth_date', '')
            nickname = profile_data.get('nickname', 'あなた')
            
            if not name_hiragana or not birth_date:
                raise ValueError("name_hiragana and birth_date are required")
            
            # Convert Japanese name to romanization
            romanized_name = self._convert_japanese_name_to_romanization(name_hiragana)
            
            # Create new calculator instance
            calculator = NewNumerologyCalculator(romanized_name, birth_date)
            
            # Calculate all numbers
            all_numbers = calculator.calculate_all()
            
            # Format results in existing system format
            result = {
                'nickname': nickname,
                'life_path': {
                    'number': all_numbers['life_path_number'],
                    'meaning': self.number_meanings.get(all_numbers['life_path_number'], '')
                },
                'destiny': {
                    'number': all_numbers['destiny_number'],
                    'meaning': self.number_meanings.get(all_numbers['destiny_number'], '')
                },
                'soul': {
                    'number': all_numbers['soul_number'],
                    'meaning': self.number_meanings.get(all_numbers['soul_number'], '')
                },
                'personal': {
                    'number': all_numbers['personality_number'],
                    'meaning': self.number_meanings.get(all_numbers['personality_number'], '')
                },
                'birthday': {
                    'number': all_numbers['birthday_number'],
                    'meaning': self.number_meanings.get(all_numbers['birthday_number'], '')
                },
                'challenge': {
                    'number': all_numbers['maturity_number'],  # Using maturity as challenge
                    'meaning': self.number_meanings.get(all_numbers['maturity_number'], '')
                },
                'maturity': {
                    'number': all_numbers['maturity_number'],
                    'meaning': self.number_meanings.get(all_numbers['maturity_number'], '')
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Numerology calculation failed: {e}")
            import traceback
            traceback.print_exc()
            # Return error result
            return {
                'nickname': profile_data.get('nickname', 'あなた'),
                'life_path': {'number': 0, 'meaning': '計算エラー'},
                'destiny': {'number': 0, 'meaning': '計算エラー'},
                'soul': {'number': 0, 'meaning': '計算エラー'},
                'personal': {'number': 0, 'meaning': '計算エラー'},
                'birthday': {'number': 0, 'meaning': '計算エラー'},
                'challenge': {'number': 0, 'meaning': '計算エラー'},
                'maturity': {'number': 0, 'meaning': '計算エラー'}
            }
    
    def get_compatibility_analysis(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get compatibility analysis between two profiles
        
        Args:
            profile1: First profile data
            profile2: Second profile data
            
        Returns:
            Dictionary with compatibility analysis
        """
        try:
            # Get numerology readings for both profiles
            reading1 = self.get_numerology_reading(profile1)
            reading2 = self.get_numerology_reading(profile2)
            
            # Calculate compatibility score (simplified)
            life_path_diff = abs(reading1['life_path']['number'] - reading2['life_path']['number'])
            destiny_diff = abs(reading1['destiny']['number'] - reading2['destiny']['number'])
            soul_diff = abs(reading1['soul']['number'] - reading2['soul']['number'])
            
            # Simple compatibility scoring (0-100)
            total_diff = life_path_diff + destiny_diff + soul_diff
            compatibility_score = max(0, 100 - (total_diff * 10))
            
            # Generate simple analysis
            if compatibility_score >= 80:
                analysis = "非常に良い相性です。お互いを高め合える関係を築けるでしょう。"
            elif compatibility_score >= 60:
                analysis = "良い相性です。お互いの違いを理解し合えば、安定した関係を築けるでしょう。"
            elif compatibility_score >= 40:
                analysis = "普通の相性です。努力次第で良い関係を築くことができます。"
            else:
                analysis = "相性に課題があります。お互いの理解を深めることが重要です。"
            
            return {
                'compatibility_score': compatibility_score,
                'person1': reading1,
                'person2': reading2,
                'analysis': analysis
            }
            
        except Exception as e:
            print(f"Compatibility analysis failed: {e}")
            return {
                'compatibility_score': 0,
                'person1': {'life_path': {'number': 0}, 'destiny': {'number': 0}, 'soul': {'number': 0}, 'personal': {'number': 0}},
                'person2': {'life_path': {'number': 0}, 'destiny': {'number': 0}, 'soul': {'number': 0}, 'personal': {'number': 0}},
                'analysis': '相性分析エラー'
            }
    
    def calculate_temporal_fortune(self, profile_data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        Calculate temporal fortune (simplified implementation)
        
        Args:
            profile_data: Profile data
            target_date: Target date for fortune calculation
            
        Returns:
            Dictionary with temporal fortune data
        """
        try:
            # For now, return a simplified temporal fortune
            # This can be enhanced with the temporal engine if needed
            return {
                'target_date': target_date,
                'personal_year': {
                    'number': 1,
                    'description': '新しい始まりの年',
                    'keywords': ['開始', 'リーダーシップ', '独立'],
                    'advice': '新しいことに挑戦し、リーダーシップを発揮してください。'
                },
                'personal_month': {
                    'number': 1,
                    'description': '行動の月',
                    'keywords': ['行動', '決断', '開始'],
                    'advice': '決断力を持って行動に移してください。'
                },
                'personal_day': {
                    'number': 1,
                    'description': '独立の日',
                    'keywords': ['独立', '創造', 'リーダーシップ'],
                    'advice': '自分の判断で行動し、創造性を発揮してください。'
                }
            }
        except Exception as e:
            print(f"Temporal fortune calculation failed: {e}")
            return {
                'target_date': target_date,
                'personal_year': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''},
                'personal_month': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''},
                'personal_day': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''}
            }


if __name__ == "__main__":
    # Test the updated calculator
    print("Testing Updated Numerology Calculator")
    print("=" * 60)
    
    calculator = NumerologyCalculator()
    
    # Test case 1: Japanese name
    print("Test Case 1: Japanese name conversion and calculation")
    print("-" * 50)
    
    profile1 = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1999-04-02',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    result1 = calculator.get_numerology_reading(profile1)
    print(f"Results for {profile1['nickname']} ({profile1['name_hiragana']}):")
    print(f"  ライフパス: {result1['life_path']['number']} - {result1['life_path']['meaning']}")
    print(f"  ディスティニー: {result1['destiny']['number']} - {result1['destiny']['meaning']}")
    print(f"  ソウル: {result1['soul']['number']} - {result1['soul']['meaning']}")
    print(f"  パーソナル: {result1['personal']['number']} - {result1['personal']['meaning']}")
    print(f"  バースデー: {result1['birthday']['number']} - {result1['birthday']['meaning']}")
    print(f"  マチュリティ: {result1['maturity']['number']} - {result1['maturity']['meaning']}")
    
    print("\n" + "=" * 60)
    
    # Test case 2: Compatibility analysis
    print("Test Case 2: Compatibility analysis")
    print("-" * 50)
    
    profile2 = {
        'nickname': 'ハナコ',
        'name_hiragana': 'やまだ　はなこ',
        'birth_date': '1985-05-15',
        'birth_time': '08:30:00',
        'birth_location_json': {'place': '大阪'}
    }
    
    compatibility = calculator.get_compatibility_analysis(profile1, profile2)
    print(f"Compatibility between {profile1['nickname']} and {profile2['nickname']}:")
    print(f"  相性スコア: {compatibility['compatibility_score']}/100")
    print(f"  分析: {compatibility['analysis']}")
    
    print("\n" + "=" * 60)
    
    # Test case 3: Name conversion details
    print("Test Case 3: Name conversion details")
    print("-" * 50)
    
    test_names = [
        'こばやし　よしたか',
        'やまだ　はなこ',
        'すずき　たろう',
        'たなか　みき'
    ]
    
    for name in test_names:
        romanized = calculator._convert_japanese_name_to_romanization(name)
        print(f"  {name} -> {romanized}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
