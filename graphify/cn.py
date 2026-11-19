"""Graphify CN additions: Chinese entry point and an offline graph digest."""
from __future__ import annotations

import argparse
from collections import Counter
import html
import json
from pathlib import Path
import sys


def _cell(value: object) -> str:
    return html.escape(str(value)).replace('|', '&#124;').replace('\r', ' ').replace('\n', ' ')


def digest(data: object, top: int = 10) -> str:
    """Summarize a Graphify node-link export without a model or graph mutation."""
    if not isinstance(data, dict):
        raise ValueError('图谱根节点必须是 JSON 对象')
    nodes = data.get('nodes')
    links = data.get('links', data.get('edges'))
    if not isinstance(nodes, list) or not isinstance(links, list):
        raise ValueError('图谱必须包含 nodes 和 links（或 edges）数组')
    if top < 1:
        raise ValueError('top 必须大于 0')
    ids: dict[object, dict] = {}
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get('id'), (str, int)):
            raise ValueError('每个节点必须具有字符串或整数 id')
        if node['id'] in ids:
            raise ValueError('图谱存在重复节点 id')
        ids[node['id']] = node
    degree: Counter = Counter()
    evidence: Counter = Counter()
    dangling = 0
    for link in links:
        if not isinstance(link, dict):
            raise ValueError('每条关系必须是 JSON 对象')
        source, target = link.get('source'), link.get('target')
        if not isinstance(source, (str, int)) or not isinstance(target, (str, int)):
            raise ValueError('关系 source/target 必须是节点 id')
        if source not in ids or target not in ids:
            dangling += 1
        if source in ids:
            degree[source] += 1
        if target in ids:
            degree[target] += 1
        tag = str(link.get('confidence', '')).upper()
        evidence[tag if tag in {'EXTRACTED', 'INFERRED', 'AMBIGUOUS'} else 'UNKNOWN'] += 1
    isolated = sum(degree[node_id] == 0 for node_id in ids)
    sourced = sum(bool(n.get('source_location') or n.get('source_file')) for n in nodes)
    lines = [
        '# 图谱速览', '',
        f'- 节点：{len(nodes)}', f'- 关系：{len(links)}',
        f'- 孤立节点：{isolated}', f'- 带来源字段的节点：{sourced}',
        f'- 端点缺失的关系：{dangling}', '',
        '## 关系证据', '',
        '| 标记 | 数量 | 含义 |', '|---|---:|---|',
    ]
    for tag, meaning in [
        ('EXTRACTED', '原图谱标记为直接提取'),
        ('INFERRED', '原图谱标记为推断'),
        ('AMBIGUOUS', '原图谱标记为含糊'),
        ('UNKNOWN', '未标记或未知标记'),
    ]:
        lines.append(f'| {tag} | {evidence[tag]} | {meaning} |')
    lines += ['', '## 连接较多的节点', '',
              '| 节点 | 关系端点数 | 来源 |', '|---|---:|---|']
    ordered = sorted(ids, key=lambda key: (-degree[key], str(key)))[:top]
    for node_id in ordered:
        node = ids[node_id]
        label = node.get('label') or node.get('name') or node_id
        location = node.get('source_location') or node.get('source_file') or '未标注'
        lines.append(f'| {_cell(label)} | {degree[node_id]} | {_cell(location)} |')
    lines += ['', '统计来自当前 JSON 快照；证据标记沿用图谱，不代表重新核实。',
              '连接数按关系端点累计，自环计两次、平行关系分别计数；连接多不等于业务重要。',
              '来源字段存在不等于原文件仍有效。此摘要不调用模型，也不验证图谱是否最新。', '']
    return '\n'.join(lines)


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    args = sys.argv[1:]
    if not args or args[0] in {'-h', '--help'}:
        print('Graphify CN — 代码与文档知识图谱\n\n'
              '  graphify-cn digest [graph.json] [--top 10] [--output 摘要.md]\n'
              '  graphify-cn <上游命令及参数>\n\n'
              'digest 只读本地图谱并输出中文统计，不调用模型。\n'
              '其他命令直接使用现有 Graphify 引擎；完整帮助：graphify --help。')
        return
    if args[0] != 'digest':
        from graphify.__main__ import main as upstream_main
        upstream_main()
        return
    parser = argparse.ArgumentParser(prog='graphify-cn digest', description='只读图谱的中文统计摘要')
    parser.add_argument('graph', nargs='?', default='graphify-out/graph.json')
    parser.add_argument('--top', type=int, default=10, help='最多列出的节点数')
    parser.add_argument('--output', type=Path, help='写入新的 UTF-8 Markdown 文件（不覆盖已有文件）')
    opts = parser.parse_args(args[1:])
    try:
        data = json.loads(Path(opts.graph).read_text(encoding='utf-8-sig'))
        report = digest(data, opts.top)
        if opts.output:
            with opts.output.open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(report)
            print(f'已写入：{opts.output.resolve()}')
        else:
            print(report, end='')
    except (OSError, ValueError) as exc:
        parser.exit(2, f'无法生成摘要：{exc}\n')


if __name__ == '__main__':
    main()
