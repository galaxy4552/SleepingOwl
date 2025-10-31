import csv

# ===============================================
# 🦉 NewCoolOwl - Smart Homophone Corrector
# ===============================================

CSV_PATH = "homophone_candidates.csv"

# -----------------------------------------------
# 載入修字資料
# -----------------------------------------------
corrections_auto = {}    # ≥0.90 → 自動修正
corrections_hint = {}    # 0.80–0.89 → 顯示建議

with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        wrong = row["wrong_word"].strip()
        correct = row["correct_word"].strip()
        sim = float(row["semantic_sim"])

        if sim >= 0.90:
            corrections_auto[wrong] = correct
        elif 0.80 <= sim < 0.90:
            corrections_hint[wrong] = (correct, sim)

print(f"💎 自動修正詞數：{len(corrections_auto)}")
print(f"🧠 提示建議詞數：{len(corrections_hint)}")
print("---------------------------------------------")

# -----------------------------------------------
# 修正文句
# -----------------------------------------------
def correct_sentence(sentence: str):
    # 第一層：自動修正
    for wrong, correct in corrections_auto.items():
        if wrong in sentence:
            sentence = sentence.replace(wrong, correct)
    # 第二層：提示建議
    hints = []
    for wrong, (correct, sim) in corrections_hint.items():
        if wrong in sentence:
            hints.append((wrong, correct, sim))
    return sentence, hints


# -----------------------------------------------
# 測試輸入
# -----------------------------------------------
if __name__ == "__main__":
    while True:
        text = input("\n📝 請輸入句子（或輸入 exit 離開）：")
        if text.lower() == "exit":
            break

        result, hints = correct_sentence(text)
        print(f"💡 修正結果：{result}")

        if hints:
            print("🧠 建議修正：")
            for wrong, correct, sim in hints:
                print(f"  - 你是否想輸入「{correct}」？ (相似度 {sim:.3f}) [TAB 切換]")
        else:
            print("✅ 沒有修正建議。")
