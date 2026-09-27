# 위성망 MA-DRL 라우팅 시뮬레이터

작성·확인일: 2026-09-27

[원본 README](README.md) · [한국어 학습 가이드](guide/README.md) · [코드 아키텍처](docs/archify/README.md)

## 번역 범위

[원본 저장소](https://github.com/hundong2/MA-DRL_Routing_Simulator)의 영어 README 구조에 따른 **한국어 번역 요약**이다. 분석 기준은 `29b9325e3938d620ccd017dc1b475ce704fc6dd9`이다. 저장소에서 LICENSE 파일과 명시적 번역·재배포 허락을 확인하지 못해 전문 복제는 하지 않았다. 논문의 공개 라이선스가 코드에도 적용된다고 가정하지 않는다. 아래 ‘확인 메모’는 번역이 아니라 코드 대조 결과다.

## 소개와 데모

위성군을 통해 전달되는 데이터 블록과 지연을 SimPy 이산사건 시뮬레이션으로 연구한다. 말라가에서 로스앤젤레스로 전달하는 [이동 위성군 데모](https://drive.google.com/file/d/1214G8oXsMLaqqRrAIqweVkSTFjZ3FOHx/view?usp=sharing)가 있다.

## 요구 사항과 설치

원문은 Python 3.9(권장 3.9.12), 가상환경과 [requirements.txt](requirements.txt)를 안내한다. 큰 이력을 피하려고 얕은 복제를 권한다. 운영체제 호환성과 모델 신뢰성 점검은 [설치 가이드](guide/01_getting_started.md)를 먼저 읽는다.

## 동작 설명

지상국이 목적지별 블록을 생성한다. 비학습 방식은 최단 경로를 미리 계산하고, 강화학습 방식은 전달 과정에서 다음 위성을 선택한다. 지상국과 위성 링크의 FIFO 대기열, 전송·전파 지연을 처리한다. 위성 위치를 갱신하면 링크도 다시 연결한다.

## 사용과 후처리

[SimulationRL.py](SimulationRL.py)는 학습 라우팅, [Simulation.py](Simulation.py)는 기준 경로와 링크율 실험의 진입점이다. CSV가 지상국·위성군·부하·기간을 지정한다. 추가 학습 설정은 코드에서 조절한다. 생성 결과는 [후처리 노트북](Post-Processing/Post-Results.ipynb)으로 분석한다. 인구 자료 출처는 [GPW v4](https://sedac.ciesin.columbia.edu/data/collection/gpw-v4/sets/browse)다.

## 연락과 인용

문제는 저장소 issue 또는 [저자 Scholar](https://scholar.google.es/citations?hl=es&user=6PZm2aYAAAAJ)를 통해 확인한다. 연구 이용 시 원문 Citation의 서지정보를 사용한다.

- *Continual Deep Reinforcement Learning for Decentralized Satellite Routing*, 2025, [DOI](https://doi.org/10.1109/TCOMM.2025.3562522).
- *An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks*, SPAICE2024, 420–424, [DOI](https://doi.org/10.5281/zenodo.13885645).

## 알려진 문제

원문은 이동 후 오래된 이웃으로 전송하는 문제와 과거 트래픽 생성 분모 오류를 알린다. 드롭 빈도와 코드 버전을 결과에 함께 보고해야 한다.

## 확인 메모: 현재 코드와 과거 설명의 차이

- 현재 `inputRL.csv`에는 `Pathing` 열이 없다. 실제 선택은 `SimulationRL.py`의 전역 `pathing`이다.
- `inputsRL.py`라는 파일은 없다. RL 설정은 `SimulationRL.py`에 있다.
- 기본 실행은 4초이고 `movementTime=10`이다. 기본 조건으로 반복 이동 성능을 평가할 수 없다.
- `onlinePhase=True`가 `explore=False`, `importQVals=True`를 설정한다. 새 모델 학습과 동일한 실행이 아니다.
- CSV 저장 후 그림용 지연을 ms로 변환한다. 저장 CSV의 초 단위에 주의한다.
- `.npy` 객체·H5 모델은 신뢰할 수 있는 파일만 격리 환경에서 처리한다.

전체 학습 실행은 이번 문서 작업에서 검증하지 않았다. [검증 범위와 실행 기록](guide/verification.md)을 참고한다.
