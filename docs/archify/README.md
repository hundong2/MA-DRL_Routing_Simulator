# 실제 코드 아키텍처

작성·검증일: 2026-09-27

[대화형 architecture HTML](architecture.html) · [원본 JSON](architecture.json) · [학습 가이드](../../guide/README.md) · [캡처 모음](architecture.visual-check.html)

## 분석 범위

저장소: [hundong2/MA-DRL_Routing_Simulator](https://github.com/hundong2/MA-DRL_Routing_Simulator)

코드 기준 revision: `29b9325e3938d620ccd017dc1b475ce704fc6dd9` (문서 추가 이전). `SimulationRL.py`의 기본 online Deep Q-Learning 실행 경로를 7개 구성요소로 압축했다. 모든 파일·옵션을 그린 전체 call graph는 아니다. `Simulation.py` 기준 경로 구현, FL/CKA 실험, 모든 plotting 보조함수는 제외했다.

Archify 2.17의 architecture/showcase를 사용했다. 한국어 설명은 유지하되 `meta.locale`을 생략했으므로 **고정 Viewer UI와 HTML lang은 영어 fallback**이다. Backend 표시는 프로세스 내부 로직 분류이고 실제 웹 백엔드를 의미하지 않는다. External 표시는 로컬 입출력 파일이며 외부 서버가 아니다.

## 코드 근거와 실행 흐름

| 구성 | 실제 근거 | 역할 |
| --- | --- | --- |
| 실험 입력 | `inputRL.csv:1`, `SimulationRL.py:86,242` | CSV·전역값·지도 위치 |
| 실행 제어 | `SimulationRL.py:6594,6798` | main, CSV 로드, SimPy 환경, 실행 및 집계 |
| 환경 초기화 | `SimulationRL.py:4426,5128` | Earth/지상국/위성/그래프와 링크 이벤트 생성 |
| 패킷 이벤트 | `SimulationRL.py:911,1055,1360` | 송수신·전파·FIFO 대기와 다음 hop 요청 |
| 이동과 재연결 | `SimulationRL.py:2082,3355,2798` | Earth가 이동 process를 예약하고 토폴로지 갱신 |
| 다음 hop 학습 | `SimulationRL.py:4144,4332,4375` | 행동 선택·학습·경험 저장 |
| 측정 결과 | `SimulationRL.py:6677,6435,6055` | 실행 종료 후 통계·CSV·그림·모델 저장 |

`RunSimulation`은 `initialize`를 호출하고 `env.run`으로 예약된 사건을 진행시킨다. `initialize`는 `Earth`를 만들고 `createGraph`를 호출하며 `env.process(sat.sendBlock(...))`를 등록한다. 지상국 생성 이벤트와 위성 receive 이벤트가 링크별 패킷 흐름을 만든다. receive는 조건에 따라 로컬/전역 `DDQNA.makeDeepAction`을 호출한다. 온라인 분기에서는 이전 위성 agent의 replay buffer를 갱신한다. 반환·피드백 간선은 도식에서 생략했으며 패킷 흐름이 실제로 일방향 DAG라는 뜻은 아니다.

현재 `train`의 target 식은 표준 DDQN과 차이가 있다. [정확한 대조](../../guide/02_core_concepts.md#현재-구현과-표준식의-구체적-차이)를 참고한다. 다이어그램은 구현 위치·호출 관계이지 알고리즘 정확성 인증이 아니다.

## 신뢰 경계와 제한

단일 Python 프로세스와 로컬 파일 I/O를 확인했다. 확인되지 않은 RPC, 서버 인증, 클라우드 배포, 위성별 독립 프로세스 경계는 그리지 않았다. `keras.models.load_model`이 모델 입력을 읽고 결과 저장 함수가 로컬 경로에 쓴다. 객체 NPY/pickle과 모델은 출처 검토가 필요하다. 전체 TensorFlow 설치·학습·궤도/통신 모델 검증은 이번 작업 범위 밖이다.

## 검증 receipt

```text
diagram_type: architecture
output: D:/workspace/laboratory/MA-DRL_Routing_Simulator/docs/archify/architecture.html
specification_sha256: ad0ff07183d9bdd86d38f9ba9a087e02bead9ece4eb91ac4577d6ec4306aee6a
artifact_sha256: 6be572ea702257fd1ecf0a67589735b2ffd0982622571c3863ae52661cd014f0
validation: 9/9 showcase, 0 errors, 0 warnings
browser_evidence: passed
visual_review: passed
correction_rounds: 1
```

명세 5,291 bytes, HTML 710,991 bytes. `deliver` exit 0, 코드 source reference 18개 검증. 초기 자동 배치 label 충돌 3개는 진단이 제안한 좌표를 한 번에 하나씩 적용해 제거했다. 이후 화면 검토에서 큰 화면 하단 여백을 줄이도록 수직 간격을 한 차례 수정하고 validate/deliver/visual-check를 다시 수행했다.

- 자동 증거: [architecture.visual-check.json](architecture.visual-check.json), 현재 HTML SHA와 일치. 1440×900, 1600×1000, 1920×1080, 2048×1320에서 가로·세로 overflow 없음.
- 별도 지각 검토: 최종 1440×900 및 2048×1320의 light/dark PNG 네 장을 이미지 도구로 확인. 노드·카드 잘림, 관계선 교차, 라벨 충돌 없음. 큰 화면에서도 카드까지 균형 있게 표시됨.
- 자동 receipt의 `visualReview: pending`은 그대로 유지한다. 자동 검사가 사람/이미지 검토를 대신하지 않으므로 이 문서에 별도 기록했다.
- 검색·focus·내보내기 기능의 수동 상호작용 검증은 수행하지 않았다. static screenshot 검토를 기능 전체 시험으로 확대 해석하지 않는다.
