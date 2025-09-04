"""
タロットカードデータベース
78枚の完全なタロットデッキ（大アルカナ22枚 + 小アルカナ56枚）
"""

from typing import List, Dict, Any

class TarotCard:
    """タロットカードクラス"""
    
    def __init__(self, card_id: str, name: str, description: str, keywords: List[str], 
                 suit: str = None, number: int = None, element: str = None):
        self.id = card_id
        self.name = name
        self.description = description
        self.keywords = keywords
        self.suit = suit  # 大アルカナの場合はNone
        self.number = number  # 大アルカナの場合はNone
        self.element = element  # 小アルカナの元素

def get_major_arcana() -> List[TarotCard]:
    """大アルカナ22枚を取得"""
    return [
        TarotCard('fool', '愚者', '新しい始まり、純真さ、冒険心、自由な精神', 
                 ['新しい始まり', '純真さ', '冒険心', '自由', '可能性', '直感'], None, 0, '風'),
        TarotCard('magician', '魔術師', '創造力、意志の力、実現力、スキル', 
                 ['創造力', '意志の力', '実現力', 'スキル', '自信', '集中力'], None, 1, '風'),
        TarotCard('high-priestess', '女教皇', '直感、神秘、内なる知恵、静寂', 
                 ['直感', '神秘', '内なる知恵', '静寂', '神秘', '内省'], None, 2, '水'),
        TarotCard('empress', '女帝', '豊穣、母性、創造性、自然の恵み', 
                 ['豊穣', '母性', '創造性', '自然', '愛', '美'], None, 3, '土'),
        TarotCard('emperor', '皇帝', '権威、リーダーシップ、安定、構造', 
                 ['権威', 'リーダーシップ', '安定', '構造', '力', '秩序'], None, 4, '火'),
        TarotCard('hierophant', '教皇', '伝統、教育、精神的な導き、信仰', 
                 ['伝統', '教育', '精神的な導き', '信仰', '学習', '儀式'], None, 5, '土'),
        TarotCard('lovers', '恋人', '愛、選択、調和、関係性', 
                 ['愛', '選択', '調和', '関係', '決断', '結合'], None, 6, '風'),
        TarotCard('chariot', '戦車', '勝利、意志、前進、制御', 
                 ['勝利', '意志', '前進', '制御', '成功', '決意'], None, 7, '水'),
        TarotCard('strength', '力', '内なる強さ、勇気、忍耐、優しさ', 
                 ['内なる強さ', '勇気', '忍耐', '優しさ', '自信', '自制'], None, 8, '火'),
        TarotCard('hermit', '隠者', '内省、孤独、導き、知恵', 
                 ['内省', '孤独', '導き', '知恵', '探求', '啓発'], None, 9, '土'),
        TarotCard('wheel-of-fortune', '運命の輪', '変化、運命、循環、転機', 
                 ['変化', '運命', '循環', '転機', '機会', '流れ'], None, 10, '火'),
        TarotCard('justice', '正義', 'バランス、真実、公正、責任', 
                 ['バランス', '真実', '公正', '責任', '真理', '法'], None, 11, '風'),
        TarotCard('hanged-man', '吊るされた男', '犠牲、新しい視点、待機、解放', 
                 ['犠牲', '新しい視点', '待機', '解放', '悟り', '受容'], None, 12, '水'),
        TarotCard('death', '死神', '終わりと始まり、変容、再生、変化', 
                 ['終わりと始まり', '変容', '再生', '変化', '解放', '浄化'], None, 13, '水'),
        TarotCard('temperance', '節制', 'バランス、調和、節制、忍耐', 
                 ['バランス', '調和', '節制', '忍耐', '調和', '統合'], None, 14, '火'),
        TarotCard('devil', '悪魔', '束縛、物質主義、欲望、執着', 
                 ['束縛', '物質主義', '欲望', '執着', '解放', '誘惑'], None, 15, '土'),
        TarotCard('tower', '塔', '突然の変化、破壊、啓示、混乱', 
                 ['突然の変化', '破壊', '啓示', '混乱', '解放', '覚醒'], None, 16, '火'),
        TarotCard('star', '星', '希望、インスピレーション、癒し、導き', 
                 ['希望', 'インスピレーション', '癒し', '導き', '信仰', '理想'], None, 17, '風'),
        TarotCard('moon', '月', '直感、幻想、無意識、神秘', 
                 ['直感', '幻想', '無意識', '神秘', '感情', '不安'], None, 18, '水'),
        TarotCard('sun', '太陽', '成功、喜び、活力、明るさ', 
                 ['成功', '喜び', '活力', '明るさ', '繁栄', '達成'], None, 19, '火'),
        TarotCard('judgement', '審判', '復活、覚醒、救済、召命', 
                 ['復活', '覚醒', '救済', '召命', '変容', '再生'], None, 20, '火'),
        TarotCard('world', '世界', '完成、達成、統合、旅の終わり', 
                 ['完成', '達成', '統合', '旅の終わり', '成功', '満足'], None, 21, '土')
    ]

