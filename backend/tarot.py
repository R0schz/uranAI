"""
タロット占いアルゴリズム
JavaScript版を参考にしたPython実装（78枚デッキ対応）
"""

from typing import Dict, Any, List, Optional
import random
import json
import concurrent.futures
from datetime import datetime
from .tarot_data import get_full_tarot_deck, TarotCard, get_card_meaning, get_card_keywords, get_card_image_path, get_reversed_meaning

class TarotPosition:
    """タロット位置クラス"""
    
    def __init__(self, name: str, meaning: str):
        self.name = name
        self.meaning = meaning

class TarotSpread:
    """タロットスプレッドクラス"""
    
    def __init__(self, spread_id: str, name: str, description: str, card_count: int, positions: List[TarotPosition]):
        self.id = spread_id
        self.name = name
        self.description = description
        self.card_count = card_count
        self.positions = positions

class DrawnCard:
    """引かれたカードクラス"""
    
    def __init__(self, card: TarotCard, is_reversed: bool, position: TarotPosition):
        self.card = card
        self.is_reversed = is_reversed
        self.position = position

class TarotCalculator:
    """タロット占い計算クラス"""
    
    def __init__(self):
        self.tarot_deck = get_full_tarot_deck()  # 78枚の完全なデッキ
        self.tarot_spreads = self._initialize_tarot_spreads()
    
    def _initialize_tarot_spreads(self) -> Dict[str, TarotSpread]:
        """タロットスプレッドを初期化"""
        return {
            'threeCards': TarotSpread(
                'threeCards',
                '3枚スプレッド',
                '過去・現在・未来を表す基本的なスプレッド',
                3,
                [
                    TarotPosition('過去', '過去の状況や影響'),
                    TarotPosition('現在', '現在の状況や課題'),
                    TarotPosition('未来', '未来の可能性や方向性')
                ]
            ),
            'celticCross': TarotSpread(
                'celticCross',
                'ケルト十字',
                '詳細な状況分析に適した伝統的なスプレッド',
                10,
                [
                    TarotPosition('現在', '現在の状況'),
                    TarotPosition('課題', '直面している課題'),
                    TarotPosition('過去', '過去の影響'),
                    TarotPosition('未来', '近い未来'),
                    TarotPosition('意識', '意識していること'),
                    TarotPosition('無意識', '無意識の影響'),
                    TarotPosition('希望と恐れ', '希望と恐れ'),
                    TarotPosition('環境', '周囲の環境'),
                    TarotPosition('導き', '内なる導き'),
                    TarotPosition('結果', '最終的な結果')
                ]
            ),
            'horseshoe': TarotSpread(
                'horseshoe',
                '馬蹄形',
                '7枚のカードによる未来予測スプレッド',
                7,
                [
                    TarotPosition('過去', '過去の影響'),
                    TarotPosition('現在', '現在の状況'),
                    TarotPosition('隠れた影響', '隠れた影響要因'),
                    TarotPosition('障害', '直面する障害'),
                    TarotPosition('環境', '周囲の環境'),
                    TarotPosition('希望と恐れ', '希望と恐れ'),
                    TarotPosition('結果', '最終的な結果')
                ]
            )
        }
    
    def shuffle_and_draw(self, count: int) -> List[Dict[str, Any]]:
        """カードをシャッフルして指定された枚数を引く"""
        shuffled = self.tarot_deck.copy()
        random.shuffle(shuffled)
        
        drawn_cards = []
        for i in range(count):
            card = shuffled[i]
            is_reversed = random.random() < 0.5
            drawn_cards.append({
                'card': card,
                'is_reversed': is_reversed
            })
        
        return drawn_cards
    
    def select_optimal_spread(self, question: str) -> str:
        """質問に基づいて最適なスプレッドを選択（AI使用）"""
        try:
            from ai_analysis import AIAnalysisGenerator
            ai_generator = AIAnalysisGenerator()
            
            # 利用可能なスプレッドの説明
            spreads_info = {
                'threeCards': '3枚スプレッド - 過去・現在・未来を表す基本的なスプレッド',
                'celticCross': 'ケルト十字 - 10枚のカードで詳細な分析を行う伝統的なスプレッド',
                'horseshoe': 'ホースシュー - 7枚のカードで未来の流れを読み解くスプレッド'
            }
            
            prompt = f"""あなたは経験豊富なタロット占い師です。以下の質問に対して最適なスプレッドを選択してください。

質問: {question}

利用可能なスプレッド:
1. threeCards: 3枚スプレッド - 過去・現在・未来を表す基本的なスプレッド
2. celticCross: ケルト十字 - 10枚のカードで詳細な分析を行う伝統的なスプレッド  
3. horseshoe: ホースシュー - 7枚のカードで未来の流れを読み解くスプレッド

質問の内容に最も適したスプレッドを選択し、以下の形式で回答してください：
選択したスプレッド: [スプレッドID]

例：
- 一般的な質問や簡単な相談 → threeCards
- 複雑な問題や詳細な分析が必要 → celticCross
- 未来の流れや方向性を知りたい → horseshoe"""

            response_text = ai_generator._generate_with_groq(prompt, max_tokens=200)
            
            # レスポンスからスプレッドIDを抽出
            if 'threeCards' in response_text:
                return 'threeCards'
            elif 'celticCross' in response_text:
                return 'celticCross'
            elif 'horseshoe' in response_text:
                return 'horseshoe'
            else:
                # フォールバック: キーワードベースの選択
                return self._select_spread_by_keywords(question)
                
        except Exception as e:
            print(f"AI spread selection error: {e}")
            # フォールバック: キーワードベースの選択
            return self._select_spread_by_keywords(question)
    
    def _select_spread_by_keywords(self, question: str) -> str:
        """キーワードベースのスプレッド選択（フォールバック）"""
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ['未来', '将来', 'これから', '流れ', '方向']):
            return 'horseshoe'
        elif any(keyword in question_lower for keyword in ['詳細', '詳しく', '分析', '複雑', '深く']):
            return 'celticCross'
        else:
            return 'threeCards'  # デフォルト
    
    def select_compatibility_spread(self, consultation: str) -> str:
        """相性占い用のスプレッドを選択（AI使用）"""
        try:
            from ai_analysis import AIAnalysisGenerator
            ai_generator = AIAnalysisGenerator()
            
            prompt = f"""あなたは経験豊富なタロット占い師です。以下の相性占いの相談に対して最適なスプレッドを選択してください。

相談内容: {consultation if consultation else "一般的な相性について"}

相性占いで利用可能なスプレッド:
1. threeCards: 3枚スプレッド - 過去・現在・未来の関係性を表す基本的なスプレッド
2. celticCross: ケルト十字 - 10枚のカードで詳細な相性分析を行う伝統的なスプレッド  
3. horseshoe: ホースシュー - 7枚のカードで関係の流れを読み解くスプレッド

相談内容に最も適したスプレッドを選択し、以下の形式で回答してください：
選択したスプレッド: [スプレッドID]

例：
- 一般的な相性や簡単な関係性の質問 → threeCards
- 複雑な関係や詳細な相性分析が必要 → celticCross
- 関係の流れや方向性を知りたい → horseshoe"""

            response_text = ai_generator._generate_with_groq(prompt, max_tokens=200)
            
            # レスポンスからスプレッドIDを抽出
            if 'threeCards' in response_text:
                return 'threeCards'
            elif 'celticCross' in response_text:
                return 'celticCross'
            elif 'horseshoe' in response_text:
                return 'horseshoe'
            else:
                # フォールバック: 相性占いでは詳細分析を優先
                return 'celticCross'
                
        except Exception as e:
            print(f"AI compatibility spread selection error: {e}")
            # フォールバック: 相性占いでは詳細分析を優先
            return 'celticCross'
    
    def perform_tarot_reading(self, question: str, nickname: str = "あなた") -> Dict[str, Any]:
        """タロット占いを実行"""
        try:
            # 最適なスプレッドを選択
            spread_id = self.select_optimal_spread(question)
            spread = self.tarot_spreads[spread_id]
            
            # カードを引く
            drawn_raw_cards = self.shuffle_and_draw(spread.card_count)
            
            # 位置情報を付与
            drawn_cards = []
            for i, card_data in enumerate(drawn_raw_cards):
                drawn_card = DrawnCard(
                    card=card_data['card'],
                    is_reversed=card_data['is_reversed'],
                    position=spread.positions[i]
                )
                drawn_cards.append(drawn_card)
            
            # 結果を構築
            result = {
                'question': question,
                'nickname': nickname,
                'spread_name': spread.name,
                'spread_description': spread.description,
                'drawn_cards': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # 引かれたカードの情報を並列で構築
            import concurrent.futures
            
            def build_card_info(drawn_card):
                return {
                    'card_name': drawn_card.card.name,
                    'card_description': get_card_meaning(drawn_card.card, drawn_card.is_reversed),
                    'card_keywords': get_card_keywords(drawn_card.card, drawn_card.is_reversed),
                    'card_suit': drawn_card.card.suit,
                    'card_number': drawn_card.card.number,
                    'card_element': drawn_card.card.element,
                    'card_image_path': get_card_image_path(drawn_card.card),
                    'is_reversed': drawn_card.is_reversed,
                    'reversed_meaning': get_reversed_meaning(drawn_card.card) if drawn_card.is_reversed else None,
                    'position_name': drawn_card.position.name,
                    'position_meaning': drawn_card.position.meaning
                }
            
            # カード情報を並列で構築
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(drawn_cards), 4)) as executor:
                card_futures = [executor.submit(build_card_info, drawn_card) for drawn_card in drawn_cards]
                result['drawn_cards'] = [future.result() for future in card_futures]
            
            return result
            
        except Exception as e:
            print(f"タロット占い実行エラー: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_tarot_result(question, nickname)
    
    def _get_default_tarot_result(self, question: str, nickname: str) -> Dict[str, Any]:
        """デフォルトのタロット結果を返す"""
        return {
            'question': question,
            'nickname': nickname,
            'spread_name': '3枚スプレッド',
            'spread_description': '基本的なスプレッド',
            'drawn_cards': [
                {
                    'card_name': '愚者',
                    'card_description': '新しい始まり、純真さ、冒険心、自由な精神',
                    'card_keywords': ['新しい始まり', '純真さ', '冒険心', '自由', '可能性', '直感'],
                    'card_suit': None,
                    'card_number': 0,
                    'card_element': '風',
                    'card_image_path': '/images/tarot/00-TheFool.jpg',
                    'is_reversed': False,
                    'reversed_meaning': None,
                    'position_name': '過去',
                    'position_meaning': '過去の状況や影響'
                },
                {
                    'card_name': '太陽',
                    'card_description': '成功、喜び、活力、明るさ',
                    'card_keywords': ['成功', '喜び', '活力', '明るさ', '繁栄', '達成'],
                    'card_suit': None,
                    'card_number': 19,
                    'card_element': '火',
                    'card_image_path': '/images/tarot/19-TheSun.jpg',
                    'is_reversed': False,
                    'reversed_meaning': None,
                    'position_name': '現在',
                    'position_meaning': '現在の状況や課題'
                },
                {
                    'card_name': '世界',
                    'card_description': '完成、達成、統合、旅の終わり',
                    'card_keywords': ['完成', '達成', '統合', '旅の終わり', '成功', '満足'],
                    'card_suit': None,
                    'card_number': 21,
                    'card_element': '土',
                    'card_image_path': '/images/tarot/21-TheWorld.jpg',
                    'is_reversed': False,
                    'reversed_meaning': None,
                    'position_name': '未来',
                    'position_meaning': '未来の可能性や方向性'
                }
            ],
            'timestamp': datetime.now().isoformat()
        }
    
    def get_compatibility_analysis(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any], consultation: str = "") -> Dict[str, Any]:
        """相性タロット占いを実行"""
        try:
            # 相性占い用のスプレッドをAIで選択
            spread_id = self.select_compatibility_spread(consultation)
            spread = self.tarot_spreads[spread_id]
            
            # カードを引く
            drawn_raw_cards = self.shuffle_and_draw(spread.card_count)
            
            # 位置情報を付与
            drawn_cards = []
            for i, card_data in enumerate(drawn_raw_cards):
                drawn_card = DrawnCard(
                    card=card_data['card'],
                    is_reversed=card_data['is_reversed'],
                    position=spread.positions[i]
                )
                drawn_cards.append(drawn_card)
            
            # 相性スコアを計算（簡易版）
            compatibility_score = self._calculate_tarot_compatibility_score(drawn_cards)
            
            # 結果を構築
            result = {
                'person1_nickname': profile1_data.get('nickname', 'あなた'),
                'person2_nickname': profile2_data.get('nickname', '相手'),
                'consultation': consultation,
                'spread_name': spread.name,
                'compatibility_score': compatibility_score,
                'drawn_cards': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # 引かれたカードの情報を並列で構築
            def build_compatibility_card_info(drawn_card):
                return {
                    'card_name': drawn_card.card.name,
                    'card_description': get_card_meaning(drawn_card.card, drawn_card.is_reversed),
                    'card_keywords': get_card_keywords(drawn_card.card, drawn_card.is_reversed),
                    'card_suit': drawn_card.card.suit,
                    'card_number': drawn_card.card.number,
                    'card_element': drawn_card.card.element,
                    'card_image_path': get_card_image_path(drawn_card.card),
                    'is_reversed': drawn_card.is_reversed,
                    'reversed_meaning': get_reversed_meaning(drawn_card.card) if drawn_card.is_reversed else None,
                    'position_name': drawn_card.position.name,
                    'position_meaning': drawn_card.position.meaning
                }
            
            # カード情報を並列で構築
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(drawn_cards), 4)) as executor:
                card_futures = [executor.submit(build_compatibility_card_info, drawn_card) for drawn_card in drawn_cards]
                result['drawn_cards'] = [future.result() for future in card_futures]
            
            return result
            
        except Exception as e:
            print(f"相性タロット占い実行エラー: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_compatibility_result(profile1_data, profile2_data, consultation)
    
    def _calculate_tarot_compatibility_score(self, drawn_cards: List[DrawnCard]) -> int:
        """タロットカードから相性スコアを計算（78枚デッキ対応）"""
        try:
            # ポジティブなカードの数をカウント（大アルカナ）
            positive_major_cards = ['太陽', '世界', '星', '恋人', '力', '節制', '正義', '魔術師', '女帝', '皇帝', '愚者', '戦車']
            negative_major_cards = ['塔', '悪魔', '死神', '吊るされた男', '月']
            
            # 小アルカナのポジティブ/ネガティブカード
            positive_minor_cards = ['エース', '2', '3', '6', '9', '10']  # 一般的にポジティブな数字
            negative_minor_cards = ['5', '7', '8']  # 一般的にネガティブな数字
            
            positive_count = 0
            negative_count = 0
            
            for drawn_card in drawn_cards:
                card_name = drawn_card.card.name
                is_reversed = drawn_card.is_reversed
                card_suit = drawn_card.card.suit
                card_number = drawn_card.card.number
                
                # 大アルカナの判定
                if card_suit is None:  # 大アルカナ
                    if card_name in positive_major_cards and not is_reversed:
                        positive_count += 1
                    elif card_name in negative_major_cards or (card_name in positive_major_cards and is_reversed):
                        negative_count += 1
                
                # 小アルカナの判定
                else:
                    number_str = str(card_number) if isinstance(card_number, int) else card_number
                    if number_str in positive_minor_cards and not is_reversed:
                        positive_count += 1
                    elif number_str in negative_minor_cards or (number_str in positive_minor_cards and is_reversed):
                        negative_count += 1
                
                # 逆位置の場合は一般的にネガティブ
                if is_reversed:
                    negative_count += 0.5
            
            # スコアを計算（0-100）
            total_cards = len(drawn_cards)
            if total_cards == 0:
                return 50
            
            positive_ratio = positive_count / total_cards
            negative_ratio = negative_count / total_cards
            
            # ベーススコア50から調整
            base_score = 50
            score_adjustment = (positive_ratio - negative_ratio) * 30
            
            final_score = int(base_score + score_adjustment)
            
            # 0-100の範囲に制限
            return max(0, min(100, final_score))
            
        except Exception as e:
            print(f"タロット相性スコア計算エラー: {e}")
            return 50  # デフォルトスコア
    
    def _get_default_compatibility_result(self, profile1_data: Dict[str, Any], profile2_data: Dict[str, Any], consultation: str) -> Dict[str, Any]:
        """デフォルトの相性タロット結果を返す"""
        return {
            'person1_nickname': profile1_data.get('nickname', 'あなた'),
            'person2_nickname': profile2_data.get('nickname', '相手'),
            'consultation': consultation,
            'spread_name': 'ケルト十字',
            'compatibility_score': 50,
            'drawn_cards': [
                {
                    'card_name': '恋人',
                    'card_description': '愛、選択、調和、関係性',
                    'card_keywords': ['愛', '選択', '調和', '関係', '決断', '結合'],
                    'card_suit': None,
                    'card_number': 6,
                    'card_element': '風',
                    'card_image_path': '/images/tarot/06-TheLovers.jpg',
                    'is_reversed': False,
                    'reversed_meaning': None,
                    'position_name': '現在',
                    'position_meaning': '現在の状況'
                },
                {
                    'card_name': '太陽',
                    'card_description': '成功、喜び、活力、明るさ',
                    'card_keywords': ['成功', '喜び', '活力', '明るさ', '繁栄', '達成'],
                    'card_suit': None,
                    'card_number': 19,
                    'card_element': '火',
                    'card_image_path': '/images/tarot/19-TheSun.jpg',
                    'is_reversed': False,
                    'reversed_meaning': None,
                    'position_name': '結果',
                    'position_meaning': '最終的な結果'
                }
            ],
            'timestamp': datetime.now().isoformat()
        }

# 使用例
if __name__ == "__main__":
    calculator = TarotCalculator()
    
    # 個人占いの例
    result = calculator.perform_tarot_reading("今日の運勢はどうですか？", "太郎")
    print("個人占い結果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 相性占いの例
    profile1 = {'nickname': '花子'}
    profile2 = {'nickname': '太郎'}
    compatibility_result = calculator.get_compatibility_analysis(profile1, profile2, "恋愛の相性について")
    print("\n相性占い結果:")
    print(json.dumps(compatibility_result, ensure_ascii=False, indent=2))
