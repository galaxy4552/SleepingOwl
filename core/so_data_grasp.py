# so_data_grasp.py
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SODataGrasp:
    def __init__(self, model_path="./model/bge-small-zh-v1.5"):
        self.model = SentenceTransformer(model_path)

    def load_csv(self, path="./data/homophone_candidates.csv"):
        self.df = pd.read_csv(path)
        print(f"[✅] 已載入 {len(self.df)} 筆資料")
        return self.df

    def embed_all(self, column="candidate"):
        texts = self.df[column].tolist()
        self.embeddings = self.model.encode(texts, normalize_embeddings=True)
        print(f"[✅] 已產生 {len(self.embeddings)} 個 embedding 向量")
        return self.embeddings

    def visualize_similarity(self, sample_size=5):
        idx = np.random.choice(len(self.embeddings), sample_size, replace=False)
        subset = self.df.iloc[idx]["candidate"].tolist()
        emb_subset = self.embeddings[idx]
        sim = cosine_similarity(emb_subset)
        print("\n🔍 隨機取樣的相似度矩陣：")
        print(pd.DataFrame(sim, index=subset, columns=subset))

if __name__ == "__main__":
    grasp = SODataGrasp()
    grasp.load_csv()
    grasp.embed_all()
    grasp.visualize_similarity()
