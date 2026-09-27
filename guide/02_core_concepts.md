# 02. 기초 개념과 코드 읽기

## 시간과 단위

링크 지연의 교육용 분해는 `queue_seconds + block_bits / rate_bps + distance_m / c_mps`다. `BLOCK_SIZE=64800`은 bit이며 byte와 혼용하면 전송 시간이 8배 달라진다. 전송 지연은 데이터를 링크에 넣는 시간, 전파 지연은 신호가 공간을 이동하는 시간이다. 이벤트 큐와 링크별 송신 큐는 다른 자료구조다.

| 용어 | 코드에서의 역할 |
| --- | --- |
| GT/Gateway, 지상국 | 데이터 생성·송수신 끝점 |
| ISL, Inter-Satellite Link | 위성 사이 링크, 링크별 FIFO |
| GSL, Ground-to-Satellite Link | 지상국↔위성 링크 |
| LEO, Low Earth Orbit | 저궤도 위성군의 위치·연결 모델 |
| DQN, Deep Q-Network | 관측 상태에서 네 방향의 행동 가치를 출력 |
| DDQN, Double DQN | 행동 선택망과 목표 평가망을 분리 |
| Replay buffer | 이전 전이를 모아 minibatch 학습 |
| Continual learning | 변화 중 관측을 받아 정책을 계속 갱신하는 설정 |

## 대표 실행 경로

`SimulationRL.py:6798`의 main → `RunSimulation:6594` → `initialize:4426` → `Earth:1984`와 `createGraph:5128` → `env.run` → 지상국/위성 이벤트 → 통계·그림·모델 저장이다. 실제 구현은 단일 Python 프로세스의 큰 파일에 모여 있다. 다중 에이전트라고 해서 위성별 운영체제 프로세스나 네트워크 RPC가 생기는 것은 아니다.

- `Gateway:1360`: 데이터 생성, 송신 큐, `timeToFullBlock:1837`의 부하 할당.
- `Satellite.receiveBlock:911`: 전파 대기 후 다음 경로 선택. `sendBlock:1055`: 링크별 전송.
- `Earth.updateSatelliteProcessesRL:2798`, `moveConstellation:3355`: 이동에 따라 연결과 이벤트를 갱신.
- `DDQNAgent:3948`: 상태/행동, 모델 생성/복원, 추론과 학습. `ExperienceReplay:4375`는 bounded deque.
- `getDeepStateDiff:5649`: 기본 상대 위치 관측 구성. 상태 28개 기본 설정과 행동 4개를 입력/출력 점검에 사용하되 옵션 변경 때 다시 확인한다.
- `getQueueReward:5909`, `getDistanceRewardV4:5988`: 지연과 거리 진전에 대한 보상.
- `plotSaveAllLatencies:6425`: CSV와 시각화. `to_csv`가 ms 변환보다 먼저다.

## 원리 실습

`reward_lab.py`는 신뢰된 현재 소스에서 **산술 return만 허용하는 검사 후** `getQueueReward`만 실행한다. 전체 스크립트 import나 모델 로드는 하지 않는다. 함수 하나의 단위 계약 테스트이며 학습 알고리즘 전체 테스트가 아니다.

큐 보상은 `w1 * (1 - 10**queueTime)`이다. `queueTime`이 초이므로 9 ms는 `0.009`를 입력한다. 지연이 길수록 음의 크기가 커진다. 단순히 ‘지연 최소화’라고 부르기보다 비선형 보상 스케일과 도착 보상의 상대 크기를 살핀다.

기본 거리 보상 V4는 `w2 * (목적지 거리 감소량 - 이동거리/w4) / biggestDist`다. `biggestDist`는 그래프 생성 때 갱신되는 정규화 기준이므로 초기값 -1만 보고 물리적 의미를 부여하면 안 된다. 단위·부호·도착 시 보상·재방문 패널티를 함께 분석한다.

DDQN의 교육용 target은 `r + gamma*(1-done)*Q_target(s', argmax_a Q_online(s',a))`다. 실습은 두 망의 최고 행동을 일부러 다르게 만들어 구별한다. 실제 `train`의 loss target 구성·terminal masking·업데이트 빈도와 추가 비교해야 한다. toy 식의 통과가 실제 TensorFlow 학습 구현의 정확성을 보증하지 않는다.

### 현재 구현과 표준식의 구체적 차이

기준 revision의 `train:4332`를 대조하면 다음이 확인된다.

| 항목 | 현재 코드 | 해석 |
| --- | --- | --- |
| 다음 행동 선택 | `np.max(self.qTarget(nextStates), axis=1)` (`ddqn=True`) | online argmax와 target 평가를 분리한 표준 DDQN이 아님 |
| 종료 처리 | `Dones`를 읽지만 `expectedRewards`에 사용하지 않음 | 도착 전이에도 bootstrap 항이 남을 수 있음 |
| 학습 target | `acts * expectedRewards[:, None]` 전체 벡터를 MSE로 학습 | 선택하지 않은 행동의 target도 0으로 설정됨 |
| 실제 loss | `createModel`은 MSE와 기본 Adam으로 compile | 생성자에 선언된 Huber 객체와 동일하지 않음 |

예를 들어 reward=1, gamma=0.9, online=[1,5], target=[100,2]라면 표준 DDQN toy target은 2.8, 현재 코드의 max-target 식은 91이다. 종료 전이의 표준 target은 1이다. 이 계산은 관찰한 식의 차이를 설명하는 것이며 전체 학습 결과나 버그 수정의 효과를 측정한 것은 아니다. 논문식 재현을 원하면 수정 전후를 별도 revision과 회귀 테스트로 관리해야 한다.

[가이드로 돌아가기](README.md)
