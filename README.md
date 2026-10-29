# Project standards

A small index of reusable defaults. Start with the foundation, then apply the
specialized standards that fit the project.

## How to read this repository

The **standards repo** is this dev-standards repository. The **subject repo** is
the repository being assessed or changed. These terms apply throughout the
standards repo.

Readers MUST start with this README and the linked adoption guide at the current
HEAD of the standards repo's `main` branch. This is the **front matter**: current
discovery and process guidance. Reading it does not upgrade a subject repo's
adopted standards. Individual standard versions and their source refs are
recorded separately under BAS-002. If current `main` cannot be accessed, readers
MUST disclose that limitation rather than present a cached copy as current.

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY have the meanings in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119), as clarified by
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174), only when capitalized:

| Keyword | Meaning |
| --- | --- |
| MUST / MUST NOT | A requirement / prohibition. |
| SHOULD / SHOULD NOT | A recommendation / discouraged practice; departing requires understanding and weighing the consequences. |
| MAY | An option; omission is not a compliance gap. |

Lowercase prose explains requirements, examples, and rationale; it does not add
unmarked normative obligations. Each standard links to this convention at its
source revision. Subject repos MUST document departures from SHOULD or SHOULD NOT provisions
with reasons. A departure from MUST is an explicit exception, not satisfaction
of that requirement; compliance claims MUST disclose such exceptions.

## Standards index

| Standard number | Version | Date | Name | Application note |
| --- | --- | --- | --- | --- |
| BAS-001 | 4 | 2026-10-29 | [Repository and development fundamentals](bas-001-repository-and-development-fundamentals.md) | Every project: hosting, public-source privacy, language/tooling choices, and CI. |
| BAS-002 | 2 | 2026-10-29 | [Recording standards adoption](bas-002-recording-standards-adoption.md) | Every repository adopting dev-standards: per-standard README adoption records and exceptions. |
| CAS-001 | 3 | 2026-10-29 | [Container application repositories](cas-001-container-application-repositories.md) | Container images for Compose or Kubernetes; inherits BAS-001. |

See BAS-002 for how projects record their adoption of dev-standards.

## This repository's adoption

This repository is both the subject repo and the standards repo. Standards
source: [bchociej/dev-standards](https://github.com/bchociej/dev-standards).

| Standard | Version | Source ref | Status |
| --- | --- | --- | --- |
| BAS-001 | 4 | [`7a58229755dadb9a0c77d72bfe976030ce82d076`](https://github.com/bchociej/dev-standards/blob/7a58229755dadb9a0c77d72bfe976030ce82d076/bas-001-repository-and-development-fundamentals.md) | Adopted with the tooling departure below |
| BAS-002 | 2 | [`7a58229755dadb9a0c77d72bfe976030ce82d076`](https://github.com/bchociej/dev-standards/blob/7a58229755dadb9a0c77d72bfe976030ce82d076/bas-002-recording-standards-adoption.md) | Adopted |

See [adoption notes](docs/standards.md) for scope, the justified Python-tooling
departure, verification, and limitations. CAS-001 does not apply.

Run local checks with `python3 scripts/check_docs.py` and `git diff --check`.

## Adopting these standards

Agents receiving a terse instruction such as `adopt ~/code/dev-standards`
SHOULD treat the named path as the standards repo, the repository being worked
on as the subject repo, and follow this section. The instruction starts the
adoption workflow; it does not by itself approve an implementation plan or
change the subject repo's existing development norms.

Follow the [adoption guide](docs/adopting.md) to select applicable standards,
assess gaps, agree on changes, and verify adoption. Humans can use it as a
checklist; agents must preserve the project's existing development norms and
obtain consent to the adoption plan before implementing it, unless that scope
has already been approved.

To ask an agent to start:

> Assess the subject repo for adoption of standards from the standards repo,
> dev-standards. First read the standards repo's README and adoption guide at the
> current HEAD of main. Inspect the subject repo's instructions, development
> norms, and existing per-standard adoption records. Propose applicable standard
> versions and source refs, gaps, exceptions, changes, validation, and the Git
> workflow. Obtain my consent before implementing the plan unless I have already
> approved that scope. Then complete, verify, and record the agreed adoption.

## Maintaining this index

Maintain this index whenever a standard is added, revised, renamed, or retired.
Each row records the standard number, version, date, linked name, and application
note. Readers should not have to open every standard to discover its scope.

Name standard files with the lowercase standard number, a dash, and the lowercase
hyphen-separated name, followed by `.md`, for example
`bas-001-repository-and-development-fundamentals.md`.

A standard's version MUST increase when its normative requirements, scope, or
required dependency versions change. Editorial clarifications MAY retain the
version if they do not change obligations. The index and standard header MUST
agree on version and date. Dependent standards MUST be reviewed when a dependency
changes; their declared version requirements change only deliberately.

A standard ID MUST NOT be reused for a different purpose. Retired standards MUST
remain discoverable in Git history; the index MUST identify retirement and any
replacement. Older adopted versions remain available through their recorded refs.
