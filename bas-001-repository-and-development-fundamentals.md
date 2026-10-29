# BAS-001: Repository and development fundamentals

Version 5.0.0 — October 29, 2026. Applies to all subject repos, whether or not they
use containers. Terms and requirement keywords follow the
[README conventions](README.md#how-to-read-this-repository) at this source ref.
More specific standards build on this one; they do not silently override it.

## Personalization assumptions

This standard presumes the user is **Ben Chociej (GitHub: `bchociej`)**. This name
and account are intentionally public identifiers authorized for inclusion here.
That authorization does not extend to other personal or deployment information.

For another user, personalizable assumptions such as the GitHub namespace and
any assumptions about internal network topology SHOULD be scrutinized, discussed
with that user, and forked or customized to suit them. The source-safety requirements
below still apply.

## Hosting and visibility

Source control SHOULD be hosted on **GitHub under `bchociej`**, with CI on
**GitHub Actions**. Repositories SHOULD be **public**. Departures require a strong,
specific reason; convenience or hypothetical future sensitivity is insufficient.
These recommendations guide setup; they do not authorize publishing an existing
private repository, pushing, or deploying without user instruction.

## Keep source safe to publish

Subject repos MUST keep secrets and identifying personal or deployment information
out of SCM, including source, documentation, fixtures, generated files, and commit
history. Contributors MUST apply the same protection to issues, pull requests,
CI logs, and uploaded artifacts:

- Passwords, tokens, private keys, cookies, and real credentials MUST NOT be
  committed. Encoding them, ignoring another copy, or later deleting them from
  the working tree does not make committed secrets safe.
- The owner's LAN, VPN sites, actual addressing, private hostnames, topology,
  deployment inventory, and particular owned-device identifiers such as MAC
  addresses or serial numbers MUST NOT be recorded. Personal filesystem paths
  and private chat links MUST NOT be committed. Actual site configuration MUST
  remain outside SCM and be injected through local files, stores, or tooling.
- Model numbers, hardware families, firmware versions, protocols, and other
  non-identifying target specifications MAY be documented.
- Examples and test fixtures MUST use synthetic identities and credentials.
  Material derived from real exports, screenshots, and logs MUST be reviewed
  and sanitized before inclusion.

Subject repos MUST set appropriate `.gitignore` rules before adding local
configuration, secrets, outputs, or tooling state. Ignore rules do not protect
tracked files or erase history. Contributors MUST review staged changes and
relevant history before publishing. A public-safe author identity SHOULD be used
when a personal email should not be exposed. Private visibility does not relax
these requirements.

## Development and CI

Projects SHOULD prefer existing software and a small amount of integration over
custom machinery. Language choices below are recommendations for new work, not
requirements to rewrite working projects. Retaining suitable alternative tooling
requires a documented reason rather than an automatic migration.

- **Python** SHOULD be considered for small services, automation, and glue.
  Python projects SHOULD use uv, `pyproject.toml`, and `uv.lock`.
- **Node.js with TypeScript** SHOULD be considered for web applications.
  TypeScript projects SHOULD use Biome for linting/formatting and Vitest for tests,
  with a separate type check where useful.
- **Go** SHOULD be considered for system-oriented services and infrastructure
  tools. Its standard tooling and libraries SHOULD be preferred where they fit.

Projects MUST commit reproducible dependency records, such as lockfiles or Go
module records, and MUST use locked dependency installation or synchronization
in CI where supported. Runtime requirements SHOULD be kept separate from
development tools, and runtime artifacts SHOULD contain only runtime needs.

Projects MUST run meaningful checks in CI: tests and language-appropriate
lint/format checks where applicable. Documentation-only repos MAY use document
and link checks without artificial application tests. Shell scripts SHOULD be
checked with ShellCheck. Workflows MUST use minimal permissions and MUST NOT
expose secrets in their output.

Build, artifact publication, and deployment stages are explicit project decisions;
adoption does not add them automatically. Local edits and commits do not by
themselves authorize a push, publication, or deployment.

## Adoption records

Subject repos MUST also apply **BAS-002 version ^3.0.0**:
[Recording standards adoption](bas-002-recording-standards-adoption.md), using
the source ref recorded for that dependency.
