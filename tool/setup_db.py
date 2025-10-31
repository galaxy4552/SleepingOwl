from core.learn_sqlite import init_db, import_homophones

# 初始化資料庫
init_db()

# 匯入資料
import_homophones("data/homophone_candidates.csv")
