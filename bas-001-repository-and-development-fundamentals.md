# BAS-001: Repository and development fundamentals

Version 1 — October 29, 2026. These defaults apply to all projects, whether or not
they use containers. More specific standards build on this one; they do not
silently override it. Record deliberate exceptions and their concrete reason in
the project's documentation, without disclosing the information being protected.

## Hosting and visibility

Presumptively host source control on **GitHub under `bchociej`**, with CI on
**GitHub Actions**. Repositories are **public by default**. Choose private visibility
or different hosting only for a strong, specific, compelling reason; convenience
or hypothetical future sensitivity is not enough. This default guides project
setup; it does not authorize publishing an existing private repository, pushing,
or deploying without the applicable user instruction.

## Keep source safe to publish

Keep sensitive and personal information out of SCM: source, documentation,
examples, fixtures, generated files, and commit history. The same care applies
to repository issues, pull requests, CI logs, and uploaded artifacts.

- Never commit passwords, API tokens, private keys, session cookies, or real
  service credentials. Base64, an ignored copy elsewhere, or later deletion from
  the working tree does not make a committed secret safe.
- Do not describe the owner's LAN, VPN sites, actual addressing, private hostnames,
  topology, or deployment inventory. Do not commit identifiers of particular owned
  devices, such as MAC addresses or serial numbers, or personal filesystem paths
  and private chat links. Keep actual site configuration outside SCM; inject it
  through local files, configuration/secret stores, or deployment tooling.
- **Model numbers, supported hardware families, firmware versions, protocols, and
  other non-identifying target specifications are appropriate.** They explain
  what the project supports without documenting a particular owned device.
- Use clearly synthetic examples and test fixtures. Sanitize real exports and
  reports before deriving public documentation; copying them wholesale is not a
  substitute for review. Check screenshots and logs for incidental disclosures.

Set appropriate `.gitignore` rules before adding local configuration, secrets,
outputs, or tooling state. Review the staged diff and relevant history before
publishing. Ignore rules neither protect tracked files nor erase history. Use a
public-safe author identity, such as the account's GitHub noreply email, when a
personal email address should not be exposed. Private visibility is not a reason
to put secrets or personal deployment details into application SCM.

## Development and CI

Keep it simple. Let the standard library, package ecosystem, and existing tools
guide the implementation per application. Prefer a small amount of integration
around suitable existing software over custom machinery. These preferences do
not require rewriting a working project:

- **Python:** a good default for small services, automation, and glue. Use uv,
  `pyproject.toml`, and `uv.lock`; separate development and runtime dependencies
  and use locked synchronization in CI.
- **Node.js with TypeScript:** a preferred option for web applications. Use Biome
  for linting/formatting, Vitest for tests, and a separate type check where useful.
  Commit the chosen package manager's lockfile and use locked installs in CI.
- **Go:** the usual starting point for system-oriented services and infrastructure
  tools. Prefer its standard tooling and libraries where they fit; commit module
  dependency records.

Use established language tooling and reproducible dependency records. Keep
runtime requirements separate from development tools; ship only what the runtime
needs. Run meaningful tests and language-appropriate lint/format checks in GitHub
Actions. Shell scripts use ShellCheck. Grant workflows minimal permissions and
keep secrets out of their output.

Build, artifact publication, and deployment stages are explicit project decisions;
adopting this standard does not add them automatically. Local edits and commits
do not by themselves authorize a push, publication, or deployment.

## Referencing standards

A project's README should name the applicable standard IDs and versions, link to
them, and record the standards Git revision it follows. **BAS-001 version 1** is
the foundation; add specialized standards such as CAS-001 only when applicable.
Follow a specialized standard's explicit foundation reference rather than copying
its inherited requirements into every project.

With sibling local checkouts, the README link to this document is
`../standards/bas-001-repository-and-development-fundamentals.md`. Use `../standards/cas-001-container-application-repositories.md` for
CAS-001. Replace or supplement local links with canonical repository URLs once
hosting is configured. Do not guess or imply a published location that does not
exist yet. Record a newer standards commit when adopting changes; a reference is
not a request to silently rewrite existing projects whenever a standard changes.

Do not copy standards into each repository. Keep only project-specific commands,
choices, and justified exceptions there. If a specialized standard conflicts with
this foundation, resolve and document the exception explicitly.
