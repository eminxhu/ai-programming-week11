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
