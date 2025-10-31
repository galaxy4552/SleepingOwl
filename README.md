# SleepingOwl-Homophone 🦉
同音詞語意重排序模組

## 結構
/SleepingOwl-Homophone
├ model/ ← 放置 bge-small-zh-v1.5 模型
├ data/homophone_candidates.csv
├ so_homophone_encoder.py ← Embedding 生成器
├ so_homophone_ranker.py ← 排序器
├ example_reorder.py ← 範例執行檔
└ README.

[ 使用者打字 ]
       ↓
[ 新酷音 ]  ← 傳入你打的注音（ㄗㄨㄛˇ ㄓㄥˋ）
       ↓
[ SleepingOwl-Homophone ]
   ├─ so_homophone_encoder.py   → 把「佐證」「佐証」轉成語意向量
   ├─ so_homophone_ranker.py    → 比較語意距離（例如 0.92 vs 0.75）
   ├─ cuting_bopomofo.py        → 先把所有同音字詞依注音分群
   ├─ data_split/               → 每一群注音的語義矩陣結果
   └─ model/bge-small-zh-v1.5/  → 預訓練語義模型（會算懂語意的數學向量）
       ↓
[ 結果：哪個詞更符合語意或常用語 ]
       ↓
[ 傳回給輸入法 UI → 讓候選詞重排 ]

未來

SleepingOwl/
 ├─ core/                       🧠 核心邏輯引擎
 │   ├─ __init__.py
 │   ├─ so_homophone_encoder.py
 │   ├─ so_homophone_ranker.py
 │   ├─ learn_sqlite.py         
 │   ├─ learn_toggle.py         ← 學習開關
 │   └─ utils.py
 │
 ├─ server/                     🌐 對外 API 層
 │   ├─ server_fastapi.py
 │   └─ websocket_handler.py
 │
 ├─ ui/                         💬 視覺化層（未來可視化）
 │   └─ ui_candidate.py
 │
 ├─ data/                       📦 原始資料
 │   └─ homophone_candidates.csv
 homophone_space.db
 ├─ table: words        ← 所有字詞（含注音與索引）
 ├─ table: homophones   ← 同音群組（群ID、注音）
 ├─ table: pairs        ← 各同音詞對 + 語意分數
 └─ table: embeddings   ← 可選，用於快取語意向量
 ├─ model/                      🧩 預訓練模型
 │   └─ bge-small-zh-v1.5/
 │
 ├─ scripts/                    🛠️ 一次性處理工具
 │   ├─ setup_db.py
 │   ├─ cuting_bopomofo.py
 │   └─ import_embedding.py
 │
 ├─ homophone_space.db          💾 SQLite 主資料庫
 ├─ config_learning.json        ⚙️ 學習開關設定檔
 ├─ README.md
 ├─ LICENSE
 └─ .gitignore

## 使用方法
```bash
pip install -U sentence-transformers pandas scikit-learn numpy
python example_reorder.py"# SleepingOwl" 

---
### 📜 License & Attribution
SleepingOwl-Homophone © 2025 SadlyOwl  
Licensed under the Apache License 2.0

This project integrates open models from:
- **BAAI/bge-small-zh-v1.5** (Apache License 2.0)  
  © Beijing Academy of Artificial Intelligence  
  Used for semantic embedding of Chinese text.

All rights for upstream components belong to their original authors.

This project interacts with or extends **libchewing / 新酷音 (New Chewing)**  
which is licensed under **LGPL v2.1**.  
All rights of libchewing belong to their respective authors.

🧠 Data Privacy
All user selections and adjustments are stored locally in SQLite.  
No data is uploaded or shared.  
Future versions may include an ethical toggle for language personality learning.