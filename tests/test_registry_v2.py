import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.registry import AssetRegistry


class AssetRegistryV2Tests(unittest.TestCase):
    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _run(self, *command: str, cwd: Path) -> str:
        return subprocess.check_output(command, cwd=cwd, text=True).strip()

    def _fixture(self, temporary: Path) -> dict:
        temporary.mkdir(parents=True, exist_ok=True)
        source = temporary / "source"
        source.mkdir()
        (source / "LICENSE.txt").write_text("Apache-2.0\n", encoding="utf-8")
        (source / "module.txt").write_text("source fixture\n", encoding="utf-8")
        self._run("git", "init", "-b", "main", cwd=source)
        self._run("git", "config", "user.name", "fixture", cwd=source)
        self._run("git", "config", "user.email", "fixture@example.invalid", cwd=source)
        self._run("git", "remote", "add", "origin", "https://github.com/CompVis/zigma.git", cwd=source)
        self._run("git", "add", "LICENSE.txt", "module.txt", cwd=source)
        self._run("git", "commit", "-m", "fixture", cwd=source)

        checkpoint = temporary / "checkpoint.bin"
        checkpoint.write_bytes(b"checkpoint-fixture")
        vae = temporary / "vae.bin"
        vae.write_bytes(b"vae-fixture")
        checkpoint_metadata = temporary / "checkpoint_metadata.json"
        checkpoint_metadata.write_text(
            json.dumps(
                {
                    "format_version": "1.0",
                    "experiment_id": "fixture",
                    "epoch": 0,
                    "resolved_config_path": "config.json",
                }
            ),
            encoding="utf-8",
        )
        dataset_manifest = temporary / "dataset_manifest.json"
        dataset_manifest.write_text(
            json.dumps(
                {
                    "format_version": "1.0",
                    "dataset_id": "fixture",
                    "root_uri": "file:///fixture",
                    "split_files": {"train": "train.txt"},
                    "license": "fixture-license",
                }
            ),
            encoding="utf-8",
        )
        return {
            "format_version": "2.0",
            "source": {
                "repository_url": "https://github.com/CompVis/zigma.git",
                "checkout_path": str(source),
                "commit": self._run("git", "rev-parse", "HEAD", cwd=source),
                "git_tree_id": self._run("git", "rev-parse", "HEAD^{tree}", cwd=source),
                "source_tree_sha256": AssetRegistry.source_tree_sha256(source),
                "worktree_clean": True,
                "license": "Apache-2.0",
                "license_path": str(source / "LICENSE.txt"),
                "license_sha256": self._sha256(source / "LICENSE.txt"),
                "provenance_evidence": "https://github.com/CompVis/zigma.git",
            },
            "checkpoint": {
                "path": str(checkpoint),
                "sha256": self._sha256(checkpoint),
                "size_bytes": checkpoint.stat().st_size,
                "license": "Apache-2.0",
                "provenance_evidence": "https://huggingface.co/taohu/zigma",
                "metadata_path": str(checkpoint_metadata),
            },
            "vae": {
                "id": "fixture/vae",
                "revision": "0123456789abcdef0123456789abcdef01234567",
                "path": str(vae),
                "sha256": self._sha256(vae),
                "size_bytes": vae.stat().st_size,
                "license": "Apache-2.0",
                "provenance_evidence": "https://example.invalid/vae",
            },
            "dataset": {
                "manifest_path": str(dataset_manifest),
                "license": "fixture-license",
                "provenance_evidence": "https://example.invalid/dataset",
            },
        }

    def test_v2_positive_fixture_validates_all_static_contracts(self):
        with tempfile.TemporaryDirectory() as temporary:
            registry = AssetRegistry(self._fixture(Path(temporary)))
            result = registry.validate()
        self.assertEqual(result["status"], "unproven")
        self.assertEqual(result["blocked_codes"], [])

    def test_v2_negative_asset_contracts_preserve_scope_blocked_codes(self):
        with tempfile.TemporaryDirectory() as temporary:
            for field, replacement, expected_code in (
                ("sha256", "0" * 64, "BLOCKED_CHECKPOINT_IDENTITY"),
                ("size_bytes", 1, "BLOCKED_CHECKPOINT_IDENTITY"),
                ("path", str(Path(temporary) / "missing.bin"), "BLOCKED_CHECKPOINT_IDENTITY"),
                ("license", "", "BLOCKED_LICENSE"),
                ("provenance_evidence", "", "BLOCKED_CHECKPOINT_IDENTITY"),
            ):
                with self.subTest(field=field):
                    payload = self._fixture(Path(temporary) / field)
                    payload["checkpoint"][field] = replacement
                    result = AssetRegistry(payload).validate()
                    self.assertEqual(result["status"], "blocked")
                    self.assertIn(expected_code, result["blocked_codes"])

    def test_v1_registry_remains_readable(self):
        legacy = AssetRegistry.empty().to_dict()
        AssetRegistry.validate_schema_document(legacy, AssetRegistry.schema_document())
        self.assertIn("BLOCKED_SOURCE_AMBIGUITY", AssetRegistry(legacy).validate()["blocked_codes"])

    def test_checkpoint_and_dataset_schema_paths_and_unsupported_keywords(self):
        checkpoint = {
            "format_version": "1.0",
            "experiment_id": "fixture",
            "epoch": 0,
            "resolved_config_path": "config.json",
        }
        dataset = {
            "format_version": "1.0",
            "dataset_id": "fixture",
            "root_uri": "file:///fixture",
            "split_files": {"train": "train.txt"},
        }
        AssetRegistry.validate_checkpoint_metadata(checkpoint)
        AssetRegistry.validate_dataset_manifest(dataset)
        with self.assertRaises(ValueError):
            AssetRegistry.validate_checkpoint_metadata({**checkpoint, "epoch": -1})
        with self.assertRaises(ValueError):
            AssetRegistry.validate_dataset_manifest({**dataset, "split_files": {"train": 1}})
        with self.assertRaises(ValueError):
            AssetRegistry.validate_schema_document(
                {"value": "x"},
                {"type": "object", "properties": {"value": {"type": "string", "pattern": ".*"}}},
            )

    def test_partial_v2_registry_keeps_all_unverified_asset_codes(self):
        with tempfile.TemporaryDirectory() as temporary:
            payload = self._fixture(Path(temporary))
            payload["checkpoint"] = {key: None for key in payload["checkpoint"]}
            payload["vae"] = {key: None for key in payload["vae"]}
            payload["dataset"] = {key: None for key in payload["dataset"]}
            result = AssetRegistry(payload).validate()
        self.assertEqual(result["status"], "blocked")
        self.assertIn("BLOCKED_CHECKPOINT_IDENTITY", result["blocked_codes"])
        self.assertIn("BLOCKED_VAE_IDENTITY", result["blocked_codes"])
        self.assertIn("BLOCKED_DATA_CONTRACT", result["blocked_codes"])
        self.assertIn("BLOCKED_LICENSE", result["blocked_codes"])
