# Cyberpunk AVP automation design

Status: written design approved October 13, 2026. Implementation-plan review and execution-method selection are the next gate. Commands and paths below describe the proposed interface, not tools that already exist.

## Outcome

A user with the supported Mac game copy can prepare, verify and sign the working native 2D Cyberpunk host through a resumable CLI, then explicitly deploy it to their own Apple Vision Pro. Success means a second developer can reproduce the accepted 2D behavior from published source and documented prerequisites without relying on the original developer's generated frameworks or local paths.

The known baseline is Mac ARM64 Cyberpunk 2.3 on M2 Vision Pro, with native 1280×720 output and confirmed movement, aiming/firing, pointer/scroll and arrow-turn input. VR research remains separately selectable and does not alter the baseline pipeline.

## Repository ownership and implementation location

Implementation belongs in the VisiRupt engine repository. The Cyberpunk companion repository owns this design, workflow, supported-build documentation and reproduction reports. Do not duplicate the engine or converters here.

Develop in an isolated engine checkout based on an explicitly recorded source revision. The active research checkout, accepted host, installed application and original game files stay outside its write boundary. Project generation, frameworks, DerivedData, logs, credentials and receipts live in a user-selected private workspace outside tracked source.

Use Python standard-library orchestration, uv for Python execution/development, existing XcodeGen/Xcode tools, and Make wrappers for common commands. A GUI installer can use the same CLI later; it is outside this first implementation. Avoid a shell-only orchestration layer because checkpoints, Mach-O validation and structured errors need shared typed data and tests.

## Proposed CLI

Entry point: `uv run --no-project python tools/visirupt.py`. Make targets invoke the same implementation. All mutating stages require an explicit private workspace; paths containing spaces work. No command defaults to deploying or launching.

| Command | Behavior | Observable completion |
| --- | --- | --- |
| `doctor` | Inspect tools, SDK, source revision, recipe and storage; identify original game when supplied | Structured prerequisite result; no purchase, build or device changes |
| `plan` | Resolve stage graph and show writes, input identities, external downloads and expected device actions | Human-readable plan plus private machine-readable plan; no build or device changes |
| `prepare` | Build authored providers/Curl and adapt private copies of exact supported game inputs | Ten prepared frameworks with passing invariant reports |
| `verify` | Revalidate inputs, prepared frameworks, dependency providers and receipt consistency | Explicit pass/fail for every gate; no inferred gameplay success |
| `build` | Generate the native host project in private workspace and build/sign with the supplied team | Verified signed app, entitlement report and preserved recipe identity |
| `transfer` | Deploy/update receiver only when explicitly requested; deliver owned assets through one selected transport | Every required file has a native whole-file completion receipt |
| `install` | Check current device/container/signing compatibility and normally install/update verified host | Completed installation receipt; asset container retained |
| `launch` | Explicitly launch the verified installed host | Launch receipt only; human/gameplay acceptance recorded separately |
| `status` | Show stages, failure reason, resume eligibility and next required action | Redacted console summary; full private receipts retained |
| `report` | Produce a privacy-filtered reproduction summary for review | Separate shareable draft; never automatically posted |

Common selectors are `--workspace`, `--game`, `--recipe`, and `--device` where applicable. Signing configuration is explicit for `build`; it is not inferred from the original developer's team. Transport selection is explicit for `transfer`. `prepare` reuses valid checkpoints automatically; rebuilding an invalid stage does not require deleting the workspace. There is no force option that bypasses identity, invariant, signing or asset checks.

The first implementation must document and ship the exact parser, option syntax and Make equivalents together; this table defines command semantics rather than fixing an unimplemented configuration-file schema.

## Versioned recipe and inputs

Initial recipe: `cyberpunk-mac-2.3-2d-v1`, targeting ARM64 VISIONOS minimum 26.0 / tested SDK 27.0. The four original binary hashes, initial-pool words, provider routes and section checks are defined in [build inputs](../../build-inputs.md), [framework preparation](../../framework-preparation.md) and [module preparation](../../game-module-preparation.md).

