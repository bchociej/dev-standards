"""The exact/caret stable-SemVer subset supported by dev-standards."""

import re

NUMBER = r"(?:0|[1-9][0-9]*)"
VERSION = re.compile(rf"{NUMBER}\.{NUMBER}\.{NUMBER}")
DEPENDENCY = re.compile(r"\*\*([A-Z]+-\d+) version ([^*]+)\*\*")


def parse(version):
    if not VERSION.fullmatch(version):
        raise ValueError(f"invalid stable semantic version: {version}")
    return tuple(map(int, version.split(".")))


def satisfies(version, spec):
    """Legacy integers are exact IDs, never aliases for X.0.0."""
    if re.fullmatch(NUMBER, spec):
        return version == spec
    caret = spec.startswith("^")
    lower = parse(spec[1:] if caret else spec)
    actual = parse(version)
    if not caret:
        return actual == lower
    major, minor, patch = lower
    if major:
        upper = (major + 1, 0, 0)
    elif minor:
        upper = (0, minor + 1, 0)
    else:
        upper = (0, 0, patch + 1)
    return lower <= actual < upper


def document_version(text):
    match = re.search(r"^Version ([^ ]+) —", text, re.M)
    if not match:
        raise ValueError("missing version header")
    return match.group(1)


def dependency_errors(selection):
    """Validate a complete chosen graph; do not silently choose other versions.

    selection maps each ID to its (exact version, document text).
    """
    errors = []
    for sid, (_, text) in selection.items():
        for dependency, spec in DEPENDENCY.findall(text):
            if dependency not in selection:
                errors.append(f"{sid}: missing dependency {dependency} {spec}")
                continue
            version = selection[dependency][0]
            try:
                compatible = satisfies(version, spec)
            except ValueError as exc:
                errors.append(f"{sid}: {exc}")
                continue
            if not compatible:
                errors.append(f"{sid}: {dependency} {version} does not satisfy {spec}")
    return errors
