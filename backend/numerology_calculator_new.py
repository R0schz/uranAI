#!/usr/bin/env python3
"""
Modern Numerology Calculator
数秘術の6つのコアナンバーを計算するクラス
"""

import re
from datetime import datetime
from typing import Dict, Any


class NumerologyCalculator:
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
        Initialize the NumerologyCalculator
        
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
    
    def get_name_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the name processing
        
        Returns:
            Dictionary with name processing details
        """
        vowels = self._get_vowels_from_name(self.full_name)
        consonants = self._get_consonants_from_name(self.full_name)
        
        return {
            "full_name": self.full_name,
            "vowels": vowels,
            "consonants": consonants,
            "vowel_numbers": self._name_to_numbers(vowels),
            "consonant_numbers": self._name_to_numbers(consonants),
            "all_name_numbers": self._name_to_numbers(self.full_name)
        }


if __name__ == "__main__":
    # Example 1: General case
    print("Example 1: General case")
    print("=" * 50)
    person1 = NumerologyCalculator("YAMADA TARO", "1990-08-26")
    all_numbers1 = person1.calculate_all()
    print(f"Results for YAMADA TARO (1990-08-26):")
    for name, number in all_numbers1.items():
        print(f"  {name}: {number}")
    
    # Show name processing details
    name_info1 = person1.get_name_info()
    print(f"\nName processing details:")
    print(f"  Full name: {name_info1['full_name']}")
    print(f"  Vowels: {name_info1['vowels']} -> {name_info1['vowel_numbers']}")
    print(f"  Consonants: {name_info1['consonants']} -> {name_info1['consonant_numbers']}")
    
    print("\n" + "=" * 50)
    
    # Example 2: Case involving Master Numbers
    print("Example 2: Case involving Master Numbers")
    print("=" * 50)
    person2 = NumerologyCalculator("KATO RYO", "1975-05-15")
    all_numbers2 = person2.calculate_all()
    print(f"Results for KATO RYO (1975-05-15):")
    for name, number in all_numbers2.items():
        print(f"  {name}: {number}")
    
    # Show name processing details
    name_info2 = person2.get_name_info()
    print(f"\nName processing details:")
    print(f"  Full name: {name_info2['full_name']}")
    print(f"  Vowels: {name_info2['vowels']} -> {name_info2['vowel_numbers']}")
    print(f"  Consonants: {name_info2['consonants']} -> {name_info2['consonant_numbers']}")
    
    print("\n" + "=" * 50)
    
    # Example 3: Test with "こばやし　よしたか" converted to romanization
    print("Example 3: Test with Japanese name (Kobayashi Yoshitaka)")
    print("=" * 50)
    person3 = NumerologyCalculator("KOBAYASHI YOSHITAKA", "1999-04-02")
    all_numbers3 = person3.calculate_all()
    print(f"Results for KOBAYASHI YOSHITAKA (1999-04-02):")
    for name, number in all_numbers3.items():
        print(f"  {name}: {number}")
    
    # Show name processing details
    name_info3 = person3.get_name_info()
    print(f"\nName processing details:")
    print(f"  Full name: {name_info3['full_name']}")
    print(f"  Vowels: {name_info3['vowels']} -> {name_info3['vowel_numbers']}")
    print(f"  Consonants: {name_info3['consonants']} -> {name_info3['consonant_numbers']}")
    
    print("\n" + "=" * 50)
    
    # Example 4: Test reduction method with different contexts
    print("Example 4: Test reduction method with different contexts")
    print("=" * 50)
    test_calculator = NumerologyCalculator("TEST NAME", "2000-01-01")
    
    # Test numbers that would become Master Numbers
    test_numbers = [29, 38, 47, 56]
    
    for num in test_numbers:
        default_reduction = test_calculator._reduce_number(num, context='default')
        soul_reduction = test_calculator._reduce_number(num, context='soul')
        print(f"  {num} -> default: {default_reduction}, soul: {soul_reduction}")
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")
