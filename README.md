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

## 使用方法
```bash
pip install -U sentence-transformers pandas scikit-learn numpy
python example_reorder.py"# SleepingOwl" 
