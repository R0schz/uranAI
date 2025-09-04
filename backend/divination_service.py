"""
占い結果生成サービス
数秘術と西洋占星術の結果を統合してAI鑑定文を生成
"""

from typing import Dict, Any, List
from .numerology_calculator import NumerologyCalculator
from .horoscope import HoroscopeCalculator
from .tarot import TarotCalculator
from .ai_analysis import AIAnalysisGenerator
import json
import asyncio
import concurrent.futures

class DivinationService:
    """占い結果生成サービス"""
    
    def __init__(self):
        self.numerology_calculator = NumerologyCalculator()
        self.horoscope_calculator = HoroscopeCalculator()
        self.tarot_calculator = TarotCalculator()
        self.ai_generator = AIAnalysisGenerator()
    
    def _calculate_temporal_fortune_safe(self, profile: Dict[str, Any], target_date: str) -> Dict[str, Any] | None:
        """安全な今日の運勢計算（エラーハンドリング付き）"""
        try:
            return self.numerology_calculator.calculate_temporal_fortune(profile, target_date)
        except Exception as e:
            print(f"Temporal fortune calculation failed: {e}")
            return None
    
    def _extract_target_date_from_consultation(self, consultation: str) -> str | None:
        """相談内容から特定の日付を抽出"""
        if not consultation:
            return None
        
        import re
        from datetime import datetime, timedelta
        
        # 日付パターンを検索
        date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{1,2})月(\d{1,2})日',
            r'(\d{1,2})日',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{1,2})/(\d{1,2})',
            r'(\d{1,2})/(\d{1,2})/(\d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, consultation)
            if match:
                groups = match.groups()
                try:
                    if len(groups) == 3:
                        if len(groups[0]) == 4:  # 年が4桁
                            year, month, day = groups
                        else:  # 月/日/年
                            month, day, year = groups
                    elif len(groups) == 2:
                        if len(groups[0]) == 4:  # 年-月-日
                            year, month, day = groups
                            day = '01'  # 日が指定されていない場合は1日
                        else:  # 月/日
                            month, day = groups
                            year = datetime.now().year
                    else:  # 日のみ
                        day = groups[0]
                        month = datetime.now().month
                        year = datetime.now().year
                    
                    # 日付を構築
                    target_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    
                    # 日付の妥当性をチェック
                    datetime.strptime(target_date, "%Y-%m-%d")
                    return target_date
                except ValueError:
                    continue
        
        # 相対的な日付表現をチェック
        relative_patterns = {
            '今日': 0,
            '明日': 1,
            '明後日': 2,
            '来週': 7,
            '来月': 30
        }
        
        for keyword, days in relative_patterns.items():
            if keyword in consultation:
                target_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                return target_date
        
        return None
    
    def generate_divination_result(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """占い結果を生成"""
        fortune_type = request_data.get('type')
        profiles = request_data.get('profiles', [])
        consultation = request_data.get('consultation', '')
        
        if not profiles:
            raise ValueError("プロフィールデータが必要です")
        
        if fortune_type == 'numerology':
            return self._generate_numerology_result(profiles, consultation)
        elif fortune_type == 'horoscope':
            return self._generate_horoscope_result(profiles, consultation)
        elif fortune_type == 'tarot':
            return self._generate_tarot_result(profiles, consultation)
        elif fortune_type == 'comprehensive':
            return self._generate_comprehensive_result(profiles, consultation)
        else:
            raise ValueError(f"未対応の占術タイプ: {fortune_type}")
    
    def _generate_numerology_result(self, profiles: List[Dict[str, Any]], consultation: str) -> Dict[str, Any]:
        """数秘術の結果を生成"""
        if len(profiles) == 1:
            # 個人占い
            profile = profiles[0]
            
            # 数秘術計算を先に完了（精度を保つため）
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # 数秘術計算、今日の運勢計算、AI分析を並列実行
                numerology_future = executor.submit(self.numerology_calculator.get_numerology_reading, profile)
                
                from datetime import date
                today = date.today().isoformat()
                temporal_future = executor.submit(self._calculate_temporal_fortune_safe, profile, today)
                
                # 数秘術計算の完了を待機
                numerology_data = numerology_future.result()
                temporal_fortune = temporal_future.result()
                
                # AI分析を並列実行（数秘術データが揃った後）
                ai_future = executor.submit(self.ai_generator.generate_numerology_analysis, numerology_data, consultation)
                
                # ビジュアル結果を生成
                visual_result = self._generate_numerology_visual(numerology_data)
                
                # AI分析の完了を待機
                ai_analysis = ai_future.result()
            
            return {
                'fortune_type': 'numerology',
                'purpose': 'personal',
                'numerology_data': numerology_data,
                'temporal_fortune': temporal_fortune,
                'ai_analysis': ai_analysis,
                'visual_result': visual_result
            }
        else:
            # 相性占い（並列処理最適化）
            print(f"Generating compatibility numerology result for {len(profiles)} profiles")
            profile1, profile2 = profiles[0], profiles[1]
            print(f"Profile 1: {profile1}")
            print(f"Profile 2: {profile2}")
            
            try:
                # 並列処理で相性分析を実行
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    compatibility_future = executor.submit(self.numerology_calculator.get_compatibility_analysis, profile1, profile2, consultation)
                    compatibility_data = compatibility_future.result()
                
                print(f"Compatibility data generated: {compatibility_data}")
                # AI analysis is now handled within get_compatibility_analysis
                ai_analysis = compatibility_data.get('analysis', '相性分析を生成中です...')
                # 後処理チェックを適用
                if ai_analysis:
                    ai_analysis = self.ai_generator._fix_nickname_usage(
                        ai_analysis, 
                        profile1.get('nickname', 'あなた'), 
                        profile2.get('nickname', '相手')
                    )
                print(f"AI analysis generated for compatibility with consultation: {consultation}")
            except Exception as e:
                print(f"Error in compatibility analysis: {e}")
                import traceback
                traceback.print_exc()
                raise
            
            return {
                'fortune_type': 'numerology',
                'purpose': 'compatibility',
                'compatibility_data': compatibility_data,
                'ai_analysis': ai_analysis,
                'visual_result': self._generate_compatibility_visual(compatibility_data, 'numerology')
            }
    
    def _generate_horoscope_result(self, profiles: List[Dict[str, Any]], consultation: str) -> Dict[str, Any]:
        """西洋占星術の結果を生成（AI判断によるトランジット法対応）"""
        if len(profiles) == 1:
            # 個人占い（並列処理最適化）
            profile = profiles[0]
            
            # AIにトランジット法を使用すべきか判断させる
            should_use_transit = self.ai_generator.should_use_transit_method(consultation)
            target_date = None
            
            if should_use_transit:
                # AIに日時を推測させる
                target_date = self.ai_generator.predict_target_date(consultation)
                print(f"AI判断: トランジット法を使用、対象日時: {target_date}")
            else:
                print(f"AI判断: 通常のホロスコープ計算を使用")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                if target_date:
                    # トランジット法を使用
                    horoscope_future = executor.submit(self.horoscope_calculator.calculate_transit_horoscope, profile, target_date)
                else:
                    # 通常のホロスコープ計算
                    horoscope_future = executor.submit(self.horoscope_calculator.calculate_horoscope, profile)
                
                horoscope_data = horoscope_future.result()
                
                # ニックネームを追加
                horoscope_data['nickname'] = profile.get('nickname', 'あなた')
                
                # AI分析を並列実行
                ai_future = executor.submit(self.ai_generator.generate_horoscope_analysis, horoscope_data, consultation)
                ai_analysis = ai_future.result()
            
            return {
                'fortune_type': 'horoscope',
                'purpose': 'personal',
                'horoscope_data': horoscope_data,
                'ai_analysis': ai_analysis,
                'visual_result': self._generate_horoscope_visual(horoscope_data)
            }
        else:
            # 相性占い（並列処理最適化）
            profile1, profile2 = profiles[0], profiles[1]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                compatibility_future = executor.submit(self.horoscope_calculator.get_compatibility_analysis, profile1, profile2, consultation)
                compatibility_data = compatibility_future.result()
            
            # AI分析は既にcompatibility_dataに含まれているが、後処理チェックを適用
            ai_analysis = compatibility_data.get('analysis', '')
            if ai_analysis:
                # 後処理チェックを適用
                ai_analysis = self.ai_generator._fix_nickname_usage(
                    ai_analysis, 
                    profile1.get('nickname', 'あなた'), 
                    profile2.get('nickname', '相手')
                )
            
            return {
                'fortune_type': 'horoscope',
                'purpose': 'compatibility',
                'compatibility_data': compatibility_data,
                'ai_analysis': ai_analysis,
                'visual_result': self._generate_compatibility_visual(compatibility_data, 'horoscope')
            }
    
    def _generate_tarot_result(self, profiles: List[Dict[str, Any]], consultation: str) -> Dict[str, Any]:
        """タロット占いの結果を生成（並列処理で高速化）"""
        if len(profiles) == 1:
            # 個人占い
            profile = profiles[0]
            nickname = profile.get('nickname', 'あなた')
            
            # タロット計算とAI分析を並列実行
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # タロット計算を開始
                tarot_future = executor.submit(self.tarot_calculator.perform_tarot_reading, consultation, nickname)
                
                # タロット計算の完了を待機
                tarot_data = tarot_future.result()
                
                # AI分析を並列実行（タロットデータが揃った後）
                ai_future = executor.submit(self.ai_generator.generate_tarot_analysis, tarot_data, consultation)
                
                # ビジュアル結果を生成（並列）
                visual_future = executor.submit(self._generate_tarot_visual, tarot_data)
                
                # 結果を取得
                ai_analysis = ai_future.result()
                visual_result = visual_future.result()
            
            return {
                'fortune_type': 'tarot',
                'purpose': 'personal',
                'tarot_data': tarot_data,
                'ai_analysis': ai_analysis,
                'visual_result': visual_result
            }
        else:
            # 相性占い
            profile1, profile2 = profiles[0], profiles[1]
            
            # 相性タロット計算とAI分析を並列実行
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # 相性タロット計算を開始
                tarot_future = executor.submit(self.tarot_calculator.get_compatibility_analysis, profile1, profile2, consultation)
                
                # タロット計算の完了を待機
                tarot_data = tarot_future.result()
                
                # AI分析を並列実行（タロットデータが揃った後）
                ai_future = executor.submit(self.ai_generator.generate_compatibility_analysis, tarot_data, 'tarot', consultation)
                
                # ビジュアル結果を生成（並列）
                visual_future = executor.submit(self._generate_tarot_compatibility_visual, tarot_data)
                
                # 結果を取得
                ai_analysis = ai_future.result()
                visual_result = visual_future.result()
            
            return {
                'fortune_type': 'tarot',
                'purpose': 'compatibility',
                'compatibility_data': tarot_data,
                'ai_analysis': ai_analysis,
                'visual_result': visual_result
            }
    
    def _generate_comprehensive_result(self, profiles: List[Dict[str, Any]], consultation: str) -> Dict[str, Any]:
        """総合占いの結果を生成"""
        if len(profiles) == 1:
            # 個人占い
            profile = profiles[0]
            
            # 数秘術と西洋占星術の両方を計算
            numerology_data = self.numerology_calculator.get_numerology_reading(profile)
            horoscope_data = self.horoscope_calculator.calculate_horoscope(profile)
            
            # 総合的なAI分析を生成
            ai_analysis = self._generate_comprehensive_analysis(numerology_data, horoscope_data, consultation)
            
            return {
                'fortune_type': 'comprehensive',
                'purpose': 'personal',
                'numerology_data': numerology_data,
                'horoscope_data': horoscope_data,
                'ai_analysis': ai_analysis,
                'visual_result': self._generate_comprehensive_visual(numerology_data, horoscope_data)
            }
        else:
            # 相性占い
            profile1, profile2 = profiles[0], profiles[1]
            
            # 数秘術と西洋占星術の相性分析
            numerology_compatibility = self.numerology_calculator.get_compatibility_analysis(profile1, profile2, consultation)
            # fortune_typeを追加
            numerology_compatibility['fortune_type'] = 'numerology'
            horoscope_compatibility = self.horoscope_calculator.get_compatibility_analysis(profile1, profile2, consultation)
            # fortune_typeを追加
            horoscope_compatibility['fortune_type'] = 'horoscope'
            
            # 総合的な相性分析を生成
            ai_analysis = self._generate_comprehensive_compatibility_analysis(
                numerology_compatibility, horoscope_compatibility, consultation
            )
            
            return {
                'fortune_type': 'comprehensive',
                'purpose': 'compatibility',
                'numerology_compatibility': numerology_compatibility,
                'horoscope_compatibility': horoscope_compatibility,
                'ai_analysis': ai_analysis,
                'visual_result': self._generate_comprehensive_compatibility_visual(
                    numerology_compatibility, horoscope_compatibility
                )
            }
    
    def _generate_numerology_visual(self, numerology_data: Dict[str, Any]) -> Dict[str, Any]:
        """数秘術のビジュアル結果を生成"""
        return {
            'type': 'numerology',
            'numbers': {
                'life_path': numerology_data['life_path']['number'],
                'destiny': numerology_data['destiny']['number'],
                'soul': numerology_data['soul']['number'],
                'personal': numerology_data['personal']['number'],
                'birthday': numerology_data['birthday']['number'],
                'maturity': numerology_data['maturity']['number']
            },
            'chart_data': {
                'labels': ['ライフパス', 'ディスティニー', 'ソウル', 'パーソナル', 'バースデー', 'マチュリティー'],
                'values': [
                    numerology_data['life_path']['number'],
                    numerology_data['destiny']['number'],
                    numerology_data['soul']['number'],
                    numerology_data['personal']['number'],
                    numerology_data['birthday']['number'],
                    numerology_data['maturity']['number']
                ]
            }
        }
    
    def _generate_horoscope_visual(self, horoscope_data: Dict[str, Any]) -> Dict[str, Any]:
        """西洋占星術のビジュアル結果を生成"""
        return {
            'type': 'horoscope',
            'signs': {
                'sun': horoscope_data['sun_sign'],
                'moon': horoscope_data['moon_sign'],
                'rising': horoscope_data['rising_sign']
            },
            'planets': horoscope_data['planets'],
            'aspects': horoscope_data['aspects'],
            'chart_data': {
                'sun': {
                    'sign': horoscope_data['sun_sign'],
                    'degree': horoscope_data['planets']['sun']['degree'],
                    'symbol': self._get_sign_symbol(horoscope_data['sun_sign'])
                },
                'moon': {
                    'sign': horoscope_data['moon_sign'],
                    'degree': horoscope_data['planets']['moon']['degree'],
                    'symbol': self._get_sign_symbol(horoscope_data['moon_sign'])
                },
                'rising': {
                    'sign': horoscope_data['rising_sign'],
                    'degree': 0,  # 上昇星座の度数は通常0度
                    'symbol': self._get_sign_symbol(horoscope_data['rising_sign'])
                }
            }
        }
    
    def _get_sign_symbol(self, sign: str) -> str:
        """星座のシンボルを取得"""
        symbols = {
            'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
            'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
            'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'
        }
        return symbols.get(sign, '?')
    
    def _generate_compatibility_visual(self, compatibility_data: Dict[str, Any], fortune_type: str) -> Dict[str, Any]:
        """相性のビジュアル結果を生成"""
        if fortune_type == 'numerology':
            return {
                'type': 'numerology_compatibility',
                'score': compatibility_data['compatibility_score'],
                'person1_numbers': {
                    'life_path': compatibility_data['person1']['life_path']['number'],
                    'destiny': compatibility_data['person1']['destiny']['number']
                },
                'person2_numbers': {
                    'life_path': compatibility_data['person2']['life_path']['number'],
                    'destiny': compatibility_data['person2']['destiny']['number']
                }
            }
        else:  # horoscope
            return {
                'type': 'horoscope_compatibility',
                'score': compatibility_data['compatibility_score'],
                'person1_signs': {
                    'sun': compatibility_data['person1']['sun_sign'],
                    'moon': compatibility_data['person1']['moon_sign'],
                    'rising': compatibility_data['person1']['rising_sign']
                },
                'person2_signs': {
                    'sun': compatibility_data['person2']['sun_sign'],
                    'moon': compatibility_data['person2']['moon_sign'],
                    'rising': compatibility_data['person2']['rising_sign']
                },
                'chart_data': {
                    'person1': {
                        'sun': {
                            'sign': compatibility_data['person1']['sun_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person1']['sun_sign'])
                        },
                        'moon': {
                            'sign': compatibility_data['person1']['moon_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person1']['moon_sign'])
                        },
                        'rising': {
                            'sign': compatibility_data['person1']['rising_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person1']['rising_sign'])
                        }
                    },
                    'person2': {
                        'sun': {
                            'sign': compatibility_data['person2']['sun_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person2']['sun_sign'])
                        },
                        'moon': {
                            'sign': compatibility_data['person2']['moon_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person2']['moon_sign'])
                        },
                        'rising': {
                            'sign': compatibility_data['person2']['rising_sign'],
                            'symbol': self._get_sign_symbol(compatibility_data['person2']['rising_sign'])
                        }
                    }
                }
            }
    
    def _generate_comprehensive_visual(self, numerology_data: Dict[str, Any], horoscope_data: Dict[str, Any]) -> Dict[str, Any]:
        """総合占いのビジュアル結果を生成"""
        return {
            'type': 'comprehensive',
            'numerology': self._generate_numerology_visual(numerology_data),
            'horoscope': self._generate_horoscope_visual(horoscope_data)
        }
    
    def _generate_comprehensive_compatibility_visual(self, numerology_compatibility: Dict[str, Any], horoscope_compatibility: Dict[str, Any]) -> Dict[str, Any]:
        """総合相性のビジュアル結果を生成"""
        return {
            'type': 'comprehensive_compatibility',
            'numerology': self._generate_compatibility_visual(numerology_compatibility, 'numerology'),
            'horoscope': self._generate_compatibility_visual(horoscope_compatibility, 'horoscope')
        }
    
    def _generate_comprehensive_analysis(self, numerology_data: Dict[str, Any], horoscope_data: Dict[str, Any], consultation: str) -> str:
        """総合的なAI分析を生成"""
        try:
            # 数秘術と西洋占星術の分析を統合
            numerology_analysis = self.ai_generator.generate_numerology_analysis(numerology_data, consultation)
            horoscope_analysis = self.ai_generator.generate_horoscope_analysis(horoscope_data, consultation)
            
            # 統合された分析を生成
            prompt = f"""
あなたは経験豊富な占い師です。以下の数秘術と西洋占星術の分析を統合して、総合的な鑑定文を生成してください。

【数秘術分析】
{numerology_analysis}

【西洋占星術分析】
{horoscope_analysis}

【相談内容】
{consultation if consultation else "一般的な運勢について"}

以下の形式で総合的な鑑定文を生成してください：
1. 全体的な性格と特徴（数秘術と西洋占星術の共通点）
2. 人生の方向性と使命
3. 恋愛・人間関係
4. 仕事・キャリア
5. 今後のアドバイス

温かみがあり、希望を与える内容で、具体的で実用的なアドバイスを含めてください。
"""
            
            response = self.ai_generator.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"総合分析生成エラー: {e}")
            return f"""
【総合占い結果】

数秘術と西洋占星術の両方から、あなたの人生の可能性を探りました。

数秘術では、ライフパスナンバー{numerology_data['life_path']['number']}が示すように、
あなたには特別な使命があります。

西洋占星術では、{horoscope_data['sun_sign']}の太陽星座が示すように、
あなたの基本的な性格は{self._get_sign_meaning(horoscope_data['sun_sign'])}です。

この二つの占術が示す共通点を活かして、充実した人生を送っていきましょう。
"""
    
    def _generate_comprehensive_compatibility_analysis(self, numerology_compatibility: Dict[str, Any], horoscope_compatibility: Dict[str, Any], consultation: str = "") -> str:
        """総合的な相性分析を生成"""
        try:
            # 数秘術と西洋占星術の相性分析を統合
            numerology_analysis = self.ai_generator.generate_compatibility_analysis(numerology_compatibility, 'numerology', consultation)
            horoscope_analysis = self.ai_generator.generate_compatibility_analysis(horoscope_compatibility, 'horoscope', consultation)
            
            # 統合された相性分析を生成
            prompt = f"""
あなたは経験豊富な占い師です。以下の数秘術と西洋占星術の相性分析を統合して、総合的な相性鑑定文を生成してください。

【数秘術相性分析】
{numerology_analysis}

【西洋占星術相性分析】
{horoscope_analysis}

【相談内容】
{consultation if consultation else "一般的な相性について"}

以下の形式で総合的な相性鑑定文を生成してください：
1. 全体的な相性の評価
2. お互いの強みと補完関係
3. 恋愛・結婚における相性
4. 友情・ビジネスにおける相性
5. 関係を深めるためのアドバイス

相談内容を踏まえて、温かみがあり、建設的なアドバイスを含めてください。
"""
            
            response = self.ai_generator.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"総合相性分析生成エラー: {e}")
            return f"""
【総合相性分析結果】

数秘術と西洋占星術の両方から、お二人の相性を分析しました。

数秘術では、相性スコア{numerology_compatibility['compatibility_score']}/100で、
お二人のライフパスナンバーが示す相性があります。

西洋占星術では、相性スコア{horoscope_compatibility['compatibility_score']}/100で、
お二人の星座の組み合わせが示す相性があります。

この二つの占術が示す相性を活かして、素晴らしい関係を築いていきましょう。
"""
    
    def _get_sign_meaning(self, sign: str) -> str:
        """星座の意味を取得"""
        meanings = {
            'Aries': '情熱的でリーダーシップがある',
            'Taurus': '安定感があり、実用的',
            'Gemini': '好奇心旺盛でコミュニケーション能力が高い',
            'Cancer': '感情的で家族を大切にする',
            'Leo': '創造的で自信に満ちている',
            'Virgo': '分析的で完璧主義',
            'Libra': 'バランス感覚があり、調和を求める',
            'Scorpio': '神秘的で情熱的',
            'Sagittarius': '冒険的で哲学的な思考',
            'Capricorn': '責任感が強く、目標志向',
            'Aquarius': '革新的で独立心が強い',
            'Pisces': '直感的で共感力が高い'
        }
        return meanings.get(sign, '特別な意味')
    
    def _generate_tarot_visual(self, tarot_data: Dict[str, Any]) -> Dict[str, Any]:
        """タロット占いのビジュアル結果を生成"""
        return {
            'type': 'tarot',
            'spread_name': tarot_data.get('spread_name', 'タロットスプレッド'),
            'drawn_cards': tarot_data.get('drawn_cards', []),
            'question': tarot_data.get('question', ''),
            'nickname': tarot_data.get('nickname', 'あなた')
        }
    
    def _generate_tarot_compatibility_visual(self, tarot_data: Dict[str, Any]) -> Dict[str, Any]:
        """タロット相性占いのビジュアル結果を生成"""
        return {
            'type': 'tarot_compatibility',
            'spread_name': tarot_data.get('spread_name', 'ケルト十字'),
            'drawn_cards': tarot_data.get('drawn_cards', []),
            'compatibility_score': tarot_data.get('compatibility_score', 50),
            'person1_nickname': tarot_data.get('person1_nickname', '人物1'),
            'person2_nickname': tarot_data.get('person2_nickname', '人物2'),
            'consultation': tarot_data.get('consultation', '')
        }
