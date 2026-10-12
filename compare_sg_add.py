"""Legacy additions-only comparison; modified IDs are reported by the full CLI."""
from change_detection import detect_changes as _detect_changes
from change_detection import main as _main, read_json, save_json, _highlight


def detect_changes(graph1, graph2):
    report = _detect_changes(graph1, graph2)
    return {kind: [_highlight(node, [128, 128, 128])
                   for node in report[f'added_{kind}']]
            for kind in ('nodes', 'edges')}


if __name__ == '__main__':
    _main(additions_only=True)
