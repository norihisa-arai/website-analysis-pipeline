import os
import pytesseract
from PIL import Image, ImageFilter
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # 進捗バー

# ★ 画像前処理関数（白黒化＋二値化＋ノイズ除去）
def preprocess_image(image):
    image = image.convert("L")  # グレースケール化
    image = image.point(lambda x: 0 if x < 140 else 255)  # 二値化
    image = image.filter(ImageFilter.MedianFilter())  # ノイズ除去
    return image

def ocr_image(image_path):
    """1枚の画像をOCR"""
    filename = os.path.basename(image_path)
    image = Image.open(image_path)
    image = preprocess_image(image)  # ★ 前処理追加
    config = '--psm 6'  # ★ 単一ブロック想定
    text = pytesseract.image_to_string(image, lang="jpn+eng", config=config)  # ★ 言語強化
    return filename, text

def process_folder(folder_path):
    """1フォルダ内の画像をOCRしてtxtにまとめる"""
    folder_name = os.path.basename(folder_path)
    output_txt = os.path.join(folder_path, f"{folder_name}.txt")

    image_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not image_files:
        print(f"画像が見つかりません: {folder_name}")
        return

    ocr_results = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(ocr_image, img) for img in image_files]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"OCR進捗: {folder_name}"):
            filename, text = future.result()
            ocr_results.append((filename, text))

    ocr_results.sort(key=lambda x: x[0])

    with open(output_txt, "w", encoding="utf-8") as f:
        for filename, text in ocr_results:
            f.write(f"=== {filename} ===\n")
            f.write(text.strip())
            f.write("\n\n")

    print(f"OCR完了: {output_txt}")

def main():
    base_folder = r"C:\Users\tohjo\OneDrive\桌面\荒井\プロジェクト\対象企業の得意分野とハッシュタグ分析\playwright_output"

    target_folders = [
        os.path.join(base_folder, d)
        for d in os.listdir(base_folder)
        if os.path.isdir(os.path.join(base_folder, d)) and d.startswith("for-ocr_")
    ]

    if not target_folders:
        print("対象フォルダ（for-ocr_で始まる）が見つかりませんでした。")
        return

    for folder in target_folders:
        process_folder(folder)

    print("\nすべてのOCR処理が完了しました！")

if __name__ == "__main__":
    main()
