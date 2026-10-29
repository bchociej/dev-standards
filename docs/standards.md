# This repository's standards adoption

The [README adoption records](../README.md#this-repositorys-adoption) identify the
applied versions and their source refs. This documentation-only repository is
both subject repo and standards repo; its working standards can advance without
silently changing its adopted versions. The recorded integer versions are legacy
exact identifiers. They remain in force until the deliberately deferred
[SemVer transition](../TODO.md) is completed after publication.

## Scope and choices

BAS-001 applies to this repository's hosting, source safety, and development
checks. BAS-002 applies to its adoption records. CAS-001 does not apply because
this repository ships no container application. Application tests, runtime
packaging, image publication, and deployment are inapplicable.

The repository uses GitHub under `bchociej` and GitHub Actions. Adoption adds only
document checks, not publication or deployment. Existing user instructions govern
commits and pushes; adoption does not create standing authorization for either.
Git commits use the established GitHub noreply identity. The standard owner's
explicitly authorized public name and account are intentional documentation.

BAS-001's Python tooling SHOULD recommendation is not followed: the checker uses
only the Python standard library, has no installed dependencies, and runs with
`python3` locally and the runner's Python in CI. uv, a package manifest, and a
lockfile would add packaging machinery without locking any third-party packages.
There are no external Python dependencies to record or synchronize. The checkout
action is pinned to a commit; the runner and Python patch version are not pinned.
This tradeoff suits a small document checker, whose supported language baseline
is Python 3.10 or later. There are no known MUST exceptions.

## Verification and limitations

The adoption assessment used standards source commit
`7a58229755dadb9a0c77d72bfe976030ce82d076` for both recorded standards. Current
remote `main` front matter was verified at
`2998139febafc5ef6a8d98f6291939c211c353b1` before the approved implementation.
The subsequent local commit adds the approved BAS-001 personalization change.

Run `python3 scripts/check_docs.py` and `git diff --check` from the repository
root; run `python3 -m unittest discover -s tests` for constraint and checker
regressions. The checker validates local inline Markdown links and headings, basic
whitespace, index names/versions/dates, SemVer release immutability, the current
selected dependency graph, and this repository's pinned adoption sources and
their transitive constraints. CI fetches full history for these checks. Fenced examples are excluded from link and requirement scans.
The checker targets this repo's Markdown conventions, not all Markdown syntax.

Local checks passed during the original adoption. The SemVer maintenance update
adds caret-boundary, invalid-version, dependency-conflict, and checker-regression
tests. Run the commands above for the current result. Remote CI for these changes
requires an authorized commit and push; follow-up is tracked in TODO.md.

External link availability, hosting visibility, and all possible sensitive
information are not established by the checker. Source and history review is
still a human or agent task, not a claim of comprehensive secret scanning.
Automated checks do not decide whether prose changes are semantically breaking.
These limitations and the documented SHOULD departure do not silently upgrade
the legacy adoption records.
