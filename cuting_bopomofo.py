import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# === 載入資料與模型 ===
df = pd.read_csv("data/homophone_candidates.csv")
model = SentenceTransformer("./model/bge-small-zh-v1.5")

# === 建立輸出資料夾 ===
output_dir = "data_split"
os.makedirs(output_dir, exist_ok=True)

group_count = 0

# === 逐注音群組分批處理 ===
for bopomofo, group in df.groupby("bopomofo"):
    group_count += 1
    print(f"\n=== {bopomofo} ===")

    # 收集該群組的所有詞
    words = sorted(set(group["word1"].tolist() + group["word2"].tolist()))
    if len(words) < 2:
        continue  # 跳過只有一個詞的群組

    # 生成向量
    vecs = model.encode(words, normalize_embeddings=True)

    # 計算相似度矩陣
    sim = cosine_similarity(vecs)
    df_matrix = pd.DataFrame(sim, index=words, columns=words).round(3)

    # 只印出非全 1.0 的群組（避免刷滿螢幕）
    if not np.allclose(sim, 1.0):
        print(df_matrix)

    # === 儲存成 CSV ===
    # 把特殊符號轉成安全檔名（例如 ㄧˊ → _yi2）
    safe_name = (
        bopomofo.replace(" ", "_")
        .replace("ˇ", "3")
        .replace("ˋ", "4")
        .replace("ˊ", "2")
        .replace("˙", "5")
    )

    output_path = os.path.join(output_dir, f"{safe_name}.csv")
    df_matrix.to_csv(output_path, encoding="utf-8-sig")

print(f"\n💾 共輸出 {group_count} 個注音群組，存放於 {output_dir}/")
