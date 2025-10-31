# core/so_homophone_ranker.py
from core.so_homophone_encoder import SOHomophoneEncoder
from core.learn_sqlite import DB_PATH
import sqlite3

# -------------------------------
# 🦉 Step 1：正規化注音（去掉聲調符號）
# -------------------------------
def normalize_bopomofo(bpmf: str) -> str:
    """移除所有聲調符號（ˊ ˇ ˋ ˙）"""
    for tone in ["ˊ", "ˇ", "ˋ", "˙"]:
        bpmf = bpmf.replace(tone, "")
    return bpmf.strip()


# -------------------------------
# 🦉 Step 2：候選詞排序查詢
# -------------------------------
def rank_candidates(query: str, top_n: int = 10):
    """
    根據注音或詞查詢同音群，並依平均語意分數排序。
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1️⃣ 正規化注音（移除聲調符號）
    query_norm = normalize_bopomofo(query)

    # 2️⃣ 嘗試用無聲調的注音查詢
    rows = cur.execute(
        """
        SELECT word_a, word_b, score
        FROM pairs
        WHERE REPLACE(REPLACE(REPLACE(REPLACE(bopomofo, 'ˊ', ''), 'ˇ', ''), 'ˋ', ''), '˙', '') = ?
        """,
        (query_norm,)
    ).fetchall()

    # 3️⃣ 若找不到，再嘗試用詞本身查注音群
    if not rows:
        rows = cur.execute(
            "SELECT word_a, word_b, score FROM pairs WHERE word_a = ? OR word_b = ?",
            (query, query)
        ).fetchall()

    conn.close()

    if not rows:
        print(f"⚠️ 沒找到 {query} 的資料。")
        return []

    # 4️⃣ 整理每個詞的平均分數
    scores = {}
    for w1, w2, s in rows:
        scores[w1] = scores.get(w1, []) + [s]
        scores[w2] = scores.get(w2, []) + [s]

    avg_scores = [(w, sum(v)/len(v)) for w, v in scores.items()]
    avg_scores.sort(key=lambda x: x[1], reverse=True)

    return avg_scores[:top_n]
