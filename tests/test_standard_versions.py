import unittest

from scripts.standard_versions import dependency_errors, parse, satisfies


class VersionTests(unittest.TestCase):
    def test_caret_boundaries(self):
        for spec, accepted, rejected in [
            ("^5.1.2", ["5.1.2", "5.9.0"], ["5.1.1", "6.0.0"]),
            ("^0.2.3", ["0.2.3", "0.2.9"], ["0.2.2", "0.3.0"]),
            ("^0.0.3", ["0.0.3"], ["0.0.2", "0.0.4"]),
            ("^0.0.0", ["0.0.0"], ["0.0.1"]),
        ]:
            for version in accepted:
                self.assertTrue(satisfies(version, spec), (version, spec))
            for version in rejected:
                self.assertFalse(satisfies(version, spec), (version, spec))

    def test_exact_and_legacy_are_not_ranges_or_aliases(self):
        self.assertTrue(satisfies("5.0.0", "5.0.0"))
        self.assertFalse(satisfies("5.0.1", "5.0.0"))
        self.assertTrue(satisfies("4", "4"))
        self.assertFalse(satisfies("4.0.0", "4"))
        with self.assertRaises(ValueError):
            satisfies("4", "^4.0.0")

    def test_unsupported_versions_are_rejected(self):
        for invalid in ["01.2.3", "1.02.3", "1.2.03", "1.2", "v1.2.3",
                        "1.2.3-rc.1", "1.2.3+build", "^1.2.3", "1.2.*"]:
            with self.assertRaises(ValueError):
                parse(invalid)

    def test_current_transitive_selection_is_compatible(self):
        selected = {
            "CAS-001": ("4.0.0", "**BAS-001 version ^5.0.0**"),
            "BAS-001": ("5.2.0", "**BAS-002 version ^3.0.0**"),
            "BAS-002": ("3.1.0", ""),
        }
        self.assertEqual(dependency_errors(selected), [])
        selected["BAS-002"] = ("4.0.0", "")
        self.assertIn("does not satisfy", dependency_errors(selected)[0])
        del selected["BAS-002"]
        self.assertIn("missing dependency", dependency_errors(selected)[0])

    def test_conflicting_diamond_is_rejected(self):
        selected = {
            "ONE-001": ("1.0.0", "**BAS-001 version ^5.0.0**"),
            "TWO-001": ("1.0.0", "**BAS-001 version ^6.0.0**"),
            "BAS-001": ("5.0.0", ""),
        }
        self.assertEqual(len(dependency_errors(selected)), 1)


if __name__ == "__main__":
    unittest.main()
