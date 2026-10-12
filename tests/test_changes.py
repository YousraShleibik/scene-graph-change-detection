from copy import deepcopy
import importlib.util
from pathlib import Path
import tempfile
import unittest

from change_detection import detect_changes, main


class ChangeTests(unittest.TestCase):
    def test_simultaneous_additions_and_deletions_survive(self):
        old = {'nodes': [{'id': 1}, {'id': 2}], 'edges': [{'source': 1, 'target': 2}]}
        new = {'nodes': [{'id': 2}, {'id': 3}], 'edges': [{'source': 2, 'target': 3}]}
        snapshot = deepcopy((old, new))
        report = detect_changes(old, new)
        self.assertEqual([n['id'] for n in report['added_nodes']], [3])
        self.assertEqual([n['id'] for n in report['deleted_nodes']], [1])
        self.assertEqual(len(report['nodes']), 2)
        self.assertEqual(len(report['edges']), 2)
        self.assertEqual((old, new), snapshot)

    def test_attribute_change_is_modification(self):
        old = {'nodes': [{'id': 1, 'attributes': {'position': [0, 0, 0]}}]}
        new = {'nodes': [{'id': 1, 'attributes': {'position': [1, 0, 0]}}]}
        report = detect_changes(old, new)
        self.assertFalse(report['added_nodes'])
        self.assertFalse(report['deleted_nodes'])
        self.assertEqual(report['modified_nodes'][0]['before'], old['nodes'][0])
        self.assertEqual(report['nodes'][0]['attributes']['color'], [0, 255, 0])

    def test_color_only_and_list_order_do_not_create_changes(self):
        old = {'nodes': [{'id': 1, 'color': 'red'}, {'id': 2, 'attributes': {'color': 'red'}}]}
        new = {'nodes': [{'id': 2, 'attributes': {'color': 'green'}}, {'id': 1, 'color': 'blue'}]}
        self.assertFalse(detect_changes(old, new)['nodes'])

    def test_edge_weight_and_parallel_edge_keys(self):
        old = {'nodes': [], 'edges': [{'source': 1, 'target': 2, 'key': 0, 'weight': 1}]}
        new = {'nodes': [], 'edges': [{'source': 1, 'target': 2, 'key': 0, 'weight': 2},
                                    {'source': 1, 'target': 2, 'key': 1}]}
        report = detect_changes(old, new)
        self.assertEqual(len(report['modified_edges']), 1)
        self.assertEqual(len(report['added_edges']), 1)

    def test_validation_and_empty_graphs(self):
        for graph in [{'nodes': [{'id': 1}, {'id': 1}]}, {'nodes': [{}]}, [], {'nodes': 'bad'}]:
            with self.assertRaises(ValueError):
                detect_changes(graph, {'nodes': []})
        self.assertFalse(detect_changes({'nodes': []}, {'nodes': []})['nodes'])

    def test_report_is_deterministic(self):
        old, new = {'nodes': [{'id': 3}, {'id': 'a'}]}, {'nodes': [{'id': 'b'}, {'id': 4}]}
        self.assertEqual(detect_changes(old, new), detect_changes(old, new))
        self.assertEqual([n['id'] for n in detect_changes(old, new)['added_nodes']], ['b', 4])

    def test_default_cli_and_input_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'changes.json'
            report = main(['--output', str(output)])
            self.assertTrue(output.is_file())
            self.assertIn('added_nodes', report)
            from change_detection import ROOT
            with self.assertRaises(SystemExit):
                main(['--output', str(ROOT / 'dsg_backend_run1.json')])

    def test_legacy_imports_do_not_write_files(self):
        from unittest.mock import patch
        root = Path(__file__).resolve().parents[1]
        for path in root.glob('*.py'):
            if path.name == 'change_detection.py':
                continue
            spec = importlib.util.spec_from_file_location('legacy_demo', path)
            module = importlib.util.module_from_spec(spec)
            with patch('builtins.open', side_effect=AssertionError('Unexpected file access on import')):
                spec.loader.exec_module(module)


if __name__ == '__main__':
    unittest.main()
