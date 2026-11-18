
import pytest
import runpy
from pathlib import Path

from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    csv_file = tmp_path / "scores_with_blank_line.csv"
    csv_file.write_text("name,score\n학생,90\n\n", encoding="utf-8")
    kept, skipped = load_scores(csv_file)
    assert kept == [("학생", 90)]
    assert len(skipped) == 0


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과를_돌려준다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize(
    ("score", "is_valid"),
    [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)],
)
def test_점수_경계값(tmp_path, score, is_valid):
    csv_file = tmp_path / "scores_boundary.csv"
    csv_file.write_text(f"name,score\n학생{score},{score}\n", encoding="utf-8")
    kept, skipped = load_scores(csv_file)
    assert ((f"학생{score}", score) in kept) is is_valid


def test_이름이_비어_있으면_건너뛴다(tmp_path):
    csv_file = tmp_path / "scores_empty_name.csv"
    csv_file.write_text("name,score\n,90\n", encoding="utf-8")

    kept, skipped = load_scores(csv_file)

    assert kept == []
    assert "이름이 비어 있음" in repr(skipped)


def test_main_실행_시_읽은_줄과_건너뛴_줄을_출력한다(tmp_path, monkeypatch, capsys):
    (tmp_path / "scores.csv").write_text(
        "name,score\n정상학생,90\n잘못된학생,abc\n", encoding="utf-8"
    )
    script = Path(__file__).with_name("load_scores.py")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", [str(script), str(tmp_path / "scores.csv")])

    runpy.run_path(str(script), run_name="__main__")

    output_lines = capsys.readouterr().out.splitlines()
    assert any("읽은" in line and "1" in line for line in output_lines)
    assert any("건너뛴" in line and "1" in line for line in output_lines)