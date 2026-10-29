# CAS-001: Container application repositories

Version 1 — October 29, 2026. This is the default convention for applications
shipped as one or more container images and deployed with Docker Compose or
Kubernetes. Keep the implementation small; record deliberate exceptions in the
application's deployment notes.

## Platform default

Target **Linux on amd64 (x86-64)** by default: container images, Docker hosts,
Kubernetes worker nodes, and any self-managed control-plane nodes. Assume no other
OS or architecture support unless a project explicitly needs it. Multi-architecture
builds, emulation, and portability work are optional project decisions, not baseline
requirements. Image builds and deployment records should consistently target
`linux/amd64`; document deliberate exceptions.

## Repository layout

For a single component:

```text
app/                         Application source (or the language's usual src/)
tests/                       Automated tests
container/                   Dockerfile, entrypoint, image process configuration
deploy/compose/compose.yaml   Compose deployment
deploy/kubernetes/           Kubernetes manifests and kustomization.yaml, when used
examples/                    Synthetic configuration and example templates
docs/deployment.md           Application-specific operating instructions
.github/workflows/           CI checks
README.md                    Purpose, quick start, standard reference
```

Keep language dependency manifests, lockfiles, and `.dockerignore` at the repo
root. Build from that root, for example:
`docker build -f container/Dockerfile .`. Keep the build context restricted and
exclude credentials, local inventories, generated output, and development state.
Adjust Dockerfile COPY paths when moving image files.

When there are independently built components, use
`services/<component>/{src,tests,Dockerfile}` (or the component's native language
layout), with component-specific dependencies and lockfiles unless a shared
workspace is intentional. Keep orchestration under the common `deploy/` tree.
Do not split a small application merely to satisfy this layout.

## Image and deployment contract

Build an environment-neutral image. Supply hostnames, inventories, configuration,
and credentials at deployment time. Promote the same image between environments
and deployment targets. Production deployment records should identify the image
by digest, or an immutable release tag with its resolved digest recorded.

Keep actual site configuration and secrets out of public source. Use private
configuration storage, a private deployment repo, or a secret manager. ConfigMaps
are for non-sensitive data; Kubernetes Secrets still require appropriate RBAC,
storage encryption, and backup handling. Base64 is not encryption. Examples must
contain synthetic identities only.

Use the application's native configuration interface where practical: mounted
configuration files, environment variables, or supported configuration APIs. On
Kubernetes, use ConfigMaps and Secrets where they earn their operational complexity;
on Compose, bind mounts, environment files, and secrets are reasonable equivalents.
Do not introduce templating, a custom configuration controller, or generated files
merely because an application has one replica. Choose the simplest approach that
keeps configuration reviewable and credentials appropriately protected.

Mount file-based configuration inputs read-only where possible. Run the final long-lived process in the
foreground, with the entrypoint using `exec`, so shutdown signals reach it. Log
operational events without credentials or rendered secret-bearing documents.
Document writable paths, dependencies, listener ports, and who terminates TLS.

## Single-replica applications

One replica is a reasonable simple deployment choice, independent of how the
application consumes configuration. Use native ConfigMap/Secret injection or the
application's existing configuration mechanism when it fits. Choose restart or a
supported reload deliberately, and document how changes become active and how
readiness confirms successful initialization.

When overlapping instances are undesirable, use a Kubernetes Deployment with
`replicas: 1`, no autoscaling, and strategy `Recreate`; do not use a rolling surge
that briefly creates a second writer. Avoid manually deleting pods during an
update. These settings control normal managed rollouts; they are not distributed
fencing against every failure or external scaling action. Compose should likewise
have one service instance. Accept and document the brief outage while it restarts.
If overlap is harmless and availability warrants another update strategy, record
that choice instead of imposing Recreate solely because replicas is set to one.

Persist genuinely durable application data separately and document backups and
recovery. Do not classify databases or irreplaceable state as disposable output.
Scaling requires a separate concurrency and ownership design where state is shared.

### Optional pattern: render files at startup

Some applications, such as Asterisk or a provisioning file server, benefit from
assembling native configuration from structured inputs, templates, and secrets.
For those applications, this is a reasonable lifecycle:

1. The operator selects a coherent source revision and image version.
2. Startup validates all required inputs and renders generated files locally.
3. The server starts only after rendering succeeds. Startup failure is nonzero;
   readiness must not report success before successful initialization.
4. Source changes take effect through an explicit recreate/restart, unless the
   application has a deliberately supported and verified reload workflow.

Use ephemeral local output when it can be reproduced entirely from inputs:
Compose tmpfs/container-local storage or Kubernetes emptyDir. Treat generated
files as secret-bearing if their inputs contain secrets. The authoritative data
is the source snapshot, not the running container or its generated files. A PVC
is not automatically needed for disposable generated configuration. Rendering is
an application-specific choice; it does not replace ConfigMaps or Secrets, which
can still supply the renderer's inputs.

