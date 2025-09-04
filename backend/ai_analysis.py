"""
AI鑑定文生成機能
Groq/compound-miniを使用した鑑定文生成
"""

import google.generativeai as genai
from groq import Groq
from typing import Dict, Any, List
import os
import concurrent.futures
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local')

class AIAnalysisGenerator:
    """AI鑑定文生成クラス"""
    
    def __init__(self):
        # Google Gemini APIキーを設定（フォールバック用）
        gemini_api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        else:
            self.gemini_model = None
        
        # Groq APIキーを設定
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            raise ValueError("GROQ_API_KEYが設定されていません")
        
        self.groq_client = Groq(api_key=groq_api_key)
        self.groq_model = "llama-3.3-70b-versatile"
        
        # キャッシュ機能を追加（メモリ効率化）
        self._cache = {}
        self._cache_size_limit = 100  # キャッシュサイズ制限
        self._processing_requests = set()  # 処理中のリクエストを追跡
        
        # AIスコア生成の設定（環境変数で制御可能）
        self.use_ai_scoring = os.getenv('USE_AI_SCORING', 'true').lower() == 'true'
        
        # 並列処理用のスレッドプール
        import concurrent.futures
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    
    def __del__(self):
        """リソースクリーンアップ"""
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=False)
    
    def _generate_with_groq(self, prompt: str, max_tokens: int = 1000) -> str:
        """Groqを使用してテキストを生成（判断・推測用）"""
        try:
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": "あなたは専門的な占い師です。日本語で丁寧に回答してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq生成エラー: {e}")
            # フォールバック: Geminiを使用
            if self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    return response.text.strip()
                except Exception as gemini_error:
                    print(f"Gemini生成エラー: {gemini_error}")
                    return self._get_timeout_message()
            else:
                return self._get_timeout_message()
    
    def _generate_analysis_with_gemini(self, prompt: str) -> str:
        """Gemini 2.5 Flash Liteを使用して鑑定文を生成"""
        try:
            if not self.gemini_model:
                raise ValueError("Gemini model not available")
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Gemini鑑定文生成エラー: {e}")
            # フォールバック: Groqを使用
            try:
                return self._generate_with_groq(prompt, max_tokens=1000)
            except Exception as groq_error:
                print(f"Groqフォールバックエラー: {groq_error}")
                return self._get_timeout_message()
    
    def generate_numerology_analysis(self, numerology_data: Dict[str, Any], consultation: str = "") -> str:
        """数秘術の鑑定文を生成"""
        # キャッシュキーを生成
        cache_key = f"numerology_{numerology_data['life_path']['number']}_{numerology_data['destiny']['number']}_{numerology_data['soul']['number']}_{numerology_data['personal']['number']}_{numerology_data['birthday']['number']}_{numerology_data['maturity']['number']}_{consultation}"
        
        # キャッシュから取得を試行
        if cache_key in self._cache:
            print(f"AI分析をキャッシュから取得: {cache_key}")
            return self._cache[cache_key]
        
        # キャッシュサイズ制限チェック
        if len(self._cache) >= self._cache_size_limit:
            # 古いキャッシュエントリを削除（FIFO）
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        # 処理中のリクエストをチェック（重複防止）
        if cache_key in self._processing_requests:
            print(f"AI分析が既に処理中: {cache_key}")
            return self._get_default_numerology_analysis(numerology_data)
        
        # 処理中フラグを設定
        self._processing_requests.add(cache_key)
        
        # ニックネームを取得（プロファイルデータから）
        nickname = numerology_data.get('nickname', 'あなた')
        
        prompt = f"""数秘術師として、{nickname}さんの数秘術を分析してください。

数秘術: LP{numerology_data['life_path']['number']}, D{numerology_data['destiny']['number']}, S{numerology_data['soul']['number']}, P{numerology_data['personal']['number']}, B{numerology_data['birthday']['number']}, M{numerology_data['maturity']['number']}

相談: {consultation if consultation else "今日の運勢について"}

500文字以内で、{nickname}さんに向けた温かい鑑定文を生成してください。"""
        
        try:
            print(f"AI分析を新規生成: {cache_key}")
            print(f"プロンプト: {prompt[:100]}...")
            
            # タイムアウト処理付きでAI分析を実行（並列処理最適化）
            future = self._executor.submit(self._generate_analysis_with_gemini, prompt)
            result = future.result(timeout=25)  # 25秒に短縮
                
            print(f"AI分析完了: {len(result)}文字")
                
            # キャッシュに保存
            self._cache[cache_key] = result
            return result
            
        except concurrent.futures.TimeoutError:
            print("AI数秘術分析タイムアウト（25秒）")
            return self._get_timeout_message()
        except Exception as e:
            print(f"AI鑑定文生成エラー: {e}")
            print(f"エラーの詳細: {type(e).__name__}: {str(e)}")
            return self._get_default_numerology_analysis(numerology_data)
        finally:
            # 処理中フラグをクリア
            self._processing_requests.discard(cache_key)
    
    def generate_horoscope_analysis(self, horoscope_data: Dict[str, Any], consultation: str = "") -> str:
        """西洋占星術の鑑定文を生成"""
        # キャッシュキーを生成
        cache_key = f"horoscope_{horoscope_data.get('sun_sign', '')}_{horoscope_data.get('moon_sign', '')}_{horoscope_data.get('rising_sign', '')}_{consultation}"
        
        # キャッシュから取得を試行
        if cache_key in self._cache:
            print(f"AI分析をキャッシュから取得: {cache_key}")
            return self._cache[cache_key]
        
        # 処理中のリクエストをチェック（重複防止）
        if cache_key in self._processing_requests:
            print(f"AI分析が既に処理中: {cache_key}")
            return self._get_default_horoscope_analysis(horoscope_data)
        
        # 処理中フラグを設定
        self._processing_requests.add(cache_key)
        
        sun_sign = horoscope_data.get('sun_sign', 'Aries')
        moon_sign = horoscope_data.get('moon_sign', 'Cancer')
        rising_sign = horoscope_data.get('rising_sign', 'Leo')
        
        # ニックネームを取得
        nickname = horoscope_data.get('nickname', 'あなた')
        
        prompt = f"""西洋占星術師として、{nickname}さんのホロスコープを分析してください。

ホロスコープ: 太陽{sun_sign}, 月{moon_sign}, 上昇{rising_sign}

相談: {consultation if consultation else "今日の運勢について"}

500文字以内で、{nickname}さんに向けた温かい鑑定文を生成してください。"""
        
        try:
            print(f"AI分析を新規生成: {cache_key}")
            print(f"プロンプト: {prompt[:100]}...")
            
            # タイムアウト処理付きでAI分析を実行（並列処理最適化）
            future = self._executor.submit(self._generate_analysis_with_gemini, prompt)
            result = future.result(timeout=25)  # 25秒に短縮
                
            print(f"AI分析完了: {len(result)}文字")
                
            # キャッシュに保存
            self._cache[cache_key] = result
            return result
        except concurrent.futures.TimeoutError:
            print("AIホロスコープ分析タイムアウト（25秒）")
            return self._get_timeout_message()
        except Exception as e:
            print(f"AI鑑定文生成エラー: {e}")
            print(f"エラーの詳細: {type(e).__name__}: {str(e)}")
            return self._get_default_horoscope_analysis(horoscope_data)
        finally:
            # 処理中フラグをクリア
            self._processing_requests.discard(cache_key)
    
    def generate_tarot_analysis(self, tarot_data: Dict[str, Any], consultation: str = "") -> str:
        """タロット占いの鑑定文を生成"""
        # ニックネームを取得
        nickname = tarot_data.get('nickname', 'あなた')
        
        # カード情報を詳細に構築
        drawn_cards = tarot_data.get('drawn_cards', [])
        spread_name = tarot_data.get('spread_name', 'タロットスプレッド')
        
        cards_info = []
        for i, card in enumerate(drawn_cards):
            card_name = card.get('card_name', '')
            position_name = card.get('position_name', '')
            position_meaning = card.get('position_meaning', '')
            is_reversed = card.get('is_reversed', False)
            card_description = card.get('card_description', '')
            reversed_meaning = card.get('reversed_meaning', '')
            
            # 逆位置の場合は特別に強調
            if is_reversed and reversed_meaning:
                card_text = f"【{position_name}】{card_name}（逆位置）\n意味: {reversed_meaning}\n位置の意味: {position_meaning}"
            else:
                card_text = f"【{position_name}】{card_name}\n意味: {card_description}\n位置の意味: {position_meaning}"
            
            cards_info.append(card_text)
        
        cards_text = "\n\n".join(cards_info)
        
        prompt = f"""あなたは経験豊富なタロット占い師です。以下のタロットカードから温かい鑑定文を生成してください。

【{nickname}さんのタロット占い結果】
スプレッド: {spread_name}

引かれたカード:
{cards_text}

相談内容: {consultation if consultation else "今日の運勢について"}

【重要】
- 逆位置のカードがある場合は、その特別な意味を必ず考慮してください
- 各カードの位置（過去・現在・未来など）の意味も重要です
- {nickname}さんという名前で呼びかけてください

500文字前後で、{nickname}さんに向けた温かい鑑定文を生成してください。
逆位置のカードの意味や、各位置でのカードの意味を適切に解釈し、
具体的で実用的なアドバイスを含めてください。"""
        
        try:
            # タイムアウト設定を追加（タロット分析の高速化）
            future = self._executor.submit(self._generate_analysis_with_gemini, prompt)
            result = future.result(timeout=20)  # 20秒に短縮
            return result
        except Exception as e:
            print(f"AI tarot analysis error: {e}")
            return f"{nickname}さんのタロット占いの鑑定文を生成中です..."

    def generate_comprehensive_analysis(self, comprehensive_data: Dict[str, Any], consultation: str = "") -> str:
        """総合鑑定の鑑定文を生成"""
        # ニックネームを取得
        nickname = comprehensive_data.get('nickname', 'あなた')
        
        prompt = f"""総合占い師として、以下の複数の占術結果から温かい鑑定文を生成してください。

{nickname}さんの総合鑑定:
数秘術: {comprehensive_data.get('numerology', 'データ取得中...')}
ホロスコープ: {comprehensive_data.get('horoscope', 'データ取得中...')}
タロット: {comprehensive_data.get('tarot', 'データ取得中...')}

相談: {consultation if consultation else "今日の運勢について"}

500文字前後で、{nickname}さんに向けた総合鑑定文を生成してください。
複数の占術の結果を統合し、温かく希望的な内容で、具体的で実用的なアドバイスを含めてください。"""
        
        try:
            return self._generate_with_groq(prompt, max_tokens=1000)
        except Exception as e:
            print(f"AI comprehensive analysis error: {e}")
            return f"{nickname}さんの総合鑑定文を生成中です..."

    def generate_compatibility_analysis(self, compatibility_data: Dict[str, Any], fortune_type: str, consultation: str = "") -> str:
        """相性分析の鑑定文を生成"""
        if fortune_type == 'numerology':
            return self._generate_numerology_compatibility(compatibility_data, consultation)
        elif fortune_type == 'horoscope':
            return self._generate_horoscope_compatibility(compatibility_data, consultation)
        elif fortune_type == 'tarot':
            return self._generate_tarot_compatibility(compatibility_data, consultation)
        else:
            return "相性分析を生成中です..."
    
    def _generate_numerology_compatibility(self, data: Dict[str, Any], consultation: str = "") -> str:
        """数秘術相性分析を生成"""
        person1 = data['person1']
        person2 = data['person2']
        score = data.get('compatibility_score', 50)  # デフォルト値を設定
        
        # 簡潔なプロンプトでタイムアウトを回避
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        
        prompt = f"""数秘術師として相性分析してください。

{person1_nickname}: ライフパス{person1['life_path']['number']}, ディスティニー{person1['destiny']['number']}
{person2_nickname}: ライフパス{person2['life_path']['number']}, ディスティニー{person2['destiny']['number']}
相性スコア: {score}/100

相談: {consultation if consultation else "一般的な相性"}

【重要】「{person1_nickname}さん」と「{person2_nickname}さん」のニックネームを使用してください。

500文字以内で、{person1_nickname}さんと{person2_nickname}さんの相性を分析してください。"""
        
        try:
            # タイムアウト設定を追加（並列処理最適化）
            future = self._executor.submit(self._generate_analysis_with_gemini, prompt)
            analysis_text = future.result(timeout=25)  # 25秒に短縮
                
            # ニックネームの後処理チェック
            analysis_text = self._fix_nickname_usage(analysis_text, person1_nickname, person2_nickname)
                
            return analysis_text
        except concurrent.futures.TimeoutError:
            print("AI相性分析タイムアウト（25秒）")
            return self._get_timeout_message()
        except Exception as e:
            print(f"AI相性分析生成エラー: {e}")
            return self._get_fallback_compatibility_analysis(data)
    
    def _get_fallback_compatibility_analysis(self, data: Dict[str, Any]) -> str:
        """フォールバック用の相性分析"""
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        score = data.get('compatibility_score', 50)  # デフォルト値を設定
        fortune_type = data.get('fortune_type', 'numerology')
        
        # 占いの種類に応じた分析
        if fortune_type == 'horoscope':
            if score >= 80:
                return f"{person1_nickname}さんと{person2_nickname}さんは非常に良い相性です。星座のエネルギーが調和し、お互いを高め合える素晴らしい関係を築けるでしょう。"
            elif score >= 60:
                return f"{person1_nickname}さんと{person2_nickname}さんは良い相性です。星座の特性を理解し合えば、安定した関係を築けるでしょう。"
            elif score >= 40:
                return f"{person1_nickname}さんと{person2_nickname}さんは普通の相性です。努力次第で良い関係を築くことができます。星座の違いを理解し合うことが大切です。"
            else:
                return f"{person1_nickname}さんと{person2_nickname}さんの相性には課題があります。お互いの星座の特性を理解し、時間をかけて関係を築いていくことをお勧めします。"
        elif fortune_type == 'tarot':
            if score >= 80:
                return f"{person1_nickname}さんと{person2_nickname}さんは非常に良い相性です。タロットカードが示すように、お互いを高め合える素晴らしい関係を築けるでしょう。"
            elif score >= 60:
                return f"{person1_nickname}さんと{person2_nickname}さんは良い相性です。カードの導きに従い、安定した関係を築けるでしょう。"
            elif score >= 40:
                return f"{person1_nickname}さんと{person2_nickname}さんは普通の相性です。努力次第で良い関係を築くことができます。カードのメッセージを大切にしてください。"
            else:
                return f"{person1_nickname}さんと{person2_nickname}さんの相性には課題があります。カードが示すメッセージを理解し、時間をかけて関係を築いていくことをお勧めします。"
        else:  # numerology
            if score >= 80:
                return f"{person1_nickname}さんと{person2_nickname}さんは非常に良い相性です。数秘術のエネルギーが調和し、お互いを高め合える素晴らしい関係を築けるでしょう。"
            elif score >= 60:
                return f"{person1_nickname}さんと{person2_nickname}さんは良い相性です。数秘術の観点からも、バランスの取れた関係性が期待できます。"
            elif score >= 40:
                return f"{person1_nickname}さんと{person2_nickname}さんは普通の相性です。数秘術のエネルギーを活かして、お互いを理解し合うことが大切です。"
            else:
                return f"{person1_nickname}さんと{person2_nickname}さんの相性には課題があります。数秘術の観点からも、時間をかけて関係を築いていくことをお勧めします。"
    
    def _generate_horoscope_compatibility(self, data: Dict[str, Any], consultation: str = "") -> str:
        """西洋占星術相性分析を生成"""
        person1 = data['person1']
        person2 = data['person2']
        score = data.get('compatibility_score', 50)  # デフォルト値を設定
        
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        
        # 星座名を日本語に変換
        sun_sign1_jp = self._convert_sign_to_japanese(person1['sun_sign'])
        moon_sign1_jp = self._convert_sign_to_japanese(person1['moon_sign'])
        sun_sign2_jp = self._convert_sign_to_japanese(person2['sun_sign'])
        moon_sign2_jp = self._convert_sign_to_japanese(person2['moon_sign'])
        
        prompt = f"""西洋占星術師として、以下の相性を分析してください。

{person1_nickname}: 太陽{sun_sign1_jp}, 月{moon_sign1_jp}
{person2_nickname}: 太陽{sun_sign2_jp}, 月{moon_sign2_jp}
相性スコア: {score}/100

相談内容: {consultation if consultation else "一般的な相性について"}

【重要】「{person1_nickname}さん」と「{person2_nickname}さん」のニックネームを使用してください。

500文字前後で、{person1_nickname}さんと{person2_nickname}さんの相性分析を生成してください。"""
        
        try:
            analysis_text = self._generate_with_groq(prompt, max_tokens=1000)
            
            # ニックネームの後処理チェック
            analysis_text = self._fix_nickname_usage(analysis_text, person1_nickname, person2_nickname)
            
            return analysis_text
        except Exception as e:
            print(f"AI相性分析生成エラー: {e}")
            return self._get_fallback_compatibility_analysis(data)
    
    def _generate_tarot_compatibility(self, data: Dict[str, Any], consultation: str = "") -> str:
        """タロット相性分析を生成"""
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        compatibility_score = data.get('compatibility_score', 50)
        
        # カード情報を詳細に構築
        drawn_cards = data.get('drawn_cards', [])
        spread_name = data.get('spread_name', 'ケルト十字')
        
        cards_info = []
        for i, card in enumerate(drawn_cards):
            card_name = card.get('card_name', '')
            position_name = card.get('position_name', '')
            position_meaning = card.get('position_meaning', '')
            is_reversed = card.get('is_reversed', False)
            card_description = card.get('card_description', '')
            reversed_meaning = card.get('reversed_meaning', '')
            
            # 逆位置の場合は特別に強調
            if is_reversed and reversed_meaning:
                card_text = f"【{position_name}】{card_name}（逆位置）\n意味: {reversed_meaning}\n位置の意味: {position_meaning}"
            else:
                card_text = f"【{position_name}】{card_name}\n意味: {card_description}\n位置の意味: {position_meaning}"
            
            cards_info.append(card_text)
        
        cards_text = "\n\n".join(cards_info)
        
        prompt = f"""あなたは経験豊富なタロット占い師です。以下の相性タロットから温かい相性分析を生成してください。

【{person1_nickname}さんと{person2_nickname}さんの相性タロット】
スプレッド: {spread_name}
相性スコア: {compatibility_score}/100

引かれたカード:
{cards_text}

相談内容: {consultation if consultation else "一般的な相性について"}

【重要】
- 逆位置のカードがある場合は、その特別な意味を必ず考慮してください
- 各カードの位置（現在・過去・未来など）の意味も重要です
- 必ず「{person1_nickname}さん」と「{person2_nickname}さん」のニックネームを使用してください
- 相性スコアも参考にしてください

500文字前後で、{person1_nickname}さんと{person2_nickname}さんの相性分析を生成してください。
逆位置のカードの意味や、各位置でのカードの意味を適切に解釈し、
具体的で実用的なアドバイスを含めてください。"""
        
        try:
            # タイムアウト設定を追加（相性タロット分析の高速化）
            future = self._executor.submit(self._generate_analysis_with_gemini, prompt)
            result = future.result(timeout=20)  # 20秒に短縮
            return result
        except Exception as e:
            print(f"AI相性分析生成エラー: {e}")
            return self._get_fallback_compatibility_analysis(data)
    
    def _get_sign_meaning(self, sign: str) -> str:
        """星座の意味を取得"""
        meanings = {
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
        return meanings.get(sign, f'{sign} - 特別な意味')
    
    def _get_default_numerology_analysis(self, numerology_data: Dict[str, Any]) -> str:
        """デフォルトの数秘術鑑定文"""
        life_path = numerology_data['life_path']['number']
        return f"""
【数秘術鑑定結果】

あなたのライフパスナンバーは{life_path}です。
この数字は、あなたの人生の方向性と使命を示しています。

{self._get_number_analysis(life_path)}

数秘術は、あなたの潜在能力と人生の可能性を教えてくれます。
今日から、この数字の力を意識して生活してみてください。
"""
    
    def _get_default_horoscope_analysis(self, horoscope_data: Dict[str, Any]) -> str:
        """デフォルトの西洋占星術鑑定文"""
        sun_sign = horoscope_data.get('sun_sign', 'Aries')
        return f"""
【西洋占星術鑑定結果】

あなたの太陽星座は{sun_sign}です。
この星座は、あなたの基本的な性格とアイデンティティを示しています。

{self._get_sign_analysis(sun_sign)}

ホロスコープは、あなたの人生の可能性を教えてくれます。
今日から、この星座の特性を活かして生活してみてください。
"""
    
    def _get_number_analysis(self, number: int) -> str:
        """数字の分析を取得"""
        analyses = {
            1: "リーダーシップと創造性に満ちた人生が待っています。独立心を大切にし、新しい道を切り開いていきましょう。",
            2: "協調性とバランス感覚があなたの強みです。周囲との調和を大切にし、平和な関係を築いていきましょう。",
            3: "表現力と創造性が豊かな人生が約束されています。芸術やコミュニケーションの分野で才能を発揮できるでしょう。",
            4: "安定と実用性を重視する人生です。着実に努力を重ね、長期的な目標に向かって進んでいきましょう。",
            5: "自由と変化に満ちた人生が待っています。新しい経験を恐れず、冒険心を持って挑戦していきましょう。",
            6: "責任感と愛情深さがあなたの特徴です。家族や周囲の人々を大切にし、調和の取れた関係を築いていきましょう。",
            7: "精神性と内省的な人生が約束されています。深い思考と直感を大切にし、内面の成長を目指していきましょう。",
            8: "成功と物質的達成があなたの目標です。リーダーシップを発揮し、大きな成果を上げることができるでしょう。",
            9: "完成と智慧に満ちた人生です。奉仕の精神を持ち、他者のために行動することで、真の幸せを見つけられるでしょう。",
            11: "直感と啓示に満ちた特別な人生です。スピリチュアルな成長を目指し、高い意識レベルを追求していきましょう。",
            22: "マスタービルダーとしての使命があります。大きな夢を実現し、社会に貢献する人生が待っています。",
            33: "マスターティーチャーとしての特別な使命があります。他者を癒し、導くことで、真の幸せを見つけられるでしょう。"
        }
        return analyses.get(number, "特別な意味を持つ数字です。")
    
    def _get_sign_analysis(self, sign: str) -> str:
        """星座の分析を取得"""
        analyses = {
            'Aries': "情熱的でリーダーシップに満ちた人生が待っています。新しい挑戦を恐れず、積極的に行動していきましょう。",
            'Taurus': "安定感と実用性を重視する人生です。着実に努力を重ね、美しいものを大切にしていきましょう。",
            'Gemini': "好奇心旺盛でコミュニケーション能力が高い人生です。新しい知識を学び、多様な人々と交流していきましょう。",
            'Cancer': "感情的で家族を大切にする人生です。直感を信じ、愛する人々との絆を深めていきましょう。",
            'Leo': "創造的で自信に満ちた人生が約束されています。自己表現を大切にし、周囲を明るく照らしていきましょう。",
            'Virgo': "分析的で完璧主義な人生です。細部にこだわり、実用的な解決策を見つけていきましょう。",
            'Libra': "バランス感覚と調和を求める人生です。美しさと正義を大切にし、平和な関係を築いていきましょう。",
            'Scorpio': "神秘的で情熱的な人生が待っています。深い洞察力を持ち、真実を追求していきましょう。",
            'Sagittarius': "冒険的で哲学的な人生です。新しい文化や思想に触れ、人生の意味を探求していきましょう。",
            'Capricorn': "責任感と目標志向の人生です。長期的な視点を持ち、着実に成功を積み上げていきましょう。",
            'Aquarius': "革新的で独立心が強い人生です。新しいアイデアを大切にし、社会の進歩に貢献していきましょう。",
            'Pisces': "直感的で共感力が高い人生です。芸術やスピリチュアルな分野で才能を発揮し、他者を癒していきましょう。"
        }
        return analyses.get(sign, "特別な意味を持つ星座です。")
    
    def _get_default_horoscope_analysis(self, horoscope_data: Dict[str, Any]) -> str:
        """デフォルトのホロスコープ分析を取得"""
        nickname = horoscope_data.get('nickname', 'あなた')
        sun_sign = horoscope_data.get('sun_sign', 'Aries')
        moon_sign = horoscope_data.get('moon_sign', 'Cancer')
        rising_sign = horoscope_data.get('rising_sign', 'Leo')
        
        return f"""{nickname}さん、こんにちは！西洋占星術師uranAIです。

{nickname}さんのホロスコープを拝見しました。太陽星座が{sun_sign}、月星座が{moon_sign}、上昇星座が{rising_sign}という素晴らしい組み合わせですね。

太陽星座の{sun_sign}は、{self._get_sign_analysis(sun_sign)}

月星座の{moon_sign}は、感情面で{self._get_sign_analysis(moon_sign)}

上昇星座の{rising_sign}は、第一印象として{self._get_sign_analysis(rising_sign)}

{nickname}さんは、これらの星座の特性を活かして、素晴らしい人生を歩んでいけるでしょう。星々からのメッセージを信じて、前向きに進んでいってくださいね。

uranAIは、{nickname}さんの輝く未来を心から応援しています！"""
    
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
    
    def _fix_nickname_usage(self, text: str, person1_nickname: str, person2_nickname: str) -> str:
        """ニックネームの使用を修正する後処理"""
        import re
        
        # 人物1、人物2などの一般的な呼び方をニックネームに置換
        # より具体的なパターンから先に処理する
        replacements = [
            (r'人物1さんさん', f'{person1_nickname}さん'),
            (r'人物2さんさん', f'{person2_nickname}さん'),
            (r'人物1さん', f'{person1_nickname}さん'),
            (r'人物2さん', f'{person2_nickname}さん'),
            (r'人物1', f'{person1_nickname}さん'),
            (r'人物2', f'{person2_nickname}さん'),
            (r'あなたさん', f'{person1_nickname}さん'),
            (r'相手さん', f'{person2_nickname}さん'),
            (r'あなた', f'{person1_nickname}さん'),
            (r'相手', f'{person2_nickname}さん'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def generate_ai_compatibility_score(self, data: Dict[str, Any], fortune_type: str) -> int:
        """AIを使用して相性スコアを生成"""
        # AIスコア生成が無効の場合はデフォルトスコアを返す
        if not self.use_ai_scoring:
            return 50
        
        try:
            if fortune_type == 'numerology':
                return self._generate_numerology_ai_score(data)
            elif fortune_type == 'horoscope':
                return self._generate_horoscope_ai_score(data)
            elif fortune_type == 'tarot':
                return self._generate_tarot_ai_score(data)
            else:
                return 50  # デフォルトスコア
        except Exception as e:
            print(f"AI score generation failed: {e}")
            return 50  # フォールバックスコア
    
    def _generate_numerology_ai_score(self, data: Dict[str, Any]) -> int:
        """数秘術のAI相性スコアを生成"""
        person1 = data['person1']
        person2 = data['person2']
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        consultation = data.get('consultation', '')
        
        prompt = f"""数秘術師として、以下の二人の相性スコアを0-100の整数で算出してください。

{person1_nickname}: LP{person1['life_path']['number']}, D{person1['destiny']['number']}, S{person1['soul']['number']}, P{person1['personal']['number']}
{person2_nickname}: LP{person2['life_path']['number']}, D{person2['destiny']['number']}, S{person2['soul']['number']}, P{person2['personal']['number']}

相談内容: {consultation if consultation else "一般的な相性について"}

数秘術の観点から、お二人の相性を総合的に評価し、0-100の整数でスコアを算出してください。
数値のみを回答してください（例: 75）"""

        try:
            score_text = self._generate_with_groq(prompt, max_tokens=100)
            # 数値のみを抽出
            import re
            score_match = re.search(r'\b(\d{1,3})\b', score_text)
            if score_match:
                score = int(score_match.group(1))
                return max(0, min(100, score))  # 0-100の範囲に制限
            else:
                return 50
        except Exception as e:
            print(f"Numerology AI score generation failed: {e}")
            return 50
    
    def _generate_horoscope_ai_score(self, data: Dict[str, Any]) -> int:
        """ホロスコープのAI相性スコアを生成"""
        person1 = data['person1']
        person2 = data['person2']
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        consultation = data.get('consultation', '')
        
        # 星座名を日本語に変換
        sun_sign1_jp = self._convert_sign_to_japanese(person1['sun_sign'])
        moon_sign1_jp = self._convert_sign_to_japanese(person1['moon_sign'])
        sun_sign2_jp = self._convert_sign_to_japanese(person2['sun_sign'])
        moon_sign2_jp = self._convert_sign_to_japanese(person2['moon_sign'])
        
        prompt = f"""西洋占星術師として、以下の二人の相性スコアを0-100の整数で算出してください。

{person1_nickname}: 太陽{sun_sign1_jp}, 月{moon_sign1_jp}
{person2_nickname}: 太陽{sun_sign2_jp}, 月{moon_sign2_jp}

相談内容: {consultation if consultation else "一般的な相性について"}

西洋占星術の観点から、お二人の相性を総合的に評価し、0-100の整数でスコアを算出してください。
数値のみを回答してください（例: 75）"""

        try:
            score_text = self._generate_with_groq(prompt, max_tokens=100)
            # 数値のみを抽出
            import re
            score_match = re.search(r'\b(\d{1,3})\b', score_text)
            if score_match:
                score = int(score_match.group(1))
                return max(0, min(100, score))  # 0-100の範囲に制限
            else:
                return 50
        except Exception as e:
            print(f"Horoscope AI score generation failed: {e}")
            # フォールバック: 従来のアルゴリズムを使用
            try:
                from horoscope import HoroscopeCalculator
                calculator = HoroscopeCalculator()
                return calculator._calculate_enhanced_compatibility_score(data['person1'], data['person2'], data.get('consultation', ''))
            except Exception as fallback_error:
                print(f"Fallback score calculation failed: {fallback_error}")
                return 50
    
    def _generate_tarot_ai_score(self, data: Dict[str, Any]) -> int:
        """タロットのAI相性スコアを生成"""
        person1_nickname = data.get('person1_nickname', '人物1')
        person2_nickname = data.get('person2_nickname', '人物2')
        consultation = data.get('consultation', '')
        cards = data.get('cards', '相性タロット - カード情報を生成中...')
        
        prompt = f"""タロット占い師として、以下の二人の相性スコアを0-100の整数で算出してください。

{person1_nickname}さんと{person2_nickname}さんの相性タロット
カード: {cards}

相談内容: {consultation if consultation else "一般的な相性について"}

タロットカードの導きから、お二人の相性を総合的に評価し、0-100の整数でスコアを算出してください。
数値のみを回答してください（例: 75）"""

        try:
            score_text = self._generate_with_groq(prompt, max_tokens=100)
            # 数値のみを抽出
            import re
            score_match = re.search(r'\b(\d{1,3})\b', score_text)
            if score_match:
                score = int(score_match.group(1))
                return max(0, min(100, score))  # 0-100の範囲に制限
            else:
                return 50
        except Exception as e:
            print(f"Tarot AI score generation failed: {e}")
            return 50
    
    def _get_timeout_message(self) -> str:
        """AI分析タイムアウト時のメッセージを生成"""
        return """申し訳ございません。AI分析の処理に時間がかかっております。

通信環境の良い場所で再度お試しください。安定したインターネット接続がある場所で占いを実行していただくと、より快適にご利用いただけます。

しばらく時間をおいてから再度お試しください。"""
    
    def should_use_transit_method(self, consultation: str) -> bool:
        """相談内容からトランジット法を使用すべきかAIに判断させる"""
        if not consultation:
            return False
        
        try:
            prompt = f"""あなたは西洋占星術の専門家です。以下の相談内容を分析し、トランジット法（特定の時点での惑星位置分析）を使用すべきかどうかを判断してください。

相談内容: {consultation}

判断基準:
- 特定の日時や期間についての質問（例：「明日の運勢」「来週の仕事」「今年の恋愛」）
- 未来の特定のイベントについて（例：「来月の試験」「年末の旅行」）
- 過去の特定の日時について（例：「先月の出来事」「去年の転職」）
- 季節や時期に関する質問（例：「春の運勢」「夏の恋愛」）

上記のいずれかに該当する場合は「YES」、一般的な性格分析や現在の状況についての質問の場合は「NO」と回答してください。

回答形式: YES または NO"""
            
            result = self._generate_with_groq(prompt, max_tokens=50)
            result = result.strip().upper()
            
            print(f"トランジット法判断結果: {result}")
            return result == "YES"
            
        except Exception as e:
            print(f"トランジット法判断エラー: {e}")
            return False
    
    def predict_target_date(self, consultation: str) -> str:
        """相談内容から対象日時をAIに推測させる"""
        if not consultation:
            return None
        
        try:
            from datetime import datetime, timedelta
            
            prompt = f"""あなたは西洋占星術の専門家です。以下の相談内容を分析し、トランジット法で分析すべき具体的な日時を推測してください。

相談内容: {consultation}

推測の指針:
- 明確な日付が指定されている場合は、その日付を使用
- 相対的な表現（「明日」「来週」「来月」など）の場合は、現在日時から計算
- 季節や時期の表現の場合は、該当する具体的な日付を推測
- イベント名が指定されている場合は、そのイベントの予想日時を推測

現在の日時: {datetime.now().strftime('%Y年%m月%d日 %H時%M分')}

回答形式: YYYY-MM-DD HH:MM の形式で回答してください。
例: 2024-12-25 14:30

推測した日時:"""
            
            result = self._generate_with_groq(prompt, max_tokens=100)
            result = result.strip()
            
            # 日時形式を検証
            try:
                predicted_datetime = datetime.strptime(result, '%Y-%m-%d %H:%M')
                print(f"AI推測日時: {result}")
                return result
            except ValueError:
                print(f"日時形式エラー: {result}")
                # フォールバック: 明日の正午
                tomorrow = datetime.now() + timedelta(days=1)
                fallback_date = tomorrow.strftime('%Y-%m-%d 12:00')
                print(f"フォールバック日時: {fallback_date}")
                return fallback_date
            
        except Exception as e:
            print(f"日時推測エラー: {e}")
            # フォールバック: 明日の正午
            from datetime import datetime, timedelta
            tomorrow = datetime.now() + timedelta(days=1)
            fallback_date = tomorrow.strftime('%Y-%m-%d 12:00')
            print(f"フォールバック日時: {fallback_date}")
            return fallback_date