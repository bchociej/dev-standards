# Working on dev-standards

Read the README and adoption guide, then follow
[the versioning policy](docs/versioning.md).

Before implementing a breaking change, flag its concrete impact and proposed
major version bump to the user. Existing explicit approval for that scope is
sufficient; do not repeatedly request it. Do not silently classify stronger
requirements or incompatible dependency changes as compatible.

For every standards change, maintain correct SemVer headers, dates, index
entries, dependency constraints, and examples. Review transitive dependencies
and ensure the resulting published set is conflict-free. Preserve released
versions through Git history; never silently reinterpret old declarations.

Run `python3 scripts/check_docs.py`, `python3 -m unittest discover -s tests`,
and `git diff --check` before completion. Automated checks cannot establish
semantic compatibility; review the meaning of changes as well.

Keep deferred work in TODO.md. Do not commit or push without applicable user
authorization; preserve the public-safe identity used in repository history.
