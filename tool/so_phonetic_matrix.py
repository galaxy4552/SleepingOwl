# so_phonetic_matrix.py
"""
SleepingOwl - 同注音語意矩陣生成器
依據注音群組建立 embedding 相似度矩陣。
"""

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SOPhoneticMatrix:
    def __init__(self, model_path="./model/bge-small-zh-v1.5"):
        self.model = SentenceTransformer(model_path)
    
    def load_csv(self, path="./data/homophone_candidates.csv"):
        self.df = pd.read_csv(path)
        print(f"[✅] 已載入 {len(self.df)} 筆資料")
        return self.df

    def build_matrix(self):
        grouped = self.df.groupby("bopomofo")
        for bopomofo, group in grouped:
            words = sorted(set(group["word1"].tolist() + group["word2"].tolist()))
            if len(words) < 2:
                continue
            
            embeddings = self.model.encode(words, normalize_embeddings=True)
            sim_matrix = cosine_similarity(embeddings)

            print(f"\n=== {bopomofo} ===")
            df_matrix = pd.DataFrame(sim_matrix, index=words, columns=words)
            print(df_matrix.round(3))

    def export_all(self, out_dir="./output_matrices"):
        import os
        os.makedirs(out_dir, exist_ok=True)
        grouped = self.df.groupby("bopomofo")
        for bopomofo, group in grouped:
            words = sorted(set(group["word1"].tolist() + group["word2"].tolist()))
            if len(words) < 2:
                continue
            embeddings = self.model.encode(words, normalize_embeddings=True)
            sim_matrix = cosine_similarity(embeddings)
            df_matrix = pd.DataFrame(sim_matrix, index=words, columns=words)
            safe_name = bopomofo.replace(" ", "_").replace("ˇ","3").replace("ˋ","4").replace("ˊ","2").replace("˙","5")
            df_matrix.to_csv(f"{out_dir}/{safe_name}.csv", encoding="utf-8-sig")
        print(f"[💾] 所有矩陣已輸出至 {out_dir}/")

if __name__ == "__main__":
    so = SOPhoneticMatrix()
    so.load_csv("./data/homophone_candidates.csv")
    so.build_matrix()
    # so.export_all()  # 若要批次匯出所有矩陣
