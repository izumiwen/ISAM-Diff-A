import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.bootstrap import load_config, prepare_run


class BootstrapTests(unittest.TestCase):
    def test_base_config_has_only_blocked_or_null_research_values(self):
        config = load_config(ROOT / "configs" / "base.yaml")
        self.assertEqual(config["research_contract"]["status"], "blocked")
        self.assertTrue(
            all(value is None for value in config["research_contract"]["fields"].values())
        )

    def test_prepare_run_writes_receipt_and_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "run"
            receipt = prepare_run(
                config_path=ROOT / "configs" / "base.yaml",
                output_dir=output_dir,
                command=["test"],
            )
            self.assertTrue((output_dir / "resolved_config.yaml").is_file())
            self.assertTrue((output_dir / "run_metadata.json").is_file())
            self.assertTrue((output_dir / "checksums.sha256").is_file())
            self.assertTrue((output_dir / "diagnostics" / "02_cli_help.stdout").is_file())
            self.assertTrue((output_dir / "diagnostics" / "03_schema_and_receipt_smoke.stdout").is_file())
            self.assertIn("BLOCKED_SOURCE_AMBIGUITY", receipt["blocked_codes"])
            with self.assertRaises(FileExistsError):
                prepare_run(
                    config_path=ROOT / "configs" / "base.yaml",
                    output_dir=output_dir,
                    command=["test"],
                )

    def test_receipt_checksum_matches_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            output_dir = Path(temporary) / "run"
            prepare_run(ROOT / "configs" / "base.yaml", output_dir, ["test"])
            metadata = json.loads((output_dir / "run_metadata.json").read_text())
            checksums = (output_dir / "checksums.sha256").read_text()
            self.assertEqual(len(metadata["config_sha256"]), 64)
            self.assertIn("run_metadata.json", checksums)
