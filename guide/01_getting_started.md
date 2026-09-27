# 01. 환경 준비와 최소 실행

## 두 종류의 실행을 구별하기

경량 학습 예제는 Python 표준 라이브러리만 사용한다. 저장소 루트에서 실행한다.

```sh
python guide/examples/preflight.py
python guide/examples/reward_lab.py
python guide/examples/analyze_latency.py
python -m unittest discover -s guide/examples -p "test_*.py" -v
```

기대 결과: 설정과 입력 파일 존재 여부, 9 ms 대기 보상 약 -0.4188(`w1=20`), fixture 수신 패킷 4개의 평균 25 ms·p95 40 ms. 이것은 TensorFlow 학습 성공 여부를 확인하는 smoke test가 아니다.

## 전체 시뮬레이터 환경

원 README는 Python 3.9.12를 권장한다. 현재 `requirements.txt`에는 `tensorflow==2.13.0`, `tensorflow-macos==2.13.0`, `appnope`, `wincertstore` 등 서로 다른 플랫폼 대상이 함께 있다. 그대로 설치하면 실패할 수 있다. 패키지 버전을 최신으로 일괄 변경하면 논문 재현과 멀어지므로 대상 OS를 먼저 정한다. 오래된 환경은 별도 VM/컨테이너에서 사용하고 민감한 자격 증명과 분리한다.

권장 절차(전체 설치는 이번 작업에서 실행하지 않음):

1. Python 3.9 환경을 별도로 만든다. `python -m venv .venv-sim`을 실행한다.
2. Windows PowerShell은 `.venv-sim/Scripts/Activate.ps1`, POSIX는 `source .venv-sim/bin/activate`로 활성화한다.
3. `python -m pip --version`으로 격리 환경을 확인한다.
4. `requirements.txt`를 검토해 플랫폼별 파일을 별도로 만든다. Windows/Linux에서는 `tensorflow-macos`, `appnope` 등의 적합성을 검토하고, macOS에서도 `wincertstore` 등 플랫폼 차이를 확인한다. 이 문서는 검증되지 않은 대체 lockfile을 제공하지 않는다.
5. 검토한 파일을 `python -m pip install -r <검토한-요구사항-파일>`로 설치하고 `python -m pip check`를 실행한다. Python·OS·패키지 목록을 실험과 함께 보관한다.
6. 다음 import 확인을 통과한 뒤 모델과 입력 자료의 출처를 확인한다.

```sh
python -c "import simpy, numpy, pandas, networkx, tensorflow; print(tensorflow.__version__)"
```

저장소 루트에서 실행해야 상대 경로가 일치한다. `python SimulationRL.py`는 로그·그림·모델 결과를 쓰며 기본 pretrained H5를 불러온다. `python Simulation.py`는 기준 시뮬레이터다. 단순 import만으로도 많은 의존성과 전역 초기화를 요구하므로 설정 확인 용도로 import하지 않는다.

## 실제 기본값 점검

| 항목 | 현재 값/위치 | 의미 |
| --- | --- | --- |
| 경로 선택 | `pathing=pathings[5]` | Deep Q-Learning |
| 활성 지상국 | `GTs=[2]` | CSV 앞쪽 두 곳, Malaga와 Los Angeles |
| CSV 첫 행 | Kepler, 0.5, Latency, 4.00 | 위성군, 부하 비율, 유형, 초 |
| 이동 간격 | `movementTime=10` | 기본 4초보다 길다 |
| 위치 이동 배율 | `ndeltas=5805.44/20` | 이벤트 간격과 물리적 위치 변화량을 구별 |
| 실행 단계 | `onlinePhase=True` | 위성별 DDQN agent 구성 |
| 조건부 설정 | `explore=False`, `importQVals=True` | 온라인 분기에서 덮어쓴다 |
| 모델 | `pre_trained_NNs/qNetwork_2GTs.h5`, `qTarget_2GTs.h5` | 신뢰 확인 후 사용 |
| 입력 지도 | `Population Map/gpw_v4_population_count_rev11_2020_15_min.tif` | 파일 존재·출처 확인 |

`inputRL.csv`는 첫 데이터 행만 공통 파라미터를 담고 나머지는 위치 목록이다. 뒤 행의 비어 있는 파라미터는 곧바로 손상으로 해석하지 않는다. 현재 CSV에 Pathing을 추가해도 RL 코드의 주석 처리된 읽기 부분은 자동 활성화되지 않는다.

## 초기화 실패를 읽는 순서

- 패키지 설치 실패: Python·OS·아키텍처와 wheel 지원 여부, 플랫폼 전용 항목을 확인한다.
- 모델 파일 없음: `importQVals`와 실제 경로 확인. 예외를 출력한 뒤 정상 모델이 없는 상태로 진행할 위험도 있다.
- 경로 없음: 최소 두 지상국과 연결 가능한 경로가 필요하다. `initialize()`는 `paths[0]`, `paths[1]`를 참조한다.
- 짧은 실험의 그림 오류: 수신 패킷이 없으면 `pathBlocks[1][-1]` 같은 후처리 인덱싱 전제를 만족하지 못할 수 있다.
- 장시간 실행: 위성별 모델 초기화·그림 생성량·학습 빈도·패킷량을 구분해 측정한다. 시뮬레이션 4초는 실제 계산 4초가 아니다.

[가이드로 돌아가기](README.md)
