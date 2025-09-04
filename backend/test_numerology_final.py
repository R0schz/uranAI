#!/usr/bin/env python3
"""
数秘術の最終テストスクリプト
名前変換と数秘術計算の完全な検証
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from numerology import Pythagorean
import pykakasi
from datetime import date

def test_complete_numerology_flow():
    """数秘術の完全なフローテスト"""
    
    print("数秘術の完全なフローテスト")
    print("=" * 60)
    
    # メインテストケース: こばやし　よしたか
    test_name = "こばやし　よしたか"
    birth_date = "1999-04-02"
    birth_time = "12:00:00"
    nickname = "コバトン"
    
    print(f"テスト対象:")
    print(f"  名前: {test_name}")
    print(f"  生年月日: {birth_date}")
    print(f"  生時: {birth_time}")
    print(f"  ニックネーム: {nickname}")
    print()
    
    # 1. 名前の分離と変換
    print("1. 名前の分離と変換:")
    name_parts = test_name.split()
    last_name = name_parts[0]
    first_name = name_parts[1]
    
    kks = pykakasi.kakasi()
    last_name_result = kks.convert(last_name)
    first_name_result = kks.convert(first_name)
    
    last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
    first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
    
    print(f"  元の名前: {test_name}")
    print(f"  分離後: 名字='{last_name}', 名前='{first_name}'")
    print(f"  ローマ字変換: 名字='{last_name_romaji}', 名前='{first_name_romaji}'")
    print()
    
    # 2. numerologyライブラリでの直接計算
    print("2. numerologyライブラリでの直接計算:")
    try:
        pythagorean = Pythagorean(
            first_name=first_name_romaji,
            last_name=last_name_romaji,
            birthdate=birth_date
        )
        
        print(f"  ライフパスナンバー: {pythagorean.life_path_number}")
        print(f"  ディスティニーナンバー: {pythagorean.destiny_number}")
        print(f"  パーソナリティナンバー: {pythagorean.personality_number}")
        print(f"  ハートデザイアナンバー: {pythagorean.hearth_desire_number}")
        print(f"  アクティブナンバー: {pythagorean.active_number}")
        print(f"  レガシーナンバー: {pythagorean.legacy_number}")
        print(f"  パワーナンバー: {pythagorean.power_number}")
        print()
        
    except Exception as e:
        print(f"  エラー: {e}")
        return
    
    # 3. NumerologyCalculatorでの計算
    print("3. NumerologyCalculatorでの計算:")
    try:
        calculator = NumerologyCalculator()
        
        profile_data = {
            'nickname': nickname,
            'name_hiragana': test_name,
            'birth_date': birth_date,
            'birth_time': birth_time,
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
        print()
        
    except Exception as e:
        print(f"  エラー: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 計算結果の比較
    print("4. 計算結果の比較:")
    print(f"  ライフパス: 直接={pythagorean.life_path_number}, Calculator={result['life_path']['number']}, 一致={pythagorean.life_path_number == result['life_path']['number']}")
    print(f"  ディスティニー: 直接={pythagorean.destiny_number}, Calculator={result['destiny']['number']}, 一致={pythagorean.destiny_number == result['destiny']['number']}")
    print(f"  パーソナル: 直接={pythagorean.personality_number}, Calculator={result['personal']['number']}, 一致={pythagorean.personality_number == result['personal']['number']}")
    print(f"  ソウル: 直接={pythagorean.hearth_desire_number}, Calculator={result['soul']['number']}, 一致={pythagorean.hearth_desire_number == result['soul']['number']}")
    print(f"  バースデー: 直接={pythagorean.active_number}, Calculator={result['birthday']['number']}, 一致={pythagorean.active_number == result['birthday']['number']}")
    print(f"  マチュリティ: 直接={pythagorean.legacy_number}, Calculator={result['maturity']['number']}, 一致={pythagorean.legacy_number == result['maturity']['number']}")
    print()
    
    # 5. 時間軸運勢計算
    print("5. 時間軸運勢計算:")
    try:
        today = date.today().isoformat()
        temporal_result = calculator.calculate_temporal_fortune(profile_data, today)
        
        print(f"  対象日: {temporal_result['target_date']}")
        print(f"  パーソナルイヤー: {temporal_result['personal_year']['number']}")
        print(f"  パーソナルマンス: {temporal_result['personal_month']['number']}")
        print(f"  パーソナルデイ: {temporal_result['personal_day']['number']}")
        print()
        
    except Exception as e:
        print(f"  時間軸運勢計算エラー: {e}")
        print()
    
    # 6. 相性計算テスト
    print("6. 相性計算テスト:")
    try:
        profile2 = {
            'nickname': 'ハナコ',
            'name_hiragana': 'やまだ　はなこ',
            'birth_date': '1985-05-15',
            'birth_time': '08:30:00',
            'birth_location_json': {'place': '大阪'}
        }
        
        compatibility_result = calculator.get_compatibility_analysis(profile_data, profile2)
        
        print(f"  相性スコア: {compatibility_result['compatibility_score']}/100")
        print(f"  人物1 (コバトン): LP={compatibility_result['person1']['life_path']['number']}, D={compatibility_result['person1']['destiny']['number']}")
        print(f"  人物2 (ハナコ): LP={compatibility_result['person2']['life_path']['number']}, D={compatibility_result['person2']['destiny']['number']}")
        print(f"  相性分析: {compatibility_result['analysis']}")
        print()
        
    except Exception as e:
        print(f"  相性計算エラー: {e}")
        print()

def test_multiple_names():
    """複数の名前でのテスト"""
    
    print("複数の名前でのテスト")
    print("=" * 60)
    
    test_cases = [
        {
            'name': 'やまだ　はなこ',
            'birth_date': '1985-05-15',
            'nickname': 'ハナコ'
        },
        {
            'name': 'すずき　たろう',
            'birth_date': '1992-12-25',
            'nickname': 'タロウ'
        },
        {
            'name': 'たなか　みき',
            'birth_date': '2000-03-03',
            'nickname': 'ミキ'
        }
    ]
    
    calculator = NumerologyCalculator()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"テストケース {i}: {test_case['name']}")
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
            
            print(f"  ライフパス: {result['life_path']['number']} - {result['life_path']['meaning']}")
            print(f"  ディスティニー: {result['destiny']['number']} - {result['destiny']['meaning']}")
            print(f"  ソウル: {result['soul']['number']} - {result['soul']['meaning']}")
            print(f"  パーソナル: {result['personal']['number']} - {result['personal']['meaning']}")
            print()
            
        except Exception as e:
            print(f"  エラー: {e}")
            print()

def test_edge_cases():
    """エッジケースのテスト"""
    
    print("エッジケースのテスト")
    print("=" * 60)
    
    edge_cases = [
        {
            'name': 'あい　うえお',  # 母音のみ
            'birth_date': '1988-08-08',
            'nickname': 'アイ'
        },
        {
            'name': 'かきくけこ　さしすせそ',  # 長い名前
            'birth_date': '1975-07-07',
            'nickname': 'カキク'
        }
    ]
    
    calculator = NumerologyCalculator()
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"エッジケース {i}: {test_case['name']}")
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
            print()
            
        except Exception as e:
            print(f"  エラー: {e}")
            print()

if __name__ == "__main__":
    print("数秘術最終テスト開始")
    print("=" * 60)
    
    test_complete_numerology_flow()
    test_multiple_names()
    test_edge_cases()
    
    print("=" * 60)
    print("数秘術最終テスト完了")
