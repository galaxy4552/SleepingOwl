from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
model.save("./model/bge-small-zh-v1.5")  # 下載後儲存到本地