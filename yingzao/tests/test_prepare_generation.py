#!/usr/bin/env python3
"""Regression tests for the fixed ImageGen handoff manifest."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_generation.py"


PROMPT = """Primary transformation: Extract and materially reinterpret the real subject in one editorial scene.
Image roles: Image 1 is the edit target. Image 2 is the primary visual reference. Image 3 is the spatial typeset scaffold.
Composition diagnosis: The source has no deliberate title lane.
Composition repair: Shift the connected subject once and rebuild only a continuous wall field.
Subject treatment: Extract the real subject, change its scale, and apply region-specific material treatment.
Background treatment: Build one active mineral color field with a second low-frequency material zone.
Interaction: Let one real roof edge pass in front of the title while preserving legibility.
Reference transfer: Transfer the reference's subject/background/type mechanism, not merely its palette.
Identity invariants: Preserve the plaque, roof hierarchy, doorway, and real asymmetric details.
Typography layout: Follow Image 3's title slots, shared axis, reading order, and overlap boundary.
Display glyph design: Reinterpret only “飞檐” as a locked wordmark; do not copy a stock font silhouette.
Text (verbatim): “飞檐”; “善化寺”.
Do not add: invented architecture, mirrored parts, fake inscriptions, foreign text, or UI cards.
"""


class PrepareGenerationTests(unittest.TestCase):
    def make_fixture(self, root: Path, *, guide_render: str = "scaffold", prompt: str = PROMPT) -> list[str]:
        run_dir = root / "output" / "yingzao" / "run"
        analysis = run_dir / "analysis"
        analysis.mkdir(parents=True)
        source = root / "source.jpg"
        reference = root / "reference.jpg"
        guide = analysis / "typeset-guide.png"
        Image.new("RGB", (320, 240), "#403020").save(source)
        Image.new("RGB", (240, 320), "#203040").save(reference)
        Image.new("RGB", (640, 360), "#EEEEEC").save(guide)
        spec = analysis / "typeset-spec.json"
        spec.write_text(
            json.dumps(
                {
                    "mode": "typeset-guide",
                    "canvas": [640, 360],
                    "layers": [
                        {
                            "id": "display-title",
                            "role": "display",
                            "text": "飞檐",
                            "glyph_design_mode": "reinterpret",
                            "guide_render": guide_render,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        report = analysis / "typeset-report.json"
        report.write_text(json.dumps({"passed": True, "canvas": [640, 360]}), encoding="utf-8")
        glyph = analysis / "glyph-brief.md"
        glyph.write_text(
            "飞：横向屋檐决定长横、方切端点和高重心；保持全部标准笔画。\n"
            "檐：斗拱叠涩决定开放字腔和层级横画；保持木、詹的标准拓扑。\n" * 5,
            encoding="utf-8",
        )
        prompt_path = analysis / "generation-prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        return [
            sys.executable,
            str(SCRIPT),
            "--run-dir",
            str(run_dir),
            "--source",
            str(source),
            "--reference",
            str(reference),
            "--guide",
            str(guide),
            "--typeset-spec",
            str(spec),
            "--typeset-report",
            str(report),
            "--glyph-brief",
            str(glyph),
            "--prompt",
            str(prompt_path),
            "--output-image",
            str(run_dir / "final" / "poster.png"),
        ]

    def test_compiles_self_contained_three_image_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            completed = subprocess.run(self.make_fixture(root), capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            manifest_path = root / "output" / "yingzao" / "run" / "analysis" / "generation-call.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["input_order"], ["edit-target", "primary-visual-reference", "typeset-guide"])
            self.assertEqual(len(manifest["referenced_image_paths"]), 3)
            self.assertTrue(all(Path(path).is_file() for path in manifest["referenced_image_paths"]))
            self.assertEqual(manifest["prompt"], PROMPT.strip())
            self.assertEqual(manifest["tool_arguments"]["prompt"], PROMPT.strip())
            self.assertEqual(
                manifest["tool_arguments"]["referenced_image_paths"], manifest["referenced_image_paths"]
            )
            self.assertEqual(Path(manifest["prompt_path"]).name, "04-imagegen-prompt.txt")
            self.assertEqual(len(manifest["call_signature"]), 64)

    def test_rejects_prompt_that_drops_a_model_work_domain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            prompt = PROMPT.replace("Subject treatment:", "Subject notes:")
            completed = subprocess.run(
                self.make_fixture(root, prompt=prompt), capture_output=True, text=True, check=False
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("Subject treatment:", completed.stdout)

    def test_rejects_stock_font_silhouette_for_reinterpret_title(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            completed = subprocess.run(
                self.make_fixture(root, guide_render="text"), capture_output=True, text=True, check=False
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("reinterpret requires guide_render=scaffold", completed.stdout)

    def test_appends_named_support_images_after_the_fixed_three_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            prompt = PROMPT.replace(
                "Image 3 is the spatial typeset scaffold.",
                "Image 3 is the spatial typeset scaffold. Image 4 is a same-place food support source.",
            )
            command = self.make_fixture(root, prompt=prompt)
            support = root / "support.jpg"
            Image.new("RGB", (300, 220), "#604020").save(support)
            insertion = command.index("--typeset-spec")
            command[insertion:insertion] = ["--support", str(support)]
            completed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            manifest = json.loads(
                (root / "output" / "yingzao" / "run" / "analysis" / "generation-call.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["input_order"][-1], "support-1")
            self.assertEqual(len(manifest["referenced_image_paths"]), 4)


if __name__ == "__main__":
    unittest.main()
