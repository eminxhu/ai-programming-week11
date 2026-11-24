# ai-programming-week11

# 성적 관리 프로그램

## 1. What - 무엇을 하나요?
CSV 파일에서 학생의 이름과 점수를 읽고,
유효한 점수만 골라내는 프로그램입니다.
잘못된 데이터는 제외하고 그 이유를 기록합니다.

## 2. Why - 왜 만들었나요?
실제 CSV 파일에는 빈 줄, 잘못된 점수,
이름이 없는 데이터 등이 포함될 수 있습니다.
이러한 데이터를 안전하게 처리하고
오류를 확인하기 위해 만들었습니다.

## 3. How - 어떻게 사용하나요?
Python이 설치된 환경에서 실행합니다.

```bash
python load_scores.py scores.csv
```

## 4. 테스트 방법
먼저 pytest를 설치합니다.

```bash
python -m pip install pytest pytest-cov
```

테스트를 실행합니다.

```bash
python -m pytest test_load_scores.py test_ai_A.py test_ai_B.py
```

커버리지를 확인합니다.

```bash
python -m pytest test_load_scores.py --cov=load_scores --cov-report=term-missing
```

## 5. 파일 구성
- load_scores.py: 성적 CSV 처리 프로그램
- scores.csv: 정상 데이터 예시
- empty.csv: 빈 데이터 테스트 파일
- weird.csv: 비정상 데이터 테스트 파일
- test_load_scores.py: 직접 작성한 테스트
- test_ai_A.py: 코드를 제공하여 AI가 만든 테스트
- test_ai_B.py: 명세를 제공하여 AI가 만든 테스트
- README.md: 프로그램 설명 문서
- LICENSE: MIT 라이선스

## 6. 만든 사람 및 AI 활용
- 작성자: 이민주_2026101040
- AI 활용: GitHub Copilot을 이용한
  테스트 코드 생성, 오류 수정 및 테스트 비교
- 최종 테스트 결과는 직접 실행하여 확인함

## 데이터

- 출처: AI 협업 프로그래밍 12주차 실습 배포 자료
- 파일명: scores_2026.csv
- 인코딩: UTF-8
- 원본 데이터: 114행 5열
- 정제 후 데이터: 100행 5열

### 열 설명
- 학번: 학생 식별 번호
- 이름: 학생 이름
- 반: 학생이 소속된 반
- 과목: 평가 과목
- 점수: 0~100점 사이의 정수

### 데이터 정제 방법
- 점수가 비어 있는 6행 삭제
- 완전히 동일한 중복 4행 삭제
- 반과 과목의 앞뒤 공백 제거
- 정상 점수 범위를 벗어난 4행 삭제

### 빈 칸 처리 이유
점수가 비어 있는 행을 0점으로 처리하면 실제로
0점을 받은 학생과 구분할 수 없고 평균에도
영향을 주기 때문에 해당 행을 삭제하였다.

### 실행 및 검증 방법
교수님이 배포한 scores_2026.csv와 mini.csv를
week12 폴더에 넣은 후 다음 명령어를 실행한다.

    cd week12
    python3 analysis.py
    python3 -m pytest -q

테스트 결과: 4 passed