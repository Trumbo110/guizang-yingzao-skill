#!/usr/bin/env python3
"""Compile and validate the exact three-image handoff for an ImageGen edit call."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

from _runtime import ensure_runtime

ensure_runtime(("PIL",))

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing Pillow. Run scripts/check_dependencies.py.") from exc


REQUIRED_PROMPT_SECTIONS = (
    "Primary transformation:",
    "Image roles:",
    "Composition diagnosis:",
    "Composition repair:",
    "Subject treatment:",
    "Background treatment:",
    "Interaction:",
    "Reference transfer:",
    "Identity invariants:",
    "Typography layout:",
    "Text (verbatim):",
    "Do not add:",
)
OPTIONAL_PROMPT_SECTIONS = ("Display glyph design:",)
ALL_PROMPT_SECTIONS = REQUIRED_PROMPT_SECTIONS + OPTIONAL_PROMPT_SECTIONS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--guide", type=Path, required=True)
    parser.add_argument("--support", type=Path, action="append", default=[])
    parser.add_argument("--typeset-spec", type=Path, required=True)
    parser.add_argument("--typeset-report", type=Path, required=True)
    parser.add_argument("--glyph-brief", type=Path)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output-image", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_metadata(path: Path) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            return {"width": image.width, "height": image.height, "format": image.format}
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read image {path}: {exc}") from exc


def staged_image(source: Path, destination_base: Path) -> Path:
    suffix = source.suffix.lower() or ".png"
    destination = destination_base.with_suffix(suffix)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != destination.resolve():
        shutil.copy2(source, destination)
    return destination.resolve()


def section_value(prompt: str, heading: str) -> str:
    start = prompt.find(heading)
    if start < 0:
        return ""
    content_start = start + len(heading)
    later = [prompt.find(other, content_start) for other in ALL_PROMPT_SECTIONS if other != heading]
    later = [position for position in later if position >= 0]
    content_end = min(later) if later else len(prompt)
    return prompt[content_start:content_end].strip()


def printable_characters(text: str) -> list[str]:
    return [character for character in text if not character.isspace()]


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main() -> int:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    analysis_dir = run_dir / "analysis"
    inputs_dir = run_dir / "inputs"
    errors: list[str] = []

    required_files = {
        "source": args.source,
        "reference": args.reference,
        "guide": args.guide,
        "typeset spec": args.typeset_spec,
        "typeset report": args.typeset_report,
        "prompt": args.prompt,
    }
    required_files.update(
        {f"support image {index}": path for index, path in enumerate(args.support, start=1)}
    )
    for label, path in required_files.items():
        if not path.is_file():
            errors.append(f"{label} not found: {path}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    try:
        spec = load_json(args.typeset_spec)
        report = load_json(args.typeset_report)
        prompt = args.prompt.read_text(encoding="utf-8").strip()
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if report.get("passed") is not True:
        errors.append("typeset report must have passed=true")
    if list(spec.get("canvas", [])) != list(report.get("canvas", [])):
        errors.append("typeset spec canvas does not match typeset report canvas")

    image_data: dict[str, dict[str, Any]] = {}
    for label, path in (("source", args.source), ("reference", args.reference), ("guide", args.guide)):
        try:
            image_data[label] = image_metadata(path)
        except ValueError as exc:
            errors.append(str(exc))
    if "guide" in image_data and image_data["guide"]:
        guide_canvas = [image_data["guide"]["width"], image_data["guide"]["height"]]
        if guide_canvas != list(report.get("canvas", [])):
            errors.append(f"guide canvas {guide_canvas} does not match report canvas {report.get('canvas')}")

    missing_sections = [heading for heading in REQUIRED_PROMPT_SECTIONS if not section_value(prompt, heading)]
    if missing_sections:
        errors.append("prompt sections missing or empty: " + ", ".join(missing_sections))
    roles = section_value(prompt, "Image roles:")
    if roles and not all(label in roles for label in ("Image 1", "Image 2", "Image 3")):
        errors.append("Image roles must explicitly name Image 1, Image 2, and Image 3")
    for index, _path in enumerate(args.support, start=4):
        if roles and f"Image {index}" not in roles:
            errors.append(f"Image roles must explicitly name optional support Image {index}")

    display_layers = []
    for layer in spec.get("layers", []):
        role = str(layer.get("role", "")).strip().lower().replace("_", "-")
        if role in {"display", "display-title", "title", "structural-title"}:
            display_layers.append(layer)
    reinterpret_layers = [
        layer for layer in display_layers if str(layer.get("glyph_design_mode", "")).strip().lower() == "reinterpret"
    ]
    for layer in display_layers:
        mode = str(layer.get("glyph_design_mode", "")).strip().lower()
        if mode not in {"literal", "reinterpret"}:
            errors.append(f"{layer.get('id', 'display layer')}: missing explicit glyph_design_mode")
        if mode == "reinterpret" and str(layer.get("guide_render", "")).strip().lower() != "scaffold":
            errors.append(f"{layer.get('id', 'display layer')}: reinterpret requires guide_render=scaffold")

    if reinterpret_layers:
        if args.glyph_brief is None or not args.glyph_brief.is_file():
            errors.append("reinterpret display text requires --glyph-brief")
            glyph_brief = ""
        else:
            glyph_brief = args.glyph_brief.read_text(encoding="utf-8").strip()
            if len(glyph_brief) < 200:
                errors.append("glyph brief is too short to contain visible morphology and per-character actions")
        display_prompt = section_value(prompt, "Display glyph design:")
        if not display_prompt:
            errors.append("reinterpret display text requires a non-empty Display glyph design section")
        for layer in reinterpret_layers:
            title = str(layer.get("text", "")).strip()
            if title and title not in display_prompt:
                errors.append(f"Display glyph design must name the exact title {title!r}")
            missing_brief_chars = [char for char in printable_characters(title) if char not in glyph_brief]
            if missing_brief_chars:
                errors.append(
                    f"glyph brief does not cover every title character in {title!r}: "
                    + " ".join(missing_brief_chars)
                )
    elif section_value(prompt, "Display glyph design:"):
        errors.append("Display glyph design is present but no display layer is marked reinterpret")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    all_source_paths = [args.source, args.reference, args.guide, *args.support]
    source_hashes = [sha256(path) for path in all_source_paths]
    if len(set(source_hashes)) != len(source_hashes):
        print("ERROR: every source, reference, guide, and support input must be a distinct image")
        return 1
    output_image = args.output_image.resolve()
    if not is_within(output_image, run_dir / "final"):
        print(f"ERROR: output image must be inside {run_dir / 'final'}")
        return 1
    manifest_path = (args.manifest or (analysis_dir / "generation-call.json")).resolve()
    if not is_within(manifest_path, analysis_dir):
        print(f"ERROR: manifest must be inside {analysis_dir}")
        return 1

    staged_source = staged_image(args.source, inputs_dir / "01-edit-target")
    staged_reference = staged_image(args.reference, inputs_dir / "02-primary-reference")
    staged_guide = staged_image(args.guide, inputs_dir / "03-typeset-guide")
    staged_supports = [
        staged_image(path, inputs_dir / f"{index:02d}-support-{index - 3:02d}")
        for index, path in enumerate(args.support, start=4)
    ]
    staged_paths = [staged_source, staged_reference, staged_guide, *staged_supports]
    hashes = [sha256(path) for path in staged_paths]
    for index, path in enumerate(args.support, start=1):
        image_data[f"support-{index}"] = image_metadata(path)

    analysis_dir.mkdir(parents=True, exist_ok=True)
    staged_prompt = (analysis_dir / "04-imagegen-prompt.txt").resolve()
    staged_prompt.write_text(prompt + "\n", encoding="utf-8")
    output_image.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    tool_arguments = {
        "prompt": prompt,
        "referenced_image_paths": [str(path) for path in staged_paths],
    }
    input_order = [
        "edit-target",
        "primary-visual-reference",
        "typeset-guide",
        *[f"support-{index}" for index in range(1, len(staged_supports) + 1)],
    ]
    metadata_labels = (
        "source",
        "reference",
        "guide",
        *[f"support-{index}" for index in range(1, len(staged_supports) + 1)],
    )
    manifest = {
        "schema_version": 1,
        "action": "edit",
        "input_order": input_order,
        "referenced_image_paths": tool_arguments["referenced_image_paths"],
        "prompt_path": str(staged_prompt),
        "prompt": prompt,
        "tool_arguments": tool_arguments,
        "typeset_spec_path": str(args.typeset_spec.resolve()),
        "typeset_report_path": str(args.typeset_report.resolve()),
        "glyph_brief_path": str(args.glyph_brief.resolve()) if args.glyph_brief else None,
        "output_path": str(output_image),
        "inputs": [
            {
                "role": role,
                "path": str(path),
                "sha256": digest,
                **image_data[label],
            }
            for role, label, path, digest in zip(
                input_order,
                metadata_labels,
                staged_paths,
                hashes,
            )
        ],
    }
    manifest["call_signature"] = hashlib.sha256(
        ("\n".join(hashes) + "\n" + prompt).encode("utf-8")
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"READY: exact ImageGen handoff written to {manifest_path}")
    print("Pass manifest.tool_arguments to ImageGen without rewriting, reordering, or omission.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
