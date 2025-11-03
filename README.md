# Website Analysis Pipeline – Crawl → Screenshot → OCR → GPT → Excel

## 🧭 Overview
対象Webサイトの下位階層URLを収集し、スクリーンショット → OCR → GPT分析 → Excel転記までを一気通貫で行う半自動パイプラインです。

- 01: BeautifulSoup4で下層リンクを再帰取得
- 02: Playwrightで各URLを全画面スクショ（並列）
- 03: TesseractでOCR（IMPROVED版は前処理あり）
- 04: GPTで企業の得意分野・ハッシュタグを抽出
- 05: GPT出力をExcelテンプレートに自動転記（`-1` と `-2` の2系統あり）

> **注意**: `05-1_*.py` と `05-2_*.py` は **どちらか一方** を運用します。`-2` は新バージョンですが、ケースにより優劣は異なります。

---

## 🔄 Workflow
```mermaid
flowchart TD
  A01[01 Crawl URLs<br>BeautifulSoup4] --> A02[02 Screenshot<br>Playwright]
  A02 --> A03[03 OCR<br>Tesseract]
  A03 --> A04[04 GPT Analysis<br>企業強み＋ハッシュタグ]
  A04 --> A05[05 Write to Excel<br>Structure_Beauty.xlsx]
```
---
## 🧰 Requirements
Python 3.10+
Node.js（Playwright初回セットアップで必要な場合あり）
```
pip install -r requirements.txt
# Playwright 初回のみ
python -m playwright install
```
---
## 🚀 Quick Start
```
# 01: URL収集（Excelの起点URLから下層リンク再帰取得）
python 01_crawl_urls/main.py

# 02: URL群をヘッドレスで全画面スクショ（並列）
python 02_screenshot_pages/main.py

# 03: スクショをOCRしてテキスト化（改良版推奨）
python 03_ocr_text_extraction/main_improved.py

# 04: GPTで分析（プロンプトは 04_gpt_analysis/analysis_prompt.txt）
#  → 出力を transcripted_*.xlsx などに保存

# 05: Excelテンプレに自動転記（-1 または -2 を選択）
python 05_excel_output/move_results_v2.py
```
