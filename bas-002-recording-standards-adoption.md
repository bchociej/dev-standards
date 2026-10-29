# BAS-002: Recording standards adoption

Version 3.0.0 — October 29, 2026. Applies to every subject repo adopting standards
from the standards repo. Terms and requirement keywords follow the
[README conventions](README.md#how-to-read-this-repository) at this source ref.

## Per-standard README records

The subject repo's `README.md` MUST record each applied standard separately,
including required dependencies. Each entry MUST identify:

- The standard ID and adopted version spec. Subject repos SHOULD use a caret
  spec such as `^5.0.0`; an exact SemVer version MAY be used instead.
- The exact resolved version satisfying that spec and all dependency constraints.
- A source ref in the standards repo at which the resolved version can be found,
  and a link or repository location and path sufficient to retrieve it.
- Adoption status and any exceptions or remaining gaps, directly or by a link
  to supporting notes.

The subject repo MAY use different source refs for different standards. It MUST
satisfy each adopted standard's dependency specs using one resolved version per
standard ID. Conflicts MUST be resolved explicitly rather than silently
substituted. Specs and caret bounds follow the
[versioning policy](docs/versioning.md) at this source ref.

A source ref MAY be static or dynamic. Before relying on a dynamic ref, readers
MUST resolve it and verify that it still contains the recorded resolved version.
If it no longer does, they MUST report the mismatch and MUST NOT silently change
the resolved version. A static ref is usually easier to reproduce.

There is no repository-wide dev-standards target ref. Current front matter at
`main` supports discovery and process; it does not replace these adoption records.
Links MUST identify real locations; unpublished canonical URLs MUST NOT be invented.

For example, a subject README could contain this illustrative record (replace
all placeholders with real values):

```markdown
## Applied standards

Standards repo: <repository URL or local checkout location>

| Standard | Version spec | Resolved version | Source ref and path | Status |
| --- | --- | --- | --- | --- |
| BAS-001 | ^5.0.0 | 5.0.0 | <ref>:bas-001-repository-and-development-fundamentals.md | Adopted |
| BAS-002 | ^3.0.0 | 3.0.0 | <ref>:bas-002-recording-standards-adoption.md | Adopted |

Exceptions and verification limitations: <none, or link to supporting notes>.
```

## Supporting notes and verification

The subject repo SHOULD keep substantive adoption notes in `docs/standards.md`,
linked from its README. Each exception MUST identify the requirement and concrete
reason without disclosing protected information. Remaining gaps and lasting
verification limitations MUST be recorded. Incomplete adoption MUST be labeled
**adoption in progress**; references alone are not evidence of compliance.

Assessment results MUST identify the resolved commit for each source ref so the
requirements evaluated remain reproducible. Results MAY live in the usual review
or change record, with lasting limitations linked from the README. Compliance
with documented exceptions MUST be distinguished from unqualified compliance.

Subject repos SHOULD reference standards rather than copy their text or maintain
an exhaustive duplicate requirements checklist. Project-specific commands and
choices belong in subject repo documentation.

## Changes and agent consent

Agents MUST consult the user before changing the subject repo to meet adopted
standards or to adopt other versions, including when a source ref advances or an
existing gap is discovered. Neither an adoption record nor new front matter
authorizes autonomous remediation. Existing user approval for a concrete scope
remains valid; work beyond that scope MUST receive further consent.

Adoption records MUST be updated when agreed changes alter the adopted versions,
source refs, status, or exceptions. New standards repo commits do not themselves
change the subject repo's adopted versions.

## Transition from legacy adoption records

A subject repo with legacy integer versions or exact-only records MUST preserve
their meaning until a deliberate migration is approved. Adding `.0.0` to a legacy
integer is not a version conversion. Existing source refs remain evidence of the
old requirements; migration MUST NOT rewrite those historical standards.

1. Read current `main` front matter and inventory the subject repo's existing
   standard IDs, exact versions, source refs, exceptions, and verification.
2. Identify candidate SemVer releases and read their changes, especially across
   major boundaries. The [versioning policy](docs/versioning.md#legacy-migration)
   names the initial releases; it does not assert equivalent obligations.
3. Propose a spec for each standard, preferably `^X.Y.Z`, and choose exact
   resolutions with source refs. Check the complete transitive dependency set;
   agents MUST report conflicts before implementation.
4. Assess requirement gaps and present the changes, exceptions, and validation.
   Agents MUST obtain consent before changing the subject repo or its adoption
   records unless that concrete scope is already approved.
5. Implement and verify the agreed scope, then replace the old README entries
   with spec, resolved version, source ref, and status. Record resolved commits
   and preserve still-relevant exceptions and limitations in the adoption notes.

A range does not prove compliance with every matching future release. Existing
assessment results apply to the recorded resolution. Later matching releases
require review and consultation before agents update that resolution or change
the subject repo. If migration is deferred, the old records remain valid under
their original standards; they MUST NOT be presented as migrated SemVer records.
