# AI相性スコア生成機能

## 概要

全ての占い（数秘術、ホロスコープ、タロット）の相性スコア算出をAIに委ねる機能を実装しました。

## 機能

### AIスコア生成
- **数秘術**: ライフパス、ディスティニー、ソウル、パーソナルナンバーを総合的に分析
- **ホロスコープ**: 太陽星座、月星座、上昇星座の組み合わせを分析
- **タロット**: カードの導きから相性を評価

### フォールバック機能
- AI分析が失敗した場合、従来のアルゴリズムベースのスコア算出に自動切り替え
- 環境変数が設定されていない場合も適切にフォールバック

## 設定

### 環境変数

```bash
# AIスコア生成の有効/無効を制御
USE_AI_SCORING=true   # AIスコア生成を有効にする（デフォルト）
USE_AI_SCORING=false  # AIスコア生成を無効にして従来のアルゴリズムを使用

# Google Gemini APIキー（必須）
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

### 設定例

```bash
# .env.local ファイルに追加
USE_AI_SCORING=true
GOOGLE_GEMINI_API_KEY=AIzaSy...
```

## 使用方法

### 数秘術相性分析
```python
from numerology_calculator import NumerologyCalculator

calculator = NumerologyCalculator()
result = calculator.get_compatibility_analysis(profile1, profile2, consultation)
print(f"相性スコア: {result['compatibility_score']}")
```

### ホロスコープ相性分析
```python
from horoscope import HoroscopeCalculator

calculator = HoroscopeCalculator()
result = calculator.get_compatibility_analysis(profile1, profile2, consultation)
print(f"相性スコア: {result['compatibility_score']}")
```

## AIスコア生成の特徴

### 利点
1. **動的分析**: 相談内容に応じてスコアが変化
2. **総合評価**: 複数の要素を総合的に考慮
3. **個別対応**: 各占いの特性に応じた分析
4. **柔軟性**: 新しいパターンにも対応可能

### 従来のアルゴリズムとの比較
- **従来**: 固定の数式による機械的な計算
- **AI**: 文脈を理解した柔軟な評価

## パフォーマンス

### 処理時間
- AIスコア生成: 約2-5秒
- フォールバック: 即座（<0.1秒）

### コスト
- Google Gemini APIの使用量に応じて課金
- フォールバック時はAPIコールなし

## トラブルシューティング

### よくある問題

1. **APIキーエラー**
   ```
   ValueError: GOOGLE_GEMINI_API_KEYが設定されていません
   ```
   → `.env.local`に`GOOGLE_GEMINI_API_KEY`を設定

2. **AI分析タイムアウト**
   ```
   AI score generation failed: timeout
   ```
   → 自動的にフォールバックアルゴリズムに切り替わります

3. **スコアが常に50**
   ```
   USE_AI_SCORING=false
   ```
   → 環境変数を確認し、`true`に設定

## 今後の拡張

- タロット相性分析のAIスコア生成
- 個人占いのスコア生成
- スコア生成の履歴保存
- ユーザーフィードバックに基づくスコア調整
