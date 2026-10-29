# Project standards

A small index of reusable defaults. Start with the foundation, then apply the
specialized standards that fit the project.

| Standard | When to apply it |
| --- | --- |
| [BAS-001 v1: Repository and development fundamentals](fundamentals.md) | Every project. Public GitHub source under `bchociej`, privacy boundaries, language/tooling choices, and GitHub Actions checks. |
| [CAS-001 v1: Container application repositories](container-applications.md) | When shipping one or more container images for Compose or Kubernetes. Adds Linux/amd64 defaults, repo layout, configuration, updates, and recovery; inherits BAS-001. |

Projects reference applicable standard IDs, versions, and the standards Git
revision rather than copying the text. Keep project-specific commands and justified
exceptions in the project's own documentation.

Maintain this index whenever a standard is added, renamed, or retired. Give each
entry a link and a short explanation of when it applies; do not make readers open
every standard to discover its scope.
