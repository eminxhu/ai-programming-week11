import pandas as pd


def 정제(df):
    cleaned = df.copy()

    # 점수가 비어 있는 행을 삭제한다.
    cleaned = cleaned.dropna(subset=["점수"])
    print(f"점수 결측 제거 후 행 수: {len(cleaned)}")

    # 모든 열의 값이 같은 중복 행을 삭제한다.
    cleaned = cleaned.drop_duplicates()
    print(f"중복 제거 후 행 수: {len(cleaned)}")

    # 반과 과목 값의 앞뒤 공백을 제거한다.
    cleaned["반"] = cleaned["반"].str.strip()
    cleaned["과목"] = cleaned["과목"].str.strip()
    print(f"공백 제거 후 행 수: {len(cleaned)}")

    # 점수가 정수가 아니거나 0~100 범위 밖인 행을 삭제한다.
    valid_scores = cleaned["점수"].between(0, 100) & cleaned["점수"].mod(1).eq(0)
    cleaned = cleaned.loc[valid_scores].copy()
    cleaned["점수"] = cleaned["점수"].astype(int)
    print(f"점수 범위 확인 후 행 수: {len(cleaned)}")

    return cleaned


def 반별평균(df):
    statistics = df.groupby("반")["점수"].agg(["count", "mean", "median", "max"])
    statistics = statistics.rename(
        columns={
            "count": "개수",
            "mean": "평균",
            "median": "중앙값",
            "max": "최댓값",
        }
    ).round(2)
    print(statistics)
    return statistics["평균"]


if __name__ == "__main__":
    df = pd.read_csv("scores_2026.csv")
    print("시작 행 수:", len(df))
    df = 정제(df)

    print("반 종류:", sorted(df["반"].unique()))
    print("과목 종류:", sorted(df["과목"].unique()))

    math_df = df[df["과목"] == "수학"]
    print("수학 행 수:", len(math_df))

    class1_high_score_df = df[(df["반"] == "1반") & (df["점수"] >= 90)]

    class_score_average = df.groupby("반")["점수"].mean()
    print("반별 점수 평균:")
    print(class_score_average)
    반별평균(df)

    subject_class_score_average = df.groupby(["과목", "반"])["점수"].mean()
    print("과목·반별 점수 평균:")
    print(subject_class_score_average)