def get_minor_arcana() -> List[TarotCard]:
    """小アルカナ56枚を取得"""
    cards = []
    
    # 各スートの定義
    suits = {
        'wands': {'name': 'ワンド', 'element': '火', 'theme': '創造、情熱、行動'},
        'cups': {'name': 'カップ', 'element': '水', 'theme': '感情、愛、直感'},
        'swords': {'name': 'ソード', 'element': '風', 'theme': '思考、コミュニケーション、知性'},
        'pentacles': {'name': 'ペンタクル', 'element': '土', 'theme': '物質、仕事、健康'}
    }
    
    # 各スートの数字カード（1-10）
    for suit_key, suit_info in suits.items():
        suit_name = suit_info['name']
        element = suit_info['element']
        theme = suit_info['theme']
        
        # エース（1）
        cards.append(TarotCard(
            f'{suit_key}_ace', f'{suit_name}のエース', 
            f'{theme}の新しい始まり、可能性、潜在能力',
            ['新しい始まり', '可能性', '潜在能力', '純粋なエネルギー'],
            suit_key, 1, element
        ))
        
        # 2-10
        number_meanings = {
            2: {'name': '選択', 'desc': '選択、バランス、協力'},
            3: {'name': '成長', 'desc': '成長、創造、協力'},
            4: {'name': '安定', 'desc': '安定、構造、基盤'},
            5: {'name': '変化', 'desc': '変化、挑戦、動揺'},
            6: {'name': '調和', 'desc': '調和、バランス、協力'},
            7: {'name': '挑戦', 'desc': '挑戦、成長、内省'},
            8: {'name': '動き', 'desc': '動き、進歩、変化'},
            9: {'name': '完成', 'desc': '完成、満足、達成'},
            10: {'name': '完成', 'desc': '完成、満足、新しいサイクル'}
        }
        
        for num in range(2, 11):
            meaning = number_meanings[num]
            cards.append(TarotCard(
                f'{suit_key}_{num}', f'{suit_name}の{num}',
                f'{meaning["desc"]} - {theme}',
                [meaning['name'], theme, '成長', '経験'],
                suit_key, num, element
            ))
    
    # 宮廷カード（ペイジ、ナイト、クイーン、キング）
    court_cards = {
        'page': {'name': 'ペイジ', 'desc': '学習、新しい始まり、好奇心'},
        'knight': {'name': 'ナイト', 'desc': '行動、情熱、冒険'},
        'queen': {'name': 'クイーン', 'desc': '成熟、直感、内なる力'},
        'king': {'name': 'キング', 'desc': '権威、統制、専門性'}
    }
    
    for suit_key, suit_info in suits.items():
        suit_name = suit_info['name']
        element = suit_info['element']
        theme = suit_info['theme']
        
        for court_key, court_info in court_cards.items():
            cards.append(TarotCard(
                f'{suit_key}_{court_key}', f'{suit_name}の{court_info["name"]}',
                f'{court_info["desc"]} - {theme}',
                [court_info['name'], theme, '人格', '表現'],
                suit_key, court_key, element
            ))
    
    return cards

