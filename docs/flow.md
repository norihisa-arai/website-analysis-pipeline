# Workflow Diagram

```mermaid
flowchart TD
  A01["01 Crawl URLs<br>BeautifulSoup4"] --> A02["02 Screenshot<br>Playwright"]
  A02 --> A03["03 OCR<br>Tesseract"]
  A03 --> A04["04 GPT Analysis<br>企業強み＋ハッシュタグ"]
  A04 --> A05["05 Write to Excel<br>Structure_Beauty.xlsx"]
```

💡 **ポイント**  
- これは GitHub 上で自動的に「矢印付きのフローチャート」として描画されます。  
- これを `docs/flow.md` にしておくと、READMEをスッキリ保ったままワークフローを別ページで見せられます。  

---

## （４）⚙️ requirements.txt  
> 「このプロジェクトを動かすために必要なPythonパッケージを一覧にする」

### 🎯 目的  
- 誰が見ても「どんなライブラリを使っているか」がわかる。  
- ほかの人（採用担当・技術者）が簡単に再現できる。  

### 💪 あなたがやること
1️⃣ `website-analysis-pipeline/` の直下に `requirements.txt` を作る。  
2️⃣ 次の内容をコピペして保存👇  

```txt
beautifulsoup4
requests
lxml
pandas
openpyxl
tqdm```
playwright
Pillow
pytesseract
opencv-python
python-dotenv
