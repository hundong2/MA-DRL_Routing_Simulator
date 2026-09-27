import tempfile
import unittest
from pathlib import Path
from analyze_latency import summarize
from preflight import inspect
from reward_lab import load_queue_reward, ddqn_target


class ExamplesTest(unittest.TestCase):
    def test_config(self):
        result = inspect()
        self.assertGreater(result['location_count'], 1)
        self.assertEqual(result['first_csv_row']['Constellation'], 'Kepler')
        self.assertEqual(result['top_level_literals_only']['GTs'], [2])

    def test_source_queue_reward(self):
        reward = load_queue_reward()
        self.assertEqual(reward(0, 20), 0)
        self.assertAlmostEqual(reward(0.009, 20), 20 * (1 - 10 ** 0.009))
        self.assertLess(reward(0.020, 20), reward(0.009, 20))
        with self.assertRaises(ValueError):
            reward(-1, 20)

    def test_ddqn(self):
        self.assertAlmostEqual(ddqn_target(1, 0.9, [1, 5], [100, 2]), 2.8)
        self.assertEqual(ddqn_target(1, 0.9, [1, 5], [100, 2], True), 1)
        with self.assertRaises(ValueError):
            ddqn_target(1, 0.9, [1], [2, 3])

    def test_latency_fixture(self):
        result = summarize()
        self.assertEqual(result['mean_ms'], 25)
        self.assertEqual(result['p95_nearest_rank_ms'], 40)
        self.assertIsNone(result['delivery_ratio'])

    def test_bad_data(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'bad.csv'
            for content in ('Latency\n', 'Other\n2\n', 'Latency\nnan\n', 'Latency\n-1\n'):
                path.write_text(content, encoding='utf-8')
                with self.assertRaises(ValueError):
                    summarize(path)


if __name__ == '__main__':
    unittest.main()
