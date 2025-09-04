#!/usr/bin/env python3
"""
数秘術の包括的テストスクリプト
名前変換と数秘術計算の両方を詳細にテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from numerology import Pythagorean
import pykakasi
from datetime import date

def test_numerology_calculation_detailed():
    """数秘術計算の詳細テスト"""
    
    print("数秘術計算の詳細テスト")
    print("=" * 60)
    
    # テストケース1: こばやし　よしたか
    test_cases = [
        {
            'name': 'こばやし　よしたか',
            'birth_date': '1990-01-01',
            'birth_time': '12:00:00',
            'nickname': 'コバトン'
        },
        {
            'name': 'やまだ　はなこ',
            'birth_date': '1985-05-15',
            'birth_time': '08:30:00',
            'nickname': 'ハナコ'
        },
        {
            'name': 'すずき　たろう',
            'birth_date': '1992-12-25',
            'birth_time': '15:45:00',
            'nickname': 'タロウ'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nテストケース {i}: {test_case['name']}")
        print("-" * 40)
        
        # 1. 名前の分離と変換
        name_parts = test_case['name'].split()
        if len(name_parts) >= 2:
            last_name = name_parts[0]
            first_name = name_parts[1]
            
            kks = pykakasi.kakasi()
            last_name_result = kks.convert(last_name)
            first_name_result = kks.convert(first_name)
            
            last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
            first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
            
            print(f"名前分離:")
            print(f"  元の名前: {test_case['name']}")
            print(f"  名字: {last_name} → {last_name_romaji}")
            print(f"  名前: {first_name} → {first_name_romaji}")
            
            # 2. numerologyライブラリでの直接計算
            print(f"\nnumerologyライブラリでの直接計算:")
            try:
                pythagorean = Pythagorean(
                    first_name=first_name_romaji,
                    last_name=last_name_romaji,
                    birthdate=test_case['birth_date']
                )
                
                print(f"  ライフパスナンバー: {pythagorean.life_path_number}")
                print(f"  ディスティニーナンバー: {pythagorean.destiny_number}")
                print(f"  パーソナリティナンバー: {pythagorean.personality_number}")
                print(f"  ハートデザイアナンバー: {pythagorean.hearth_desire_number}")
                print(f"  アクティブナンバー: {pythagorean.active_number}")
                print(f"  レガシーナンバー: {pythagorean.legacy_number}")
                print(f"  パワーナンバー: {pythagorean.power_number}")
                
            except Exception as e:
                print(f"  エラー: {e}")
            
            # 3. NumerologyCalculatorでの計算
            print(f"\nNumerologyCalculatorでの計算:")
            try:
                calculator = NumerologyCalculator()
                
                profile_data = {
                    'nickname': test_case['nickname'],
                    'name_hiragana': test_case['name'],
                    'birth_date': test_case['birth_date'],
                    'birth_time': test_case['birth_time'],
                    'birth_location_json': {'place': '東京'}
                }
                
                result = calculator.get_numerology_reading(profile_data)
                
                print(f"  ニックネーム: {result['nickname']}")
                print(f"  ライフパス: {result['life_path']['number']} - {result['life_path']['meaning']}")
                print(f"  ディスティニー: {result['destiny']['number']} - {result['destiny']['meaning']}")
                print(f"  ソウル: {result['soul']['number']} - {result['soul']['meaning']}")
                print(f"  パーソナル: {result['personal']['number']} - {result['personal']['meaning']}")
                print(f"  バースデー: {result['birthday']['number']} - {result['birthday']['meaning']}")
                print(f"  チャレンジ: {result['challenge']['number']} - {result['challenge']['meaning']}")
                print(f"  マチュリティ: {result['maturity']['number']} - {result['maturity']['meaning']}")
                
            except Exception as e:
                print(f"  エラー: {e}")
                import traceback
                traceback.print_exc()
            
            # 4. 計算結果の比較
            print(f"\n計算結果の比較:")
            try:
                # 直接計算とCalculatorの結果を比較
                direct_life_path = pythagorean.life_path_number
                calc_life_path = result['life_path']['number']
                
                direct_destiny = pythagorean.destiny_number
                calc_destiny = result['destiny']['number']
                
                direct_personal = pythagorean.personality_number
                calc_personal = result['personal']['number']
                
                print(f"  ライフパス: 直接={direct_life_path}, Calculator={calc_life_path}, 一致={direct_life_path == calc_life_path}")
                print(f"  ディスティニー: 直接={direct_destiny}, Calculator={calc_destiny}, 一致={direct_destiny == calc_destiny}")
                print(f"  パーソナル: 直接={direct_personal}, Calculator={calc_personal}, 一致={direct_personal == calc_personal}")
                
            except Exception as e:
                print(f"  比較エラー: {e}")

def test_temporal_fortune_calculation():
    """時間軸運勢計算のテスト"""
    
    print("\n" + "=" * 60)
    print("時間軸運勢計算のテスト")
    print("=" * 60)
    
    test_profile = {
        'nickname': 'テストユーザー',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1990-01-01',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    calculator = NumerologyCalculator()
    
    # 今日の日付でテスト
    today = date.today().isoformat()
    print(f"テスト日付: {today}")
    
    try:
        temporal_result = calculator.calculate_temporal_fortune(test_profile, today)
        
        print(f"\n時間軸運勢計算結果:")
        print(f"  対象日: {temporal_result['target_date']}")
        print(f"  パーソナルイヤー: {temporal_result['personal_year']['number']} - {temporal_result['personal_year']['description']}")
        print(f"  パーソナルマンス: {temporal_result['personal_month']['number']} - {temporal_result['personal_month']['description']}")
        print(f"  パーソナルデイ: {temporal_result['personal_day']['number']} - {temporal_result['personal_day']['description']}")
        
        print(f"\nキーワード:")
        print(f"  年: {temporal_result['personal_year']['keywords']}")
        print(f"  月: {temporal_result['personal_month']['keywords']}")
        print(f"  日: {temporal_result['personal_day']['keywords']}")
        
        print(f"\nアドバイス:")
        print(f"  年: {temporal_result['personal_year']['advice']}")
        print(f"  月: {temporal_result['personal_month']['advice']}")
        print(f"  日: {temporal_result['personal_day']['advice']}")
        
    except Exception as e:
        print(f"時間軸運勢計算エラー: {e}")
        import traceback
        traceback.print_exc()

def test_compatibility_calculation():
    """相性計算のテスト"""
    
    print("\n" + "=" * 60)
    print("相性計算のテスト")
    print("=" * 60)
    
    profile1 = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1990-01-01',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    profile2 = {
        'nickname': 'ハナコ',
        'name_hiragana': 'やまだ　はなこ',
        'birth_date': '1985-05-15',
        'birth_time': '08:30:00',
        'birth_location_json': {'place': '大阪'}
    }
    
    calculator = NumerologyCalculator()
    
    try:
        compatibility_result = calculator.get_compatibility_analysis(profile1, profile2)
        
        print(f"相性計算結果:")
        print(f"  相性スコア: {compatibility_result['compatibility_score']}/100")
        
        print(f"\n人物1 (コバトン):")
        print(f"  ライフパス: {compatibility_result['person1']['life_path']['number']}")
        print(f"  ディスティニー: {compatibility_result['person1']['destiny']['number']}")
        print(f"  ソウル: {compatibility_result['person1']['soul']['number']}")
        print(f"  パーソナル: {compatibility_result['person1']['personal']['number']}")
        
        print(f"\n人物2 (ハナコ):")
        print(f"  ライフパス: {compatibility_result['person2']['life_path']['number']}")
        print(f"  ディスティニー: {compatibility_result['person2']['destiny']['number']}")
        print(f"  ソウル: {compatibility_result['person2']['soul']['number']}")
        print(f"  パーソナル: {compatibility_result['person2']['personal']['number']}")
        
        print(f"\n相性分析:")
        print(f"  {compatibility_result['analysis']}")
        
    except Exception as e:
        print(f"相性計算エラー: {e}")
        import traceback
        traceback.print_exc()

def test_edge_cases():
    """エッジケースのテスト"""
    
    print("\n" + "=" * 60)
    print("エッジケースのテスト")
    print("=" * 60)
    
    edge_cases = [
        {
            'name': 'たなか　みき',  # 短い名前
            'birth_date': '2000-03-03',
            'nickname': 'ミキ'
        },
        {
            'name': 'さとう　じろう',  # 長い名字
            'birth_date': '1975-07-07',
            'nickname': 'ジロー'
        },
        {
            'name': 'あい　うえお',  # 母音のみ
            'birth_date': '1988-08-08',
            'nickname': 'アイ'
        }
    ]
    
    calculator = NumerologyCalculator()
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"\nエッジケース {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            profile_data = {
                'nickname': test_case['nickname'],
                'name_hiragana': test_case['name'],
                'birth_date': test_case['birth_date'],
                'birth_time': '12:00:00',
                'birth_location_json': {'place': '東京'}
            }
            
            result = calculator.get_numerology_reading(profile_data)
            
            print(f"  ライフパス: {result['life_path']['number']}")
            print(f"  ディスティニー: {result['destiny']['number']}")
            print(f"  ソウル: {result['soul']['number']}")
            print(f"  パーソナル: {result['personal']['number']}")
            
        except Exception as e:
            print(f"  エラー: {e}")

def test_number_meanings():
    """数秘術ナンバーの意味のテスト"""
    
    print("\n" + "=" * 60)
    print("数秘術ナンバーの意味のテスト")
    print("=" * 60)
    
    calculator = NumerologyCalculator()
    
    # 1-9の数秘術ナンバーの意味をテスト
    for number in range(1, 10):
        meaning = calculator.number_meanings.get(number, '意味なし')
        print(f"  ナンバー {number}: {meaning}")

if __name__ == "__main__":
    print("数秘術包括的テスト開始")
    print("=" * 60)
    
    test_numerology_calculation_detailed()
    test_temporal_fortune_calculation()
    test_compatibility_calculation()
    test_edge_cases()
    test_number_meanings()
    
    print("\n" + "=" * 60)
    print("数秘術包括的テスト完了")
