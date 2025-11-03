# 01. Crawl URLs (BeautifulSoup4)

## Purpose
起点URL（Excelの指定列）から、同一ドメイン配下の下位階層リンクを再帰的に収集します。

## Input
- `beautifulsoup-url_list.xlsx`（例）: 起点URLが記入されたExcel

## Output
- `beautifulsoup-url_list.xlsx` の別シート／CSV: 収集したURL一覧

## Run
```bash
python main.py
