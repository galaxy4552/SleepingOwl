# so_homophone_ranker.py
"""
SleepingOwl Homophone Ranker
利用 encoder 產生的 embedding，比對同音候選詞語意相似度。
"""
import pandas as pd
import numpy as np
from so_homophone_encoder import SOHomophoneEncoder
from sklearn.metrics.pairwise import cosine_similarity

class SOHomophoneRanker:
    def __init__(self, csv_path: str = "./data/homophone_candidates.csv", model_path: str = "./model/bge-small-zh-v1.5"):
        self.encoder = SOHomophoneEncoder(model_path)
        self.df = pd.read_csv(csv_path)
        if "key" not in self.df.columns or "candidate" not in self.df.columns:
            raise ValueError("CSV 檔必須包含 'key' 與 'candidate' 欄位。")
        print(f"[✅] 已載入 {len(self.df)} 組候選詞。")

    def rank(self, input_text: str, key: str, top_k: int = 5):
        """
        根據輸入語句與 key 的候選詞，比對語意相似度。
        """
        subset = self.df[self.df["key"] == key]
        if subset.empty:
            return []

        candidates = subset["candidate"].tolist()
        input_emb = self.encoder.encode(input_text)
        cand_emb = self.encoder.encode(candidates)

        sims = cosine_similarity(input_emb, cand_emb)[0]
        ranked = sorted(zip(candidates, sims), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

if __name__ == "__main__":
    ranker = SOHomophoneRanker()
    results = ranker.rank("我好累", key="累", top_k=3)
    for cand, score in results:
        print(f"{cand} ({score:.4f})")
