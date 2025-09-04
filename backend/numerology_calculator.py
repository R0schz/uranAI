#!/usr/bin/env python3
"""
Updated Numerology Calculator
既存システムとの統合を考慮した数秘術計算クラス
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pykakasi
import re
from datetime import datetime, date
from typing import Dict, Any, List


class ModernNumerologyCalculator:
    """
    Modern Numerology Calculator
    
    人のフルネームと生年月日から6つのコアナンバーを計算するクラス
    """
    
    # Pythagorean Alphabet-to-Number Conversion Chart
    PYTHAGOREAN_CHART = {
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
    
    # Vowel and Consonant Definitions
    VOWELS = {'A', 'E', 'I', 'O', 'U'}
    CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')  # Y is always a consonant
    
    def __init__(self, full_name: str, birth_date: str):
        """
        Initialize the ModernNumerologyCalculator
        
        Args:
            full_name: Person's full name in Hepburn romanization (e.g., "TANAKA TARO")
            birth_date: Birth date in "YYYY-MM-DD" format
            
        Raises:
            ValueError: If input formats are invalid
        """
        # Validate and clean full name
        if not isinstance(full_name, str) or not full_name.strip():
            raise ValueError("Full name must be a non-empty string")
        
        # Clean name: convert to uppercase and remove non-alphabetic characters
        self.full_name = re.sub(r'[^A-Za-z\s]', '', full_name.upper().strip())
        if not self.full_name:
            raise ValueError("Full name must contain at least one alphabetic character")
        
        # Validate and parse birth date
        try:
            self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Birth date must be in YYYY-MM-DD format")
        
        # Store date components
        self.year = self.birth_date.year
        self.month = self.birth_date.month
        self.day = self.birth_date.day
        
        # Validate date components
        if self.year < 1 or self.year > 9999:
            raise ValueError("Year must be between 1 and 9999")
        if self.month < 1 or self.month > 12:
            raise ValueError("Month must be between 1 and 12")
        if self.day < 1 or self.day > 31:
            raise ValueError("Day must be between 1 and 31")
    
    def _reduce_number(self, number: int, context: str = 'default') -> int:
        """
        Apply numerical reduction principle
        
        Args:
            number: Integer to reduce
            context: Context for Master Number determination ('default' or 'soul')
            
        Returns:
            Reduced number (1-9 or Master Number)
        """
        if number <= 0:
            return 0
        
        # Define Master Numbers based on context
        if context == 'soul':
            master_numbers = {11, 22, 33, 44}
        else:  # default context
            master_numbers = {11, 22, 33}
        
        current_number = number
        
        while current_number > 9:
            # Check if current number is a Master Number
            if current_number in master_numbers:
                return current_number
            
            # Sum digits
            digit_sum = sum(int(digit) for digit in str(current_number))
            current_number = digit_sum
        
        return current_number
    
    def _name_to_numbers(self, name_part: str) -> list:
        """
        Convert name part to list of numbers using Pythagorean chart
        
        Args:
            name_part: Part of name to convert
            
        Returns:
            List of numbers corresponding to each letter
        """
        numbers = []
        for char in name_part:
            if char in self.PYTHAGOREAN_CHART:
                numbers.append(self.PYTHAGOREAN_CHART[char])
        return numbers
    
    def _get_vowels_from_name(self, name: str) -> str:
        """
        Extract vowels from name
        
        Args:
            name: Full name string
            
        Returns:
            String containing only vowels
        """
        return ''.join(char for char in name if char in self.VOWELS)
    
    def _get_consonants_from_name(self, name: str) -> str:
        """
        Extract consonants from name (including Y)
        
        Args:
            name: Full name string
            
        Returns:
            String containing only consonants
        """
        return ''.join(char for char in name if char in self.CONSONANTS)
    
    def calculate_life_path(self) -> int:
        """
        Calculate Life Path Number
        
        Decomposes the full birth date (year, month, day) into individual digits,
        sums all these digits together, and applies numerical reduction.
        
        Returns:
            Life Path Number (1-9 or Master Number 11, 22, 33)
        """
        # Decompose date into individual digits
        date_digits = []
        date_digits.extend([int(d) for d in str(self.year)])
        date_digits.extend([int(d) for d in str(self.month)])
        date_digits.extend([int(d) for d in str(self.day)])
        
        # Sum all digits
        total_sum = sum(date_digits)
        
        # Apply numerical reduction
        return self._reduce_number(total_sum, context='default')
    
    def calculate_birthday(self) -> int:
        """
        Calculate Birthday Number
        
        Uses only the 'day' part of the birth date, sums the digits,
        and reduces to a single-digit root number.
        Master Number exception does NOT apply to this calculation.
        
        Returns:
            Birthday Number (1-9)
        """
        # Sum digits of day
        day_digits = [int(d) for d in str(self.day)]
        total_sum = sum(day_digits)
        
        # Always reduce to single digit (no Master Number exception)
        while total_sum > 9:
            total_sum = sum(int(d) for d in str(total_sum))
        
        return total_sum
    
    def calculate_destiny(self) -> int:
        """
        Calculate Destiny Number
        
        Uses the full name, converts each letter to its corresponding number
        using the Pythagorean chart, sums all numbers, and applies reduction.
        
        Returns:
            Destiny Number (1-9 or Master Number 11, 22, 33)
        """
        # Convert full name to numbers
        name_numbers = self._name_to_numbers(self.full_name)
        
        # Sum all numbers
        total_sum = sum(name_numbers)
        
        # Apply numerical reduction
        return self._reduce_number(total_sum, context='default')
    
    def calculate_soul(self) -> int:
        """
        Calculate Soul Number
        
        Uses only the vowels (A, E, I, O, U) from the full name,
        converts each vowel to its corresponding number, sums all numbers,
        and applies reduction with extended Master Numbers (including 44).
        
        Returns:
            Soul Number (1-9 or Master Number 11, 22, 33, 44)
        """
        # Extract vowels from full name
        vowels = self._get_vowels_from_name(self.full_name)
        
        # Convert vowels to numbers
        vowel_numbers = self._name_to_numbers(vowels)
        
        # Sum all numbers
        total_sum = sum(vowel_numbers)
        
        # Apply numerical reduction with soul context (includes 44)
        return self._reduce_number(total_sum, context='soul')
    
    def calculate_personality(self) -> int:
        """
        Calculate Personality Number
        
        Uses only the consonants from the full name (including 'Y'),
        converts each consonant to its corresponding number, sums all numbers,
        and applies reduction.
        
        Returns:
            Personality Number (1-9 or Master Number 11, 22, 33)
        """
        # Extract consonants from full name
        consonants = self._get_consonants_from_name(self.full_name)
        
        # Convert consonants to numbers
        consonant_numbers = self._name_to_numbers(consonants)
        
        # Sum all numbers
        total_sum = sum(consonant_numbers)
        
        # Apply numerical reduction
        return self._reduce_number(total_sum, context='default')
    
    def calculate_maturity(self) -> int:
        """
        Calculate Maturity Number
        
        Sums the Life Path Number and Destiny Number (using full values,
        even if they are Master Numbers), then applies numerical reduction.
        
        Returns:
            Maturity Number (1-9 or Master Number 11, 22, 33)
        """
        # Get Life Path and Destiny numbers
        life_path = self.calculate_life_path()
        destiny = self.calculate_destiny()
        
        # Sum the full values (even if Master Numbers)
        total_sum = life_path + destiny
        
        # Apply numerical reduction
        return self._reduce_number(total_sum, context='default')
    
    def calculate_all(self) -> Dict[str, int]:
        """
        Calculate all six core numerology numbers
        
        Returns:
            Dictionary containing all six numbers with user-friendly keys
        """
        return {
            "life_path_number": self.calculate_life_path(),
            "birthday_number": self.calculate_birthday(),
            "destiny_number": self.calculate_destiny(),
            "soul_number": self.calculate_soul(),
            "personality_number": self.calculate_personality(),
            "maturity_number": self.calculate_maturity()
        }


class NumerologyCalculator:
    """
    Updated Numerology Calculator
    
    既存システムとの互換性を保ちつつ、新しいアルゴリズムを使用する数秘術計算クラス
    """
    
    def __init__(self):
        """Initialize the calculator with number meanings"""
        self.number_meanings = {
            1: 'リーダーシップ、独立、創造性',
            2: '協調性、バランス、直感',
            3: '表現力、創造性、コミュニケーション',
            4: '安定、実用性、組織力',
            5: '自由、変化、冒険',
            6: '責任、愛情、調和',
            7: '精神性、分析、内省',
            8: '成功、権力、物質的達成',
            9: '完成、智慧、奉仕',
            11: '直感、啓示、スピリチュアル',
            22: '最高の職人、実現力、大いなる目的',
            33: 'マスター教師、癒し、奉仕',
            44: '実用的な理想主義、建設的な変化'
        }
    
    def _convert_japanese_name_to_romanization(self, name_hiragana: str) -> str:
        """
        Convert Japanese hiragana name to Hepburn romanization
        
        Args:
            name_hiragana: Japanese name in hiragana (e.g., "こばやし　よしたか")
            
        Returns:
            Romanized name in uppercase (e.g., "KOBAYASHI YOSHITAKA")
        """
        # Split name by space
        name_parts = name_hiragana.split()
        if len(name_parts) < 2:
            # If no space, treat as single name
            name_parts = [name_hiragana]
        
        # Convert each part to romanization
        kks = pykakasi.kakasi()
        romanized_parts = []
        
        for part in name_parts:
            result = kks.convert(part)
            romanized_part = ''.join([item['hepburn'] for item in result])
            romanized_parts.append(romanized_part.upper())
        
        return ' '.join(romanized_parts)
    
    def get_numerology_reading(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get numerology reading for a profile (compatible with existing system)
        
        Args:
            profile_data: Profile data containing name_hiragana, birth_date, etc.
            
        Returns:
            Dictionary with numerology results in existing format
        """
        try:
            # Extract data from profile
            name_hiragana = profile_data.get('name_hiragana', '')
            birth_date = profile_data.get('birth_date', '')
            nickname = profile_data.get('nickname', 'あなた')
            
            if not name_hiragana or not birth_date:
                raise ValueError("name_hiragana and birth_date are required")
            
            # Convert Japanese name to romanization
            romanized_name = self._convert_japanese_name_to_romanization(name_hiragana)
            
            # Create new calculator instance
            calculator = ModernNumerologyCalculator(romanized_name, birth_date)
            
            # Calculate all numbers
            all_numbers = calculator.calculate_all()
            
            # Format results in existing system format
            result = {
                'nickname': nickname,
                'life_path': {
                    'number': all_numbers['life_path_number'],
                    'meaning': self.number_meanings.get(all_numbers['life_path_number'], '')
                },
                'destiny': {
                    'number': all_numbers['destiny_number'],
                    'meaning': self.number_meanings.get(all_numbers['destiny_number'], '')
                },
                'soul': {
                    'number': all_numbers['soul_number'],
                    'meaning': self.number_meanings.get(all_numbers['soul_number'], '')
                },
                'personal': {
                    'number': all_numbers['personality_number'],
                    'meaning': self.number_meanings.get(all_numbers['personality_number'], '')
                },
                'birthday': {
                    'number': all_numbers['birthday_number'],
                    'meaning': self.number_meanings.get(all_numbers['birthday_number'], '')
                },
                'challenge': {
                    'number': all_numbers['maturity_number'],  # Using maturity as challenge
                    'meaning': self.number_meanings.get(all_numbers['maturity_number'], '')
                },
                'maturity': {
                    'number': all_numbers['maturity_number'],
                    'meaning': self.number_meanings.get(all_numbers['maturity_number'], '')
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Numerology calculation failed: {e}")
            import traceback
            traceback.print_exc()
            # Return error result
            return {
                'nickname': profile_data.get('nickname', 'あなた'),
                'life_path': {'number': 0, 'meaning': '計算エラー'},
                'destiny': {'number': 0, 'meaning': '計算エラー'},
                'soul': {'number': 0, 'meaning': '計算エラー'},
                'personal': {'number': 0, 'meaning': '計算エラー'},
                'birthday': {'number': 0, 'meaning': '計算エラー'},
                'challenge': {'number': 0, 'meaning': '計算エラー'},
                'maturity': {'number': 0, 'meaning': '計算エラー'}
            }
    
    def get_compatibility_analysis(self, profile1: Dict[str, Any], profile2: Dict[str, Any], consultation: str = "") -> Dict[str, Any]:
        """
        Get compatibility analysis between two profiles
        
        Args:
            profile1: First profile data
            profile2: Second profile data
            consultation: Consultation content for AI analysis
            
        Returns:
            Dictionary with compatibility analysis
        """
        try:
            # Get numerology readings for both profiles
            reading1 = self.get_numerology_reading(profile1)
            reading2 = self.get_numerology_reading(profile2)
            
            # AIを使用してスコアを生成
            compatibility_data = {
                'person1': reading1,
                'person2': reading2,
                'person1_nickname': profile1.get('nickname', 'あなた'),
                'person2_nickname': profile2.get('nickname', '相手'),
                'consultation': consultation
            }
            
            try:
                from ai_analysis import AIAnalysisGenerator
                ai_generator = AIAnalysisGenerator()
                compatibility_score = ai_generator.generate_ai_compatibility_score(compatibility_data, 'numerology')
            except Exception as e:
                print(f"AI score generation failed, using fallback: {e}")
                # フォールバック: 従来のアルゴリズム
                life_path_diff = abs(reading1['life_path']['number'] - reading2['life_path']['number'])
                destiny_diff = abs(reading1['destiny']['number'] - reading2['destiny']['number'])
                soul_diff = abs(reading1['soul']['number'] - reading2['soul']['number'])
                
                life_path_score = max(0, 100 - (life_path_diff * 12))
                destiny_score = max(0, 100 - (destiny_diff * 12))
                soul_score = max(0, 100 - (soul_diff * 12))
                
                compatibility_score = int((life_path_score * 0.5 + destiny_score * 0.3 + soul_score * 0.2))
                compatibility_score = max(20, compatibility_score)
            
            # Prepare data for AI analysis
            compatibility_data['compatibility_score'] = compatibility_score
            compatibility_data['analysis'] = ''  # Will be filled by AI
            
            # Generate AI analysis using the same system as other divination types
            try:
                from ai_analysis import AIAnalysisGenerator
                ai_generator = AIAnalysisGenerator()
                analysis = ai_generator.generate_compatibility_analysis(compatibility_data, 'numerology', consultation)
            except Exception as ai_error:
                print(f"AI analysis failed, using fallback: {ai_error}")
                # Enhanced fallback analysis with nicknames and consultation context
                analysis = self._get_enhanced_fallback_analysis(profile1, profile2, compatibility_score, consultation)
            
            return {
                'compatibility_score': compatibility_score,
                'person1': reading1,
                'person2': reading2,
                'analysis': analysis
            }
            
        except Exception as e:
            print(f"Compatibility analysis failed: {e}")
            return {
                'compatibility_score': 0,
                'person1': {'life_path': {'number': 0}, 'destiny': {'number': 0}, 'soul': {'number': 0}, 'personal': {'number': 0}},
                'person2': {'life_path': {'number': 0}, 'destiny': {'number': 0}, 'soul': {'number': 0}, 'personal': {'number': 0}},
                'analysis': '相性分析エラー'
            }
    
    def calculate_temporal_fortune(self, profile_data: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        Calculate temporal fortune using proper numerology algorithms
        
        Args:
            profile_data: Profile data
            target_date: Target date for fortune calculation
            
        Returns:
            Dictionary with temporal fortune data
        """
        try:
            # Extract data from profile
            name_hiragana = profile_data.get('name_hiragana', '')
            birth_date = profile_data.get('birth_date', '')
            
            if not name_hiragana or not birth_date:
                raise ValueError("name_hiragana and birth_date are required")
            
            # Convert Japanese name to romanization
            romanized_name = self._convert_japanese_name_to_romanization(name_hiragana)
            
            # Create calculator instance
            calculator = ModernNumerologyCalculator(romanized_name, birth_date)
            
            # Parse target date
            target_dt = datetime.strptime(target_date, "%Y-%m-%d").date()
            
            # Calculate temporal numbers
            personal_year = self._calculate_personal_year(calculator, target_dt)
            personal_month = self._calculate_personal_month(personal_year, target_dt.month)
            personal_day = self._calculate_personal_day(personal_year, target_dt.month, target_dt.day)
            
            return {
                'target_date': target_date,
                'personal_year': {
                    'number': personal_year,
                    'description': self._get_year_description(personal_year),
                    'keywords': self._get_year_keywords(personal_year),
                    'advice': self._get_year_advice(personal_year)
                },
                'personal_month': {
                    'number': personal_month,
                    'description': self._get_month_description(personal_month),
                    'keywords': self._get_month_keywords(personal_month),
                    'advice': self._get_month_advice(personal_month)
                },
                'personal_day': {
                    'number': personal_day,
                    'description': self._get_day_description(personal_day),
                    'keywords': self._get_day_keywords(personal_day),
                    'advice': self._get_day_advice(personal_day)
                }
            }
        except Exception as e:
            print(f"Temporal fortune calculation failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'target_date': target_date,
                'personal_year': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''},
                'personal_month': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''},
                'personal_day': {'number': 0, 'description': '計算エラー', 'keywords': [], 'advice': ''}
            }
    
    def _calculate_personal_year(self, calculator: ModernNumerologyCalculator, target_date: date) -> int:
        """
        Calculate Personal Year Number
        
        Args:
            calculator: ModernNumerologyCalculator instance
            target_date: Target date
            
        Returns:
            Personal Year Number (1-9)
        """
        # Get birth date components
        birth_year = calculator.year
        birth_month = calculator.month
        birth_day = calculator.day
        
        # Determine cycle year (birthday-based)
        if (target_date.month, target_date.day) < (birth_month, birth_day):
            cycle_year = target_date.year - 1
        else:
            cycle_year = target_date.year
        
        # Sum digits of birth month, day, and cycle year
        month_sum = sum(int(digit) for digit in str(birth_month))
        day_sum = sum(int(digit) for digit in str(birth_day))
        year_sum = sum(int(digit) for digit in str(cycle_year))
        
        total_sum = month_sum + day_sum + year_sum
        
        # Reduce to single digit (no Master Number exception for Personal Year)
        while total_sum > 9:
            total_sum = sum(int(digit) for digit in str(total_sum))
        
        return total_sum
    
    def _calculate_personal_month(self, personal_year: int, target_month: int) -> int:
        """
        Calculate Personal Month Number
        
        Args:
            personal_year: Personal Year Number
            target_month: Target month (1-12)
            
        Returns:
            Personal Month Number (1-9)
        """
        # Sum personal year and target month
        total_sum = personal_year + target_month
        
        # Reduce to single digit (no Master Number exception for Personal Month)
        while total_sum > 9:
            total_sum = sum(int(digit) for digit in str(total_sum))
        
        return total_sum
    
    def _calculate_personal_day(self, personal_year: int, target_month: int, target_day: int) -> int:
        """
        Calculate Personal Day Number
        
        Args:
            personal_year: Personal Year Number
            target_month: Target month (1-12)
            target_day: Target day (1-31)
            
        Returns:
            Personal Day Number (1-9)
        """
        # Sum personal year, target month, and target day
        total_sum = personal_year + target_month + target_day
        
        # Reduce to single digit (no Master Number exception for Personal Day)
        while total_sum > 9:
            total_sum = sum(int(digit) for digit in str(total_sum))
        
        return total_sum
    
    def _get_year_description(self, year_number: int) -> str:
        """Get description for Personal Year Number"""
        descriptions = {
            1: '新しい始まりの年。リーダーシップと独立を重視する時期です。',
            2: '協力と調和の年。人間関係を育み、計画を練る時期です。',
            3: '創造性と表現の年。コミュニケーションと自己表現が重要です。',
            4: '安定と建設の年。実用的な努力と組織化が求められます。',
            5: '変化と自由の年。新しい体験と冒険を求める時期です。',
            6: '責任と愛情の年。家族やコミュニティとの調和が重要です。',
            7: '内省と精神性の年。自己理解と深い学びの時期です。',
            8: '成功と権力の年。物質的達成とリーダーシップが重要です。',
            9: '完成と智慧の年。奉仕と新しいサイクルの準備の時期です。'
        }
        return descriptions.get(year_number, '未知の年')
    
    def _get_year_keywords(self, year_number: int) -> List[str]:
        """Get keywords for Personal Year Number"""
        keywords = {
            1: ['開始', 'リーダーシップ', '独立', '創造性'],
            2: ['協力', '調和', '忍耐', 'バランス'],
            3: ['表現', '創造性', 'コミュニケーション', '楽観'],
            4: ['安定', '実用性', '組織', '努力'],
            5: ['変化', '自由', '冒険', '多様性'],
            6: ['責任', '愛情', '調和', '奉仕'],
            7: ['内省', '精神性', '分析', '直感'],
            8: ['成功', '権力', '物質的達成', 'リーダーシップ'],
            9: ['完成', '智慧', '奉仕', '新しいサイクル']
        }
        return keywords.get(year_number, [])
    
    def _get_year_advice(self, year_number: int) -> str:
        """Get advice for Personal Year Number"""
        advice = {
            1: '新しいことに挑戦し、リーダーシップを発揮してください。',
            2: '急がずに、周囲との調和を大切にしながら進んでください。',
            3: '創造性を発揮し、コミュニケーションを大切にしてください。',
            4: '着実な努力を重ね、組織的に物事を進めてください。',
            5: '変化を恐れず、新しい体験に積極的に取り組んでください。',
            6: '家族やコミュニティとの関係を大切にしてください。',
            7: '内省の時間を持ち、深い学びに集中してください。',
            8: '目標に向かって集中し、リーダーシップを発揮してください。',
            9: '奉仕の精神を持ち、新しいサイクルの準備をしてください。'
        }
        return advice.get(year_number, '')
    
    def _get_month_description(self, month_number: int) -> str:
        """Get description for Personal Month Number"""
        descriptions = {
            1: '行動と決断の月。新しいプロジェクトを開始する時期です。',
            2: '協力と調和の月。周囲との関係を深める時期です。',
            3: '創造性と表現の月。アートやコミュニケーションが重要です。',
            4: '安定と建設の月。実用的な作業に集中する時期です。',
            5: '変化と自由の月。新しい体験を求める時期です。',
            6: '責任と愛情の月。家族やコミュニティに焦点を当てる時期です。',
            7: '内省と精神性の月。自己理解を深める時期です。',
            8: '成功と権力の月。目標達成に集中する時期です。',
            9: '完成と智慧の月。奉仕と新しいサイクルの準備の時期です。'
        }
        return descriptions.get(month_number, '未知の月')
    
    def _get_month_keywords(self, month_number: int) -> List[str]:
        """Get keywords for Personal Month Number"""
        keywords = {
            1: ['行動', '決断', '開始', 'リーダーシップ'],
            2: ['協力', '調和', '忍耐', 'バランス'],
            3: ['創造性', '表現', 'コミュニケーション', '楽観'],
            4: ['安定', '実用性', '組織', '努力'],
            5: ['変化', '自由', '冒険', '多様性'],
            6: ['責任', '愛情', '調和', '奉仕'],
            7: ['内省', '精神性', '分析', '直感'],
            8: ['成功', '権力', '物質的達成', 'リーダーシップ'],
            9: ['完成', '智慧', '奉仕', '新しいサイクル']
        }
        return keywords.get(month_number, [])
    
    def _get_month_advice(self, month_number: int) -> str:
        """Get advice for Personal Month Number"""
        advice = {
            1: '決断力を持って行動に移してください。',
            2: '周囲との協調を大切にし、急がずに進んでください。',
            3: '創造性を発揮し、表現活動に取り組んでください。',
            4: '着実な努力を重ね、実用的な作業に集中してください。',
            5: '変化を恐れず、新しい体験に挑戦してください。',
            6: '家族やコミュニティとの関係を大切にしてください。',
            7: '内省の時間を持ち、自己理解を深めてください。',
            8: '目標達成に向けて集中し、リーダーシップを発揮してください。',
            9: '奉仕の精神を持ち、新しいサイクルの準備をしてください。'
        }
        return advice.get(month_number, '')
    
    def _get_day_description(self, day_number: int) -> str:
        """Get description for Personal Day Number"""
        descriptions = {
            1: '独立と創造の日。リーダーシップを発揮する日です。',
            2: '協力と調和の日。周囲との関係を大切にする日です。',
            3: '表現と創造性の日。コミュニケーションが重要です。',
            4: '安定と実用性の日。着実な作業に集中する日です。',
            5: '変化と自由の日。新しい体験を求める日です。',
            6: '責任と愛情の日。家族やコミュニティに焦点を当てる日です。',
            7: '内省と精神性の日。自己理解を深める日です。',
            8: '成功と権力の日。目標達成に集中する日です。',
            9: '完成と智慧の日。奉仕と新しいサイクルの準備の日です。'
        }
        return descriptions.get(day_number, '未知の日')
    
    def _get_day_keywords(self, day_number: int) -> List[str]:
        """Get keywords for Personal Day Number"""
        keywords = {
            1: ['独立', '創造', 'リーダーシップ', '開始'],
            2: ['協力', '調和', '忍耐', 'バランス'],
            3: ['表現', '創造性', 'コミュニケーション', '楽観'],
            4: ['安定', '実用性', '組織', '努力'],
            5: ['変化', '自由', '冒険', '多様性'],
            6: ['責任', '愛情', '調和', '奉仕'],
            7: ['内省', '精神性', '分析', '直感'],
            8: ['成功', '権力', '物質的達成', 'リーダーシップ'],
            9: ['完成', '智慧', '奉仕', '新しいサイクル']
        }
        return keywords.get(day_number, [])
    
    def _get_day_advice(self, day_number: int) -> str:
        """Get advice for Personal Day Number"""
        advice = {
            1: '自分の判断で行動し、創造性を発揮してください。',
            2: '周囲との調和を大切にし、協力を求めましょう。',
            3: '表現活動に取り組み、コミュニケーションを大切にしてください。',
            4: '着実な作業に集中し、組織的に進めてください。',
            5: '変化を恐れず、新しいことに挑戦してください。',
            6: '家族やコミュニティとの関係を大切にしてください。',
            7: '内省の時間を持ち、直感を信じてください。',
            8: '目標達成に向けて集中し、リーダーシップを発揮してください。',
            9: '奉仕の精神を持ち、新しいサイクルの準備をしてください。'
        }
        return advice.get(day_number, '')
    
    def _get_enhanced_fallback_analysis(self, profile1: Dict[str, Any], profile2: Dict[str, Any], compatibility_score: int, consultation: str) -> str:
        """Enhanced fallback analysis with consultation context"""
        nickname1 = profile1.get('nickname', 'あなた')
        nickname2 = profile2.get('nickname', '相手')
        
        # Base analysis based on compatibility score
        if compatibility_score >= 80:
            base_analysis = f"{nickname1}さんと{nickname2}さんは非常に良い相性です。お互いを高め合える素晴らしい関係を築けるでしょう。"
        elif compatibility_score >= 60:
            base_analysis = f"{nickname1}さんと{nickname2}さんは良い相性です。お互いの違いを理解し合えば、安定した関係を築けるでしょう。"
        elif compatibility_score >= 40:
            base_analysis = f"{nickname1}さんと{nickname2}さんは普通の相性です。努力次第で良い関係を築くことができます。"
        else:
            base_analysis = f"{nickname1}さんと{nickname2}さんの相性には課題があります。お互いの理解を深めることが重要です。"
        
        # Add consultation context if provided
        if consultation and consultation.strip():
            if "恋愛" in consultation or "恋" in consultation:
                context = "恋愛関係において、数秘術のエネルギーが調和し、お互いを支え合える関係を築けるでしょう。"
            elif "結婚" in consultation or "婚" in consultation:
                context = "結婚を考える上で、数秘術の観点からも安定した関係性が期待できます。"
            elif "友情" in consultation or "友" in consultation:
                context = "友情関係において、数秘術のエネルギーが互いを高め合う良い関係を築けるでしょう。"
            elif "仕事" in consultation or "職" in consultation:
                context = "仕事関係において、数秘術のエネルギーが協力し合える良いパートナーシップを築けるでしょう。"
            else:
                context = "数秘術の観点からも、お互いを理解し合うことで良い関係を築けるでしょう。"
            
            return f"{base_analysis} {context}"
        
        return base_analysis


if __name__ == "__main__":
    # Test the updated calculator
    print("Testing Updated Numerology Calculator")
    print("=" * 60)
    
    calculator = NumerologyCalculator()
    
    # Test case 1: Japanese name
    print("Test Case 1: Japanese name conversion and calculation")
    print("-" * 50)
    
    profile1 = {
        'nickname': 'コバトン',
        'name_hiragana': 'こばやし　よしたか',
        'birth_date': '1999-04-02',
        'birth_time': '12:00:00',
        'birth_location_json': {'place': '東京'}
    }
    
    result1 = calculator.get_numerology_reading(profile1)
    print(f"Results for {profile1['nickname']} ({profile1['name_hiragana']}):")
    print(f"  ライフパス: {result1['life_path']['number']} - {result1['life_path']['meaning']}")
    print(f"  ディスティニー: {result1['destiny']['number']} - {result1['destiny']['meaning']}")
    print(f"  ソウル: {result1['soul']['number']} - {result1['soul']['meaning']}")
    print(f"  パーソナル: {result1['personal']['number']} - {result1['personal']['meaning']}")
    print(f"  バースデー: {result1['birthday']['number']} - {result1['birthday']['meaning']}")
    print(f"  マチュリティ: {result1['maturity']['number']} - {result1['maturity']['meaning']}")
    
    print("\n" + "=" * 60)
    
    # Test case 2: Compatibility analysis
    print("Test Case 2: Compatibility analysis")
    print("-" * 50)
    
    profile2 = {
        'nickname': 'ハナコ',
        'name_hiragana': 'やまだ　はなこ',
        'birth_date': '1985-05-15',
        'birth_time': '08:30:00',
        'birth_location_json': {'place': '大阪'}
    }
    
    compatibility = calculator.get_compatibility_analysis(profile1, profile2, "テスト用の相談内容")
    print(f"Compatibility between {profile1['nickname']} and {profile2['nickname']}:")
    print(f"  相性スコア: {compatibility['compatibility_score']}/100")
    print(f"  分析: {compatibility['analysis']}")
    
    print("\n" + "=" * 60)
    
    # Test case 3: Name conversion details
    print("Test Case 3: Name conversion details")
    print("-" * 50)
    
    test_names = [
        'こばやし　よしたか',
        'やまだ　はなこ',
        'すずき　たろう',
        'たなか　みき'
    ]
    
    for name in test_names:
        romanized = calculator._convert_japanese_name_to_romanization(name)
        print(f"  {name} -> {romanized}")
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")