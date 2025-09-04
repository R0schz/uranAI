#!/usr/bin/env python3
"""
数秘術の名前変換テストスクリプト（新版）
pykakasiの新しいAPIを使用して「こばやし　よしたか」の英語変換と名字・名前の分離をテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from numerology_calculator import NumerologyCalculator
from numerology import Pythagorean
import pykakasi

def test_name_conversion_v2():
    """名前の英語変換と分離をテスト（新版API）"""
    
    # テスト用の名前
    test_name = "こばやし　よしたか"
    print(f"テスト対象の名前: {test_name}")
    print("=" * 50)
    
    # 1. pykakasiの新しいAPIを使用した英語変換テスト
    print("1. pykakasiの新しいAPIを使用した英語変換:")
    try:
        kks = pykakasi.kakasi()
        result = kks.convert(test_name)
        print(f"   変換結果: {result}")
        
        # 結果を文字列に結合
        romaji_text = ''.join([item['hepburn'] for item in result])
        print(f"   ローマ字テキスト: {romaji_text}")
        
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
        
        # 3. 各パートの英語変換（新版API）
        print("\n3. 各パートの英語変換（新版API）:")
        try:
            kks = pykakasi.kakasi()
            
            last_name_result = kks.convert(last_name)
            first_name_result = kks.convert(first_name)
            
            last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
            first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
            
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
        print(f"   数秘術計算結果:")
        for key, value in result.items():
            if key != 'nickname':
                print(f"     {key}: {value}")
        
    except Exception as e:
        print(f"   エラー: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. numerologyライブラリの直接テスト
    print("\n5. numerologyライブラリの直接テスト:")
    try:
        # 分離された名前でPythagoreanをテスト
        if len(name_parts) >= 2:
            kks = pykakasi.kakasi()
            last_name_result = kks.convert(name_parts[0])
            first_name_result = kks.convert(name_parts[1])
            
            last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
            first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
            
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
            print(f"   パーソナリティナンバー: {pythagorean.personality_number}")
            print(f"   バースデーナンバー: {pythagorean.birthday_number}")
            print(f"   マチュリティナンバー: {pythagorean.maturity_number}")
            
    except Exception as e:
        print(f"   エラー: {e}")
        import traceback
        traceback.print_exc()

def test_detailed_conversion():
    """詳細な変換テスト"""
    print("\n" + "=" * 50)
    print("詳細な変換テスト:")
    print("=" * 50)
    
    test_name = "こばやし　よしたか"
    name_parts = test_name.split()
    
    if len(name_parts) >= 2:
        last_name = name_parts[0]
        first_name = name_parts[1]
        
        print(f"元の名前: {test_name}")
        print(f"分離後 - 名字: {last_name}, 名前: {first_name}")
        
        kks = pykakasi.kakasi()
        
        # 名字の詳細変換
        print(f"\n名字 '{last_name}' の詳細変換:")
        last_name_result = kks.convert(last_name)
        for item in last_name_result:
            print(f"  原文: {item['orig']} -> ローマ字: {item['hepburn']} (読み: {item['hira']})")
        
        # 名前の詳細変換
        print(f"\n名前 '{first_name}' の詳細変換:")
        first_name_result = kks.convert(first_name)
        for item in first_name_result:
            print(f"  原文: {item['orig']} -> ローマ字: {item['hepburn']} (読み: {item['hira']})")
        
        # 最終的なローマ字
        last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
        first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
        
        print(f"\n最終的なローマ字:")
        print(f"  名字: {last_name_romaji}")
        print(f"  名前: {first_name_romaji}")
        print(f"  フルネーム: {last_name_romaji} {first_name_romaji}")

def test_numerology_calculation():
    """数秘術計算の詳細テスト"""
    print("\n" + "=" * 50)
    print("数秘術計算の詳細テスト:")
    print("=" * 50)
    
    test_name = "こばやし　よしたか"
    name_parts = test_name.split()
    
    if len(name_parts) >= 2:
        kks = pykakasi.kakasi()
        last_name_result = kks.convert(name_parts[0])
        first_name_result = kks.convert(name_parts[1])
        
        last_name_romaji = ''.join([item['hepburn'] for item in last_name_result])
        first_name_romaji = ''.join([item['hepburn'] for item in first_name_result])
        
        print(f"使用する名前: {first_name_romaji} {last_name_romaji}")
        
        try:
            # Pythagoreanオブジェクトを作成
            pythagorean = Pythagorean(
                first_name=first_name_romaji,
                last_name=last_name_romaji,
                birthdate='1990-01-01'
            )
            
            print(f"\n数秘術計算結果:")
            print(f"  ライフパスナンバー: {pythagorean.life_path_number}")
            print(f"  ディスティニーナンバー: {pythagorean.destiny_number}")
            print(f"  パーソナリティナンバー: {pythagorean.personality_number}")
            print(f"  バースデーナンバー: {pythagorean.birthday_number}")
            print(f"  マチュリティナンバー: {pythagorean.maturity_number}")
            
            # 詳細情報も表示
            print(f"\n詳細情報:")
            print(f"  フルネーム: {pythagorean.first_name} {pythagorean.last_name}")
            print(f"  生年月日: {pythagorean.birthdate}")
            
        except Exception as e:
            print(f"エラー: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("数秘術名前変換テスト開始（新版）")
    print("=" * 50)
    
    test_name_conversion_v2()
    test_detailed_conversion()
    test_numerology_calculation()
    
    print("\n" + "=" * 50)
    print("テスト完了")
