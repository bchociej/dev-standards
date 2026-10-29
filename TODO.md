# Future work

- [ ] After the SemVer releases are committed and published, migrate this repo's
  legacy BAS-001 v4 / BAS-002 v2 adoption records using BAS-002's transition
  procedure. Prefer `^5.0.0` / `^3.0.0`, recording exact resolutions and immutable
  source commits. Do not invent a commit hash for uncommitted content.
- [ ] Verify the expanded documentation and version-constraint checks in GitHub
  Actions after an authorized push, and record any lasting limitations.
- [ ] Consider a small release catalog mapping standard IDs and exact versions to
  immutable refs if history lookup becomes cumbersome. Keep publication deliberate.
- [ ] Consider broader range syntax or prereleases only if a concrete consumer
  needs them; stable exact and caret specs suffice for now.
- [ ] Consider automated comparison of changed requirements to suggest version
  bump levels. Keep human/agent semantic review mandatory: checks can validate
  syntax, immutability, and selected dependency graphs, not prove compatibility.
