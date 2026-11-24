from pathlib import Path

import pandas as pd

from analysis import 반별평균, 정제


DATA_DIR = Path(__file__).resolve().parent
scores_df = 정제(pd.read_csv(DATA_DIR / "scores_2026.csv"))
mini_df = 정제(pd.read_csv(DATA_DIR / "mini.csv"))


def test_cleaned_scores_have_100_rows():
    assert len(scores_df) == 100


def test_cleaned_scores_have_only_two_classes():
    assert set(scores_df["반"].unique()) == {"1반", "2반"}


def test_class_score_totals_equal_overall_total():
    class_totals = scores_df.groupby("반")["점수"].sum()
    assert class_totals.sum() == scores_df["점수"].sum()


def test_cleaned_mini_class_1_average_is_80():
    averages = 반별평균(mini_df)
    assert averages["1반"] == 80.0