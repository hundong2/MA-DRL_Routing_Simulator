"""수신 CSV Latency(초)를 분석한다. 전달률을 추정하지 않는다."""
import csv
import json
import math
import statistics
import sys
from pathlib import Path

FIXTURE = Path(__file__).with_name('latency_fixture.csv')


def summarize(path=FIXTURE):
    values = []
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if 'Latency' not in (reader.fieldnames or []):
            raise ValueError('필수 열 Latency(초)가 없음')
        for row in reader:
            value = float(row['Latency'])
            if not math.isfinite(value) or value < 0:
                raise ValueError('Latency는 유한한 비음수 초여야 함')
            values.append(value * 1000)
    if not values:
        raise ValueError('수신 샘플 없음')
    values.sort()
    return {'received_samples': len(values), 'mean_ms': statistics.mean(values),
            'median_ms': statistics.median(values),
            'p95_nearest_rank_ms': values[math.ceil(len(values) * 0.95) - 1],
            'delivery_ratio': None,
            'scope': '수신 완료 샘플만 분석; 생성 수와 종료 시 잔류 수는 별도 필요'}


if __name__ == '__main__':
    print(json.dumps(summarize(sys.argv[1] if len(sys.argv) > 1 else FIXTURE),
                     ensure_ascii=False, indent=2))
