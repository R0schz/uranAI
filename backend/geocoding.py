"""
Google Geocoding APIを使用した地名から座標変換機能
Google Maps Services Pythonライブラリを使用
"""

import os
import googlemaps
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import signal
import time

load_dotenv(dotenv_path='.env.local')

class GeocodingService:
    """Google Geocoding APIサービス（Google Maps Services Pythonライブラリ使用）"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self._cache = {}  # キャッシュ機能を追加
        self._api_valid = False  # APIキーの有効性フラグ
        
        if not self.api_key:
            print("警告: GOOGLE_GEMINI_API_KEYが設定されていません")
            self.gmaps = None
        else:
            try:
                self.gmaps = googlemaps.Client(key=self.api_key)
                # APIキーの有効性をテスト
                self._test_api_key()
            except Exception as e:
                print(f"Google Maps client initialization failed: {e}")
                self.gmaps = None
    
    def _test_api_key(self):
        """APIキーの有効性をテスト"""
        if not self.gmaps:
            return
        
        try:
            # 簡単なテストリクエスト（東京の座標を取得）
            test_result = self.gmaps.geocode("東京")
            if test_result:
                self._api_valid = True
                print("Google Geocoding API: 認証成功")
            else:
                self._api_valid = False
                print("Google Geocoding API: 認証失敗 - 結果が空")
        except Exception as e:
            self._api_valid = False
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg:
                print("Google Geocoding API: 認証エラー - APIキーが無効またはGeocoding APIが有効になっていません")
                print("解決方法:")
                print("1. Google Cloud ConsoleでGeocoding APIを有効にしてください")
                print("2. APIキーの制限を確認してください")
                print("3. 請求アカウントが設定されていることを確認してください")
            elif "QUOTA_EXCEEDED" in error_msg:
                print("Google Geocoding API: クォータ超過")
            elif "OVER_QUERY_LIMIT" in error_msg:
                print("Google Geocoding API: クエリ制限超過")
            else:
                print(f"Google Geocoding API: その他のエラー - {error_msg}")
    
    def geocode_address(self, address: str) -> Dict[str, Any]:
        """住所を座標に変換（キャッシュ機能付き）"""
        # キャッシュをチェック
        if address in self._cache:
            print(f"Using cached geocoding result for: {address}")
            return self._cache[address]
        
        # APIキーが無効な場合は即座にフォールバック
        if not self.gmaps or not self._api_valid:
            print(f"Google Geocoding API is not available, using default location for: {address}")
            return self._get_default_location(address)
        
        try:
            # タイムアウト機能を実装
            def timeout_handler(signum, frame):
                raise TimeoutError("Geocoding request timed out")
            
            # 10秒でタイムアウト
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)
            
            try:
                # Google Maps Services Pythonライブラリを使用してジオコーディング
                geocode_result = self.gmaps.geocode(address)
                signal.alarm(0)  # タイムアウトをキャンセル
            except TimeoutError:
                signal.alarm(0)  # タイムアウトをキャンセル
                print(f"Geocoding timeout for: {address}")
                return self._get_default_location(address)
            
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                
                # タイムゾーンを取得
                tz_str = self._get_timezone(location['lat'], location['lng'])
                
                result = {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'tz_str': tz_str,
                    'place': address,
                    'formatted_address': geocode_result[0].get('formatted_address', address)
                }
                
                # キャッシュに保存
                self._cache[address] = result
                return result
            else:
                print(f"Geocoding failed: No results found for '{address}'")
                return self._get_default_location(address)
                
        except Exception as e:
            print(f"Geocoding error: {e}")
            print(f"Falling back to default location for '{address}'")
            return self._get_default_location(address)
    
    def _get_timezone(self, lat: float, lng: float) -> str:
        """座標からタイムゾーンを取得"""
        if not self.gmaps or not self._api_valid:
            print("Google Maps API is not available, using default timezone")
            return 'Asia/Tokyo'
        
        try:
            # タイムアウト機能を実装
            def timeout_handler(signum, frame):
                raise TimeoutError("Timezone request timed out")
            
            # 5秒でタイムアウト
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
            
            try:
                # Google Maps Services Pythonライブラリを使用してタイムゾーンを取得
                timezone_result = self.gmaps.timezone((lat, lng))
                signal.alarm(0)  # タイムアウトをキャンセル
            except TimeoutError:
                signal.alarm(0)  # タイムアウトをキャンセル
                print(f"Timezone lookup timeout for: {lat}, {lng}")
                return 'Asia/Tokyo'
            
            if timezone_result and 'timeZoneId' in timezone_result:
                return timezone_result['timeZoneId']
            else:
                return 'Asia/Tokyo'
                
        except Exception as e:
            print(f"Timezone lookup error: {e}")
            return 'Asia/Tokyo'
    
    def _get_default_location(self, address: str) -> Dict[str, Any]:
        """デフォルトの座標を返す"""
        # 日本の主要都市のデフォルト座標
        default_locations = {
            '東京': {'lat': 35.6762, 'lng': 139.6503, 'tz_str': 'Asia/Tokyo'},
            '大阪': {'lat': 34.6937, 'lng': 135.5023, 'tz_str': 'Asia/Tokyo'},
            '名古屋': {'lat': 35.1815, 'lng': 136.9066, 'tz_str': 'Asia/Tokyo'},
            '福岡': {'lat': 33.5904, 'lng': 130.4017, 'tz_str': 'Asia/Tokyo'},
            '札幌': {'lat': 43.0642, 'lng': 141.3469, 'tz_str': 'Asia/Tokyo'},
            '仙台': {'lat': 38.2682, 'lng': 140.8694, 'tz_str': 'Asia/Tokyo'},
            '広島': {'lat': 34.3853, 'lng': 132.4553, 'tz_str': 'Asia/Tokyo'},
            '京都': {'lat': 35.0116, 'lng': 135.7681, 'tz_str': 'Asia/Tokyo'},
            '横浜': {'lat': 35.4437, 'lng': 139.6380, 'tz_str': 'Asia/Tokyo'},
            '神戸': {'lat': 34.6901, 'lng': 135.1956, 'tz_str': 'Asia/Tokyo'}
        }
        
        # 入力された住所に含まれる都市名を検索
        for city, coords in default_locations.items():
            if city in address:
                return {
                    'lat': coords['lat'],
                    'lng': coords['lng'],
                    'tz_str': coords['tz_str'],
                    'place': address,
                    'formatted_address': address
                }
        
        # デフォルトは東京
        return {
            'lat': 35.6762,
            'lng': 139.6503,
            'tz_str': 'Asia/Tokyo',
            'place': address or '東京',
            'formatted_address': address or '東京都'
        }