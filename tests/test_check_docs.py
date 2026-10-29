"""Exercise real document/history checks in isolated Git repositories."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="standards-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        subprocess.run(
            ["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(self.root)],
            check=True, capture_output=True,
        )
        names = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, text=True,
        ).splitlines()
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)

    def check(self, expected):
        result = subprocess.run(
            ["python3", "scripts/check_docs.py"], cwd=self.root,
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stderr

    def test_clean_documents_pass(self):
        self.check(0)

    def test_broken_anchor_fails(self):
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\n[Broken](docs/adopting.md#missing-heading)\n")
        self.assertIn("missing heading", self.check(1))

    def test_incompatible_dependency_fails(self):
        path = self.root / "cas-001-container-application-repositories.md"
        path.write_text(path.read_text().replace("version ^5.0.0", "version ^6.0.0"))
        self.assertIn("does not satisfy", self.check(1))

    def test_published_text_requires_new_version(self):
        subprocess.run(["git", "add", "--all"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "commit", "--quiet", "--allow-empty", "-m", "Fixture publication"],
            cwd=self.root, check=True,
        )
        path = self.root / "bas-001-repository-and-development-fundamentals.md"
        path.write_text(path.read_text() + "\nAn editorial change.\n")
        self.assertIn("changed without a version bump", self.check(1))

    def test_missing_adoption_source_fails(self):
        path = self.root / "README.md"
        text = path.read_text().replace(
            "blob/7a58229755dadb9a0c77d72bfe976030ce82d076/", "blob/" + "0" * 40 + "/"
        )
        path.write_text(text)
        self.assertIn("unresolvable adoption source", self.check(1))


if __name__ == "__main__":
    unittest.main()
