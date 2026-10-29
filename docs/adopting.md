# Adopting dev-standards

Read this guide and the [README front matter](../README.md) at the current HEAD
of the standards repo's `main` branch. Repository terms and requirement keywords
follow the README conventions. The index identifies candidate standards; the
subject repo's adoption records identify the version specs and resolutions
already applied.
Humans can use the steps as a checklist, agreeing on changes with the project
owner through the subject repo's normal review process.

## 1. Establish the existing development rules

Before making changes, read the subject repo's README, applicable `AGENTS.md`
files, contributor guidance, and relevant user instructions. Inspect the working
tree and preserve unrelated work. Establish the existing norms for commits,
branches, worktrees, tests, and review, including whether automatic commits are
allowed. Ask about consequential unresolved choices rather than inventing a new
workflow.

Adoption does not change authorization for commits, branches, worktrees, pushes,
publication, deployment, visibility changes, or history rewrites. Agents MUST
follow user instructions and the subject repo's pre-adoption development norms,
and MUST preserve unrelated work. Consultation for compliance changes follows
BAS-002; a standards reference is not permission to change development practices.

## 2. Select the applicable standards

Use the current [README index](../README.md) to identify standards that fit the
subject repo's actual scope. Read existing adoption records under
[BAS-002](../bas-002-recording-standards-adoption.md) before proposing changes.

For each selected standard, identify its adopted or proposed version spec and
exact resolution under the [versioning policy](versioning.md). Read that version
at its source ref and follow all transitive dependency specs. Select one version
per standard ID satisfying every applicable constraint. Different standards may
come from different refs; do not substitute the latest matching version for a
recorded resolution. Resolve each ref to a commit for the assessment. Explain
specialized selections and report dependency conflicts before implementation.
For existing integer-version records, follow
[BAS-002's transition procedure](../bas-002-recording-standards-adoption.md#transition-from-legacy-adoption-records).

## 3. Assess the gaps

Compare the subject repo with the selected standards. Distinguish applicable
requirements from conditional requirements, preferences, and optional patterns.
For each material gap, identify the requirement, current evidence, proposed
change or justified exception, and how the result can be verified. Mark
inapplicable conditional requirements with a reason when that helps review.

Keep the assessment proportionate to the project. Language preferences do not
require rewriting a working project. CAS-001's optional startup-rendering pattern
does not require adding a renderer. Do not add publication or deployment stages
merely to adopt the standards.

## 4. Agree on the adoption plan

Present each selected standard ID, version spec, exact resolved version, source
ref, and resolved commit, together with:

- The proposed changes and their scope.
- Justified exceptions, unresolved choices, and any work to defer.
- The validation needed to establish the result.
- The development workflow to follow, including commit, branch, worktree, and
  review expectations established before adoption.

Agents MUST obtain the user's consent to this plan before implementing it unless
the user has already explicitly approved that scope. Read-only assessment can
proceed before consent. Ask only about unresolved choices or authorization;
existing explicit consent remains valid and does not require repeated approval.

## 5. Implement and verify

Complete the agreed changes under the established development norms. Continue
routine implementation without repeated confirmation. If a material scope change,
conflict, or unresolved decision requires the user's input, explain the concrete
choice and obtain it before proceeding with the affected work.

Run checks appropriate to the changes and the selected standards. Review the
resulting diff for unintended changes and sensitive or identifying information.
Report what was verified, what could not be verified, and any remaining gaps.
Do not claim compliance based solely on adding standards references.

## 6. Record the adoption outcome

Record the outcome according to
[BAS-002: Recording standards adoption](../bas-002-recording-standards-adoption.md)
at its adopted or agreed source ref. Record verification results in the project's
usual review or change record.

For a later per-standard upgrade, use this same workflow to assess the changes,
agree on scope, implement, verify, and update the adoption record.
