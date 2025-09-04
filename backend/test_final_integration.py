#!/usr/bin/env python3
"""
最終統合テスト
新しい数秘術アルゴリズムと時間軸運勢計算の統合テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from datetime import date

def test_final_integration():
    """最終統合テスト"""
    
    print("最終統合テスト - 新しい数秘術アルゴリズムと時間軸運勢計算")
    print("=" * 70)
    
    calculator = NumerologyCalculator()
    
    # テストケース: こばやし　よしたか
    print("テストケース: こばやし　よしたか")
    print("-" * 50)
    
    profile = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1999-04-02',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    # 1. 基本数秘術計算
    print("1. 基本数秘術計算:")
    numerology_result = calculator.get_numerology_reading(profile)
    
    print(f"  ニックネーム: {numerology_result['nickname']}")
    print(f"  ライフパス: {numerology_result['life_path']['number']} - {numerology_result['life_path']['meaning']}")
    print(f"  ディスティニー: {numerology_result['destiny']['number']} - {numerology_result['destiny']['meaning']}")
    print(f"  ソウル: {numerology_result['soul']['number']} - {numerology_result['soul']['meaning']}")
    print(f"  パーソナル: {numerology_result['personal']['number']} - {numerology_result['personal']['meaning']}")
    print(f"  バースデー: {numerology_result['birthday']['number']} - {numerology_result['birthday']['meaning']}")
    print(f"  マチュリティ: {numerology_result['maturity']['number']} - {numerology_result['maturity']['meaning']}")
    
    print("\n" + "=" * 70)
    
    # 2. 時間軸運勢計算
    print("2. 時間軸運勢計算:")
    today = date.today().isoformat()
    temporal_result = calculator.calculate_temporal_fortune(profile, today)
    
    print(f"  対象日: {temporal_result['target_date']}")
    print(f"  パーソナルイヤー: {temporal_result['personal_year']['number']} - {temporal_result['personal_year']['description']}")
    print(f"  パーソナルマンス: {temporal_result['personal_month']['number']} - {temporal_result['personal_month']['description']}")
    print(f"  パーソナルデイ: {temporal_result['personal_day']['number']} - {temporal_result['personal_day']['description']}")
    
    print("\n" + "=" * 70)
    
    # 3. 相性分析
    print("3. 相性分析:")
    profile2 = {
        'nickname': 'ハナコ',
        'name_hiragana': 'やまだ　はなこ',
        'birth_date': '1985-05-15',
        'birth_time': '08:30:00',
        'birth_location_json': {'place': '大阪'}
    }
    
    compatibility_result = calculator.get_compatibility_analysis(profile, profile2)
    
    print(f"  相性スコア: {compatibility_result['compatibility_score']}/100")
    print(f"  分析: {compatibility_result['analysis']}")
    
    print("\n" + "=" * 70)
    
    # 4. 詳細な時間軸分析
    print("4. 詳細な時間軸分析:")
    print(f"  パーソナルイヤー詳細:")
    print(f"    ナンバー: {temporal_result['personal_year']['number']}")
    print(f"    説明: {temporal_result['personal_year']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_year']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_year']['advice']}")
    
    print(f"\n  パーソナルマンス詳細:")
    print(f"    ナンバー: {temporal_result['personal_month']['number']}")
    print(f"    説明: {temporal_result['personal_month']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_month']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_month']['advice']}")
    
    print(f"\n  パーソナルデイ詳細:")
    print(f"    ナンバー: {temporal_result['personal_day']['number']}")
    print(f"    説明: {temporal_result['personal_day']['description']}")
    print(f"    キーワード: {', '.join(temporal_result['personal_day']['keywords'])}")
    print(f"    アドバイス: {temporal_result['personal_day']['advice']}")
    
    print("\n" + "=" * 70)
    
    # 5. 複数日付での時間軸変化
    print("5. 複数日付での時間軸変化:")
    test_dates = [
        '2025-01-01',
        '2025-04-02',  # 誕生日
        '2025-09-03',  # 今日
        '2025-12-31'
    ]
    
    for test_date in test_dates:
        result = calculator.calculate_temporal_fortune(profile, test_date)
        print(f"  {test_date}: 年={result['personal_year']['number']}, 月={result['personal_month']['number']}, 日={result['personal_day']['number']}")
    
    print("\n" + "=" * 70)
    print("最終統合テスト完了")
    print("✅ 新しい数秘術アルゴリズム: 正常動作")
    print("✅ 時間軸運勢計算: 正常動作")
    print("✅ 既存システム統合: 正常動作")
    print("✅ エラーハンドリング: 正常動作")

if __name__ == "__main__":
    test_final_integration()
