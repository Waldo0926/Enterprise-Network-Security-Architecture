import copy
import json
import unittest
from pathlib import Path

from src.validator import ValidationError, validate_firewall_policy, validate_network_plan

ROOT = Path(__file__).resolve().parents[1]


class ArchitectureValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads((ROOT / "config/network_plan.json").read_text())
        cls.policy = json.loads((ROOT / "config/firewall_policy.json").read_text())

    def test_reference_plan_is_valid(self):
        self.assertTrue(validate_network_plan(self.plan))
        self.assertTrue(validate_firewall_policy(self.plan, self.policy))

    def test_overlap_is_rejected(self):
        broken = copy.deepcopy(self.plan)
        broken["segments"][1]["subnet"] = "10.20.1.0/24"
        broken["segments"][1]["gateway"] = "10.20.1.1"
        with self.assertRaises(ValidationError):
            validate_network_plan(broken)

    def test_out_of_base_network_is_rejected(self):
        broken = copy.deepcopy(self.plan)
        broken["segments"][0]["subnet"] = "10.21.0.0/23"
        broken["segments"][0]["gateway"] = "10.21.0.1"
        with self.assertRaises(ValidationError):
            validate_network_plan(broken)

    def test_non_default_deny_policy_is_rejected(self):
        broken = copy.deepcopy(self.policy)
        broken["default_action"] = "allow"
        with self.assertRaises(ValidationError):
            validate_firewall_policy(self.plan, broken)

    def test_missing_ot_isolation_is_rejected(self):
        broken = copy.deepcopy(self.policy)
        broken["rules"] = [r for r in broken["rules"] if r["id"] != "FW-010"]
        with self.assertRaises(ValidationError):
            validate_firewall_policy(self.plan, broken)


if __name__ == "__main__":
    unittest.main()
