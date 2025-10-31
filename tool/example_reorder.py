# example_reorder.py
from so_homophone_ranker import SOHomophoneRanker

if __name__ == "__main__":
    ranker = SOHomophoneRanker()
    query = "我好累"
    key = "累"
    results = ranker.rank(query, key, top_k=5)
    print("🔍 同音候選詞語意排序結果：")
    for cand, score in results:
        print(f"{cand}\t{score:.4f}")