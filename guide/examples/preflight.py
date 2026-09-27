"""설정 읽기 전용 점검. 시뮬레이터 import나 모델 역직렬화를 하지 않는다."""
import ast
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def inspect(root=ROOT):
    tree = ast.parse((root / 'SimulationRL.py').read_text(encoding='utf-8'))
    # 조건 분기까지 실행하는 평가기가 아니다. 리터럴 전역만 읽는다.
    literals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                try:
                    literals[target.id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
    with (root / 'inputRL.csv').open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        required = {'Locations', 'Constellation', 'Fraction', 'Test type', 'Test length'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('inputRL.csv 필수 열 누락')
        rows = list(reader)
    if not rows:
        raise ValueError('설정 행 없음')
    first = rows[0]
    if not 0 < float(first['Fraction']) <= 1 or float(first['Test length']) <= 0:
        raise ValueError('부하 비율과 실행 기간 확인 필요')
    selected = {key: literals.get(key) for key in (
        'GTs', 'movementTime', 'onlinePhase', 'Train', 'explore', 'importQVals', 'BLOCK_SIZE')}
    inputs = ['Gateways.csv', 'Population Map/gpw_v4_population_count_rev11_2020_15_min.tif',
              literals['nnpath'], literals['nnpathTarget']]
    return {
        'first_csv_row': first,
        'location_count': len(rows),
        'top_level_literals_only': selected,
        'input_exists': {path: (root / path).is_file() for path in inputs},
        'warning': '조건 분기는 평가하지 않음: onlinePhase 분기가 explore/importQVals를 덮어씀. '
                   '파일 존재는 설치·모델 신뢰성·전체 실행 성공을 보증하지 않음.',
    }


if __name__ == '__main__':
    print(json.dumps(inspect(), ensure_ascii=False, indent=2))
