import pytest

from load_scores import load_scores


def test_header_is_skipped_and_valid_rows_are_returned_in_order(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        "name,score\n"
        " 민지 , 85 \n"
        "민지,90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("민지", 85), ("민지", 90)]
    assert skipped == []


def test_header_only_file_returns_empty_results(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("score", "expected_kept"),
    [
        (-1, []),
        (0, [("학생", 0)]),
        (1, [("학생", 1)]),
        (99, [("학생", 99)]),
        (100, [("학생", 100)]),
        (101, []),
    ],
)
def test_score_boundaries(tmp_path, score, expected_kept):
    csv_file = tmp_path / "boundary.csv"
    csv_file.write_text(f"name,score\n학생,{score}\n", encoding="utf-8")

    kept, _ = load_scores(csv_file)

    assert kept == expected_kept


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("학생", "열 개수가 2가 아님"),
        ("학생,90,추가", "열 개수가 2가 아님"),
        ("학생,", "점수가 비어 있음"),
        ("학생,abc", "점수가 정수가 아님"),
        (",90", "이름이 비어 있음"),
    ],
)
def test_invalid_rows_are_skipped_and_reported(tmp_path, row, reason):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert skipped == [(2, row, reason)]


def test_out_of_range_scores_are_skipped_and_reported(tmp_path):
    csv_file = tmp_path / "out_of_range.csv"
    csv_file.write_text("name,score\n낮은점수,-1\n높은점수,101\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert skipped == [
        (2, "낮은점수,-1", "점수가 0~100 밖"),
        (3, "높은점수,101", "점수가 0~100 밖"),
    ]


def test_blank_line_is_ignored_and_skipped_line_number_is_preserved(tmp_path):
    csv_file = tmp_path / "blank_line.csv"
    csv_file.write_text(
        "name,score\n"
        "학생,90\n"
        "\n"
        "잘못된점수,nope\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("학생", 90)]
    assert skipped == [(4, "잘못된점수,nope", "점수가 정수가 아님")]
