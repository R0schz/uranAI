"""
数秘術の時間軸エンジン
特定の時点の運勢を算出するためのアルゴリズム
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date
import json

class NumerologyTemporalEngine:
    """数秘術の時間軸エンジン"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初期化
        
        Args:
            config: 設定オブジェクト
                - mode: 'Modern' または 'Pythagorean'
                - masterNumbers: 保持するマスターナンバーのリスト
                - romanizationStandard: ローマ字表記法
        """
        self.config = config or {
            'mode': 'Modern',
            'masterNumbers': [11, 22, 33],
            'romanizationStandard': 'Hepburn'
        }
        
        # アルファベット・数値変換表（ピタゴラス式）
        self.letter_to_number = {
            'A': 1, 'J': 1, 'S': 1,
            'B': 2, 'K': 2, 'T': 2,
            'C': 3, 'L': 3, 'U': 3,
            'D': 4, 'M': 4, 'V': 4,
            'E': 5, 'N': 5, 'W': 5,
            'F': 6, 'O': 6, 'X': 6,
            'G': 7, 'P': 7, 'Y': 7,
            'H': 8, 'Q': 8, 'Z': 8,
            'I': 9, 'R': 9
        }
        
        # 母音の定義
        self.vowels = {'A', 'E', 'I', 'O', 'U'}
        
        # 解釈マトリックス
        self.interpretation_matrix = self._load_interpretation_matrix()
    
    def reduce_to_root(self, number: int, preserve_master_numbers: Optional[List[int]] = None) -> int:
        """
        条件付き還元アルゴリズム（数根の算出）
        
        Args:
            number: 還元する数値
            preserve_master_numbers: 保持するマスターナンバーのリスト
            
        Returns:
            還元された数値（1-9またはマスターナンバー）
        """
        if preserve_master_numbers is None:
            preserve_master_numbers = self.config['masterNumbers']
        
        while number > 9:
            # 各桁の合計を計算
            digit_sum = sum(int(digit) for digit in str(number))
            
            # マスターナンバーのチェック
            if digit_sum in preserve_master_numbers:
                return digit_sum
            
            number = digit_sum
        
        return number
    
    def name_to_numbers(self, name: str) -> List[int]:
        """
        姓名を数値に変換
        
        Args:
            name: 姓名（ローマ字表記）
            
        Returns:
            数値のリスト
        """
        # 正規化（大文字に変換し、アルファベット以外を除去）
        normalized_name = ''.join(c.upper() for c in name if c.isalpha())
        
        # 各文字を数値に変換
        numbers = []
        for char in normalized_name:
            if char in self.letter_to_number:
                numbers.append(self.letter_to_number[char])
        
        return numbers
    
    def calculate_life_path_number(self, birth_date: date) -> int:
        """
        ライフパスナンバーの計算
        
        Args:
            birth_date: 生年月日
            
        Returns:
            ライフパスナンバー
        """
        # 年、月、日の各桁を合計
        year_sum = sum(int(digit) for digit in str(birth_date.year))
        month_sum = sum(int(digit) for digit in str(birth_date.month))
        day_sum = sum(int(digit) for digit in str(birth_date.day))
        
        total = year_sum + month_sum + day_sum
        return self.reduce_to_root(total)
    
    def calculate_destiny_number(self, full_name: str) -> int:
        """
        ディスティニーナンバーの計算
        
        Args:
            full_name: 出生時のフルネーム
            
        Returns:
            ディスティニーナンバー
        """
        numbers = self.name_to_numbers(full_name)
        total = sum(numbers)
        return self.reduce_to_root(total)
    
    def calculate_soul_number(self, full_name: str) -> int:
        """
        ソウルナンバーの計算（母音のみ）
        
        Args:
            full_name: 出生時のフルネーム
            
        Returns:
            ソウルナンバー
        """
        # 母音のみを抽出
        vowel_numbers = []
        for char in full_name.upper():
            if char in self.vowels and char in self.letter_to_number:
                vowel_numbers.append(self.letter_to_number[char])
        
        total = sum(vowel_numbers)
        return self.reduce_to_root(total)
    
    def calculate_personality_number(self, full_name: str) -> int:
        """
        パーソナリティーナンバーの計算（子音のみ）
        
        Args:
            full_name: 出生時のフルネーム
            
        Returns:
            パーソナリティーナンバー
        """
        # 子音のみを抽出
        consonant_numbers = []
        for char in full_name.upper():
            if char.isalpha() and char not in self.vowels and char in self.letter_to_number:
                consonant_numbers.append(self.letter_to_number[char])
        
        total = sum(consonant_numbers)
        return self.reduce_to_root(total)
    
    def calculate_birthday_number(self, birth_date: date) -> int:
        """
        バースデーナンバーの計算
        
        Args:
            birth_date: 生年月日
            
        Returns:
            バースデーナンバー
        """
        day_sum = sum(int(digit) for digit in str(birth_date.day))
        return self.reduce_to_root(day_sum)
    
    def calculate_maturity_number(self, life_path: int, destiny: int) -> int:
        """
        マチュリティーナンバーの計算
        
        Args:
            life_path: ライフパスナンバー
            destiny: ディスティニーナンバー
            
        Returns:
            マチュリティーナンバー
        """
        total = life_path + destiny
        return self.reduce_to_root(total)
    
    def calculate_personal_year_number(self, birth_date: date, target_date: date) -> int:
        """
        パーソナルイヤーナンバーの計算
        
        Args:
            birth_date: 生年月日
            target_date: 占いたい日付
            
        Returns:
            パーソナルイヤーナンバー
        """
        # サイクル年を決定（誕生日ベース）
        if (target_date.month, target_date.day) < (birth_date.month, birth_date.day):
            cycle_year = target_date.year - 1
        else:
            cycle_year = target_date.year
        
        # 誕生月、誕生日、サイクル年の各桁を合計
        month_sum = sum(int(digit) for digit in str(birth_date.month))
        day_sum = sum(int(digit) for digit in str(birth_date.day))
        year_sum = sum(int(digit) for digit in str(cycle_year))
        
        total = month_sum + day_sum + year_sum
        
        # パーソナルイヤーは1-9のサイクル概念のため、マスターナンバーを還元
        return self.reduce_to_root(total, preserve_master_numbers=[])
    
    def calculate_personal_month_number(self, personal_year: int, target_month: int) -> int:
        """
        パーソナルマンスナンバーの計算
        
        Args:
            personal_year: パーソナルイヤーナンバー
            target_month: 占いたい月
            
        Returns:
            パーソナルマンスナンバー
        """
        month_sum = sum(int(digit) for digit in str(target_month))
        total = personal_year + month_sum
        return self.reduce_to_root(total)
    
    def calculate_personal_day_number(self, personal_month: int, target_day: int, method: str = 'hierarchical') -> int:
        """
        パーソナルデイナンバーの計算
        
        Args:
            personal_month: パーソナルマンスナンバー
            target_day: 占いたい日
            method: 計算方法 ('hierarchical', 'lifepath', 'birthday')
            
        Returns:
            パーソナルデイナンバー
        """
        if method == 'hierarchical':
            # 方式A: 階層的還元法
            day_sum = sum(int(digit) for digit in str(target_day))
            total = personal_month + day_sum
            return self.reduce_to_root(total)
        
        # 他の方式は後で実装
        return self.reduce_to_root(personal_month + sum(int(digit) for digit in str(target_day)))
    
    def calculate_temporal_numbers(self, profile: Dict[str, Any], target_date: date) -> Dict[str, Any]:
        """
        特定時点の運勢ナンバーを計算
        
        Args:
            profile: 個人の数秘術プロファイル
            target_date: 占いたい日付
            
        Returns:
            時間軸ナンバーの辞書
        """
        print(f"Calculating temporal numbers for profile: {profile}")
        print(f"Target date: {target_date}")
        
        try:
            birth_date = datetime.strptime(profile['birth_date'], '%Y-%m-%d').date()
        except Exception as e:
            print(f"Error parsing birth_date: {e}")
            print(f"Profile birth_date: {profile.get('birth_date')}")
            raise
        
        # パーソナルイヤーナンバー
        personal_year = self.calculate_personal_year_number(birth_date, target_date)
        print(f"Personal year: {personal_year}")
        
        # パーソナルマンスナンバー
        personal_month = self.calculate_personal_month_number(personal_year, target_date.month)
        print(f"Personal month: {personal_month}")
        
        # パーソナルデイナンバー
        personal_day = self.calculate_personal_day_number(personal_month, target_date.day)
        print(f"Personal day: {personal_day}")
        
        try:
            interpretations = {
                'year': self.get_interpretation(personal_year, 'PersonalYear'),
                'month': self.get_interpretation(personal_month, 'PersonalMonth'),
                'day': self.get_interpretation(personal_day, 'PersonalDay')
            }
            print(f"Interpretations: {interpretations}")
        except Exception as e:
            print(f"Error getting interpretations: {e}")
            interpretations = {
                'year': {'description': '解釈エラー', 'keywords': [], 'advice': 'エラーが発生しました'},
                'month': {'description': '解釈エラー', 'keywords': [], 'advice': 'エラーが発生しました'},
                'day': {'description': '解釈エラー', 'keywords': [], 'advice': 'エラーが発生しました'}
            }
        
        return {
            'personal_year': personal_year,
            'personal_month': personal_month,
            'personal_day': personal_day,
            'target_date': target_date.isoformat(),
            'interpretations': interpretations
        }
    
    def get_interpretation(self, number: int, context: str) -> Dict[str, Any]:
        """
        数値の解釈を取得
        
        Args:
            number: 数値
            context: 文脈（PersonalYear, PersonalMonth, PersonalDay等）
            
        Returns:
            解釈の辞書
        """
        if context in self.interpretation_matrix and str(number) in self.interpretation_matrix[context]:
            return self.interpretation_matrix[context][str(number)]
        
        # デフォルトの解釈
        return {
            'keywords': ['未知のエネルギー'],
            'description': f'数値{number}の{context}における意味は、さらなる研究が必要です。',
            'advice': 'この期間は慎重に行動し、直感を大切にしてください。'
        }
    
    def _load_interpretation_matrix(self) -> Dict[str, Any]:
        """
        解釈マトリックスを読み込み
        
        Returns:
            解釈マトリックスの辞書
        """
        return {
            'PersonalYear': {
                '1': {
                    'keywords': ['新しい始まり', '独立', '革新', 'リーダーシップ'],
                    'description': '新しい9年サイクルの始まり。種をまき、独立した行動を起こすのに最適な年です。',
                    'advice': '新しいプロジェクトを開始し、自分らしい道を歩み始めましょう。'
                },
                '2': {
                    'keywords': ['忍耐', '協力', '調和', 'バランス'],
                    'description': '忍耐と協力の年。人間関係を育み、計画を練る時期です。',
                    'advice': '急がずに、周囲との調和を大切にしながら進んでください。'
                },
                '3': {
                    'keywords': ['創造性', '表現', '楽しみ', '社交性'],
                    'description': '創造性と楽しみの年。自己表現を楽しみ、社交的に過ごす時期です。',
                    'advice': '芸術的な活動やコミュニケーションを楽しみましょう。'
                },
                '4': {
                    'keywords': ['努力', '基盤作り', '安定', '堅実性'],
                    'description': '努力と基盤作りの年。安定のためにハードワークが求められる時期です。',
                    'advice': 'コツコツと努力を積み重ね、将来の基盤を築きましょう。'
                },
                '5': {
                    'keywords': ['変化', '自由', '冒険', '多才'],
                    'description': '変化と自由の年。新しいことに挑戦し、行動範囲を広げる時期です。',
                    'advice': '変化を恐れず、新しい体験を積極的に求めましょう。'
                },
                '6': {
                    'keywords': ['愛', '責任', '奉仕', '家族'],
                    'description': '愛と責任の年。家族やコミュニティへの奉仕がテーマとなります。',
                    'advice': '周囲の人々への愛情と責任感を持って行動しましょう。'
                },
                '7': {
                    'keywords': ['内省', '探求', '休息', 'スピリチュアル'],
                    'description': '内省と探求の年。一人で過ごす時間を大切にし、精神的な成長を促す時期です。',
                    'advice': '静かな時間を持ち、内面の声に耳を傾けましょう。'
                },
                '8': {
                    'keywords': ['力', '達成', '成功', '豊かさ'],
                    'description': '力と達成の年。これまでの努力が実り、豊かさや成功を手にする時期です。',
                    'advice': 'リーダーシップを発揮し、目標達成に向けて行動しましょう。'
                },
                '9': {
                    'keywords': ['完了', '手放し', '寛容', '解放'],
                    'description': '完了と手放しの年。不要なものを整理し、次のサイクルに備えるための集大成の年です。',
                    'advice': '過去を手放し、新しいサイクルへの準備を始めましょう。'
                }
            },
            'PersonalMonth': {
                '1': {
                    'keywords': ['開始', '行動', '決断'],
                    'description': '新しいことを始めるのに適した月です。',
                    'advice': '積極的に行動し、新しいプロジェクトを開始しましょう。'
                },
                '2': {
                    'keywords': ['協力', '忍耐', '調和'],
                    'description': '協力と調和を重視する月です。',
                    'advice': '周囲との協調を大切にし、急がずに進んでください。'
                },
                '3': {
                    'keywords': ['創造', '表現', '楽しみ'],
                    'description': '創造性と表現力を発揮する月です。',
                    'advice': '芸術的な活動やコミュニケーションを楽しみましょう。'
                },
                '4': {
                    'keywords': ['努力', '安定', '建設'],
                    'description': '努力と基盤作りに集中する月です。',
                    'advice': 'コツコツと努力を積み重ねましょう。'
                },
                '5': {
                    'keywords': ['変化', '自由', '冒険'],
                    'description': '変化と新しい体験を求める月です。',
                    'advice': '変化を恐れず、新しいことに挑戦しましょう。'
                },
                '6': {
                    'keywords': ['責任', '愛', '奉仕'],
                    'description': '責任と奉仕に焦点を当てる月です。',
                    'advice': '家族や周囲の人々への責任を果たしましょう。'
                },
                '7': {
                    'keywords': ['内省', '分析', '休息'],
                    'description': '内省と分析に適した月です。',
                    'advice': '静かな時間を持ち、深く考えましょう。'
                },
                '8': {
                    'keywords': ['権力', '成功', '達成'],
                    'description': '権力と成功を追求する月です。',
                    'advice': 'リーダーシップを発揮し、目標達成に集中しましょう。'
                },
                '9': {
                    'keywords': ['完了', '寛容', '手放し'],
                    'description': '完了と手放しの月です。',
                    'advice': '不要なものを手放し、新しい準備を始めましょう。'
                }
            },
            'PersonalDay': {
                '1': {
                    'keywords': ['リーダーシップ', '独立', '開始'],
                    'description': 'リーダーシップを発揮し、新しいことを始めるのに適した日です。',
                    'advice': '積極的に行動し、自分らしい道を歩みましょう。'
                },
                '2': {
                    'keywords': ['協力', '調和', '忍耐'],
                    'description': '協力と調和を重視する日です。',
                    'advice': '周囲との協調を大切にし、急がずに進んでください。'
                },
                '3': {
                    'keywords': ['創造性', '表現', '楽しみ'],
                    'description': '創造性と表現力を発揮する日です。',
                    'advice': '芸術的な活動やコミュニケーションを楽しみましょう。'
                },
                '4': {
                    'keywords': ['努力', '安定', '建設'],
                    'description': '努力と基盤作りに集中する日です。',
                    'advice': 'コツコツと努力を積み重ねましょう。'
                },
                '5': {
                    'keywords': ['変化', '自由', '冒険'],
                    'description': '変化と新しい体験を求める日です。',
                    'advice': '変化を恐れず、新しいことに挑戦しましょう。'
                },
                '6': {
                    'keywords': ['責任', '愛', '奉仕'],
                    'description': '責任と奉仕に焦点を当てる日です。',
                    'advice': '家族や周囲の人々への責任を果たしましょう。'
                },
                '7': {
                    'keywords': ['内省', '分析', '休息'],
                    'description': '内省と分析に適した日です。',
                    'advice': '静かな時間を持ち、深く考えましょう。'
                },
                '8': {
                    'keywords': ['権力', '成功', '達成'],
                    'description': '権力と成功を追求する日です。',
                    'advice': 'リーダーシップを発揮し、目標達成に集中しましょう。'
                },
                '9': {
                    'keywords': ['完了', '寛容', '手放し'],
                    'description': '完了と手放しの日です。',
                    'advice': '不要なものを手放し、新しい準備を始めましょう。'
                }
            }
        }
