import asyncio
import os
import pandas as pd
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm_asyncio

# === ExcelからURLリストを取得 ===
excel_path = r"C:\Users\tohjo\OneDrive\桌面\荒井\プロジェクト\対象企業の得意分野とハッシュタグ分析\beautifulsoup-url_list.xlsx"
df = pd.read_excel(excel_path, header=None)

# A列にTarget URL、その下にクロール済みURLがある形式
target_urls = []
total_urls = 0
for col in df.columns:
    urls = df[col].dropna().tolist()
    if urls:
        target_urls.append(urls)
        total_urls += len(urls)

# === 実行確認 ===
print(f"スクリーンショット対象URLは合計 {total_urls} 件あります。実行しますか？ (y/n)")
if input().strip().lower() != "y":
    print("処理を中止しました。")
    exit()

# === 出力ディレクトリ ===
base_output = r"C:\Users\tohjo\OneDrive\桌面\荒井\プロジェクト\対象企業の得意分野とハッシュタグ分析\playwright_output"
os.makedirs(base_output, exist_ok=True)

async def auto_scroll(page):
    """ページを下までスクロールして遅延ロードをトリガー"""
    await page.evaluate("""
        async () => {
            await new Promise(resolve => {
                let totalHeight = 0;
                const distance = 500;
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= document.body.scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 200);
            });
        }
    """)

async def capture(context, url, folder, index, retry=2):
    """1 URLをスクショ（リトライ付き）"""
    filename = f"screenshot_{index+1}.png"
    save_path = os.path.join(folder, filename)

    for attempt in range(retry+1):
        try:
            page = await context.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=120_000)

            # ページ全体をスクロールしてコンテンツをロード
            await auto_scroll(page)
            await page.wait_for_timeout(2000)  # スクロール後の描画待ち

            await page.screenshot(path=save_path, full_page=True)
            await page.close()
            await asyncio.sleep(1)  # 安定性のため各URL後に待機
            return filename
        except Exception as e:
            print(f"Error capturing {url} (try {attempt+1}/{retry+1}) - {e}")
            if attempt == retry:
                return f"FAILED_{filename}"
        await asyncio.sleep(3)  # リトライ間隔を3秒に延長

async def process_target(context, urls, domain, last_dir):
    """1 Target URL に対応する一連のURL群を処理"""
    folder_name = f"for-ocr_{domain}_{last_dir}"
    folder = os.path.join(base_output, folder_name)
    os.makedirs(folder, exist_ok=True)

    results = []
    chunk_size = 3  # 並列度を3に設定
    for start in range(0, len(urls), chunk_size):
        chunk = urls[start:start+chunk_size]
        tasks = [capture(context, u, folder, i+start) for i, u in enumerate(chunk)]
        chunk_results = await tqdm_asyncio.gather(
            *tasks,
            desc=f"スクリーンショット進捗({start+1}-{start+len(chunk)})",
            total=len(chunk)
        )
        results.extend(chunk_results)
    return folder, results

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for urls in target_urls:
            root = urls[0]
            domain = urlparse(root).netloc
            last_dir = urlparse(root).path.strip("/").split("/")[-1] or "root"
            folder, results = await process_target(context, urls, domain, last_dir)
            print(f"\n{root} のスクリーンショット完了 → {folder}")
            for name in results:
                print(f"  {name}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
