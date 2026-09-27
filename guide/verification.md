# 검증 기록

확인일: 2026-09-27. Windows, Python 3.13.5, 학습 예제는 표준 라이브러리 사용. 원 프로젝트 전체 실행 환경인 Python 3.9와 구별한다.

## 수행한 검증

- `python -m unittest discover -s guide/examples -p "test_*.py" -v`: 5개 테스트 통과. 설정 읽기, 실제 큐 보상 산술, toy DDQN, fixture 지연 통계, 잘못된 CSV 거부.
- `preflight.py`, `reward_lab.py`, `analyze_latency.py` 직접 실행 통과. 입력 31개 위치, 첫 행 4초·Kepler·0.5, 필요한 네 파일 존재 확인.
- 큐 보상(0.009초,20): -0.418789674153599. toy DDQN target: 2.8.
- fixture: 4개 수신 샘플, 평균 25 ms, median 25 ms, nearest-rank p95 40 ms. 실제 네트워크 실험 결과가 아님.
- 노트북 3개 `nbformat.validate` 및 code cell 실행 통과. 노트북 결과는 커밋에 포함하지 않아 실행 전 상태로 제공한다.
- 새 문서의 상대 파일 링크 31개 확인, 누락 없음. 원본 README의 기존 외부 URL 전체 상태 검사는 수행하지 않았다.
- [Archify 검증](../docs/archify/README.md): showcase 9/9, 오류·경고 0, 브라우저 네 해상도와 light/dark 이미지 검토 완료.

## 수행하지 않은 검증

전체 requirements 설치, TensorFlow 학습, 모델 역직렬화, CUDA/GPU, SimPy end-to-end, 논문 결과 재현, 라이선스 법률 판단은 하지 않았다. 플랫폼 혼합 의존성, 학습 target 차이, 짧은 실행의 빈 수신 결과, 이동 후 stale-neighbor 드롭 위험은 문서에 별도로 설명했다.

README 번역은 원문 구조의 한국어 요약이며 원문 전문 번역이 아니다. 설치·동작·사용·후처리·인용·알려진 문제의 누락 여부와 코드/단위/링크를 대조했다.

[가이드](README.md)
