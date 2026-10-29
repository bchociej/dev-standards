# Project standards

A small index of reusable defaults. Start with the foundation, then apply the
specialized standards that fit the project.

| Standard number | Version | Date | Name | Application note |
| --- | --- | --- | --- | --- |
| BAS-001 | 1 | 2026-10-29 | [Repository and development fundamentals](bas-001-repository-and-development-fundamentals.md) | Every project: hosting, public-source privacy, language/tooling choices, and CI. |
| CAS-001 | 1 | 2026-10-29 | [Container application repositories](cas-001-container-application-repositories.md) | Container images for Compose or Kubernetes; inherits BAS-001. |

Projects reference applicable standard IDs, versions, and the standards Git
revision rather than copying the text. Keep project-specific commands and justified
exceptions in the project's own documentation.

Maintain this index whenever a standard is added, revised, renamed, or retired.
Each row records the standard number, version, date, linked name, and application
note. Readers should not have to open every standard to discover its scope.

Name standard files with the lowercase standard number, a dash, and the lowercase
hyphen-separated name, followed by `.md`, for example
`bas-001-repository-and-development-fundamentals.md`.