def get_full_tarot_deck() -> List[TarotCard]:
    """完全な78枚のタロットデッキを取得"""
    major_arcana = get_major_arcana()
    minor_arcana = get_minor_arcana()
    return major_arcana + minor_arcana

def get_cards_by_suit(suit: str) -> List[TarotCard]:
    """指定されたスートのカードを取得"""
    deck = get_full_tarot_deck()
    return [card for card in deck if card.suit == suit]

def get_cards_by_element(element: str) -> List[TarotCard]:
    """指定された元素のカードを取得"""
    deck = get_full_tarot_deck()
    return [card for card in deck if card.element == element]

def get_major_arcana_cards() -> List[TarotCard]:
    """大アルカナのカードのみを取得"""
    return get_major_arcana()

def get_minor_arcana_cards() -> List[TarotCard]:
    """小アルカナのカードのみを取得"""
    return get_minor_arcana()

# カードの意味を取得するヘルパー関数
def get_card_image_path(card: TarotCard) -> str:
    """カードの画像パスを取得"""
    if card.suit is None:  # 大アルカナ
        # 大アルカナの画像ファイル名マッピング
        major_arcana_mapping = {
            'fool': '00-TheFool.jpg',
            'magician': '01-TheMagician.jpg',
            'high-priestess': '02-TheHighPriestess.jpg',
            'empress': '03-TheEmpress.jpg',
            'emperor': '04-TheEmperor.jpg',
            'hierophant': '05-TheHierophant.jpg',
            'lovers': '06-TheLovers.jpg',
            'chariot': '07-TheChariot.jpg',
            'strength': '08-Strength.jpg',
            'hermit': '09-TheHermit.jpg',
            'wheel-of-fortune': '10-WheelOfFortune.jpg',
            'justice': '11-Justice.jpg',
            'hanged-man': '12-TheHangedMan.jpg',
            'death': '13-Death.jpg',
            'temperance': '14-Temperance.jpg',
            'devil': '15-TheDevil.jpg',
            'tower': '16-TheTower.jpg',
            'star': '17-TheStar.jpg',
            'moon': '18-TheMoon.jpg',
            'sun': '19-TheSun.jpg',
            'judgement': '20-Judgement.jpg',
            'world': '21-TheWorld.jpg'
        }
        filename = major_arcana_mapping.get(card.id, 'CardBacks.jpg')
    else:  # 小アルカナ
        # スート名のマッピング
        suit_mapping = {
            'wands': 'Wands',
            'cups': 'Cups',
            'swords': 'Swords',
            'pentacles': 'Pentacles'
        }
        
        suit_name = suit_mapping.get(card.suit, card.suit)
        
        # 数字のマッピング
        if isinstance(card.number, int):
            number_str = f"{card.number:02d}"
        else:  # 宮廷カード
            court_mapping = {
                'page': '11',
                'knight': '12',
                'queen': '13',
                'king': '14'
            }
            number_str = court_mapping.get(card.number, '01')
        
        filename = f"{suit_name}{number_str}.jpg"
    
    return f"/images/tarot/{filename}"

def get_card_meaning(card: TarotCard, is_reversed: bool = False) -> str:
    """カードの意味を取得（逆位置対応）"""
    if is_reversed:
        return f"{card.description}（逆位置：内面化、遅延、課題）"
    return card.description

def get_card_keywords(card: TarotCard, is_reversed: bool = False) -> List[str]:
    """カードのキーワードを取得（逆位置対応）"""
    if is_reversed:
        return [f"{keyword}（課題）" for keyword in card.keywords]
    return card.keywords