The recipe is a reviewed data structure shipped with the engine, not fetched from an issue, agent submission or arbitrary URL. It records recipe schema/version, supported game hashes, declared transforms, upstream source/archive identity, required exports and target/toolchain constraints. Recipe changes invalidate affected checkpoints. An unsupported binary or SDK/toolchain combination produces an explicit unsupported result, requiring a separately reviewed recipe rather than guessed offsets.

For authored frameworks, build HostAdapters, three forwarding bridges and NativeSecurity from the recorded source revision. Build MemoryTrace as part of the host. Proprietary Bink/AppStore/Galaxy/game copies come exclusively from the user's matching installation; preserve original service implementation and ownership boundaries.

The initial Curl recipe reproduces the verified 8.14.1/Secure Transport experiment. Its archival TLS limitations remain documented. Accept a locally supplied archive matching the pinned hash, or an explicitly requested official-source download with pinned hash verification. Network retrieval is shown in the plan and never substitutes a floating latest version. Upgrading Curl/backend is a separately tested recipe change, required before claiming production dependency readiness.

## Local stage graph

1. Inspect toolchain and original inputs; make immutable private snapshots and verify their identities again after copying.
2. Build HostAdapters/DisplayBridge/IOKitBridge/MetalBridge and NativeSecurity; build/package Curl.
3. Adapt Bink and service-provider copies with the declared platform/path/ordinal rules; independently verify their complete section and import invariants.
4. Convert the exact original Cyberpunk executable, apply the two declared capacity words, route providers including MemoryTrace, and independently verify the output.
5. Assemble the source-only host and all ten framework inputs in a private project tree; apply explicit signing configuration without editing checked-in specs.
6. Build MemoryTrace and the host; embed/sign, inspect entitlements and verify final app signatures and binary postconditions.

At every stage, originals remain read-only. Reject input/output overlap, path escape and unexpected symlink traversal. Validate bounded Mach-O tables and arithmetic before reading/writing; assert expected original instruction words and prove that changed payload bytes are confined to the allowed locations. Removing providers requires preserving logical imports across both binding and symbol-table representations.

The working module's 16/8/8-GiB initial pools are virtual reservations; their configuration is not a physical-memory or gameplay-capacity guarantee. Retain all original initializer data. File wrappers must map bundle Data to `Application Support/GameData/Data` with actual native errno semantics.

Generate a minimal local arrow-turn configuration change from the user's own file only after validating its expected structure. Preserve original bytes/hash in a backup, record the resulting modified hash separately, and do not redistribute the complete original XML. Its asset-transfer receipt must not misidentify the intentional changed file as an unchanged original.

## Checkpoints, interrupted work and invalidation

Each stage has states pending, running, complete or failed. A receipt records schema version, stage, recipe version, source/toolchain fingerprint, input/output hashes, verification gates and a structured failure code. Write receipts atomically only after output verification; never promote a process exit or partial output to a successful stage.

Use separate temporary output paths and atomic publication into each stage's completed artifact directory. Fingerprints include upstream source/archive identities, relevant build flags, target SDK and all dependent artifacts. Before skipping a completed stage, recheck receipt compatibility and output hashes. Any changed or missing input/output invalidates that stage and its dependents; retain earlier evidence and quarantine partial artifacts rather than silently overwriting known-good outputs.

A workspace lock prevents concurrent mutation. Transfer additionally needs an authoritative per-device/receiver-container writer lock or process ownership check so two workspaces cannot race the same checkpoints; an existing unknown writer blocks transfer. Read-only status remains available. Interruptions stop only owned child processes and preserve committed artifacts. Do not restart Apple's shared services, delete containers or kill another research session to resolve a failure.

Signing can alter whole-file bytes. Track unsigned preparation hashes and signed artifact hashes separately; reapply semantic section/import checks after signing rather than demanding identical signatures between developers. No timestamps or local identity details establish reproducibility by themselves.

## Device and asset boundary

Local preparation/build has no device side effects. `transfer`, `install` and `launch` are separate explicit commands; plan/status identify their intended device and container first. First-run pairing, Developer Mode, developer trust and signing/account setup remain human prerequisites. No purchasing, enrollment or entitlement bypass is automated.

