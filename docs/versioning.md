# Standard versioning and compatibility

Terms and requirement keywords follow the [README conventions](../README.md).
Each standard uses [Semantic Versioning 2.0.0](https://semver.org/). Its public
interface is its scope, normative requirements, dependency constraints, and
required adoption records. Compatibility means an already conforming subject
repo can remain conforming without changes or new exceptions.

## Assigning versions

- **MAJOR:** incompatible changes, including new or stronger MUST/SHOULD
  obligations, removed supported choices, widened mandatory scope, or dependency
  changes that invalidate previously valid selections. A new SHOULD can require
  a new documented departure, so it is not automatically compatible.
- **MINOR:** compatible additions, such as optional patterns or additional
  supported choices that preserve all existing conforming implementations.
- **PATCH:** compatible corrections and editorial changes without new obligations.

Published standard text MUST NOT change without a version increment, even for
editorial fixes. Publication means inclusion on the standards repo's `main`.
Previous versions remain available at their source commits. Version bumps MUST
be assessed against the last published version, not intermediate local drafts.
Major bumps reset minor and patch to zero; minor bumps reset patch to zero.
Dates, index entries, dependencies, examples, and affected adoption notes MUST be
reviewed together. Unchanged dependents do not need cosmetic bumps.

Before changing a standard, maintainers MUST inspect its dependents and either
update them after compatibility review or explicitly retain their older
constraints. The published current set MUST have a conflict-free dependency
selection; deliberately retained older versions require identifiable source refs.
No dependency constraint means “or newer” unless it explicitly says so.

## Version specs and resolutions

Subject repos and standard dependencies SHOULD use caret specs such as `^5.0.0`.
Exact versions MAY be used when tighter control is desired. These are version
constraints, not Git refs. This repo supports stable `X.Y.Z` and `^X.Y.Z` specs,
with no leading zeroes. Prereleases, build metadata, wildcards, comparator sets,
and other range syntax are not currently supported.

Caret semantics follow [node-semver](https://github.com/npm/node-semver#caret-ranges-123-025-004):

| Spec | Accepted stable versions |
| --- | --- |
| `^5.1.2` | `>=5.1.2` and `<6.0.0` |
| `^0.2.3` | `>=0.2.3` and `<0.3.0` |
| `^0.0.3` | `>=0.0.3` and `<0.0.4` |

A resolution selects one exact version per standard ID that satisfies the subject
repo's specs and all transitive dependency specs simultaneously. Different Git
refs MAY supply different standards. If no such selection exists, readers MUST
report the conflict rather than guess compatibility or silently waive a
constraint. Searching history or widening the requested specs requires an
explicit, reviewable selection, not an implicit substitution.

A newer version matching a range is a candidate for assessment, not permission
to change code or adoption records. Agents MUST consult the user before changing
the resolved selection or remediating compliance gaps outside an approved scope.

## Legacy migration

The first SemVer releases are BAS-001 `5.0.0`, BAS-002 `3.0.0`, and CAS-001
`4.0.0`. They replace legacy BAS-001 version 4, BAS-002 version 2, and CAS-001
version 3 respectively. The major boundaries flag changed dependency and adoption
contracts; these releases are not aliases for the legacy versions.

Legacy integer versions remain exact identifiers at their historical refs. They
MUST NOT be reinterpreted as SemVer or expanded to ranges. See the normative
[BAS-002 transition procedure](../bas-002-recording-standards-adoption.md#transition-from-legacy-adoption-records)
for consumer migration.
