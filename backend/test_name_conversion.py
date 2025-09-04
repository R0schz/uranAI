#!/usr/bin/env python3
"""
数秘術の名前変換テストスクリプト
「こばやし　よしたか」の英語変換と名字・名前の分離をテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from numerology import Pythagorean
import pykakasi

def test_name_conversion():
    """名前の英語変換と分離をテスト"""
    
    # テスト用の名前
    test_name = "こばやし　よしたか"
    print(f"テスト対象の名前: {test_name}")
    print("=" * 50)
    
    # 1. pykakasiを使用した英語変換テスト
    print("1. pykakasiを使用した英語変換:")
    kks = pykakasi.kakasi()
    kks.setMode('H', 'a')  # ひらがなをローマ字に
    kks.setMode('K', 'a')  # カタカナをローマ字に
    kks.setMode('J', 'a')  # 漢字をローマ字に
    kks.setMode('s', True)  # スペースを有効にする
    conv = kks.getConverter()
    
    try:
        romaji_result = conv.do(test_name)
        print(f"   ローマ字変換結果: {romaji_result}")
    except Exception as e:
        print(f"   エラー: {e}")
    
    # 2. 名字と名前の分離テスト
    print("\n2. 名字と名前の分離:")
    name_parts = test_name.split()
    if len(name_parts) >= 2:
        last_name = name_parts[0]  # こばやし
        first_name = name_parts[1]  # よしたか
        print(f"   名字: {last_name}")
        print(f"   名前: {first_name}")
        
        # 3. 各パートの英語変換
        print("\n3. 各パートの英語変換:")
        try:
            last_name_romaji = conv.do(last_name)
            first_name_romaji = conv.do(first_name)
            print(f"   名字のローマ字: {last_name_romaji}")
            print(f"   名前のローマ字: {first_name_romaji}")
        except Exception as e:
            print(f"   エラー: {e}")
    else:
        print("   エラー: 名字と名前が正しく分離されていません")
        return
    
    # 4. NumerologyCalculatorの実際の処理をテスト
    print("\n4. NumerologyCalculatorの実際の処理:")
    try:
        calculator = NumerologyCalculator()
        
        # テスト用のプロファイルデータ
        test_profile = {
            'nickname': 'テストユーザー',
            'name_hiragana': test_name,
            'birth_date': '1990-01-01',
            'birth_time': '12:00:00',
            'birth_location_json': {'place': '東京'}
        }
        
        print(f"   プロファイル: {test_profile}")
        
        # get_numerology_readingメソッドをテスト
        result = calculator.get_numerology_reading(test_profile)
        print(f"   数秘術計算結果: {result}")
        
    except Exception as e:
        print(f"   エラー: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. numerologyライブラリの直接テスト
    print("\n5. numerologyライブラリの直接テスト:")
    try:
        # 分離された名前でPythagoreanをテスト
        if len(name_parts) >= 2:
            last_name_romaji = conv.do(name_parts[0])
            first_name_romaji = conv.do(name_parts[1])
            
            print(f"   使用する名字: {last_name_romaji}")
            print(f"   使用する名前: {first_name_romaji}")
            
            # Pythagoreanオブジェクトを作成
            pythagorean = Pythagorean(
                first_name=first_name_romaji,
                last_name=last_name_romaji,
                birthdate='1990-01-01'
            )
            
            print(f"   ライフパスナンバー: {pythagorean.life_path_number}")
            print(f"   ディスティニーナンバー: {pythagorean.destiny_number}")
            print(f"   ソウルナンバー: {pythagorean.soul_number}")
            print(f"   パーソナリティナンバー: {pythagorean.personality_number}")
            print(f"   バースデーナンバー: {pythagorean.birthday_number}")
            print(f"   マチュリティナンバー: {pythagorean.maturity_number}")
            
    except Exception as e:
        print(f"   エラー: {e}")
        import traceback
        traceback.print_exc()

def test_edge_cases():
    """エッジケースのテスト"""
    print("\n" + "=" * 50)
    print("エッジケースのテスト:")
    print("=" * 50)
    
    test_cases = [
        "やまだ　はなこ",  # 一般的な名前
        "すずき　たろう",  # 一般的な名前
        "たなか　みき",    # 短い名前
        "さとう　じろう",  # 長い名字
        "こばやし　よしたか",  # 元のテストケース
    ]
    
    kks = pykakasi.kakasi()
    kks.setMode('H', 'a')
    kks.setMode('K', 'a')
    kks.setMode('J', 'a')
    kks.setMode('s', True)
    conv = kks.getConverter()
    
    for test_name in test_cases:
        print(f"\nテストケース: {test_name}")
        name_parts = test_name.split()
        if len(name_parts) >= 2:
            last_name = name_parts[0]
            first_name = name_parts[1]
            try:
                last_name_romaji = conv.do(last_name)
                first_name_romaji = conv.do(first_name)
                print(f"  結果: {last_name_romaji} {first_name_romaji}")
            except Exception as e:
                print(f"  エラー: {e}")
        else:
            print("  エラー: 分離できませんでした")

if __name__ == "__main__":
    print("数秘術名前変換テスト開始")
    print("=" * 50)
    
    test_name_conversion()
    test_edge_cases()
    
    print("\n" + "=" * 50)
    print("テスト完了")
