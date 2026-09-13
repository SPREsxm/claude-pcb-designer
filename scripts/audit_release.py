#!/usr/bin/env python3
"""Audit a PCB fabrication release directory or zip archive.

The audit is intentionally conservative and dependency-free. It catches
missing layers, empty files, common Gerber/Excellon structure problems, and
basic BOM/CPL consistency errors. It cannot prove electrical correctness.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


GERBER_EXTENSIONS = {
    ".gbr": "unknown_gerber",
    ".ger": "unknown_gerber",
    ".art": "unknown_gerber",
    ".gtl": "top_copper",
    ".gbl": "bottom_copper",
    ".g1": "inner_copper_1",
    ".g2": "inner_copper_2",
    ".g3": "inner_copper_3",
    ".g4": "inner_copper_4",
    ".gts": "top_mask",
    ".gbs": "bottom_mask",
    ".gto": "top_silk",
    ".gbo": "bottom_silk",
    ".gko": "outline",
    ".gm1": "outline",
    ".gml": "outline",
    ".gbrjob": "gerber_job",
}
MAX_TEXT_BYTES = 2_000_000
MAX_ARCHIVE_ENTRY_BYTES = 100_000_000


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, str]:
        result = {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
        }
        if self.path:
            result["path"] = self.path
        return result


@dataclass
class ReleaseFile:
    name: str
    size: int
    kind: str
    text: str | None = None


@dataclass
class AuditResult:
    target: str
    files: list[ReleaseFile] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    bom_designators: set[str] = field(default_factory=set)
    cpl_designators: set[str] = field(default_factory=set)

    def add(self, severity: str, code: str, message: str, path: str | None = None) -> None:
        self.issues.append(Issue(severity, code, message, path))

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    def as_dict(self) -> dict[str, object]:
        kinds: dict[str, int] = {}
        for item in self.files:
            kinds[item.kind] = kinds.get(item.kind, 0) + 1
        return {
            "target": self.target,
            "summary": {
                "files": len(self.files),
                "file_kinds": dict(sorted(kinds.items())),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "bom_designators": len(self.bom_designators),
                "cpl_designators": len(self.cpl_designators),
            },
            "files": [
                {"name": item.name, "size": item.size, "kind": item.kind} for item in self.files
            ],
            "issues": [issue.as_dict() for issue in self.issues],
            "bom_only": sorted(self.bom_designators - self.cpl_designators),
            "cpl_only": sorted(self.cpl_designators - self.bom_designators),
        }


def decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def classify(name: str, text: str | None = None) -> str:
    lower = name.lower()
    suffix = Path(lower).suffix
    basename = Path(lower).name
    if suffix in GERBER_EXTENSIONS:
        kind = GERBER_EXTENSIONS[suffix]
        if kind != "unknown_gerber":
            return kind
        top = any(token in basename for token in ("top", "front", "_f_", "f_", "gtl"))
        bottom = any(token in basename for token in ("bottom", "back", "_b_", "b_", "gbl"))
        if "mask" in basename and top:
            return "top_mask"
        if "mask" in basename and bottom:
            return "bottom_mask"
        if ("silk" in basename or "legend" in basename) and top:
            return "top_silk"
        if ("silk" in basename or "legend" in basename) and bottom:
            return "bottom_silk"
        if "paste" in basename and top:
            return "top_paste"
        if "paste" in basename and bottom:
            return "bottom_paste"
        inner = re.search(r"(?:in|inner)[-_]?(\d+)", basename)
        if inner and ("cu" in basename or "copper" in basename):
            return f"inner_copper_{int(inner.group(1))}"
        if any(token in basename for token in ("edge", "outline", "profile", "gko")):
            return "outline"
        if "copper" in basename and top:
            return "top_copper"
        if "copper" in basename and bottom:
            return "bottom_copper"
        if top:
            return "top_copper"
        if bottom:
            return "bottom_copper"
        if "mask" in basename:
            return "unknown_mask"
        if "silk" in basename or "legend" in basename:
            return "unknown_silk"
        return "unknown_gerber"
    if suffix in {".drl", ".drd"}:
        return "drill"
    if suffix == ".txt":
        header = (text or "")[:4096].upper()
        if "M48" in header or "METRIC" in header or "INCH" in header:
            return "drill"
    if suffix == ".csv":
        if any(token in basename for token in ("bom", "bill", "material")):
            return "bom"
        if any(
            token in basename for token in ("cpl", "pos", "pick", "place", "centroid", "placement")
        ):
            return "cpl"
        return "csv"
    if suffix in {".md", ".txt", ".pdf"} and any(
        token in basename for token in ("readme", "fab", "drawing", "stackup", "note")
    ):
        return "documentation"
    if suffix in {".zip", ".7z", ".rar"}:
        return "archive"
    return "other"


def iter_directory(path: Path) -> Iterable[ReleaseFile]:
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        size = file_path.stat().st_size
        text = None
        if file_path.suffix.lower() in {
            ".gbr",
            ".ger",
            ".art",
            ".gtl",
            ".gbl",
            ".g1",
            ".g2",
            ".g3",
            ".g4",
            ".gts",
            ".gbs",
            ".gto",
            ".gbo",
            ".gko",
            ".gm1",
            ".gml",
            ".drl",
            ".drd",
            ".txt",
            ".csv",
        }:
            with file_path.open("rb") as handle:
                text = decode_text(handle.read(MAX_TEXT_BYTES))
        yield ReleaseFile(
            name=str(file_path.relative_to(path)),
            size=size,
            kind=classify(file_path.name, text),
            text=text,
        )


def iter_zip(path: Path) -> Iterable[ReleaseFile]:
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            suffix = Path(info.filename.lower()).suffix
            text = None
            if info.file_size > MAX_ARCHIVE_ENTRY_BYTES:
                text = None
            elif suffix in {
                ".gbr",
                ".ger",
                ".art",
                ".gtl",
                ".gbl",
                ".g1",
                ".g2",
                ".g3",
                ".g4",
                ".gts",
                ".gbs",
                ".gto",
                ".gbo",
                ".gko",
                ".gm1",
                ".gml",
                ".drl",
                ".drd",
                ".txt",
                ".csv",
            }:
                with archive.open(info) as handle:
                    text = decode_text(handle.read(MAX_TEXT_BYTES))
            yield ReleaseFile(
                name=info.filename,
                size=info.file_size,
                kind=classify(info.filename, text),
                text=text,
            )


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def find_column(fieldnames: list[str], aliases: tuple[str, ...]) -> str | None:
    mapping = {normalize_header(name): name for name in fieldnames}
    for alias in aliases:
        key = normalize_header(alias)
        if key in mapping:
            return mapping[key]
    return None


def split_designators(value: str) -> set[str]:
    designators: set[str] = set()
    for part in re.split(r"[,;\s]+", value.strip()):
        if not part:
            continue
        match = re.fullmatch(r"([A-Za-z]+)(\d+)-([A-Za-z]*)(\d+)", part)
        if match:
            prefix_a, start, prefix_b, end = match.groups()
            if prefix_b and prefix_b.upper() != prefix_a.upper():
                designators.add(part.upper())
                continue
            start_num = int(start)
            end_num = int(end)
            if end_num >= start_num and end_num - start_num <= 500:
                designators.update(
                    f"{prefix_a.upper()}{number}" for number in range(start_num, end_num + 1)
                )
                continue
        designators.add(part.upper())
    return designators


def parse_boolish(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y", "fit", "populate", "populated", "assemble"}:
        return True
    if normalized in {"0", "false", "no", "n", "dnp", "do not populate", "unfit", "exclude"}:
        return False
    return None


def is_dnp(value: str) -> bool:
    return parse_boolish(value) is False


def parse_csv_rows(text: str) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        return [], []
    return list(reader.fieldnames), [dict(row) for row in reader]


def audit_bom(result: AuditResult, item: ReleaseFile) -> None:
    if not item.text:
        result.add("error", "bom-empty", "BOM file is empty", item.name)
        return
    fieldnames, rows = parse_csv_rows(item.text)
    if not fieldnames:
        result.add("error", "bom-header", "BOM has no CSV header", item.name)
        return
    designator_col = find_column(
        fieldnames, ("designator", "designators", "refdes", "reference", "refs", "ref")
    )
    quantity_col = find_column(fieldnames, ("quantity", "qty", "count"))
    mpn_col = find_column(
        fieldnames,
        (
            "manufacturer part number",
            "manufacturer_part_number",
            "mpn",
            "manufacturer pn",
            "part number",
            "part_number",
        ),
    )
    supplier_col = find_column(
        fieldnames,
        (
            "supplier part number",
            "supplier_part_number",
            "supplier pn",
            "lcsc",
            "lcsc part",
            "lcsc part number",
            "lcsc_part_number",
        ),
    )
    package_col = find_column(
        fieldnames, ("package", "footprint", "case", "case package", "pattern")
    )
    status_col = find_column(
        fieldnames, ("status", "dnp", "do not populate", "populate", "assembly", "fit")
    )
    if not designator_col:
        result.add("error", "bom-designator-column", "BOM lacks a designator column", item.name)
    if not quantity_col:
        result.add("warning", "bom-quantity-column", "BOM lacks a quantity column", item.name)
    if not mpn_col and not supplier_col:
        result.add(
            "error",
            "bom-part-column",
            "BOM lacks a manufacturer or supplier part-number column",
            item.name,
        )
    if not package_col:
        result.add(
            "warning", "bom-package-column", "BOM lacks a package/footprint column", item.name
        )

    seen_rows: set[str] = set()
    for index, row in enumerate(rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        if not designator_col:
            continue
        raw_designators = (row.get(designator_col) or "").strip()
        designators = split_designators(raw_designators)
        if not designators:
            result.add(
                "error", "bom-missing-designator", f"BOM row {index} has no designator", item.name
            )
            continue
        status_value = (row.get(status_col) or "") if status_col else ""
        if is_dnp(status_value):
            continue
        for designator in designators:
            if designator in seen_rows:
                result.add(
                    "warning",
                    "bom-duplicate-designator",
                    f"BOM designator {designator} appears more than once",
                    item.name,
                )
            seen_rows.add(designator)
            result.bom_designators.add(designator)
        if quantity_col:
            raw_quantity = (row.get(quantity_col) or "").strip()
            if raw_quantity:
                try:
                    quantity = int(float(raw_quantity))
                    if quantity != len(designators):
                        result.add(
                            "warning",
                            "bom-quantity-mismatch",
                            f"BOM row {index} says quantity {quantity}, but lists {len(designators)} designators",
                            item.name,
                        )
                except ValueError:
                    result.add(
                        "warning",
                        "bom-quantity-invalid",
                        f"BOM row {index} has a non-numeric quantity",
                        item.name,
                    )


def audit_cpl(result: AuditResult, item: ReleaseFile) -> None:
    if not item.text:
        result.add("error", "cpl-empty", "CPL file is empty", item.name)
        return
    fieldnames, rows = parse_csv_rows(item.text)
    if not fieldnames:
        result.add("error", "cpl-header", "CPL has no CSV header", item.name)
        return
    designator_col = find_column(
        fieldnames, ("designator", "designators", "refdes", "reference", "refs", "ref")
    )
    x_col = find_column(
        fieldnames, ("mid x", "mid_x", "center x", "center_x", "posx", "x", "ref x")
    )
    y_col = find_column(
        fieldnames, ("mid y", "mid_y", "center y", "center_y", "posy", "y", "ref y")
    )
    layer_col = find_column(fieldnames, ("layer", "side", "tb", "top/bottom"))
    rotation_col = find_column(fieldnames, ("rotation", "rot", "angle", "degrees"))
    for label, column in (
        ("designator", designator_col),
        ("X", x_col),
        ("Y", y_col),
        ("layer", layer_col),
        ("rotation", rotation_col),
    ):
        if not column:
            result.add("error", "cpl-missing-column", f"CPL lacks a {label} column", item.name)
    if not designator_col:
        return

    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        designators = split_designators((row.get(designator_col) or "").strip())
        if not designators:
            result.add(
                "error", "cpl-missing-designator", f"CPL row {index} has no designator", item.name
            )
            continue
        if len(designators) != 1:
            result.add(
                "warning",
                "cpl-multiple-designators",
                f"CPL row {index} contains multiple designators; most assemblers expect one per row",
                item.name,
            )
        for designator in designators:
            if designator in seen:
                result.add(
                    "warning",
                    "cpl-duplicate-designator",
                    f"CPL designator {designator} appears more than once",
                    item.name,
                )
            seen.add(designator)
            result.cpl_designators.add(designator)


def audit_gerber(result: AuditResult, item: ReleaseFile) -> None:
    if item.size <= 0 or not item.text:
        result.add("error", "gerber-empty", "Gerber file is empty", item.name)
        return
    upper = item.text.upper()
    if "%FS" not in upper:
        result.add("warning", "gerber-format", "Gerber lacks a %FS format statement", item.name)
    if "M02" not in upper:
        result.add("warning", "gerber-termination", "Gerber lacks an M02 termination", item.name)
    if item.kind in {
        "top_copper",
        "bottom_copper",
        "inner_copper_1",
        "inner_copper_2",
        "inner_copper_3",
        "inner_copper_4",
    }:
        if "%ADD" not in upper and "D10" not in upper:
            result.add(
                "warning",
                "gerber-apertures",
                "Copper Gerber has no obvious aperture definitions",
                item.name,
            )


def audit_drill(result: AuditResult, item: ReleaseFile) -> None:
    if item.size <= 0 or not item.text:
        result.add("error", "drill-empty", "Drill file is empty", item.name)
        return
    upper = item.text.upper()
    if "M48" not in upper:
        result.add("warning", "drill-header", "Drill file lacks an M48 header", item.name)
    if "METRIC" not in upper and "INCH" not in upper:
        result.add(
            "warning", "drill-units", "Drill file does not declare METRIC or INCH", item.name
        )


def run_audit(target: Path, pcb_only: bool = False, layers: int = 2) -> AuditResult:
    result = AuditResult(target=str(target))
    if not target.exists():
        result.add("error", "target-missing", f"Release target does not exist: {target}")
        return result
    try:
        if target.is_dir():
            files = list(iter_directory(target))
        elif target.suffix.lower() == ".zip":
            files = list(iter_zip(target))
        else:
            result.add("error", "target-type", "Target must be a directory or .zip archive")
            return result
    except (OSError, zipfile.BadZipFile) as exc:
        result.add("error", "target-read", f"Could not read release target: {exc}")
        return result

    result.files = files
    if not files:
        result.add("error", "release-empty", "Release package contains no files")
        return result

    kinds: dict[str, list[ReleaseFile]] = {}
    for item in files:
        kinds.setdefault(item.kind, []).append(item)
        if item.size <= 0:
            result.add("error", "file-empty", "File is empty", item.name)
        elif item.size > MAX_ARCHIVE_ENTRY_BYTES:
            result.add(
                "error",
                "file-too-large",
                f"File exceeds the audit size limit of {MAX_ARCHIVE_ENTRY_BYTES} bytes",
                item.name,
            )
        if item.kind in {
            "top_copper",
            "bottom_copper",
            "inner_copper_1",
            "inner_copper_2",
            "inner_copper_3",
            "inner_copper_4",
        }:
            audit_gerber(result, item)
        elif item.kind == "drill":
            audit_drill(result, item)

    required_kinds = ["top_copper", "bottom_copper", "top_mask", "bottom_mask", "outline", "drill"]
    for kind in required_kinds:
        if kind not in kinds:
            result.add("error", f"missing-{kind}", f"Missing required release group: {kind}")

    expected_inner = max(0, layers - 2)
    found_inner = sum(
        len(kinds.get(f"inner_copper_{index}", [])) for index in range(1, expected_inner + 1)
    )
    if found_inner < expected_inner:
        result.add(
            "error",
            "missing-inner-copper",
            f"Expected at least {expected_inner} inner copper layer file(s), found {found_inner}",
        )

    if not pcb_only:
        if "bom" not in kinds:
            result.add("error", "missing-bom", "Missing BOM CSV")
        else:
            for item in kinds["bom"]:
                audit_bom(result, item)
        if "cpl" not in kinds:
            result.add("error", "missing-cpl", "Missing CPL/pick-and-place CSV")
        else:
            for item in kinds["cpl"]:
                audit_cpl(result, item)
        if result.bom_designators and result.cpl_designators:
            bom_only = result.bom_designators - result.cpl_designators
            cpl_only = result.cpl_designators - result.bom_designators
            if bom_only:
                result.add(
                    "warning",
                    "bom-cpl-bom-only",
                    f"{len(bom_only)} BOM designator(s) are absent from the CPL",
                )
            if cpl_only:
                result.add(
                    "warning",
                    "bom-cpl-cpl-only",
                    f"{len(cpl_only)} CPL designator(s) are absent from the BOM",
                )

    if "outline" in kinds:
        outline_text = "\n".join(item.text or "" for item in kinds["outline"]).upper()
        if "M02" not in outline_text:
            result.add("warning", "outline-termination", "Outline file may be incomplete")

    return result


def print_human(result: AuditResult) -> None:
    print(f"Release audit: {result.target}")
    print(
        f"  files={len(result.files)} errors={len(result.errors)} "
        f"warnings={len(result.warnings)}"
    )
    file_kinds: dict[str, int] = {}
    for item in result.files:
        file_kinds[item.kind] = file_kinds.get(item.kind, 0) + 1
    print(
        "  file kinds: " + ", ".join(f"{key}={value}" for key, value in sorted(file_kinds.items()))
    )
    for issue in result.issues:
        location = f" [{issue.path}]" if issue.path else ""
        print(f"  {issue.severity.upper():7} {issue.code}{location}: {issue.message}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit a PCB release package")
    parser.add_argument("target", help="release directory or .zip archive")
    parser.add_argument("--pcb-only", action="store_true", help="do not require BOM/CPL")
    parser.add_argument("--layers", type=int, default=2, help="expected copper layer count")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--allow-warnings",
        action="store_true",
        help="exit 0 when only warnings remain (errors still fail)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.layers < 1 or args.layers > 12:
        parser.error("--layers must be between 1 and 12")
    result = run_audit(Path(args.target), pcb_only=args.pcb_only, layers=args.layers)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
    else:
        print_human(result)
    if result.errors:
        return 1
    if result.warnings and not args.allow_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