## Updating and recovering

Each application's `docs/deployment.md` should provide copyable commands for:

- Building or selecting an image and validating configuration before stopping
  the current instance. Validation must use the intended image and inputs, with
  temporary output where applicable and no mutations to the active instance.
- Updating configuration and secrets as one coherent release. Prefer immutable,
  versioned configuration objects or a private Kustomize overlay with generated
  names; retain the previous source revision and its image reference for rollback.
- Applying the deployment and activating changes through a restart or a supported
  reload. For restart-based Compose deployments, use `up -d --force-recreate`
  (and `--wait` where supported). For Kubernetes, apply a changed pod template,
  or apply updated sources and use `rollout restart deployment/<name>`, then
  `rollout status`. Reload-based workflows must document validation, activation,
  and failure handling rather than assume a mounted file change is sufficient.
- Verifying readiness and a representative application operation without printing
  secrets, and checking that the requested source/image revision is active.
- Rolling back to the previous image **and source snapshot**, activating them by
  the chosen restart/reload mechanism, and verifying again. A Deployment rollback does not undo mutations to a shared
  Secret or ConfigMap. A Compose restart does not undo source edits.

Compose paths are relative to the Compose project's base directory, normally the
first Compose file's directory. If it lives under `deploy/compose/`, make build
contexts and mounts explicitly relative to that location. Give the project a
stable name so moving the file does not accidentally select a different stack.
Document an explicit `docker compose -f deploy/compose/compose.yaml ...` invocation.

Kubernetes source-volume updates can propagate while a pod is running, but an
application that reads configuration only at startup still requires a restart.
Do not assume that applying a Secret/ConfigMap triggers a restart or an application
reload; document the actual activation mechanism. Avoid concurrent operators and
keep each startup's input snapshot coherent. Plain manifests with Kustomize are
a good default; use Helm when configurable distribution warrants it. Keep ingress,
TLS certificates, namespaces, registry credentials, and site-specific policies in
private overlays where appropriate.

Configuration-dependent maintenance, such as downloading certificate inventories,
should be explicit and separate from normal serving startup. Retain provenance,
validate the downloaded material, and promote a reviewed snapshot. Serving should
not require Internet access merely to restart from existing inputs.

## Implementation choices: keep it simple

Choose the language and approach per application. Let the standard library,
package ecosystem, and existing software guide the choice; use the option that
solves the problem clearly with the least machinery. These are preferences, not
requirements to rewrite a working application:

- **Python:** a good default for small services, automation, and glue. Keep the
  uv and dependency-management conventions below.
- **Node.js with TypeScript:** a preferred option for web applications. Use Biome
  for linting/formatting and Vitest for tests, with type checking as a separate
  check where appropriate. Commit the chosen package manager's lockfile and use
  its locked installation mode in CI.
- **Go:** the usual starting point for system-oriented services, infrastructure
  tools, and similar programs. Prefer its standard tooling and libraries where
  they fit; commit module dependency records.

Before writing custom software or assembling an image, ask whether a good,
simple, efficient Docker Official Image or vendor-maintained official image on
Docker Hub already does the job. Check the publisher, maintenance, Linux/amd64
support, configuration interface, and operating footprint. Prefer using a suitable
image directly when that is the simplest solution; pin the deployed image as
specified above. A search result or an image name alone does not establish that
an image is official or suitable.

Under KISS, a small Dockerfile around an off-the-shelf tool, plus a few helper
scripts if useful, is a valid complete application. Do not introduce a framework,
custom server, or extra service just to make the project look like an application.
Keep wrappers small and focused on configuration, lifecycle, and integration.

## Development and CI

Use the language's established tooling and commit its reproducibility lockfile.
For Python, prefer uv, `pyproject.toml`, and `uv.lock`; separate development tools
from runtime dependencies and use locked synchronization in CI. Development tools
must not enter runtime images unless required there.

Run tests and language-appropriate lint/format checks in CI. Shell scripts use
ShellCheck. Grant workflows minimal permissions. Image build/publish steps are
an explicit project decision; adopting this standard does not add them or grant
permission to publish. Likewise, local changes and commits do not authorize a
push or deployment.

## Referencing this standard

Application README files should name **CAS-001 version 1**, record the standards
commit they follow, and link to this file. With sibling local checkouts, the link
from a repo-root README is `../standards/container-applications.md`. Replace or
supplement it with the standards repository's canonical URL once one exists.
Do not copy this document into every application. Keep only the application's
specific commands, settings, tradeoffs, and exceptions in its own deployment notes.
