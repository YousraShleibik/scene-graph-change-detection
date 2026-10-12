"""Compare scene graphs by stable node and edge identities."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_json(path):
    with open(path, encoding='utf-8') as stream:
        return json.load(stream)


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def _index(items, kind):
    if not isinstance(items, list):
        raise ValueError(f'{kind} must be a list')
    indexed = {}
    for item in items:
        if not isinstance(item, dict):
            raise ValueError(f'Each {kind} record must be an object')
        fields = ('id',) if kind == 'nodes' else ('source', 'target')
        if any(field not in item for field in fields):
            raise ValueError(f'{kind} records require {fields}')
        identity = tuple(item[field] for field in fields)
        if kind == 'edges':
            identity += (item.get('key', item.get('id')),)
        try:
            if identity in indexed:
                raise ValueError(f'Duplicate {kind} identity: {identity}')
            indexed[identity] = item
        except TypeError as error:
            raise ValueError(f'{kind} identities must be scalar values') from error
    return indexed


def _content(item):
    # Highlighting colors are display metadata, not scene changes.
    result = deepcopy(item)
    result.pop('color', None)
    if isinstance(result.get('attributes'), dict):
        result['attributes'].pop('color', None)
    return result


def _highlight(item, color):
    result = deepcopy(item)
    if isinstance(result.get('attributes'), dict):
        result['attributes']['color'] = color
    else:
        result['color'] = color
    return result


def detect_changes(graph1, graph2):
    if not isinstance(graph1, dict) or not isinstance(graph2, dict):
        raise ValueError('Graphs must be JSON objects with a nodes list')
    if 'nodes' not in graph1 or 'nodes' not in graph2:
        raise ValueError('Each graph must contain a nodes list')
    changes = {}
    for kind in ('nodes', 'edges'):
        old = _index(graph1.get(kind, []), kind)
        new = _index(graph2.get(kind, []), kind)
        # Preserve input order so reports are deterministic, including mixed ID types.
        added = [deepcopy(item) for key, item in new.items() if key not in old]
        deleted = [deepcopy(item) for key, item in old.items() if key not in new]
        modified = [{'before': deepcopy(old[key]), 'after': deepcopy(item)}
                    for key, item in new.items()
                    if key in old and _content(old[key]) != _content(item)]
        changes[f'added_{kind}'] = added
        changes[f'deleted_{kind}'] = deleted
        changes[f'modified_{kind}'] = modified
        # Keep legacy nodes/edges fields without overwriting simultaneous changes.
        changes[kind] = ([_highlight(item, [128, 128, 128]) for item in added]
                         + [_highlight(item, [255, 255, 0]) for item in deleted]
                         + [_highlight(item['after'], [0, 255, 0]) for item in modified])
    return changes


def main(argv=None, *, additions_only=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('old', nargs='?', type=Path, default=ROOT / 'dsg_backend_run1.json')
    parser.add_argument('new', nargs='?', type=Path, default=ROOT / 'dsg_backend_run2.json')
    parser.add_argument('--output', type=Path, default=Path('changes.json'))
    args = parser.parse_args(argv)
    if args.output.resolve() in (args.old.resolve(), args.new.resolve()):
        parser.error('output must be different from both input files')
    try:
        report = detect_changes(read_json(args.old), read_json(args.new))
        if additions_only:
            report = {kind: [_highlight(item, [128, 128, 128])
                             for item in report[f'added_{kind}']]
                      for kind in ('nodes', 'edges')}
        save_json(report, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f'error: {error}\n')
    print(f'Saved change report to {args.output}')
    return report


if __name__ == '__main__':
    main()
