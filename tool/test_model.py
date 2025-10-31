from sentence_transformers import SentenceTransformer

model = SentenceTransformer("./model/bge-small-zh-v1.5")
emb = model.encode(["你好，世界"], normalize_embeddings=True)
print("✅ 模型可用，向量維度：", emb.shape)
