"""원본 큐 보상 산술 계약과 독립 DDQN target 교육 예제."""
import ast
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_queue_reward():
    tree = ast.parse((ROOT / 'SimulationRL.py').read_text(encoding='utf-8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'getQueueReward')
    # docstring을 제외한 단일 return, 인자·숫자·산술 외에는 거부한다.
    body = function.body[1:] if isinstance(function.body[0], ast.Expr) else function.body
    if len(body) != 1 or not isinstance(body[0], ast.Return):
        raise ValueError('검토가 필요한 보상 함수 변경')
    expression = body[0].value
    permitted = (ast.BinOp, ast.Name, ast.Load, ast.Constant,
                 ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.UnaryOp, ast.USub)
    for node in ast.walk(expression):
        if not isinstance(node, permitted):
            raise ValueError('산술 외 표현식은 실행하지 않음')
        if isinstance(node, ast.Name) and node.id not in {'queueTime', 'w1'}:
            raise ValueError('외부 이름 사용 금지')
        if isinstance(node, ast.Constant) and type(node.value) not in (int, float):
            raise ValueError('숫자 외 상수 금지')
    code = compile(ast.Expression(expression), '<reviewed-queue-arithmetic>', 'eval')

    def reward(seconds, weight):
        if not (math.isfinite(seconds) and 0 <= seconds <= 1):
            raise ValueError('교육용 입력 범위는 0~1초')
        return eval(code, {'__builtins__': {}}, {'queueTime': seconds, 'w1': weight})

    return reward


def ddqn_target(reward, gamma, online, target, done=False):
    """원본 train 실행이 아닌 교과서 target의 독립 toy 구현."""
    if not online or len(online) != len(target) or not 0 <= gamma <= 1:
        raise ValueError('행동 차원 또는 할인율 오류')
    action = max(range(len(online)), key=online.__getitem__)
    return reward if done else reward + gamma * target[action]


def demo():
    queue_reward = load_queue_reward()
    print('queueTime=0.009 s, w1=20:', queue_reward(0.009, 20))
    # online은 행동 1을 선택, target 자체의 최대값 100은 행동 0에 있다.
    print('toy DDQN target:', ddqn_target(1, 0.9, [1, 5], [100, 2]))


if __name__ == '__main__':
    demo()
