# 03. OCR Text Extraction (Tesseract)

## Purpose
スクリーンショット画像から文字を抽出します。`main_improved.py` は前処理（ノイズ除去・二値化等）付き。

## Output
- `ocr_output/` に URL単位の `.txt` 保存

## Run
```bash
# 通常版
python main.py
# 改良版（推奨）
python main_improved.py
