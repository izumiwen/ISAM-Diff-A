import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.registry import AssetRegistry


class BlockedStateTests(unittest.TestCase):
    def test_partial_registry_never_reports_success(self):
        registry = AssetRegistry.empty()
        registry.values["repository_url"] = "https://example.invalid/source"
        registry.values["source_commit"] = "unverified"
        result = registry.validate()
        self.assertEqual(result["status"], "blocked")
        self.assertIn("BLOCKED_CHECKPOINT_IDENTITY", result["blocked_codes"])

