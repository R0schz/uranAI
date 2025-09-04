#!/usr/bin/env python3
"""
Integration test for the updated numerology calculator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator

def test_integration():
    """Test integration with existing system"""
    
    print("Integration Test for Updated Numerology Calculator")
    print("=" * 60)
    
    calculator = NumerologyCalculator()
    
    # Test case 1: Original test case
    print("Test Case 1: Original test case (こばやし　よしたか)")
    print("-" * 50)
    
    profile = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1999-04-02',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    result = calculator.get_numerology_reading(profile)
    
    print(f"Results for {profile['nickname']}:")
    print(f"  ライフパス: {result['life_path']['number']} - {result['life_path']['meaning']}")
    print(f"  ディスティニー: {result['destiny']['number']} - {result['destiny']['meaning']}")
    print(f"  ソウル: {result['soul']['number']} - {result['soul']['meaning']}")
    print(f"  パーソナル: {result['personal']['number']} - {result['personal']['meaning']}")
    print(f"  バースデー: {result['birthday']['number']} - {result['birthday']['meaning']}")
    print(f"  チャレンジ: {result['challenge']['number']} - {result['challenge']['meaning']}")
    print(f"  マチュリティ: {result['maturity']['number']} - {result['maturity']['meaning']}")
    
    print("\n" + "=" * 60)
    
    # Test case 2: Multiple profiles
    print("Test Case 2: Multiple profiles")
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
        },
        {
            'nickname': 'ミキ',
            'name_hiragana': 'たなか　みき',
            'birth_date': '2000-03-03',
            'birth_time': '10:00:00',
            'birth_location_json': {'place': '福岡'}
        }
    ]
    
    for i, profile in enumerate(profiles, 1):
        result = calculator.get_numerology_reading(profile)
        print(f"Profile {i} - {profile['nickname']}:")
        print(f"  ライフパス: {result['life_path']['number']}")
        print(f"  ディスティニー: {result['destiny']['number']}")
        print(f"  ソウル: {result['soul']['number']}")
        print(f"  パーソナル: {result['personal']['number']}")
        print()
    
    print("=" * 60)
    
    # Test case 3: Compatibility analysis
    print("Test Case 3: Compatibility analysis")
    print("-" * 50)
    
    compatibility = calculator.get_compatibility_analysis(profiles[0], profiles[1])
    print(f"Compatibility between {profiles[0]['nickname']} and {profiles[1]['nickname']}:")
    print(f"  相性スコア: {compatibility['compatibility_score']}/100")
    print(f"  分析: {compatibility['analysis']}")
    
    print("\n" + "=" * 60)
    
    # Test case 4: Temporal fortune
    print("Test Case 4: Temporal fortune")
    print("-" * 50)
    
    temporal = calculator.calculate_temporal_fortune(profile, "2025-09-03")
    print(f"Temporal fortune for {profile['nickname']} on {temporal['target_date']}:")
    print(f"  パーソナルイヤー: {temporal['personal_year']['number']} - {temporal['personal_year']['description']}")
    print(f"  パーソナルマンス: {temporal['personal_month']['number']} - {temporal['personal_month']['description']}")
    print(f"  パーソナルデイ: {temporal['personal_day']['number']} - {temporal['personal_day']['description']}")
    
    print("\n" + "=" * 60)
    print("Integration test completed successfully!")

if __name__ == "__main__":
    test_integration()
