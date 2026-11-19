"""Tests for the CN additions; no model, network or database needed."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from graphify.cn import digest, main


class DigestTests(unittest.TestCase):
    def test_counts_evidence_orphans_parallel_and_unsafe_labels(self):
        data = {'nodes': [{'id': 'a', 'label': '<入口>|中文\n节点', 'source_file': 'src/a.py'},
                          {'id': 'b'}, {'id': 'alone'}], 'links': [
            {'source': 'a', 'target': 'b', 'confidence': 'EXTRACTED'},
            {'source': 'a', 'target': 'b', 'confidence': 'INFERRED'},
            {'source': 'a', 'target': 'missing'},
            {'source': 'a', 'target': 'a', 'confidence': 'AMBIGUOUS'}]}
        result = digest(data)
        for value in ['节点：3', '关系：4', '孤立节点：1', '端点缺失的关系：1',
                      '| UNKNOWN | 1 |', '| INFERRED | 1 |', '&lt;入口&gt;&#124;中文 节点 | 5 |']:
            self.assertIn(value, result)

    def test_edges_compatibility_and_empty_graph(self):
        self.assertIn('关系：0', digest({'nodes': [], 'edges': []}))

    def test_invalid_graphs_fail_instead_of_fabricating_zero(self):
        for data in [[], {}, {'nodes': [], 'links': None},
                     {'nodes': [{'id': []}], 'links': []},
                     {'nodes': [{'id': 1}, {'id': 1}], 'links': []},
                     {'nodes': [], 'links': [{'source': [], 'target': 'b'}]}]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                digest(data)
        with self.assertRaises(ValueError):
            digest({'nodes': [], 'links': []}, 0)

    def test_utf8_file_output_does_not_overwrite_existing(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)/'图谱.json'
            target = Path(folder)/'摘要.md'
            source.write_text(json.dumps({'nodes': [], 'links': []}), encoding='utf-8-sig')
            args = ['graphify-cn', 'digest', str(source), '--output', str(target)]
            with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
                main()
            self.assertIn('图谱速览', target.read_text(encoding='utf-8'))
            before = target.read_bytes()
            with patch.object(sys, 'argv', args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                main()
            self.assertEqual(raised.exception.code, 2)
            self.assertEqual(target.read_bytes(), before)

    def test_other_commands_preserve_arguments(self):
        args = ['graphify-cn', 'query', '订单和支付的关系', '--budget', '1500']
        calls = []
        stub = types.ModuleType('graphify.__main__')
        stub.main = lambda: calls.append(list(sys.argv))
        with patch.dict(sys.modules, {'graphify.__main__': stub}), patch.object(sys, 'argv', args):
            main()
        self.assertEqual(calls, [args])


if __name__ == '__main__':
    unittest.main()