Preserve the tested receiver/host data container and bundle identifier `local.games.cyberpunk.assetreceiver`. Before updating an existing installation, check whether the user's signing/application identity can actually retain access to its data. A differing or unverifiable ownership relationship stops the operation for a migration decision; never assume that preserving the bundle string alone preserves data. Initial receiver deployment requires an explicit action and normal installation receipt.

Integrate the existing resumable receiver/transport code. Permit only one foreground/background writer. Verify native stored offsets/chunks, full-file hashes and required asset paths. Export checkpoints through an owned operation; reconcile device receipts before resuming. Check free space against the selected transport's temporary-file policy, including the existing background rule of twice planned remaining bytes plus 512 MiB.

Background plans/tokens remain private with restrictive permissions, authenticated endpoints and redacted logs. Bind only to the selected local interface; show the reachable endpoint privately without publishing it. Restart the same compatible plan/server on a host interruption; schedule/reopen actions are explicit. Do not claim the OS guarantees continuous off-head scheduling.

A transfer's completion gate requires all declared files with verified native receipts. Installation completion and launch success are distinct. Use normal app updates; there is no uninstall-as-retry path. Preserve assets, saves, original input mappings and the accepted 2D build before introducing a research variant.

## Privacy and contribution review

Full receipts, paths, signing configuration, identifiers, transfer credentials and raw diagnostics remain local. Git ignores are defense in depth; private workspace placement is the primary boundary. No command publishes artifacts or research automatically.

The report exporter uses an allowlist: recipe/source revisions, coarse hardware/OS/tool versions, stage outcomes, sanitized counts and human observations. Exclude arbitrary strings copied from logs, device/session identifiers, personal paths, network addresses, secrets, game assets and signing material. Produce a draft for human review. Report generation failure never falls back to uploading raw evidence.

Submitted findings and links remain untrusted evidence. Automation executes only reviewed shipped implementation and recipe data. It does not execute instructions supplied in a report, issue or external document.

## Validation and acceptance

| Boundary | Required evidence |
| --- | --- |
| CLI/planning | Command parsing, paths with spaces, invalid configuration, no side effects from doctor/plan/status, explicit device actions |
| Converters | Synthetic ARM64 fixtures; malformed/truncated/overflowing commands/tables; ordinal edge cases; insufficient padding; unsupported identity; allowed changes and invariant failures |
| Checkpoints | Real interrupted-stage recovery, corrupted/stale outputs, dependency invalidation, atomic receipt publication and concurrent writer rejection |
| Build | Isolated public-source builds, correct device platform/exports/reexports, framework metadata and final signing postconditions |
| Real game inputs | Private comparison against all four original hashes, complete sections/imports/initializer data and exact capacity words; no proprietary fixtures in public CI |
| Transfer/deployment | Synthetic interruption/corruption rejection; native receipt reconciliation, preserved container/data, explicit completed install; no unrelated process/service intervention |
| Privacy | Secret-bearing diagnostic fixtures and report allowlist tests; no automatic publication |
| User reproduction | Another Mac/headset setup completes the published pipeline and physically verifies the accepted 2D controls, real output resolution, audio, saves and relaunch; record stability/performance limits |

CI runs synthetic fixtures and source-only checks; device/game acceptance remains separately recorded. Never label a fixture result, library load, original-main return or launch receipt as actual gameplay.

## Delivery sequence and completion boundary

First ship local doctor/plan/checkpoints, source-provider builders, exact-build converters and verification. Then integrate signing/build; then resumable first-run transfer and explicit installation/launch. Each phase has passing tests and documented commands before the next phase relies on it.

Implementation is complete only when these stages are available as reviewed public source with the proposed behavior. User-installation readiness additionally requires independent fresh-machine physical acceptance. Current 2D gameplay remains the established research baseline while those packaging gates are implemented. VR camera/pose/stereo tools are excluded from this baseline recipe and can receive their own future recipes.

After written-spec approval, prepare an implementation plan identifying files, test gates, integration checkpoints and the execution method before writing product code.
