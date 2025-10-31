# ================================================
# 🦉 NewCoolOwl - Homophone Extractor (TSI version)
# ================================================
# 用途：
#   從 tsi.csv 自動找出同音異詞
#   並輸出成 homophone_candidates.csv
#
# 需求：
#   pip install sentence-transformers tqdm
# ================================================

import csv
from collections import defaultdict
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
import os

# -----------------------------------------------
# 路徑設定
# -----------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "tsi.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "homophone_candidates.csv")

# -----------------------------------------------
# Step 1. 讀入詞庫並按注音分組
# -----------------------------------------------
if not os.path.exists(DATA_PATH):
    print(f"[錯誤] 找不到詞庫檔案：{DATA_PATH}")
    print("請確認 tsi.csv 已存在。")
    exit(1)

groups = defaultdict(list)
with open(DATA_PATH, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) != 3:
            continue
        word, freq, zhuyin = row
        try:
            freq = int(freq)
        except ValueError:
            continue
        groups[zhuyin].append((word, freq))

# 只保留有多於 1 個詞的注音群
groups = {k: v for k, v in groups.items() if len(v) > 1}
print(f"分組完成，共 {len(groups)} 組具有多個同音詞。")

# -----------------------------------------------
# Step 2. 載入 embedding 模型
# -----------------------------------------------
print("載入模型 BAAI/bge-small-zh-v1.5 ...")
model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# -----------------------------------------------
# Step 3. 計算頻率比與語義相似度
# -----------------------------------------------
results = []
for zy, words in tqdm(groups.items(), desc="計算中"):
    # 按詞頻由高到低排序
    words.sort(key=lambda x: x[1], reverse=True)
    main_word, main_freq = words[0]

    # 若主要詞頻為 0，略過該組
    if main_freq == 0:
        continue

    main_vec = model.encode(main_word, normalize_embeddings=True)

    for word, freq in words[1:]:
        if main_freq == 0:  # 再次保險
            continue
        freq_ratio = round(freq / main_freq, 3)

        word_vec = model.encode(word, normalize_embeddings=True)
        sim = util.cos_sim(main_vec, word_vec).item()
        if sim > 0.7 and freq_ratio < 0.5:
            results.append([zy, word, main_word, freq_ratio, round(sim, 3)])

# -----------------------------------------------
# Step 4. 輸出結果
# -----------------------------------------------
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["zhuyin", "wrong_word", "correct_word", "freq_ratio", "semantic_sim"])
    writer.writerows(results)

print()
print(f"✅ 完成，共輸出 {len(results)} 筆結果：{OUTPUT_PATH}")
