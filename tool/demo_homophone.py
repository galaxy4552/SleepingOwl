from core.so_homophone_ranker import rank_candidates

def main():
    print("🦉 SleepingOwl Homophone Demo")
    while True:
        bpmf = input("\n輸入注音（例如 ㄗㄨㄛˇ ㄓㄥˋ）或 q 離開：")
        if bpmf.lower() == "q":
            break
        result = rank_candidates(bpmf)
        for w, s in result:
            print(f"{w:<6}  {s:.3f}")

if __name__ == "__main__":
    main()
