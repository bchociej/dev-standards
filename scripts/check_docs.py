"""Check this repo's Markdown conventions, releases, and adoption resolutions."""

from collections import Counter
from datetime import date
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from standard_versions import dependency_errors, document_version, parse, satisfies

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


def check_release(path, text):
    current = parse(document_version(text))
    for ref in git("log", "--format=%H", "--", path.name).splitlines():
        previous = git("show", f"{ref}:{path.name}")
        version = document_version(previous)
        if "." not in version:  # Pre-SemVer history has separate exact IDs.
            continue
        published = parse(version)
        if current < published:
            fail(path, f"version regressed below published {version}")
        if current == published and text != previous:
            fail(path, f"published {version} changed without a version bump")


def check_adoption(readme, standards):
    section = readme.read_text().split("## This repository's adoption\n", 1)[1]
    section = section.split("\n## ", 1)[0]
    selection = {}
    # Accept the old exact-only schema and the new spec/resolution schema.
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or not re.fullmatch(r"[A-Z]+-\d+", cells[0]):
            continue
        sid = cells[0]
        if len(cells) == 4:
            spec, link = cells[1:3]
            resolved = spec
        elif len(cells) == 5:
            spec, resolved, link = cells[1:4]
            parse(resolved)
            if spec.lstrip("^") != resolved and not spec.startswith("^"):
                raise ValueError(f"{sid}: malformed exact spec")
        else:
            fail(readme, f"malformed adoption row: {sid}")
            continue
        source = re.search(
            r"https://github.com/bchociej/dev-standards/blob/([0-9a-f]{40})/([^\s)#]+)",
            link,
        )
        if not source or sid not in standards or source[2] != standards[sid]:
            fail(readme, f"invalid adoption source: {sid}")
            continue
        if sid in selection:
            fail(readme, f"duplicate adoption ID: {sid}")
        try:
            text = git("show", f"{source[1]}:{source[2]}")
            actual = document_version(text)
            if actual != resolved or not satisfies(actual, spec):
                fail(readme, f"invalid adoption resolution: {sid}")
            selection[sid] = (actual, prose(text))
        except subprocess.CalledProcessError:
            fail(readme, f"unresolvable adoption source: {sid}")
    if not selection:
        fail(readme, "no adoption records")
    for error in dependency_errors(selection):
        fail(readme, error)
    return len(selection)


def main():
    names = git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    files = [ROOT / name for name in names if name.endswith(".md")]
    for path in files:
        text = path.read_text()
        if not text.endswith("\n") or text.endswith("\n\n"):
            fail(path, "use one final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                fail(path, f"line {number}: trailing whitespace")
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
    index = readme.read_text().split("## Standards index\n", 1)[1].split("\n## ", 1)[0]
    rows = re.findall(
        r"^\| ([A-Z]+-\d+) \| ([^ |]+) \| ([\d-]+) \| \[[^]]+\]\(([^)]+)\) \|",
        index, re.M,
    )
    standards, selection = {}, {}
    for sid, version, published, filename in rows:
        parse(version)
        path = ROOT / filename
        if sid in standards:
            fail(readme, f"duplicate index ID: {sid}")
        standards[sid] = filename
        text = path.read_text()
        selection[sid] = (version, prose(text))
        day = date.fromisoformat(published)
        expected = f"Version {version} — {day.strftime('%B')} {day.day}, {day.year}."
        if not text.startswith(f"# {sid}: ") or expected not in text.splitlines()[2]:
            fail(path, "title/version/date disagrees with index")
        if not re.fullmatch(re.escape(sid.lower()) + r"-[a-z0-9]+(?:-[a-z0-9]+)*\.md", filename):
            fail(path, "filename does not follow standard naming convention")
        check_release(path, text)
    actual = {p.name for p in ROOT.glob("*-*.md") if re.match(r"[a-z]+-\d+-", p.name)}
    if actual != set(standards.values()):
        fail(readme, "index does not cover exactly the standard files")
    for error in dependency_errors(selection):
        fail(readme, error)
    adopted = check_adoption(readme, standards)
    if ERRORS:
        print("\n".join(ERRORS), file=sys.stderr)
        return 1
    print(f"Checked {len(files)} Markdown files, {len(rows)} releases, and {adopted} resolutions.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, IndexError, FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"Invalid document metadata or Git history: {exc}", file=sys.stderr)
        raise SystemExit(1)
