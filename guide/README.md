# 위성 라우팅 코드 학습 가이드

작성일: 2026-09-27

## 목차

1. [환경 준비와 최소 실행](01_getting_started.md)
2. [기초 개념과 코드 읽기](02_core_concepts.md)
3. [심화 실험·성능·재현성](03_advanced.md)
4. [설정 점검 노트북](01_foundations.ipynb)
5. [보상과 DDQN 실습](02_practice.ipynb)
6. [지연 결과 분석 실습](03_advanced.ipynb)
7. [검증 기록](verification.md)
8. [실제 코드 아키텍처](../docs/archify/README.md)

## 출처와 작업 범위

[hundong2 fork](https://github.com/hundong2/MA-DRL_Routing_Simulator), 기본 브랜치 `main`, 분석 revision `29b9325e3938d620ccd017dc1b475ce704fc6dd9`. 원 프로젝트는 [SatCom-TELMA](https://github.com/SatCom-TELMA/MA-DRL_Routing_Simulator)다. Python 코드, CSV 설정, README, 의존성과 모델 파일 위치를 확인했다. LICENSE는 확인하지 못했다. 상용 재배포 허가나 논문과 동일한 실험 재현을 의미하지 않는다.

단일 GitHub 요청에 따라 서브모듈 안에 문서·예제를 추가했다. 원래 시뮬레이션 코드는 수정하지 않았다. 대용량 역사 대신 최신 커밋을 얕게 받고 재귀 초기화·업데이트했다.

## 한눈에 보기

문제는 ‘위성까지 가장 가까운 경로’와 ‘패킷이 가장 빨리 도착하는 경로’의 차이다. 움직이는 위성과 큐 혼잡을 SimPy에서 모사하고, 기준 최단 경로와 분산 학습 경로를 비교한다. 실제 위성 제어·무선 통신 프로그램이나 실시간 네트워크 서비스는 아니다.

## 학습 순서와 완료 기준

| 단계 | 선수 지식 | 실습과 완료 기준 |
| --- | --- | --- |
| 기초 | Python 함수·CSV·그래프 | 설정 점검 결과에서 학습 설정과 모델 불러오기 설정을 구별한다 |
| 응용 | 상태·행동·보상, 할인율 | 큐 보상 단위와 DDQN의 선택/평가 분리를 설명한다 |
| 심화 | 통계·실험 설계 | 수신 완료 패킷의 p95와 전체 전달률이 다른 이유를 설명한다 |
| 연구 | SimPy·TensorFlow, 위성 링크 | 격리 환경을 구축하고 반복 seed·토폴로지 이동·부하 실험을 수행한다 |

Python 3.9 이상에서 `python -m unittest discover -s guide/examples -p "test_*.py" -v`로 경량 예제를 검증한다. 노트북은 같은 예제의 학습 인터페이스다. TensorFlow를 설치하거나 `.h5`/`.npy`를 읽지 않는다.

[원본 README](../README.md) · [한국어 번역 요약](../README_kor.md) · [관련 논문과 독립 toy 실습](https://github.com/hundong2/laboratory/tree/main/ma-drl-satellite-routing)
