#!/usr/bin/env python3
"""
時間軸運勢計算のテストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from datetime import date

def test_temporal_fortune():
    """時間軸運勢計算のテスト"""
    
    print("時間軸運勢計算のテスト")
    print("=" * 60)
    
    calculator = NumerologyCalculator()
    
    # テストケース1: こばやし　よしたか
    print("テストケース1: こばやし　よしたか")
    print("-" * 50)
    
    profile1 = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1999-04-02',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    # 今日の日付でテスト
    today = date.today().isoformat()
    print(f"対象日: {today}")
    
    temporal_result = calculator.calculate_temporal_fortune(profile1, today)
    
    print(f"\n時間軸運勢計算結果:")
    print(f"  対象日: {temporal_result['target_date']}")
    print(f"  パーソナルイヤー: {temporal_result['personal_year']['number']}")
    print(f"    説明: {temporal_result['personal_year']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_year']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_year']['advice']}")
    
    print(f"\n  パーソナルマンス: {temporal_result['personal_month']['number']}")
    print(f"    説明: {temporal_result['personal_month']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_month']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_month']['advice']}")
    
    print(f"\n  パーソナルデイ: {temporal_result['personal_day']['number']}")
    print(f"    説明: {temporal_result['personal_day']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_day']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_day']['advice']}")
    
    print("\n" + "=" * 60)
    
    # テストケース2: 複数の日付でテスト
    print("テストケース2: 複数の日付でテスト")
    print("-" * 50)
    
    test_dates = [
        '2025-01-01',  # 新年
        '2025-04-02',  # 誕生日
        '2025-12-25',  # クリスマス
        '2026-01-01'   # 翌年
    ]
    
    for test_date in test_dates:
        result = calculator.calculate_temporal_fortune(profile1, test_date)
        print(f"\n日付: {test_date}")
        print(f"  パーソナルイヤー: {result['personal_year']['number']}")
        print(f"  パーソナルマンス: {result['personal_month']['number']}")
        print(f"  パーソナルデイ: {result['personal_day']['number']}")
    
    print("\n" + "=" * 60)
    
    # テストケース3: 異なる人物でテスト
    print("テストケース3: 異なる人物でテスト")
    print("-" * 50)
    
    profiles = [
        {
            'nickname': 'ハナコ',
            'name_hiragana': 'やまだ　はなこ',
            'birth_date': '1985-05-15',
            'birth_time': '08:30:00',
            'birth_location_json': {'place': '大阪'}
        },
        {
            'nickname': 'タロウ',
            'name_hiragana': 'すずき　たろう',
            'birth_date': '1992-12-25',
            'birth_time': '15:45:00',
            'birth_location_json': {'place': '名古屋'}
        }
    ]
    
    test_date = '2025-09-03'
    
    for profile in profiles:
        result = calculator.calculate_temporal_fortune(profile, test_date)
        print(f"\n{profile['nickname']} ({profile['name_hiragana']}) - {test_date}")
        print(f"  パーソナルイヤー: {result['personal_year']['number']} - {result['personal_year']['description']}")
        print(f"  パーソナルマンス: {result['personal_month']['number']} - {result['personal_month']['description']}")
        print(f"  パーソナルデイ: {result['personal_day']['number']} - {result['personal_day']['description']}")
    
    print("\n" + "=" * 60)
    print("時間軸運勢計算テスト完了")

if __name__ == "__main__":
    test_temporal_fortune()
