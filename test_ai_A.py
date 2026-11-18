import pytest

from load_scores import load_scores


def test_valid_rows_are_kept_in_order_and_duplicate_names_are_preserved(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(
        "name,score\n"
        " 민지 , 0 \n"
        "민지,100\n"
        '"최,네번",77\n',
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("민지", 0), ("민지", 100), ("최,네번", 77)]
    assert skipped == []


def test_header_only_file_returns_empty_lists(tmp_path):
    csv_file = tmp_path / "header_only.csv"
    csv_file.write_text("name,score\n", encoding="utf-8")

    assert load_scores(csv_file) == ([], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    ("row", "reason"),
    [
        ("학생", "열 개수가 2가 아님"),
        ("학생,90,추가", "열 개수가 2가 아님"),
        ("학생,", "점수가 비어 있음"),
        ("학생,90.5", "점수가 정수가 아님"),
        ("학생,abc", "점수가 정수가 아님"),
        ("학생,-1", "점수가 0~100 밖"),
        ("학생,101", "점수가 0~100 밖"),
        (",90", "이름이 비어 있음"),
        ("   ,90", "이름이 비어 있음"),
    ],
)
def test_invalid_rows_are_skipped_with_line_original_and_reason(
    tmp_path, row, reason
):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(f"name,score\n{row}\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert skipped == [(2, row, reason)]


def test_blank_lines_are_ignored_and_line_numbers_refer_to_csv_rows(tmp_path):
    csv_file = tmp_path / "blank_lines.csv"
    csv_file.write_text(
        "name,score\n"
        "학생,90\n"
        "\n"
        "잘못된 점수,nope\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(csv_file)

    assert kept == [("학생", 90)]
    assert skipped == [(4, "잘못된 점수,nope", "점수가 정수가 아님")]


def test_utf8_bom_is_accepted(tmp_path):
    csv_file = tmp_path / "bom.csv"
    csv_file.write_text("name,score\n학생,90\n", encoding="utf-8-sig")

    assert load_scores(csv_file) == ([("학생", 90)], [])
