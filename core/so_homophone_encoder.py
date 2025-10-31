# so_homophone_encoder.py
"""
SleepingOwl Homophone Encoder
負責載入 bge-small-zh-v1.5 模型並將輸入字詞轉為 embedding 向量。
"""
from sentence_transformers import SentenceTransformer
import numpy as np
import os

class SOHomophoneEncoder:
    def __init__(self, model_path: str = "./model/bge-small-zh-v1.5"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"找不到模型資料夾: {model_path}")
        self.model = SentenceTransformer(model_path)
        print(f"[✅] 模型已載入：{model_path}")

    def encode(self, texts):
        """
        將文字或文字列表轉成向量。
        """
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return np.array(embeddings)

if __name__ == "__main__":
    encoder = SOHomophoneEncoder()
    sample = ["我好累", "我很困"]
    vectors = encoder.encode(sample)
    print("Embedding 維度：", vectors.shape)
    