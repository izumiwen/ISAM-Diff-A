import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from project_name.registry import AssetRegistry


class AssetRegistryTests(unittest.TestCase):
    def test_empty_registry_reports_all_missing_contracts(self):
        registry = AssetRegistry.empty()
        result = registry.validate()
        self.assertEqual(result["status"], "blocked")
        self.assertIn("BLOCKED_SOURCE_AMBIGUITY", result["blocked_codes"])
        self.assertIn("BLOCKED_CHECKPOINT_IDENTITY", result["blocked_codes"])
        self.assertIn("BLOCKED_VAE_IDENTITY", result["blocked_codes"])
        self.assertIn("BLOCKED_TRANSPORT_CONTRACT", result["blocked_codes"])
        self.assertIn("BLOCKED_CONDITIONING_CONTRACT", result["blocked_codes"])
        self.assertIn("BLOCKED_DATA_CONTRACT", result["blocked_codes"])
        self.assertIn("BLOCKED_LICENSE", result["blocked_codes"])

    def test_schema_rejects_unknown_or_missing_contract_fields(self):
        schema = json.loads((ROOT / "references" / "asset_registry.schema.json").read_text())
        registry = AssetRegistry.empty().to_dict()
        AssetRegistry.validate_schema_document(registry, schema)
        registry.pop("repository_url")
        with self.assertRaises(ValueError):
            AssetRegistry.validate_schema_document(registry, schema)

