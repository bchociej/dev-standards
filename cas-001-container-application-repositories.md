# CAS-001: Container application repositories

Version 3 — October 29, 2026. Applies to subject repos shipping one or more
container images for Docker Compose or Kubernetes. Terms and requirement keywords
follow the [README conventions](README.md#how-to-read-this-repository) at this
source ref.

Subject repos MUST also apply **BAS-001 version 3**:
[Repository and development fundamentals](bas-001-repository-and-development-fundamentals.md).
Its requirements take precedence; its source ref is recorded separately.

## Platform and repository layout

Images and deployment hosts SHOULD target **Linux on amd64 (x86-64)**. Other
platforms and multi-architecture builds MAY be supported when the project needs
them; they are not baseline requirements.

For a single component, subject repos SHOULD use this layout, including only
files needed for their supported build and deployment targets:

```text
app/                         Application source (or the language's usual src/)
tests/                       Automated tests, when applicable
container/                   Dockerfile and image process configuration, if built
deploy/compose/compose.yaml  Compose deployment, when supported
deploy/kubernetes/          Kubernetes manifests and kustomization.yaml, when supported
examples/                    Synthetic configuration and example templates
docs/deployment.md          Application-specific operating instructions
.github/workflows/           CI checks
README.md                    Purpose, quick start, adoption records
```

For a single component, dependency manifests, lockfiles, and `.dockerignore`
SHOULD live at the repo root. An amd64 image build from that root is:
`docker build --platform linux/amd64 -f container/Dockerfile .`.
Subject repos using existing images directly MAY omit a Dockerfile and build
instructions. Build contexts MUST exclude credentials and identifying site data;
they SHOULD also exclude generated output and development state.

Independently built components SHOULD use
`services/<component>/{src,tests,Dockerfile}` or the language's native layout,
with component-specific dependencies and lockfiles unless a shared workspace is
intentional. Orchestration SHOULD remain under the common `deploy/` tree. Small
applications SHOULD NOT be split merely to satisfy a layout convention.

## Image and configuration contract

Images MUST be environment-neutral: actual hostnames, inventories, configuration,
and credentials are supplied at deployment time under BAS-001's privacy rules.
The same image SHOULD be promoted between environments and targets. Production
deployment records MUST identify the image by digest, or by an immutable release
tag with its resolved digest recorded.

Applications SHOULD use their native configuration interface: mounted files,
environment variables, or supported APIs. ConfigMaps and Secrets on Kubernetes,
and bind mounts, environment files, and secrets on Compose, are available
mechanisms; custom controllers and templating SHOULD NOT be introduced without
an application need. ConfigMaps MUST NOT contain sensitive data. Kubernetes
Secrets MUST have appropriate RBAC, storage encryption, and backup handling;
Base64 is not encryption. Actual site inputs remain outside SCM, including when
stored in a separate deployment repository.

File-based configuration inputs SHOULD be mounted read-only. The final
long-lived process MUST run in the foreground and receive shutdown signals;
a shell entrypoint MUST use `exec` when handing control to that process.
Logs MUST NOT expose credentials or rendered secret-bearing documents.
Deployment notes MUST identify writable paths, dependencies, listener ports,
and who terminates TLS.

## Single-replica applications

One replica MAY be used as a simple deployment choice. The deployment MUST
specify how configuration changes become active, through restart or a supported
reload, and how readiness confirms successful initialization.

When overlapping instances are undesirable, Kubernetes deployments MUST use
`replicas: 1`, no autoscaling, and strategy `Recreate`; Compose deployments MUST
likewise use one service instance. Normal updates SHOULD use the deployment
mechanism rather than manually deleting pods. These settings prevent normal
managed rollout overlap, not every failure or external scaling action; they are
not distributed fencing. The brief restart outage MUST be documented. If overlap
is harmless, another update strategy MAY be chosen without a Recreate exception.

Durable application data MUST be persisted separately, with backup and recovery
instructions. Databases and irreplaceable state MUST NOT be treated as disposable
output. Scaling shared-state applications requires a separate concurrency and
ownership design.

### Optional pattern: render files at startup

Applications such as Asterisk or provisioning file servers MAY assemble native
configuration from structured inputs, templates, and secrets at startup. If this
pattern is used:

1. The operator selects a coherent input snapshot and image version.
2. Startup MUST validate inputs and complete rendering before starting the server.
3. Initialization failure MUST exit nonzero; readiness MUST NOT report success
   before initialization completes.
4. Changes become active through the documented restart or supported reload.

Reproducible generated output SHOULD use ephemeral local storage, such as Compose
tmpfs or Kubernetes emptyDir. A PVC is not required for disposable output.
Generated files MUST be treated as secret-bearing when their inputs contain
secrets. The input snapshot remains authoritative. ConfigMaps and Secrets can
supply renderer inputs; rendering does not replace those mechanisms.

## Updating and recovering

The subject repo's `docs/deployment.md` MUST provide copyable instructions for
its supported targets covering:

- Selecting the image and validating the intended input snapshot before stopping
  the active instance. Validation MUST use the intended image and inputs without
  mutating the active instance, using temporary output where applicable.
- Updating configuration and secrets as one coherent release. Versioned immutable
  inputs or Kustomize-generated names SHOULD be used where practical. Previous
  input snapshots and image references MUST be retained for rollback.
- Activating the release through restart or supported reload. Reload instructions
  MUST include validation, activation, and failure handling.
- Verifying readiness, a representative application operation, and the active
  input/image revision without exposing secrets.
- Rolling back both the image and input snapshot, activating them, and verifying
  again. A Deployment rollback does not undo shared Secret/ConfigMap mutations;
  a Compose restart does not restore previous source files.

For restart-based Compose releases, instructions SHOULD use
`up -d --force-recreate` and `--wait` where supported. Compose instructions MUST
include an explicit invocation such as
`docker compose -f deploy/compose/compose.yaml ...` and a stable project name.
Paths MUST account for the Compose base directory, normally the first Compose
file's directory; moving a file must not accidentally select another stack.

Kubernetes instructions MUST activate startup-only configuration through a pod
template change or an explicit `rollout restart deployment/<name>`, followed by
`rollout status`. Applying a Secret/ConfigMap alone does not establish restart or
reload. Operators MUST keep each startup's input snapshot coherent and SHOULD
avoid concurrent changes. Plain manifests with Kustomize SHOULD be the starting
point; Helm MAY be used when configurable distribution warrants it. Site-specific
ingress, TLS, namespaces, registry credentials, and policies remain outside SCM
where required by BAS-001.

Configuration-dependent maintenance, such as downloading certificate inventories,
SHOULD be explicit and separate from serving startup. Downloaded material MUST
have provenance and be validated before promotion. Serving SHOULD NOT require
Internet access merely to restart from existing inputs.

## Implementation choices

Before assembling an image or writing custom software, maintainers SHOULD assess
whether a Docker Official Image or a vendor-maintained image already meets the
need. Verify publisher, maintenance, platform support, configuration interface,
and footprint; a search result or name alone does not establish suitability.
A suitable image SHOULD be used directly when that is the simplest solution.

A small Dockerfile around an existing tool, with focused helper scripts, MAY be
a complete application. Frameworks, custom servers, and extra services SHOULD NOT
be introduced merely to make the project look like an application.
