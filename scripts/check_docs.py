"""Check the Markdown conventions used by this repository; no network or packages."""

from collections import Counter
from datetime import date
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []


def fail(path, message):
    ERRORS.append(f"{path.relative_to(ROOT)}: {message}")


def prose(text):
    """Exclude fenced examples from link, heading, and dependency checks."""
    return re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M | re.S)


def anchors(text):
    counts = Counter()
    result = set()
    for heading in re.findall(r"^#{1,6} (.+)$", prose(text), re.M):
        slug = re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
        suffix = f"-{counts[slug]}" if counts[slug] else ""
        counts[slug] += 1
        result.add(slug + suffix)
    return result


def git(*args):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.DEVNULL
    )


def version_at(ref, path):
    text = git("show", f"{ref}:{path}")
    match = re.search(r"^Version (\d+) —", text, re.M)
    return match.group(1) if match else None


def main():
    files = [ROOT / name for name in git("ls-files", "--cached", "--others", "--exclude-standard").splitlines() if name.endswith(".md")]
    for path in files:
        text = path.read_text()
        if not text.endswith("\n") or text.endswith("\n\n"):
            fail(path, "use one final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(path, f"line {number}: trailing whitespace")
        # Inline Markdown links are the convention here; remote URLs are not fetched.
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", prose(text)):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            destination = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not destination.is_file():
                fail(path, f"missing local link: {target}")
            elif parts.fragment and destination.suffix == ".md":
                if unquote(parts.fragment) not in anchors(destination.read_text()):
                    fail(path, f"missing heading: {target}")

    readme = ROOT / "README.md"
    index_text = readme.read_text().split("## Standards index\n", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(r"^\| ([A-Z]+-\d+) \| (\d+) \| ([\d-]+) \| \[[^]]+\]\(([^)]+)\) \|", index_text, re.M)
    standards = {}
    for sid, version, published, filename in rows:
        path = ROOT / filename
        if sid in standards:
            fail(readme, f"duplicate index ID: {sid}")
        standards[sid] = filename
        text = path.read_text()
        day = date.fromisoformat(published)
        expected = f"Version {version} — {day.strftime('%B')} {day.day}, {day.year}."
        if not text.startswith(f"# {sid}: ") or expected not in text.splitlines()[2]:
            fail(path, "title/version/date disagrees with index")
        if not re.fullmatch(re.escape(sid.lower()) + r"-[a-z0-9]+(?:-[a-z0-9]+)*\.md", filename):
            fail(path, "filename does not follow standard naming convention")
    actual = {p.name for p in ROOT.glob("*-*.md") if re.match(r"[a-z]+-\d+-", p.name)}
    if actual != set(standards.values()):
        fail(readme, "index does not cover exactly the standard files")

    for sid, filename in standards.items():
        path = ROOT / filename
        for dependency, required in re.findall(r"\*\*([A-Z]+-\d+) version (\d+)\*\*", prose(path.read_text())):
            if dependency not in standards:
                fail(path, f"unknown dependency: {dependency}")
                continue
            dep_path = standards[dependency]
            # Dependencies may intentionally refer to older versions, not current main.
            refs = git("log", "--format=%H", "--", dep_path).splitlines()
            if not any(version_at(ref, dep_path) == required for ref in refs):
                fail(path, f"dependency {dependency} version {required} not found in history")

    # Verify this subject repo's pinned records, independently of the current index.
    adopted = readme.read_text().split("## This repository's adoption\n", 1)[1].split("\n## ", 1)[0]
    records = re.findall(r"^\| ([A-Z]+-\d+) \| (\d+) \| \[[^]]+\]\(https://github.com/bchociej/dev-standards/blob/([0-9a-f]{40})/([^)#]+)\) \|", adopted, re.M)
    if not records:
        fail(readme, "no pinned adoption records")
    for sid, version, ref, filename in records:
        try:
            if sid not in standards or filename != standards[sid] or version_at(ref, filename) != version:
                fail(readme, f"invalid adoption record: {sid}")
        except subprocess.CalledProcessError:
            fail(readme, f"unresolvable adoption source: {sid} at {ref}")
    if ERRORS:
        print("\n".join(ERRORS), file=sys.stderr)
        return 1
    print(f"Checked {len(files)} Markdown files, {len(rows)} index entries, and {len(records)} adoption records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