def get_reversed_meaning(card: TarotCard) -> str:
    """カードの逆位置の意味を取得"""
    # 大アルカナの逆位置意味
    if card.suit is None:
        reversed_meanings = {
            'fool': '軽率、無責任、危険な冒険',
            'magician': '操作、欺瞞、力の乱用',
            'high-priestess': '秘密主義、直感の無視、内面の混乱',
            'empress': '依存、過保護、創造性の阻害',
            'emperor': '独裁、権威の乱用、柔軟性の欠如',
            'hierophant': '伝統への盲従、教条主義、精神的な束縛',
            'lovers': '不調和、選択の回避、関係の破綻',
            'chariot': '制御の喪失、方向性の欠如、内なる対立',
            'strength': '弱さ、自己不信、感情の制御不能',
            'hermit': '孤立、内省の拒否、導きの無視',
            'wheel-of-fortune': '運命への抵抗、変化への恐れ、停滞',
            'justice': '不公正、偏見、責任の回避',
            'hanged-man': '犠牲の拒否、新しい視点の拒絶、停滞',
            'death': '変化への抵抗、終わりの拒否、執着',
            'temperance': '不均衡、極端、調和の欠如',
            'devil': '束縛からの解放、物質主義の克服、自由',
            'tower': '突然の変化への準備、古い構造の崩壊、解放',
            'star': '希望の喪失、インスピレーションの欠如、絶望',
            'moon': '幻想の克服、真実の認識、直感の信頼',
            'sun': '成功の阻害、喜びの欠如、活力の喪失',
            'judgement': '復活の拒否、覚醒の回避、過去への執着',
            'world': '完成の阻害、達成の遅延、統合の欠如'
        }
        return reversed_meanings.get(card.id, '内面化、遅延、課題')
    
    # 小アルカナの逆位置意味（一般的なパターン）
    else:
        if isinstance(card.number, int):
            reversed_meanings = {
                1: '新しい始まりの阻害、可能性の無視',
                2: '選択の回避、バランスの欠如',
                3: '成長の阻害、創造性の欠如',
                4: '不安定、基盤の欠如',
                5: '変化への適応、挑戦の克服',
                6: '不調和、協力の欠如',
                7: '挑戦の回避、成長の拒否',
                8: '停滞、進歩の阻害',
                9: '未完成、満足の欠如',
                10: 'サイクルの終了の拒否、新しい始まりの阻害'
            }
            return reversed_meanings.get(card.number, '内面化、遅延、課題')
        else:  # 宮廷カード
            court_reversed = {
                'page': '未熟さ、学習の拒否、好奇心の欠如',
                'knight': '行動の過剰、衝動性、方向性の欠如',
                'queen': '感情の制御不能、直感の無視、内なる力の否定',
                'king': '権威の乱用、統制の欠如、専門性の誇示'
            }
            return court_reversed.get(card.number, '内面化、遅延、課題')

# デッキの統計情報
def get_deck_statistics() -> Dict[str, Any]:
    """デッキの統計情報を取得"""
    deck = get_full_tarot_deck()
    major_arcana = get_major_arcana()
    minor_arcana = get_minor_arcana()
    
    return {
        'total_cards': len(deck),
        'major_arcana_count': len(major_arcana),
        'minor_arcana_count': len(minor_arcana),
        'suits': {
            'wands': len(get_cards_by_suit('wands')),
            'cups': len(get_cards_by_suit('cups')),
            'swords': len(get_cards_by_suit('swords')),
            'pentacles': len(get_cards_by_suit('pentacles'))
        },
        'elements': {
            'fire': len(get_cards_by_element('火')),
            'water': len(get_cards_by_element('水')),
            'air': len(get_cards_by_element('風')),
            'earth': len(get_cards_by_element('土'))
        }
    }

if __name__ == "__main__":
    # デッキの統計情報を表示
    stats = get_deck_statistics()
    print("タロットデッキ統計情報:")
    print(f"総カード数: {stats['total_cards']}枚")
    print(f"大アルカナ: {stats['major_arcana_count']}枚")
    print(f"小アルカナ: {stats['minor_arcana_count']}枚")
    print("\nスート別:")
    for suit, count in stats['suits'].items():
        print(f"  {suit}: {count}枚")
    print("\n元素別:")
    for element, count in stats['elements'].items():
        print(f"  {element}: {count}枚")
    
    # サンプルカードを表示
    deck = get_full_tarot_deck()
    print(f"\nサンプルカード（最初の5枚）:")
    for i, card in enumerate(deck[:5]):
        print(f"{i+1}. {card.name} ({card.suit or 'Major'}) - {card.description}")
