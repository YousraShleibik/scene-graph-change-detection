# Scene Graph Change Detection

A Python tool for detecting added, deleted, and modified nodes and edges between
two scene graphs. It uses stable IDs to distinguish newly observed objects from
attribute changes, and exports deterministic JSON reports with before/after
records and display colors.

## Quick start

Python 3.10 or newer. No third-party dependencies are required.

```sh
python3 change_detection.py --output changes.json
```

The included small example reports a removed chair, a moved table, an added lamp,
and changed edges. To compare the recorded scene graphs:

```sh
python3 change_detection.py dsg_backend_run1.json dsg_backend_run2.json --output changes.json
```

## Files

| Path | Purpose |
| --- | --- |
| `change_detection.py` | Comparison functions and command-line interface |
| `examples/before.json`, `examples/after.json` | Small runnable examples |
| `tests/test_changes.py` | Regression tests |
| `dsg_backend_run*.json` | Recorded backend input scene graphs |
| `dsg_frontend_run*.json` | Recorded frontend input scene graphs |
| `dsg_obj_backend_run*.json` | Recorded object-layer input scene graphs |
| `LICENSE` | Original project license |

Generated reports and node-list exports are excluded from version control.
Historical outputs and duplicate experimental scripts were removed. The six
recorded input graphs are preserved. `Old-dsg.json` and `new-dsg.json` were exact
copies of the two frontend input files and were removed as duplicates.

## Report format

- `added_nodes`, `deleted_nodes`, `added_edges`, `deleted_edges`: original records.
- `modified_nodes`, `modified_edges`: records with `before` and `after` values.
- `nodes`, `edges`: combined highlighted changes; additions are gray, deletions
  yellow, modifications green. Highlight colors use `attributes.color` when an
  attributes object exists, otherwise top-level `color`.

Nodes are matched by top-level `id`; edges by ordered `source`, `target`, and
optional `key` (or `id`). Changes to matched records are modifications. Color-only
changes are ignored. Other comparisons are exact, including positions and
bounding boxes. Duplicate identities are rejected. Missing edges default to an
empty list. Undirected endpoints must be ordered consistently; parallel edges
need unique keys or IDs. This tool compares graph records; it does not infer
object correspondence when object IDs change between runs.

Input graphs are not modified. The output path cannot overwrite either input.
Default example paths are resolved relative to the script; explicit paths and
the output path are relative to your working directory.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

## GitHub description

Python scene graph comparison for detecting added, deleted, and modified objects and relationships, with JSON reports and tests.
