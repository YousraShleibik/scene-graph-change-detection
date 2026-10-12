# Scene Graph Change Detection

Compare two JSON scene graphs to identify added, deleted, and modified nodes
and edges. This project includes recorded dynamic scene graphs and scripts for
highlighting changes in object position, labels, and bounding boxes.

## Run

Python 3.10 or newer; the comparison tools use only the standard library.

```sh
python change_detection.py dsg_backend_run1.json dsg_backend_run2.json --output changes.json
python comapre_sg_add_delete.py --output changes.json
python compare_sg_add.py --output additions.json
```

The two graph paths are optional and default to the included backend run files,
resolved relative to the script. Explicit paths and output paths are relative
to your working directory. Output cannot overwrite either input graph.

## Report format

- `added_nodes`, `deleted_nodes`, `added_edges`, `deleted_edges`: original records.
- `modified_nodes`, `modified_edges`: records with `before` and `after` values.
- `nodes`, `edges`: combined highlighted changes for legacy consumers; additions
  are gray, deletions yellow, modifications green. When a record has an
  `attributes` object, the highlight color is stored there.

Nodes are matched by top-level `id`; edges by ordered `source`, `target`, and
optional `key` (or `id`). Changes to a matched record are modifications rather
than false additions/deletions. Color-only changes are ignored. Comparisons of
other attributes are exact, including positions and bounding boxes. Missing
edges default to an empty list. Duplicate identities are rejected instead of
silently discarding records. Undirected edge endpoints must be consistently
ordered in both files; parallel edges need unique keys or IDs.

`compare_sg_add.py` reports strictly new identities; use the full comparison
for attribute changes. Its legacy importable helpers remain available.

The `filter_*`, `filtred_*`, `bb_filtred_add.py`, and `test_added_nodes*.py`
files are historical filtering demos, with their original comparison criteria
and default paths. Run those from the repository directory. They now avoid
writing files during import. Use `change_detection.py` for a complete report.
Some historical output JSON/text files predate these fixes; generate a fresh
report instead of assuming they reflect the current implementation.

## Tests

```sh
python -m unittest discover -s tests -v
```
