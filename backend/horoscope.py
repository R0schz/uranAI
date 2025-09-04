"""
西洋占星術アルゴリズム
外部設計書に基づく西洋占星術計算機能
"""

from typing import Dict, Any, List
from datetime import datetime, time
import kerykeion
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import json
import base64
import io
from geocoding import GeocodingService

class HoroscopeCalculator:
    """西洋占星術計算クラス"""
    
    def __init__(self):
        self.geocoding_service = GeocodingService()
        self.sign_meanings = {
            'Aries': '牡羊座 - 情熱的でリーダーシップがある',
            'Taurus': '牡牛座 - 安定感があり、実用的',
            'Gemini': '双子座 - 好奇心旺盛でコミュニケーション能力が高い',
            'Cancer': '蟹座 - 感情的で家族を大切にする',
            'Leo': '獅子座 - 創造的で自信に満ちている',
            'Virgo': '乙女座 - 分析的で完璧主義',
            'Libra': '天秤座 - バランス感覚があり、調和を求める',
            'Scorpio': '蠍座 - 神秘的で情熱的',
            'Sagittarius': '射手座 - 冒険的で哲学的な思考',
            'Capricorn': '山羊座 - 責任感が強く、目標志向',
            'Aquarius': '水瓶座 - 革新的で独立心が強い',
            'Pisces': '魚座 - 直感的で共感力が高い'
        }
        
        # 星座シンボルマッピング（短縮形も対応）
        self.sign_symbols = {
            'Aries': '♈', 'Ari': '♈',
            'Taurus': '♉', 'Tau': '♉',
            'Gemini': '♊', 'Gem': '♊',
            'Cancer': '♋', 'Can': '♋',
            'Leo': '♌', 'Leo': '♌',
            'Virgo': '♍', 'Vir': '♍',
            'Libra': '♎', 'Lib': '♎',
            'Scorpio': '♏', 'Sco': '♏',
            'Sagittarius': '♐', 'Sag': '♐',
            'Capricorn': '♑', 'Cap': '♑',
            'Aquarius': '♒', 'Aqu': '♒',
            'Pisces': '♓', 'Pis': '♓'
        }
        
        self.planet_meanings = {
            'Sun': '太陽 - 基本的な性格とアイデンティティ',
            'Moon': '月 - 感情と内面の世界',
            'Mercury': '水星 - コミュニケーションと思考',
            'Venus': '金星 - 愛と美、価値観',
            'Mars': '火星 - 行動力と情熱',
            'Jupiter': '木星 - 成長と拡張',
            'Saturn': '土星 - 制限と責任',
            'Uranus': '天王星 - 変化と革新',
            'Neptune': '海王星 - 直感とスピリチュアル',
            'Pluto': '冥王星 - 変容と再生'
        }
    
    def _get_japanese_sign_name(self, english_sign: str) -> str:
        """英語の星座名を日本語に変換"""
        # kerykeionライブラリの短縮形も対応
        sign_mapping = {
            'Aries': '牡羊座', 'Ari': '牡羊座',
            'Taurus': '牡牛座', 'Tau': '牡牛座',
            'Gemini': '双子座', 'Gem': '双子座',
            'Cancer': '蟹座', 'Can': '蟹座',
            'Leo': '獅子座', 'Leo': '獅子座',
            'Virgo': '乙女座', 'Vir': '乙女座',
            'Libra': '天秤座', 'Lib': '天秤座',
            'Scorpio': '蠍座', 'Sco': '蠍座',
            'Sagittarius': '射手座', 'Sag': '射手座',
            'Capricorn': '山羊座', 'Cap': '山羊座',
            'Aquarius': '水瓶座', 'Aqu': '水瓶座',
            'Pisces': '魚座', 'Pis': '魚座'
        }
        return sign_mapping.get(english_sign, english_sign)
    
    def _format_sign_with_symbol(self, english_sign: str) -> str:
        """星座名にシンボルを追加して日本語で表示"""
        japanese_name = self._get_japanese_sign_name(english_sign)
        symbol = self.sign_symbols.get(english_sign, '?')
        return f"{symbol} {japanese_name}"
    
    def generate_wheel_chart(self, profile_data: Dict[str, Any], chart_type: str = "natal") -> str:
        """ホイールチャートを生成してBase64エンコードして返す"""
        try:
            # 生年月日と時刻を取得
            birth_date = profile_data.get('birth_date', '')
            birth_time = profile_data.get('birth_time', '12:00')
            birth_location = profile_data.get('birth_location_json', {})
            
            if not birth_date:
                raise ValueError("生年月日が必要です")
            
            # 出生地の座標を取得
            place_name = birth_location.get('place', '東京')
            if 'lat' in birth_location and 'lng' in birth_location:
                lat = birth_location.get('lat', 35.6762)
                lng = birth_location.get('lng', 139.6503)
                tz_str = birth_location.get('tz_str', 'Asia/Tokyo')
            else:
                try:
                    geocoding_result = self.geocoding_service.geocode_address(place_name)
                    lat = geocoding_result['lat']
                    lng = geocoding_result['lng']
                    tz_str = geocoding_result['tz_str']
                except Exception as e:
                    print(f"Geocoding failed for '{place_name}': {e}")
                    lat = 35.6762
                    lng = 139.6503
                    tz_str = 'Asia/Tokyo'
            
            # 日付と時刻をパース
            try:
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    birth_datetime = datetime.strptime(f"{birth_date} 12:00", "%Y-%m-%d %H:%M")
            
            # AstrologicalSubjectを作成
            k = AstrologicalSubject(
                name=profile_data.get('nickname', 'User'),
                year=birth_datetime.year,
                month=birth_datetime.month,
                day=birth_datetime.day,
                hour=birth_datetime.hour,
                minute=birth_datetime.minute,
                lat=lat,
                lng=lng,
                tz_str=tz_str
            )
            
            # ホイールチャートを生成
            chart = KerykeionChartSVG(k)
            
            # テーマを設定
            chart.set_up_theme("dark")
            
            # 出力ディレクトリを設定
            from pathlib import Path
            chart.set_output_directory(Path('.'))
            
            # SVGファイルを生成
            chart.makeWheelOnlySVG(minify=True)
            
            # 生成されたファイルを読み取り
            filename = f"{profile_data.get('nickname', 'User')} - Natal Chart - Wheel Only.svg"
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                # Base64エンコード
                svg_bytes = svg_content.encode('utf-8')
                base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
                
                return f"data:image/svg+xml;base64,{base64_svg}"
            except FileNotFoundError:
                print(f"SVGファイルが見つかりません: {filename}")
                return None
            
        except Exception as e:
            print(f"ホイールチャート生成エラー: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_synastry_chart(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any]) -> str:
        """シナストリーチャートを生成してBase64エンコードして返す"""
        try:
            # 両方のプロファイルのAstrologicalSubjectを作成
            k1 = self._create_astrological_subject(profile1_data)
            k2 = self._create_astrological_subject(profile2_data)
            
            # シナストリーチャートを生成（互換性のない関数は使わない）
            chart = KerykeionChartSVG(k1, "Synastry", k2)
            
            # テーマを設定
            chart.set_up_theme("dark")
            
            # 出力ディレクトリを設定
            from pathlib import Path
            chart.set_output_directory(Path('.'))
            
            # SVGファイルを生成（通常のSVG生成を使用）
            try:
                chart.makeWheelOnlySVG(minify=True)
                filename = f"{profile1_data.get('nickname', 'User1')} - Synastry Chart - Wheel Only.svg"
                
                # 生成されたファイルを読み取り
                with open(filename, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                # Base64エンコード
                svg_bytes = svg_content.encode('utf-8')
                base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
                
                return f"data:image/svg+xml;base64,{base64_svg}"
                
            except Exception as e:
                print(f"シナストリーチャート生成エラー: {e}")
                # フォールバック: エラー表示
                return self._generate_error_synastry_chart(profile1_data, profile2_data)
            
        except Exception as e:
            print(f"シナストリーチャート生成エラー: {e}")
            import traceback
            traceback.print_exc()
            return self._generate_error_synastry_chart(profile1_data, profile2_data)
    
    def _generate_error_synastry_chart(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any]) -> str:
        """エラー表示用のシナストリーチャート（？マーク表示）"""
        try:
            # エラー表示用のSVGを生成（？マークのみ）
            svg_content = f"""
            <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <style>
                        .chart-title {{ font-family: Arial, sans-serif; font-size: 16px; fill: white; text-anchor: middle; }}
                        .chart-subtitle {{ font-family: Arial, sans-serif; font-size: 12px; fill: #ccc; text-anchor: middle; }}
                        .error-text {{ font-family: Arial, sans-serif; font-size: 48px; fill: #ff6b6b; text-anchor: middle; }}
                        .error-message {{ font-family: Arial, sans-serif; font-size: 14px; fill: #ff6b6b; text-anchor: middle; }}
                    </style>
                </defs>
                <rect width="400" height="400" fill="#000000"/>
                <text x="200" y="30" class="chart-title">シナストリーチャート</text>
                <text x="200" y="50" class="chart-subtitle">{profile1_data.get('nickname', 'User1')} × {profile2_data.get('nickname', 'User2')}</text>
                <text x="200" y="200" class="error-text">?</text>
                <text x="200" y="250" class="error-message">チャート生成エラー</text>
                <text x="200" y="380" class="chart-subtitle">相性分析チャート</text>
            </svg>
            """
            
            # Base64エンコード
            svg_bytes = svg_content.encode('utf-8')
            base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
            
            return f"data:image/svg+xml;base64,{base64_svg}"
                
        except Exception as e:
            print(f"エラー表示シナストリーチャート生成エラー: {e}")
            return None
    
    def _create_astrological_subject(self, profile_data: Dict[str, Any]) -> AstrologicalSubject:
        """プロファイルデータからAstrologicalSubjectを作成"""
        birth_date = profile_data.get('birth_date', '')
        birth_time = profile_data.get('birth_time', '12:00')
        birth_location = profile_data.get('birth_location_json', {})
        
        # 出生地の座標を取得
        place_name = birth_location.get('place', '東京')
        if 'lat' in birth_location and 'lng' in birth_location:
            lat = birth_location.get('lat', 35.6762)
            lng = birth_location.get('lng', 139.6503)
            tz_str = birth_location.get('tz_str', 'Asia/Tokyo')
        else:
            try:
                geocoding_result = self.geocoding_service.geocode_address(place_name)
                lat = geocoding_result['lat']
                lng = geocoding_result['lng']
                tz_str = geocoding_result['tz_str']
            except Exception as e:
                print(f"Geocoding failed for '{place_name}': {e}")
                lat = 35.6762
                lng = 139.6503
                tz_str = 'Asia/Tokyo'
        
        # 日付と時刻をパース
        try:
            birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
            except ValueError:
                birth_datetime = datetime.strptime(f"{birth_date} 12:00", "%Y-%m-%d %H:%M")
        
        return AstrologicalSubject(
            name=profile_data.get('nickname', 'User'),
            year=birth_datetime.year,
            month=birth_datetime.month,
            day=birth_datetime.day,
            hour=birth_datetime.hour,
            minute=birth_datetime.minute,
            lat=lat,
            lng=lng,
            tz_str=tz_str
        )
    
    def calculate_horoscope(self, profile_data: Dict[str, Any], target_date: str = None) -> Dict[str, Any]:
        """ホロスコープを計算（トランジット法対応）"""
        try:
            # 生年月日と時刻を取得
            birth_date = profile_data.get('birth_date', '')
            birth_time = profile_data.get('birth_time', '12:00')
            birth_location = profile_data.get('birth_location_json', {})
            
            if not birth_date:
                raise ValueError("生年月日が必要です")
            
            # 出生地の座標を取得（Geocoding APIを使用）
            place_name = birth_location.get('place', '東京')
            if 'lat' in birth_location and 'lng' in birth_location:
                # 既に座標が設定されている場合
                lat = birth_location.get('lat', 35.6762)
                lng = birth_location.get('lng', 139.6503)
                tz_str = birth_location.get('tz_str', 'Asia/Tokyo')
            else:
                # 地名から座標を取得（タイムアウト処理付き）
                try:
                    geocoding_result = self.geocoding_service.geocode_address(place_name)
                    lat = geocoding_result['lat']
                    lng = geocoding_result['lng']
                    tz_str = geocoding_result['tz_str']
                except Exception as e:
                    print(f"Geocoding failed for '{place_name}': {e}")
                    print("Using default Tokyo coordinates")
                    lat = 35.6762
                    lng = 139.6503
                    tz_str = 'Asia/Tokyo'
            
            # 日付と時刻をパース（様々なフォーマットに対応）
            try:
                # まず基本的なフォーマットを試す
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    # 秒が含まれている場合
                    birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # 時刻が不正な場合はデフォルト時刻を使用
                    print(f"Invalid time format: {birth_time}, using default 12:00")
                    birth_datetime = datetime.strptime(f"{birth_date} 12:00", "%Y-%m-%d %H:%M")
            
            # Kerykeionでホロスコープを計算
            k = AstrologicalSubject(
                name="User",
                year=birth_datetime.year,
                month=birth_datetime.month,
                day=birth_datetime.day,
                hour=birth_datetime.hour,
                minute=birth_datetime.minute,
                lat=lat,
                lng=lng,
                tz_str=tz_str
            )
            
            # 惑星の位置を取得
            planets = {
                'sun': {
                    'sign': k.sun.sign,
                    'sign_jp': self._format_sign_with_symbol(k.sun.sign),
                    'degree': k.sun.position,
                    'meaning': self.planet_meanings.get('Sun', '太陽の意味')
                },
                'moon': {
                    'sign': k.moon.sign,
                    'sign_jp': self._format_sign_with_symbol(k.moon.sign),
                    'degree': k.moon.position,
                    'meaning': self.planet_meanings.get('Moon', '月の意味')
                },
                'mercury': {
                    'sign': k.mercury.sign,
                    'sign_jp': self._format_sign_with_symbol(k.mercury.sign),
                    'degree': k.mercury.position,
                    'meaning': self.planet_meanings.get('Mercury', '水星の意味')
                },
                'venus': {
                    'sign': k.venus.sign,
                    'sign_jp': self._format_sign_with_symbol(k.venus.sign),
                    'degree': k.venus.position,
                    'meaning': self.planet_meanings.get('Venus', '金星の意味')
                },
                'mars': {
                    'sign': k.mars.sign,
                    'sign_jp': self._format_sign_with_symbol(k.mars.sign),
                    'degree': k.mars.position,
                    'meaning': self.planet_meanings.get('Mars', '火星の意味')
                },
                'jupiter': {
                    'sign': k.jupiter.sign,
                    'sign_jp': self._format_sign_with_symbol(k.jupiter.sign),
                    'degree': k.jupiter.position,
                    'meaning': self.planet_meanings.get('Jupiter', '木星の意味')
                },
                'saturn': {
                    'sign': k.saturn.sign,
                    'sign_jp': self._format_sign_with_symbol(k.saturn.sign),
                    'degree': k.saturn.position,
                    'meaning': self.planet_meanings.get('Saturn', '土星の意味')
                }
            }
            
            # アスペクトを計算
            aspects = self._calculate_aspects(k)
            
            # ホイールチャートを生成
            wheel_chart = self.generate_wheel_chart(profile_data)
            
            return {
                'birth_info': {
                    'date': birth_date,
                    'time': birth_time,
                    'location': birth_location
                },
                'planets': planets,
                'aspects': aspects,
                'sun_sign': k.sun.sign,
                'moon_sign': k.moon.sign,
                'rising_sign': k.ascendant.sign if hasattr(k, 'ascendant') else 'Unknown',
                'sun_sign_jp': self._format_sign_with_symbol(k.sun.sign),
                'moon_sign_jp': self._format_sign_with_symbol(k.moon.sign),
                'rising_sign_jp': self._format_sign_with_symbol(k.ascendant.sign) if hasattr(k, 'ascendant') else '? 不明',
                'wheel_chart': wheel_chart,
                'calculation_type': 'natal'
            }
            
        except Exception as e:
            print(f"ホロスコープ計算エラー: {e}")
            return self._get_default_horoscope()
    
    def _calculate_aspects(self, k: AstrologicalSubject) -> List[Dict[str, Any]]:
        """アスペクトを計算"""
        aspects = []
        
        # 主要なアスペクトを計算
        try:
            if hasattr(k, 'aspects'):
                for aspect in k.aspects:
                    aspects.append({
                        'planet1': aspect.p1.name,
                        'planet2': aspect.p2.name,
                        'aspect': aspect.aspect,
                        'orb': aspect.orb,
                        'meaning': self._get_aspect_meaning(aspect.aspect)
                    })
        except:
            # アスペクト計算に失敗した場合はデフォルト値を返す
            aspects = [
                {
                    'planet1': 'Sun',
                    'planet2': 'Moon',
                    'aspect': 'Trine',
                    'orb': 2.5,
                    'meaning': '調和の取れた関係'
                }
            ]
        
        return aspects
    
    def _get_aspect_meaning(self, aspect: str) -> str:
        """アスペクトの意味を取得"""
        aspect_meanings = {
            'Conjunction': '結合 - 強力な統合',
            'Opposition': '対立 - バランスが必要',
            'Trine': 'トライン - 調和と流れ',
            'Square': 'スクエア - 緊張と成長',
            'Sextile': 'セクスタイル - 協力と機会'
        }
        return aspect_meanings.get(aspect, '特別な関係')
    
    def _get_default_horoscope(self) -> Dict[str, Any]:
        """デフォルトのホロスコープを返す"""
        return {
            'birth_info': {
                'date': '1990-01-01',
                'time': '12:00',
                'location': {'place': '東京', 'lat': 35.6762, 'lng': 139.6503, 'tz_str': 'Asia/Tokyo'}
            },
            'planets': {
                'sun': {'sign': 'Aries', 'degree': 10, 'meaning': '太陽の意味'},
                'moon': {'sign': 'Cancer', 'degree': 15, 'meaning': '月の意味'},
                'mercury': {'sign': 'Aries', 'degree': 5, 'meaning': '水星の意味'},
                'venus': {'sign': 'Taurus', 'degree': 20, 'meaning': '金星の意味'},
                'mars': {'sign': 'Leo', 'degree': 25, 'meaning': '火星の意味'},
                'jupiter': {'sign': 'Sagittarius', 'degree': 8, 'meaning': '木星の意味'},
                'saturn': {'sign': 'Capricorn', 'degree': 12, 'meaning': '土星の意味'}
            },
            'aspects': [
                {
                    'planet1': 'Sun',
                    'planet2': 'Moon',
                    'aspect': 'Trine',
                    'orb': 2.5,
                    'meaning': '調和の取れた関係'
                }
            ],
            'sun_sign': 'Aries',
            'moon_sign': 'Cancer',
            'rising_sign': 'Leo'
        }
    
    def calculate_transit_horoscope(self, profile_data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """トランジット法でホロスコープを計算（特定の時点での惑星位置）"""
        try:
            # 生年月日と時刻を取得
            birth_date = profile_data.get('birth_date', '')
            birth_time = profile_data.get('birth_time', '12:00')
            birth_location = profile_data.get('birth_location_json', {})
            
            if not birth_date:
                raise ValueError("生年月日が必要です")
            
            # 出生地の座標を取得
            place_name = birth_location.get('place', '東京')
            if 'lat' in birth_location and 'lng' in birth_location:
                lat = birth_location.get('lat', 35.6762)
                lng = birth_location.get('lng', 139.6503)
                tz_str = birth_location.get('tz_str', 'Asia/Tokyo')
            else:
                try:
                    geocoding_result = self.geocoding_service.geocode_address(place_name)
                    lat = geocoding_result['lat']
                    lng = geocoding_result['lng']
                    tz_str = geocoding_result['tz_str']
                except Exception as e:
                    print(f"Geocoding failed for '{place_name}': {e}")
                    lat = 35.6762
                    lng = 139.6503
                    tz_str = 'Asia/Tokyo'
            
            # 生年月日をパース
            try:
                birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    birth_datetime = datetime.strptime(f"{birth_date} 12:00", "%Y-%m-%d %H:%M")
            
            # 対象日時をパース
            try:
                target_datetime = datetime.strptime(target_date, "%Y-%m-%d")
            except ValueError:
                try:
                    target_datetime = datetime.strptime(target_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    raise ValueError(f"Invalid target date format: {target_date}")
            
            # 出生時のホロスコープを計算
            birth_k = AstrologicalSubject(
                name="User",
                year=birth_datetime.year,
                month=birth_datetime.month,
                day=birth_datetime.day,
                hour=birth_datetime.hour,
                minute=birth_datetime.minute,
                lat=lat,
                lng=lng,
                tz_str=tz_str
            )
            
            # 対象時点でのホロスコープを計算（トランジット）
            transit_k = AstrologicalSubject(
                name="Transit",
                year=target_datetime.year,
                month=target_datetime.month,
                day=target_datetime.day,
                hour=target_datetime.hour,
                minute=target_datetime.minute,
                lat=lat,
                lng=lng,
                tz_str=tz_str
            )
            
            # 出生時の惑星位置
            natal_planets = {
                'sun': {
                    'sign': birth_k.sun.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.sun.sign),
                    'degree': birth_k.sun.position,
                    'meaning': self.planet_meanings.get('Sun', '太陽の意味')
                },
                'moon': {
                    'sign': birth_k.moon.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.moon.sign),
                    'degree': birth_k.moon.position,
                    'meaning': self.planet_meanings.get('Moon', '月の意味')
                },
                'mercury': {
                    'sign': birth_k.mercury.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.mercury.sign),
                    'degree': birth_k.mercury.position,
                    'meaning': self.planet_meanings.get('Mercury', '水星の意味')
                },
                'venus': {
                    'sign': birth_k.venus.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.venus.sign),
                    'degree': birth_k.venus.position,
                    'meaning': self.planet_meanings.get('Venus', '金星の意味')
                },
                'mars': {
                    'sign': birth_k.mars.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.mars.sign),
                    'degree': birth_k.mars.position,
                    'meaning': self.planet_meanings.get('Mars', '火星の意味')
                },
                'jupiter': {
                    'sign': birth_k.jupiter.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.jupiter.sign),
                    'degree': birth_k.jupiter.position,
                    'meaning': self.planet_meanings.get('Jupiter', '木星の意味')
                },
                'saturn': {
                    'sign': birth_k.saturn.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.saturn.sign),
                    'degree': birth_k.saturn.position,
                    'meaning': self.planet_meanings.get('Saturn', '土星の意味')
                },
                'uranus': {
                    'sign': birth_k.uranus.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.uranus.sign),
                    'degree': birth_k.uranus.position,
                    'meaning': self.planet_meanings.get('Uranus', '天王星の意味')
                },
                'neptune': {
                    'sign': birth_k.neptune.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.neptune.sign),
                    'degree': birth_k.neptune.position,
                    'meaning': self.planet_meanings.get('Neptune', '海王星の意味')
                },
                'pluto': {
                    'sign': birth_k.pluto.sign,
                    'sign_jp': self._format_sign_with_symbol(birth_k.pluto.sign),
                    'degree': birth_k.pluto.position,
                    'meaning': self.planet_meanings.get('Pluto', '冥王星の意味')
                }
            }
            
            # トランジット（対象時点）の惑星位置
            transit_planets = {
                'sun': {
                    'sign': transit_k.sun.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.sun.sign),
                    'degree': transit_k.sun.position,
                    'meaning': f"太陽のトランジット - {target_date}"
                },
                'moon': {
                    'sign': transit_k.moon.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.moon.sign),
                    'degree': transit_k.moon.position,
                    'meaning': f"月のトランジット - {target_date}"
                },
                'mercury': {
                    'sign': transit_k.mercury.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.mercury.sign),
                    'degree': transit_k.mercury.position,
                    'meaning': f"水星のトランジット - {target_date}"
                },
                'venus': {
                    'sign': transit_k.venus.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.venus.sign),
                    'degree': transit_k.venus.position,
                    'meaning': f"金星のトランジット - {target_date}"
                },
                'mars': {
                    'sign': transit_k.mars.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.mars.sign),
                    'degree': transit_k.mars.position,
                    'meaning': f"火星のトランジット - {target_date}"
                },
                'jupiter': {
                    'sign': transit_k.jupiter.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.jupiter.sign),
                    'degree': transit_k.jupiter.position,
                    'meaning': f"木星のトランジット - {target_date}"
                },
                'saturn': {
                    'sign': transit_k.saturn.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.saturn.sign),
                    'degree': transit_k.saturn.position,
                    'meaning': f"土星のトランジット - {target_date}"
                },
                'uranus': {
                    'sign': transit_k.uranus.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.uranus.sign),
                    'degree': transit_k.uranus.position,
                    'meaning': f"天王星のトランジット - {target_date}"
                },
                'neptune': {
                    'sign': transit_k.neptune.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.neptune.sign),
                    'degree': transit_k.neptune.position,
                    'meaning': f"海王星のトランジット - {target_date}"
                },
                'pluto': {
                    'sign': transit_k.pluto.sign,
                    'sign_jp': self._format_sign_with_symbol(transit_k.pluto.sign),
                    'degree': transit_k.pluto.position,
                    'meaning': f"冥王星のトランジット - {target_date}"
                }
            }
            
            # アスペクト（角度関係）を計算
            aspects = self._calculate_transit_aspects(natal_planets, transit_planets)
            
            # トランジット用のホイールチャートを生成
            wheel_chart = self.generate_wheel_chart(profile_data, "transit")
            
            return {
                'nickname': profile_data.get('nickname', 'あなた'),
                'target_date': target_date,
                'natal_planets': natal_planets,
                'transit_planets': transit_planets,
                'aspects': aspects,
                'sun_sign': birth_k.sun.sign,
                'moon_sign': birth_k.moon.sign,
                'rising_sign': birth_k.ascendant.sign,
                'sun_sign_jp': self._format_sign_with_symbol(birth_k.sun.sign),
                'moon_sign_jp': self._format_sign_with_symbol(birth_k.moon.sign),
                'rising_sign_jp': self._format_sign_with_symbol(birth_k.ascendant.sign),
                'birth_location': place_name,
                'calculation_type': 'transit',
                'wheel_chart': wheel_chart,
                # 既存のビジュアル生成との互換性のため
                'planets': natal_planets
            }
            
        except Exception as e:
            print(f"トランジット計算エラー: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_transit_result(profile_data, target_date)
    
    def _calculate_transit_aspects(self, natal_planets: Dict, transit_planets: Dict) -> List[Dict]:
        """トランジットアスペクトを計算"""
        aspects = []
        
        # 主要なアスペクト角度
        aspect_angles = {
            'conjunction': 0,
            'sextile': 60,
            'square': 90,
            'trine': 120,
            'opposition': 180
        }
        
        # 各トランジット惑星と出生惑星のアスペクトを計算
        for transit_planet_name, transit_planet in transit_planets.items():
            if transit_planet_name in natal_planets:
                natal_planet = natal_planets[transit_planet_name]
                
                # 角度差を計算
                angle_diff = abs(transit_planet['degree'] - natal_planet['degree'])
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # 最も近いアスペクトを特定
                closest_aspect = None
                min_diff = float('inf')
                
                for aspect_name, aspect_angle in aspect_angles.items():
                    diff = abs(angle_diff - aspect_angle)
                    if diff < min_diff and diff <= 8:  # 8度以内の許容範囲
                        min_diff = diff
                        closest_aspect = aspect_name
                
                if closest_aspect:
                    aspects.append({
                        'transit_planet': transit_planet_name,
                        'natal_planet': transit_planet_name,
                        'aspect': closest_aspect,
                        'angle': angle_diff,
                        'orb': min_diff,
                        'description': f"{transit_planet['sign_jp']}の{transit_planet_name}が出生時の{aspect_name}を形成"
                    })
        
        return aspects
    
    def _get_default_transit_result(self, profile_data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """デフォルトのトランジット結果を返す"""
        return {
            'nickname': profile_data.get('nickname', 'あなた'),
            'target_date': target_date,
            'natal_planets': {},
            'transit_planets': {},
            'aspects': [],
            'sun_sign': 'Aries',
            'moon_sign': 'Cancer',
            'rising_sign': 'Leo',
            'sun_sign_jp': '♈ 牡羊座',
            'moon_sign_jp': '♋ 蟹座',
            'rising_sign_jp': '♌ 獅子座',
            'birth_location': '東京',
            'calculation_type': 'transit'
        }
    
    def get_compatibility_analysis(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any], consultation: str = "") -> Dict[str, Any]:
        """相性分析を生成"""
        horoscope1 = self.calculate_horoscope(profile1_data)
        horoscope2 = self.calculate_horoscope(profile2_data)
        
        # AIを使用してスコアを生成
        compatibility_data = {
            'person1': horoscope1,
            'person2': horoscope2,
            'person1_nickname': profile1_data.get('nickname', 'あなた'),
            'person2_nickname': profile2_data.get('nickname', '相手'),
            'consultation': consultation
        }
        
        try:
            from ai_analysis import AIAnalysisGenerator
            ai_generator = AIAnalysisGenerator()
            compatibility_score = ai_generator.generate_ai_compatibility_score(compatibility_data, 'horoscope')
        except Exception as e:
            print(f"AI score generation failed, using fallback: {e}")
            # フォールバック: 改善されたアルゴリズム
            compatibility_score = self._calculate_enhanced_compatibility_score(horoscope1, horoscope2, consultation)
        
        # AI分析を生成
        compatibility_data['compatibility_score'] = compatibility_score
        compatibility_data['fortune_type'] = 'horoscope'
        
        try:
            from ai_analysis import AIAnalysisGenerator
            ai_generator = AIAnalysisGenerator()
            analysis = ai_generator.generate_compatibility_analysis(compatibility_data, 'horoscope', consultation)
        except Exception as e:
            print(f"AI analysis failed, using fallback: {e}")
            analysis = self._generate_compatibility_text_with_nicknames(horoscope1, horoscope2, compatibility_score, profile1_data.get('nickname', 'あなた'), profile2_data.get('nickname', '相手'), consultation)
        
        # 日本語の星座名を追加
        horoscope1['sun_sign_jp'] = self._format_sign_with_symbol(horoscope1.get('sun_sign', 'Aries'))
        horoscope1['moon_sign_jp'] = self._format_sign_with_symbol(horoscope1.get('moon_sign', 'Cancer'))
        horoscope2['sun_sign_jp'] = self._format_sign_with_symbol(horoscope2.get('sun_sign', 'Aries'))
        horoscope2['moon_sign_jp'] = self._format_sign_with_symbol(horoscope2.get('moon_sign', 'Cancer'))
        
        # シナストリーチャートを生成
        synastry_chart = self.generate_synastry_chart(profile1_data, profile2_data)
        
        return {
            'person1': horoscope1,
            'person2': horoscope2,
            'compatibility_score': compatibility_score,
            'analysis': analysis,
            'synastry_chart': synastry_chart
        }
    
    def _calculate_compatibility_score(self, horoscope1: Dict, horoscope2: Dict) -> int:
        """相性スコアを計算"""
        # 太陽星座と月星座の相性を基にスコアを計算
        sun_sign1 = self._convert_sign_name(horoscope1.get('sun_sign', 'Aries'))
        sun_sign2 = self._convert_sign_name(horoscope2.get('sun_sign', 'Aries'))
        moon_sign1 = self._convert_sign_name(horoscope1.get('moon_sign', 'Cancer'))
        moon_sign2 = self._convert_sign_name(horoscope2.get('moon_sign', 'Cancer'))
        
        # 星座の相性マトリックス（簡略版）
        compatibility_matrix = {
            'Aries': {'Aries': 60, 'Leo': 90, 'Sagittarius': 85, 'Gemini': 70, 'Aquarius': 75, 'Cancer': 40, 'Scorpio': 45, 'Pisces': 50, 'Taurus': 35, 'Virgo': 40, 'Capricorn': 45, 'Libra': 65},
            'Taurus': {'Taurus': 65, 'Virgo': 90, 'Capricorn': 85, 'Cancer': 70, 'Pisces': 75, 'Aries': 35, 'Leo': 40, 'Sagittarius': 45, 'Gemini': 50, 'Libra': 40, 'Aquarius': 45, 'Scorpio': 60},
            'Gemini': {'Gemini': 60, 'Libra': 90, 'Aquarius': 85, 'Aries': 70, 'Leo': 75, 'Cancer': 45, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 50, 'Virgo': 45, 'Capricorn': 40, 'Sagittarius': 65},
            'Cancer': {'Cancer': 65, 'Scorpio': 90, 'Pisces': 85, 'Taurus': 70, 'Virgo': 75, 'Aries': 40, 'Leo': 45, 'Sagittarius': 40, 'Gemini': 45, 'Libra': 50, 'Aquarius': 40, 'Capricorn': 60},
            'Leo': {'Leo': 60, 'Aries': 90, 'Sagittarius': 85, 'Gemini': 70, 'Libra': 75, 'Cancer': 45, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 40, 'Virgo': 45, 'Capricorn': 40, 'Aquarius': 65},
            'Virgo': {'Virgo': 65, 'Taurus': 90, 'Capricorn': 85, 'Cancer': 70, 'Scorpio': 75, 'Aries': 40, 'Leo': 45, 'Sagittarius': 40, 'Gemini': 45, 'Libra': 50, 'Aquarius': 40, 'Pisces': 60},
            'Libra': {'Libra': 60, 'Gemini': 90, 'Aquarius': 85, 'Leo': 70, 'Sagittarius': 75, 'Cancer': 50, 'Scorpio': 45, 'Pisces': 40, 'Taurus': 40, 'Virgo': 50, 'Capricorn': 45, 'Aries': 65},
            'Scorpio': {'Scorpio': 65, 'Cancer': 90, 'Pisces': 85, 'Virgo': 70, 'Capricorn': 75, 'Aries': 45, 'Leo': 40, 'Sagittarius': 35, 'Gemini': 40, 'Libra': 45, 'Aquarius': 40, 'Taurus': 60},
            'Sagittarius': {'Sagittarius': 60, 'Aries': 90, 'Leo': 85, 'Libra': 70, 'Aquarius': 75, 'Cancer': 40, 'Scorpio': 35, 'Pisces': 40, 'Taurus': 45, 'Virgo': 40, 'Capricorn': 45, 'Gemini': 65},
            'Capricorn': {'Capricorn': 65, 'Taurus': 90, 'Virgo': 85, 'Scorpio': 70, 'Pisces': 75, 'Aries': 45, 'Leo': 40, 'Sagittarius': 45, 'Gemini': 40, 'Libra': 45, 'Aquarius': 40, 'Cancer': 60},
            'Aquarius': {'Aquarius': 60, 'Gemini': 90, 'Libra': 85, 'Sagittarius': 70, 'Aries': 75, 'Cancer': 40, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 45, 'Virgo': 40, 'Capricorn': 40, 'Leo': 65},
            'Pisces': {'Pisces': 65, 'Cancer': 90, 'Scorpio': 85, 'Capricorn': 70, 'Taurus': 75, 'Aries': 50, 'Leo': 35, 'Sagittarius': 40, 'Gemini': 35, 'Libra': 40, 'Aquarius': 35, 'Virgo': 60}
        }
        
        # 太陽星座の相性スコア
        sun_score = compatibility_matrix.get(sun_sign1, {}).get(sun_sign2, 50)
        
        # 月星座の相性スコア
        moon_score = compatibility_matrix.get(moon_sign1, {}).get(moon_sign2, 50)
        
        # 太陽星座70%、月星座30%の重みで計算
        final_score = int((sun_score * 0.7) + (moon_score * 0.3))
        
        # スコアを20-100の範囲に調整
        return max(20, min(100, final_score))
    
    def _convert_sign_name(self, sign_name: str) -> str:
        """星座名を英語に変換"""
        sign_mapping = {
            '牡羊座': 'Aries', 'Ari': 'Aries',
            '牡牛座': 'Taurus', 'Tau': 'Taurus',
            '双子座': 'Gemini', 'Gem': 'Gemini',
            '蟹座': 'Cancer', 'Can': 'Cancer', 'Cancer': 'Cancer',
            '獅子座': 'Leo', 'Leo': 'Leo',
            '乙女座': 'Virgo', 'Vir': 'Virgo',
            '天秤座': 'Libra', 'Lib': 'Libra',
            '蠍座': 'Scorpio', 'Sco': 'Scorpio',
            '射手座': 'Sagittarius', 'Sag': 'Sagittarius',
            '山羊座': 'Capricorn', 'Cap': 'Capricorn',
            '水瓶座': 'Aquarius', 'Aqu': 'Aquarius',
            '魚座': 'Pisces', 'Pis': 'Pisces'
        }
        return sign_mapping.get(sign_name, 'Aries')
    
    def _generate_compatibility_text(self, horoscope1: Dict, horoscope2: Dict, score: int) -> str:
        """相性分析のテキストを生成"""
        sun_sign1 = horoscope1.get('sun_sign', 'Aries')
        sun_sign2 = horoscope2.get('sun_sign', 'Aries')
        
        if score >= 80:
            return f"{sun_sign1}と{sun_sign2}は非常に相性の良い組み合わせです。お互いを理解し合い、素晴らしい関係を築けるでしょう。"
        elif score >= 60:
            return f"{sun_sign1}と{sun_sign2}は良い相性です。お互いの違いを尊重し合えば、安定した関係を築けるでしょう。"
        elif score >= 40:
            return f"{sun_sign1}と{sun_sign2}は中程度の相性です。お互いの努力次第で良い関係を築ける可能性があります。"
        else:
            return f"{sun_sign1}と{sun_sign2}は相性に課題がありますが、お互いの理解を深めることで改善できるでしょう。"
    
    def _generate_compatibility_text_with_nicknames(self, horoscope1: Dict, horoscope2: Dict, score: int, nickname1: str, nickname2: str, consultation: str) -> str:
        """ニックネームを使用した相性分析のテキストを生成"""
        # 星座名を日本語に変換
        sun_sign1_jp = self._convert_sign_to_japanese(horoscope1.get('sun_sign', 'Aries'))
        moon_sign1_jp = self._convert_sign_to_japanese(horoscope1.get('moon_sign', 'Cancer'))
        sun_sign2_jp = self._convert_sign_to_japanese(horoscope2.get('sun_sign', 'Aries'))
        moon_sign2_jp = self._convert_sign_to_japanese(horoscope2.get('moon_sign', 'Cancer'))
        
        # 相談内容に応じた分析
        consultation_context = ""
        if consultation and consultation.strip():
            if "恋愛" in consultation or "恋" in consultation:
                consultation_context = "恋愛関係において、"
            elif "結婚" in consultation or "婚" in consultation:
                consultation_context = "結婚を考える上で、"
            elif "友情" in consultation or "友" in consultation:
                consultation_context = "友情関係において、"
            elif "仕事" in consultation or "職" in consultation:
                consultation_context = "仕事関係において、"
        
        if score >= 80:
            base_analysis = f"{nickname1}さんと{nickname2}さんは非常に良い相性です。{nickname1}さんの太陽{sun_sign1_jp}・月{moon_sign1_jp}と{nickname2}さんの太陽{sun_sign2_jp}・月{moon_sign2_jp}の組み合わせは、お互いを高め合える素晴らしい関係を築けるでしょう。"
        elif score >= 60:
            base_analysis = f"{nickname1}さんと{nickname2}さんは良い相性です。{nickname1}さんの太陽{sun_sign1_jp}・月{moon_sign1_jp}と{nickname2}さんの太陽{sun_sign2_jp}・月{moon_sign2_jp}の組み合わせは、お互いの違いを理解し合えば、安定した関係を築けるでしょう。"
        elif score >= 40:
            base_analysis = f"{nickname1}さんと{nickname2}さんは普通の相性です。{nickname1}さんの太陽{sun_sign1_jp}・月{moon_sign1_jp}と{nickname2}さんの太陽{sun_sign2_jp}・月{moon_sign2_jp}の組み合わせは、努力次第で良い関係を築くことができます。"
        else:
            base_analysis = f"{nickname1}さんと{nickname2}さんの相性には課題があります。{nickname1}さんの太陽{sun_sign1_jp}・月{moon_sign1_jp}と{nickname2}さんの太陽{sun_sign2_jp}・月{moon_sign2_jp}の組み合わせは、お互いの理解を深めることが重要です。"
        
        if consultation_context:
            return f"{base_analysis} {consultation_context}星座のエネルギーが調和し、お互いを支え合える関係を築けるでしょう。"
        else:
            return base_analysis
    
    def _convert_sign_to_japanese(self, sign_name: str) -> str:
        """星座名を日本語に変換"""
        sign_mapping = {
            'Aries': '牡羊座', 'Ari': '牡羊座',
            'Taurus': '牡牛座', 'Tau': '牡牛座',
            'Gemini': '双子座', 'Gem': '双子座',
            'Cancer': '蟹座', 'Can': '蟹座',
            'Leo': '獅子座',
            'Virgo': '乙女座', 'Vir': '乙女座',
            'Libra': '天秤座', 'Lib': '天秤座',
            'Scorpio': '蠍座', 'Sco': '蠍座',
            'Sagittarius': '射手座', 'Sag': '射手座',
            'Capricorn': '山羊座', 'Cap': '山羊座',
            'Aquarius': '水瓶座', 'Aqu': '水瓶座',
            'Pisces': '魚座', 'Pis': '魚座'
        }
        return sign_mapping.get(sign_name, '牡羊座')
    
    def _calculate_enhanced_compatibility_score(self, horoscope1: Dict, horoscope2: Dict, consultation: str) -> int:
        """改善された相性スコア計算（相談内容も考慮）"""
        # 太陽星座と月星座の相性を基にスコアを計算
        sun_sign1 = self._convert_sign_name(horoscope1.get('sun_sign', 'Aries'))
        sun_sign2 = self._convert_sign_name(horoscope2.get('sun_sign', 'Aries'))
        moon_sign1 = self._convert_sign_name(horoscope1.get('moon_sign', 'Cancer'))
        moon_sign2 = self._convert_sign_name(horoscope2.get('moon_sign', 'Cancer'))
        
        # 星座の相性マトリックス（拡張版）
        compatibility_matrix = {
            'Aries': {'Aries': 60, 'Leo': 90, 'Sagittarius': 85, 'Gemini': 70, 'Aquarius': 75, 'Cancer': 40, 'Scorpio': 45, 'Pisces': 50, 'Taurus': 35, 'Virgo': 40, 'Capricorn': 45, 'Libra': 65},
            'Taurus': {'Taurus': 65, 'Virgo': 90, 'Capricorn': 85, 'Cancer': 70, 'Pisces': 75, 'Aries': 35, 'Leo': 40, 'Sagittarius': 45, 'Gemini': 50, 'Libra': 40, 'Aquarius': 45, 'Scorpio': 60},
            'Gemini': {'Gemini': 60, 'Libra': 90, 'Aquarius': 85, 'Aries': 70, 'Leo': 75, 'Cancer': 45, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 50, 'Virgo': 45, 'Capricorn': 40, 'Sagittarius': 65},
            'Cancer': {'Cancer': 65, 'Scorpio': 90, 'Pisces': 85, 'Taurus': 70, 'Virgo': 75, 'Aries': 40, 'Leo': 45, 'Sagittarius': 40, 'Gemini': 45, 'Libra': 50, 'Aquarius': 40, 'Capricorn': 60},
            'Leo': {'Leo': 60, 'Aries': 90, 'Sagittarius': 85, 'Gemini': 70, 'Libra': 75, 'Cancer': 45, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 40, 'Virgo': 45, 'Capricorn': 40, 'Aquarius': 65},
            'Virgo': {'Virgo': 65, 'Taurus': 90, 'Capricorn': 85, 'Cancer': 70, 'Scorpio': 75, 'Aries': 40, 'Leo': 45, 'Sagittarius': 40, 'Gemini': 45, 'Libra': 50, 'Aquarius': 40, 'Pisces': 60},
            'Libra': {'Libra': 60, 'Gemini': 90, 'Aquarius': 85, 'Leo': 70, 'Sagittarius': 75, 'Cancer': 50, 'Scorpio': 45, 'Pisces': 40, 'Taurus': 40, 'Virgo': 50, 'Capricorn': 45, 'Aries': 65},
            'Scorpio': {'Scorpio': 65, 'Cancer': 90, 'Pisces': 85, 'Virgo': 70, 'Capricorn': 75, 'Aries': 45, 'Leo': 40, 'Sagittarius': 35, 'Gemini': 40, 'Libra': 45, 'Aquarius': 40, 'Taurus': 60},
            'Sagittarius': {'Sagittarius': 60, 'Aries': 90, 'Leo': 85, 'Libra': 70, 'Aquarius': 75, 'Cancer': 40, 'Scorpio': 35, 'Pisces': 40, 'Taurus': 45, 'Virgo': 40, 'Capricorn': 45, 'Gemini': 65},
            'Capricorn': {'Capricorn': 65, 'Taurus': 90, 'Virgo': 85, 'Scorpio': 70, 'Pisces': 75, 'Aries': 45, 'Leo': 40, 'Sagittarius': 45, 'Gemini': 40, 'Libra': 45, 'Aquarius': 40, 'Cancer': 60},
            'Aquarius': {'Aquarius': 60, 'Gemini': 90, 'Libra': 85, 'Sagittarius': 70, 'Aries': 75, 'Cancer': 40, 'Scorpio': 40, 'Pisces': 35, 'Taurus': 45, 'Virgo': 40, 'Capricorn': 40, 'Leo': 65},
            'Pisces': {'Pisces': 65, 'Cancer': 90, 'Scorpio': 85, 'Capricorn': 70, 'Taurus': 75, 'Aries': 50, 'Leo': 35, 'Sagittarius': 40, 'Gemini': 35, 'Libra': 40, 'Aquarius': 35, 'Virgo': 60}
        }
        
        # 太陽星座の相性スコア
        sun_score = compatibility_matrix.get(sun_sign1, {}).get(sun_sign2, 50)
        
        # 月星座の相性スコア
        moon_score = compatibility_matrix.get(moon_sign1, {}).get(moon_sign2, 50)
        
        # 太陽星座70%、月星座30%の重みで計算
        base_score = int((sun_score * 0.7) + (moon_score * 0.3))
        
        # 相談内容による調整
        consultation_bonus = 0
        if consultation and consultation.strip():
            if "恋愛" in consultation or "恋" in consultation:
                consultation_bonus = 5  # 恋愛相談は少しボーナス
            elif "結婚" in consultation or "婚" in consultation:
                consultation_bonus = 3  # 結婚相談は少しボーナス
            elif "友情" in consultation or "友" in consultation:
                consultation_bonus = 2  # 友情相談は少しボーナス
            elif "仕事" in consultation or "職" in consultation:
                consultation_bonus = 1  # 仕事相談は少しボーナス
        
        # 最終スコアを計算
        final_score = base_score + consultation_bonus
        
        # スコアを20-100の範囲に調整
        return max(20, min(100, final_score))
