#!/usr/bin/env python3
#
# Copyright (c) 2025 ParallelIQ LLC.
#
# This file is licensed under the Business Source License 1.1 (BSL 1.1).
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/paralleliq/modelspec/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from rich.console import Console
from rich.table import Table

console = Console()


def load_yaml_or_json(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def load_schema(schema_path: Path) -> Dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def format_path(err: ValidationError) -> str:
    if not err.absolute_path:
        return "$"
    parts = []
    for p in err.absolute_path:
        if isinstance(p, int):
            parts.append(f"[{p}]")
        else:
            parts.append(f".{p}")
    return "$" + "".join(parts)


@dataclass
class Issue:
    file: str
    path: str
    message: str


def schema_validate(doc: Any, schema: Dict[str, Any], file: str) -> List[Issue]:
    v = Draft202012Validator(schema)
    issues: List[Issue] = []
    for err in sorted(v.iter_errors(doc), key=lambda e: list(e.absolute_path)):
        issues.append(Issue(file=file, path=format_path(err), message=err.message))
    return issues


# MVP semantic checks: keep minimal; easy to expand later.
def semantic_checks(doc: Dict[str, Any], file: str) -> List[Issue]:
    issues: List[Issue] = []
    spec = (doc or {}).get("spec", {})
    identity = spec.get("identity", {})
    runtime = spec.get("runtime", {})

    model = identity.get("model", {}) if isinstance(identity, dict) else {}
    framework = model.get("framework")

    # Example semantic check: if framework is vllm, require runtime.batch.maxSequenceLengthTokens
    if framework == "vllm":
        batch = runtime.get("batch", {}) if isinstance(runtime, dict) else {}
        if "maxSequenceLengthTokens" not in batch:
            issues.append(Issue(
                file=file,
                path="$.spec.runtime.batch.maxSequenceLengthTokens",
                message="Required for framework=vllm (semantic check)."
            ))

    return issues


def print_issues(issues: List[Issue]) -> None:
    table = Table(title="ModelSpec Validation Errors", show_lines=True)
    table.add_column("File", style="bold")
    table.add_column("Path", style="cyan")
    table.add_column("Message", style="red")

    for it in issues:
        table.add_row(it.file, it.path, it.message)

    console.print(table)


def main() -> int:
    p = argparse.ArgumentParser(description="Validate ModelSpec files against JSON Schema.")
    p.add_argument("--schema", required=True, help="Path to schema JSON file (e.g. schema/schema.json)")
    p.add_argument("paths", nargs="+", help="One or more YAML/JSON files or directories")
    p.add_argument("--no-semantic", action="store_true", help="Disable semantic checks")
    args = p.parse_args()

    schema_path = Path(args.schema).resolve()
    schema = load_schema(schema_path)

    # Collect files to validate
    files: List[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_dir():
            for ext in ("*.yaml", "*.yml", "*.json"):
                files.extend(path.rglob(ext))
        else:
            files.append(path)

    # Validate
    all_issues: List[Issue] = []
    for f in files:
        try:
            doc = load_yaml_or_json(f)
        except Exception as e:
            all_issues.append(Issue(file=str(f), path="$", message=f"Parse error: {e}"))
            continue

        all_issues.extend(schema_validate(doc, schema, str(f)))

        if not args.no_semantic and isinstance(doc, dict):
            all_issues.extend(semantic_checks(doc, str(f)))

    if all_issues:
        print_issues(all_issues)
        return 1

    console.print("[green]✅ All ModelSpec files validated successfully.[/green]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
