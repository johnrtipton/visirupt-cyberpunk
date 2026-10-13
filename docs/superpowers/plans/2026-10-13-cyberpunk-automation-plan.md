# Cyberpunk AVP Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Provide resumable, verified preparation and explicit deployment of the supported native 2D Cyberpunk host from published source and user-owned game inputs.

**Architecture:** Implement a standard-library Python CLI in the engine repository with versioned recipes, private workspace state and independently verified conversion stages. Integrate the existing receiver instead of replacing its verified storage protocol. Keep signing, transfer, installation and launch as explicit commands with separate completion receipts.

**Tech Stack:** Python 3.11+, uv, unittest, XcodeGen, Xcode/clang/vtool/codesign/devicectl, CMake/Ninja, existing Swift/Objective-C/C sources.

**Spec:** [Approved automation design](../specs/2026-10-13-cyberpunk-automation-design.md). Approved October 13, 2026. Native inline execution was approved and the twelve source tasks are implemented in the [automation preview](../../automation.md). Fresh review findings were fixed with regression tests. Physical signing/device and independent reproduction gates remain pending.

## Global Constraints

- Implementation belongs in the VisiRupt engine repository; the Cyberpunk companion repository owns documentation.
- Initial recipe: `cyberpunk-mac-2.3-2d-v1`, targeting ARM64 VISIONOS minimum 26.0 / tested SDK 27.0.
- Use Python standard-library orchestration, uv for Python execution/development, existing XcodeGen/Xcode tools, and Make wrappers for common commands.
- All mutating stages require an explicit private workspace; paths containing spaces work. No command defaults to deploying or launching.
- There is no force option that bypasses identity, invariant, signing or asset checks.
- Originals remain read-only; retain original initializer data and change only the declared capacity words and metadata.
- Preserve the receiver/host data container and bundle identifier `local.games.cyberpunk.assetreceiver`; unverifiable signing/container ownership stops deployment.
- Full receipts, paths, signing configuration, identifiers, transfer credentials and raw diagnostics remain local. No command publishes artifacts or research automatically.
- Preserve the accepted 2D build and active VR research; no device action is implied by executing local implementation tasks.

## Review Focus

1. A workspace within the original game or tracked checkout must be rejected before any mkdir/copy; Task 1 tests both overlap directions and symlink escape.
2. A valid stage receipt with a corrupted artifact must rerun that stage and invalidate dependents; Task 2 mutates completed bytes and recipe versions.
3. A supported binary with malformed LINKEDIT must fail before writing output, even when its header looks valid; Tasks 3–5 test malformed offsets, streams and ordinals.
4. A second workspace targeting an active receiver must not start another writer; Task 9 tests device/container exclusion and unknown external activity.
5. Matching bundle strings with different or unknown signing ownership must not trigger an install or container deletion; Task 10 tests mismatched and missing ownership metadata.

## Execution setup and source boundaries

At execution time, use the git-worktree skill to attach a clean engine worktree based on a freshly verified source revision. The active engine checkout has concurrent VR work; do not reset, stage or edit it. Record the implementation base SHA in the plan execution log. The previous public documentation reference is `7bd937d683beee6d27336ec3eeb29ca43ab88d89`; it is an evidence reference, not an instruction to discard newer reviewed source.

All implementation file paths below are relative to that isolated engine checkout. Temporary scripts/builds belong in a separate scratch directory. The companion spec and recipe documentation are authoritative for the four original hashes, provider mappings and capacity words. Read the historical converters without executing them; derive reviewed parameterized code rather than copying fixed paths or simulator projects.

Implement Tasks 1–6 as local preparation checkpoint A, Tasks 7–8 as signed-build checkpoint B, and Tasks 9–12 as deployment/documentation checkpoint C. These are dependent stages of one pipeline. Commit each task after its specific tests pass; run the broader suite once per checkpoint and when integration changes justify it.

## File map and shared records

| Path | Responsibility |
| --- | --- |
| `tools/visirupt.py` | Executable CLI entry point |
| `tools/visirupt_pipeline/cli.py`, `core.py` | Parsing, errors, recipe loading, configuration/identity boundary |
| `workspace.py`, `stages.py` | Private paths, locks, atomic receipts, stage graph/invalidation |
| `macho.py`, `bindings.py` | Bounded binary decoding and provider semantics |
| `providers.py`, `game.py`, `verify.py` | Provider conversion, exact game preparation, independent postconditions |
| `builders.py`, `runner.py`, `host.py` | Controlled tools, source providers and private host generation/signing |
| `assets.py`, `device.py`, `reports.py` | Local asset manifests, transfer/device coordination, shareable allowlist |
| `recipes/cyberpunk-mac-2.3-2d-v1.json` | Reviewed declarative recipe; no credentials or proprietary bytes |
| `tests/automation/` | Synthetic fixtures, CLI/state/converter/build/device/privacy tests |
| `cyberpunk-avp/resumable/transfer.py`, `background_transfer.py` | Existing transports made configurable without changing verified protocol |
| `cyberpunk-avp/resumable/project.yml`, `Sources/AssetReceiver.swift`, `Sources/App.swift` | Local manifest generation/project portability and native writer ownership |
| `Makefile`, `.gitignore`, `.github/workflows/automation.yml`, `docs/automation.md` | Supported commands, privacy exclusions, synthetic CI and user workflow |

Shared aliases use `Recipe = dict[str, Any]`, `Receipt = dict[str, Any]`, `Artifact = dict[str, Any]` with `Any` imported from typing. Runtime decoding validates each schema; type aliases alone do not validate input. Recipe keys include schema version, id, version, target, input hashes, dependency routes, expected invariants and source archive identity. Artifact records include relative workspace path, size, SHA-256 and semantic verification outcome. Receipts additionally include stage/fingerprint/state, input/output records, gates and structured error code. Private paths never pass directly into public reports.

Error codes include `UNSUPPORTED_INPUT`, `INVALID_BINARY`, `WORKSPACE_OVERLAP`, `INVALID_RECEIPT`, `WORKSPACE_BUSY`, `DEVICE_BUSY`, `CONTAINER_OWNERSHIP_UNKNOWN`, `SOURCE_CHANGED`, `INCOMPLETE_TRANSFER` and `TOOL_FAILED`. CLI exits 0 only when its own completion gate passes; configuration failure exits 2 and a stage failure exits 1. Launch success is not a gameplay result.

### Task 1: Read-only CLI, configuration and recipe checks

**Files:** Create `tools/visirupt.py`, `tools/visirupt_pipeline/{__init__,cli,core,workspace}.py`, recipe JSON, root Makefile, and `tests/automation/test_cli.py`.

**Interfaces:** `load_recipe(path: Path) -> Recipe`; `checked_workspace(path: Path, protected: list[Path]) -> Path`; `main(argv: list[str] | None = None) -> int`. No filesystem creation during validation. Protect checkout and original-game roots in both containment directions. `doctor`, `plan` and `status` have no mutation; plan prints JSON to stdout, allowing the user to redirect it explicitly.

- [ ] Write failing overlap and no-write tests, including an original path containing spaces:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from tools.visirupt_pipeline.workspace import checked_workspace

class WorkspaceTests(TestCase):
    def test_workspace_cannot_contain_original(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "owned game"
            original.mkdir()
            with self.assertRaisesRegex(ValueError, "WORKSPACE_OVERLAP"):
                checked_workspace(root, [original])
            self.assertEqual([original], list(root.iterdir()))
```

- [ ] Run `uv run --no-project python -m unittest discover -s tests/automation -p test_cli.py -v`; require failure for missing implementation, then add nested-output, symlink-escape, unknown-recipe/SDK and dry-command subprocess tests.
- [ ] Implement the containment boundary and parser. Core checked containment is:

```python
def overlaps(a: Path, b: Path) -> bool:
    return a == b or a.is_relative_to(b) or b.is_relative_to(a)
```

Resolve paths against existing parents; reject unexpected symlinks before writing. Define every command from the spec, but return an explicit unsupported-stage error until its implementation is registered; never provide success stubs. `prepare/build/transfer/install/launch` require workspace, appropriate inputs and explicit device arguments; build requires team. Archive downloading requires `--download-source`; otherwise require `--curl-archive`.
- [ ] Run CLI tests and check `doctor --help`/`plan --help`; add `make automation-test` using standard-library unittest, and `make doctor/plan` wrappers forwarding explicit variables.
- [ ] Commit `feat: add recipe-aware automation CLI and workspace checks`.

### Task 2: Atomic receipts, locking and resume graph

**Files:** Complete `workspace.py`; create `stages.py` and `tests/automation/test_stages.py`.

**Interfaces:** `atomic_json(path: Path, value: dict) -> None`; `stage_fingerprint(inputs: dict) -> str`; `run_stage(workspace: Path, name: str, fingerprint: str, action: Callable[[Path], list[Path]]) -> Receipt`; `validate_receipt(workspace: Path, receipt: Receipt) -> bool`. Graph names: inspect, adapters, security, curl, providers, game, host, assets, transfer, install, launch. Errors preserve prior receipts and failed outputs.

- [ ] Test an interrupted action with actual child exit, corruption after completion, recipe/toolchain/source changes, dependent invalidation, lock contention and malformed receipts. The key completion assertion is:

```python
self.assertFalse(validate_receipt(workspace, receipt_after_artifact_corruption))
self.assertEqual("complete", rerun_receipt["state"])
self.assertNotEqual(old_fingerprint, changed_recipe_fingerprint)
```

Construct each receipt through `run_stage` in the tests; do not hand-author passing dictionaries.
- [ ] Run `uv run --no-project python -m unittest discover -s tests/automation -p test_stages.py -v` and observe the missing invalidation behavior.
- [ ] Implement atomic publication with private permissions and fsync; temporary output directories belong to their owned stage. Use `fcntl.flock` on the workspace lock, not PID-only stale lock files. Serialize fingerprint input deterministically:

```python
payload = json.dumps(inputs, sort_keys=True, separators=(",", ":")).encode()
fingerprint = hashlib.sha256(payload).hexdigest()
```

Hash outputs again before reuse; invalidate descendants without deleting completed upstream evidence. Handle incompatible receipt schema explicitly.
- [ ] Verify interruption leaves no complete receipt; run stage and CLI tests.
- [ ] Commit `feat: add verified stage checkpoints and resume invalidation`.

### Task 3: Bounded Mach-O and import-provider inventory

**Files:** Create `macho.py`, `bindings.py`, `tests/automation/fixtures.py`, `test_macho.py`, `test_bindings.py`.

**Interfaces:** `parse_macho(data: bytes) -> dict`; `inventory_imports(data: bytes, image: dict) -> list[dict]`; `semantic_inventory(data: bytes) -> dict`. Inventory includes header, commands, segment/section bounds, dependencies/versions, symbol entries, chained imports, legacy bind streams, initializers, exports and signature ranges. Include all formats actually present in the four inputs; reject others explicitly.

- [ ] Build synthetic ARM64 fixtures in authored Python, beginning with an empty header for parser boundary tests:

```python
import struct

def empty_macho() -> bytes:
    return struct.pack("<8I", 0xfeedfacf, 0x100000c, 0, 6, 0, 0, 0, 0)
```

Add segment/section/load-command, chained import and legacy stream constructors. Test truncated headers, cmdsize zero/overflow, section count beyond command, offsets beyond file, unterminated strings/LEB128, incompatible pointer formats, special/signed ordinals and ambiguity.
- [ ] Run parser/import tests red, using unittest discovery separately for `test_macho.py` and `test_bindings.py`.
- [ ] Implement bounded decoding. Every byte access goes through a checked slice, using this core rule:

```python
def checked_slice(data: bytes, offset: int, length: int) -> bytes:
    if offset < 0 or length < 0 or offset > len(data) or length > len(data) - offset:
        raise ValueError("INVALID_BINARY")
    return data[offset:offset + length]
```

Keep special ordinals and addends distinct from positive provider indexes. Parse source metadata without loading/executing any game code.
- [ ] Run both suites; exercise known inputs privately with read-only inventories and keep detailed reports outside Git. Confirm the original hashes still match.
- [ ] Commit `feat: add bounded Mach-O and logical import inspection`.

### Task 4: Parameterized proprietary-provider preparation

**Files:** Create `providers.py`, `verify.py`, `tests/automation/test_providers.py`.

**Interfaces:** `prepare_provider(name: str, source: Path, output: Path, recipe: Recipe) -> Artifact`; `verify_provider(name: str, original: bytes, prepared: bytes, recipe: Recipe) -> dict`. Consume Task 3 inventories, independent originals and recipe identity. Return complete prepared framework metadata and explicit gates.

- [ ] Add failing synthetic tests for Bink string-pool alignment and legacy ordinal remap, AppStore five-symbol routing, Galaxy four-symbol routing, referenced-umbrella refusal, unchanged section bytes and no output on malformed input. Assert logical providers rather than only opcode counts.
- [ ] Run `test_providers.py` red. Read the recovered framework guide and historical **device** converters; simulator platform 12 must be rejected for this recipe.
- [ ] Implement fresh-copy transforms with exact expected hash/platform guards. Bink surviving ordinal map is `{2: 1, 3: 2, 5: 3}`; AppStore appended HostAdapters ordinal is 7; Galaxy appended NativeSecurity ordinal is 6. Preserve names/flags/addends and non-ordinal descriptor bits:

```python
new_desc = (old_desc & 0xff) | (new_ordinal << 8)
```

Rewrite bounded load commands within verified header padding, retain original section positions/payloads and initializers, and package Info.plists. Align Bink strings preserving every byte and update LINKEDIT offsets/sizes. Independent verification rereads original and output rather than trusting converter assertions.
- [ ] Run synthetic suites, then privately compare prepared outputs with the original section/provider invariants: Bink 10 sections, AppStore 24, Galaxy 15. Record differences in signatures/header/LINKEDIT separately; do not require equal developer signatures.
- [ ] Commit `feat: prepare exact-build native game provider copies`.

### Task 5: Game conversion and independent verification

**Files:** Create `game.py`, extend `verify.py`, create `tests/automation/test_game.py`.

**Interfaces:** `prepare_game(source: Path, output: Path, recipe: Recipe) -> Artifact`; `verify_game(original: bytes, prepared: bytes, recipe: Recipe) -> dict`; `verify(workspace: Path, recipe: Recipe) -> Receipt`.

- [ ] Write tests for executable-to-dylib conversion with retained segment indices, PAGEZERO neutralization, command removal, positive/special ordinal handling, no header-overlap writes, original instruction mismatch, already-patched input, corrupted initializer data and signed-output semantic comparison.
- [ ] Run `test_game.py` red. Use synthetic fixtures for public tests and the four original identities for separate private verification.
- [ ] Implement MH_DYLIB conversion, identity/platform changes, audited Cocoa removal with chained/nlist remapping and all declared provider routes, including MemoryTrace at retained libSystem ordinal 20. Apply capacity words through virtual-to-file mapping only after exact original-word checks:

```python
changes = ((0x100012358, 0xd2c00209, 0xd2c00049),
           (0x10001239c, 0xd2c00109, 0xd2c00049))
```

The independent verifier reconstructs expected changes from the original inventory: 29 sections, 28 unchanged, only these two text instruction replacements; 6,538 initializer entries; original client version fields retained; logical import providers equivalent modulo declared aliases.
- [ ] Run all converter suites and privately verify the generated module. No entrypoint, game launch, debug attach or device operation occurs here.
- [ ] Commit `feat: automate verified Cyberpunk module preparation`.

### Task 6: Source provider builders and local preparation orchestration

**Files:** Create `runner.py`, `builders.py`, `tests/automation/test_builders.py`; connect `prepare/verify` in `cli.py`.

**Interfaces:** `run_tool(argv: list[str], cwd: Path, log: Path, timeout: float) -> dict`; `build_sources(source_root: Path, workspace: Path, recipe: Recipe, curl_archive: Path, download: bool = False) -> list[Artifact]`; `prepare(source_root: Path, game_root: Path, workspace: Path, recipe: Recipe, curl_archive: Path) -> Receipt`.

- [ ] Test argv handling with spaces/metacharacters, nonzero exits, timeout/interruption ownership, pinned archive rejection, archive traversal/symlink/device-member rejection, modified output invalidation, missing exports and unexpected native runtime dependencies. Never execute a subprocess through `shell=True`.
- [ ] Run builder tests red. Inject a callable runner for fake build outputs; include at least one subprocess fixture to exercise real exit/interruption behavior.
- [ ] Implement verified archive extraction with member/path/size limits, explicit optional official download and pinned SHA. Use the documented isolated XcodeGen/clang/CMake commands, building all four consolidated adapters, four-source NativeSecurity and Curl. Produce framework metadata and verify device platform, required aliases/exports and reexports before publishing each stage artifact. Do not edit checked-in project specs or use the original developer's compiled frameworks.

```python
result = subprocess.run(argv, cwd=cwd, stdout=log_handle,
                        stderr=subprocess.STDOUT, timeout=timeout, check=False)
if result.returncode:
    raise RuntimeError("TOOL_FAILED")
```

Use owned process groups where streaming/interrupt handling requires them; never terminate shared services.
- [ ] Run the local synthetic suite and rebuild from the public source in a fresh private workspace. Checkpoint A closes only when `prepare` and `verify` complete without any device call and original source bytes remain intact.
- [ ] Commit `feat: orchestrate resumable native framework preparation`.

### Task 7: Private host generation, normal signing and build verification

**Files:** Create `host.py`, `tests/automation/test_host.py`; modify the retained host/consolidated/receiver project specs only to remove developer defaults and expose supported overrides.

**Interfaces:** `build_host(source_root: Path, workspace: Path, recipe: Recipe, team: str) -> Receipt`; `inspect_signed_app(app: Path, recipe: Recipe) -> dict`. Signed outputs retain their unsigned-stage provenance and separately recorded hashes.

- [ ] Test missing signing team, missing framework, signature failure, unsupported entitlement/provisioning result, wrong bundle identity/platform and post-sign section/provider corruption. Require no automatic provisioning or device commands from `doctor/plan/prepare`.
- [ ] Run `test_host.py` red. Include executable fake-tool fixtures and test signatures as separate observations, not booleans copied from build exit status.
- [ ] Generate a private source/project tree preserving relative source relationships and rewrite only explicit build/configuration paths. Build MemoryTrace from retained Trace source; preserve all libSystem reexports and native failure behavior. Override team explicitly and invoke normal Xcode signing:

```python
argv += [f"DEVELOPMENT_TEAM={team}", "CODE_SIGN_STYLE=Automatic",
         "-allowProvisioningUpdates", "build"]
```

Verify codesign deep/strict, inspect both supported memory entitlements/provisioning acceptance and rerun independent prepared-module/provider checks against final embedded images. Reject a changed game module instead of relabeling its recipe.
- [ ] Run all local tests and one signed build when valid credentials are supplied. No install or launch is part of this gate. Checkpoint B closes with the verified app receipt; credentials absent means the signed-build gate remains explicitly untested.
- [ ] Commit `feat: build and verify a privately signed native host`.

### Task 8: Private asset manifests and reviewed input patch

**Files:** Create `assets.py`, `tests/automation/test_assets.py`; update receiver project resource generation and `Sources/App.swift` for runtime manifest loading validation.

**Interfaces:** `build_asset_manifest(game_root: Path, output: Path, recipe: Recipe) -> dict`; `patch_arrow_mapping(original: bytes) -> bytes`; `verify_asset_manifest(manifest: dict, root: Path) -> dict`.

- [ ] Test archive path normalization (`archive/Mac` to the observed `archive/mac` layout), destination collisions on case-sensitive/insensitive hosts, symlink/path escape, changed source during hashing, nonexistent archive, duplicate XML mapping, malformed XML, preserved original backup and patched-file hash distinct from original asset identity.
- [ ] Run `test_assets.py` red. Use synthetic Data trees, not real game files in public fixtures.
- [ ] Generate the receiver's private manifest from the user's matching tree, with streamed SHA/size and stable Data-relative paths; validate recipe-required directories/assets. Build original/modified configuration records separately. Insert only the two reviewed arrow buttons under normal RightX_Axis while retaining pad binding; preserve original bytes in the private backup. For existing patched input, recognize its exact expected result rather than adding duplicates.

```python
if source_hash != expected_original_hash:
    raise ValueError("SOURCE_CHANGED")
```

Revalidate source identity before transfer and during stream completion; prove source mutation cannot publish a valid completion receipt. The receiver rejects mismatched manifest identity instead of resetting stored data.
- [ ] Run asset and receiver fixture tests. Verify a private real manifest matches the source layout without copying the entire asset tree into a second generated bundle.
- [ ] Commit `feat: generate private asset manifests and verified input mapping`.

### Task 9: Parameterized transport and receiver writer exclusion

**Files:** Modify `cyberpunk-avp/resumable/{transfer,background_transfer}.py`, `Sources/AssetReceiver.swift`, `Sources/App.swift`, `project.yml`; create `tests/automation/test_transfer.py` and extend existing receiver/background tests.

**Interfaces:** `transfer_assets(workspace: Path, recipe: Recipe, device: str, transport: str, deploy_receiver: bool = False) -> Receipt`; `device_writer_lock(device: str, bundle: str, workspace: Path)` context manager. Existing tools gain explicit device/work/manifest arguments without import-time directory creation. Native lease/request ownership is authoritative across clients.

- [ ] Test two workspaces targeting one device/container, unknown external writer, receiver-side lease expiry/recovery, mismatched request IDs, corrupt native checkpoints, delayed background completion, out-of-order chunks, full-size-but-unverified files and interrupted transfers. Verify no receiver deployment without `--deploy-receiver` and no implicit uninstall.
- [ ] Run transfer tests and existing background/Swift receiver controls red for new ownership requirements.
- [ ] Replace hardcoded device paths with explicit configuration, keeping old CLI behavior only where it can safely require the new inputs. Export/reconcile native checkpoints; select exactly one transport; enforce native writer ownership and private local lock scoped to device/container. Bind the requested local interface and protect plan/token files from first creation; never print credentials. Preserve stable compatible plans on retry and require room for the selected transport policy.

```python
if any(not item["verified"] for item in native_files):
    raise RuntimeError("INCOMPLETE_TRANSFER")
```

Completion additionally checks path set, source hash, full byte count and native final SHA. An offset alone cannot satisfy the gate. At Task 9, transfer targets an already verified receiver; reject `--deploy-receiver` until Task 10 wires in the ownership-gated first-install/update path. Task 10 completes that integration with tests before deployment is enabled. OS scheduling and receiver reopen are explicit actions.
- [ ] Run transport/receiver suites and physical synthetic interrupted-transfer acceptance on a separately authorized fixture. A real large-data transfer needs an explicit device action and remains untested until recorded.
- [ ] Commit `feat: parameterize and exclusively resume native asset transfer`.

### Task 10: Explicit installation and launch with container ownership checks

**Files:** Create `device.py`, `tests/automation/test_device.py`; connect install/launch/status commands in `cli.py`.

**Interfaces:** `inspect_device(device: str, bundle: str) -> dict`; `require_update_ownership(installed: dict, candidate: dict) -> None`; `install_host(workspace: Path, device: str, app: Path) -> Receipt`; `launch_host(workspace: Path, device: str) -> Receipt`. Reject unknown metadata or ownership change before issuing install. Query tooling syntax/schema from installed devicectl help at execution time; record supported version/schema parsing.

- [ ] Write tests asserting zero install calls for unknown/different application-identifier/signing ownership even when the bundle identifier matches; assert zero uninstall/restart calls for every error. Test multiple-device ambiguity, incomplete install receipts, stale launch receipts and candidate identity changing after verification.
- [ ] Run `test_device.py` red with an injected tool runner recording every issued argv list.
- [ ] Implement current-state queries, candidate codesign/provisioning inspection and ownership comparison. Fresh device/container absence permits explicit first install; existing unverifiable data blocks update for a migration decision. Wire the Task 9 `--deploy-receiver` branch through this same ownership gate, building the receiver with the private Task 8 manifest and requiring its own completed installation receipt before sending chunks. Inspect archive/checkpoint/save preservation without silently copying private data into reports. Only issue commands named by the user's selected install/launch operation:

```python
if installed.get("exists") and (
    not installed.get("application_identifier") or
    installed["application_identifier"] != candidate["application_identifier"]
):
    raise RuntimeError("CONTAINER_OWNERSHIP_UNKNOWN")
```

Also validate applicable team/container metadata rather than relying on that one field alone. Installation completion requires the actual success receipt and candidate identity; launch never automatically claims or records gameplay.
- [ ] Run device/transfer integration fixtures. Perform physical update/launch only with explicit target/action authorization; preserve other research jobs and record skipped physical gates separately.
- [ ] Commit `feat: gate explicit deployment on verified container ownership`.

### Task 11: Status, private diagnostics and shareable reports

**Files:** Create `reports.py`, `tests/automation/test_reports.py`; finish status/report CLI and Make wrappers.

**Interfaces:** `public_report(private: dict) -> dict`; `stage_status(workspace: Path) -> dict`. Public fields: recipe id/version, source revision, validated coarse hardware/OS/tool versions, stage success/failure codes, sanitized counts and explicit human-test statuses. Unknown/freeform fields are excluded.

- [ ] Test secrets in nested receipts, raw stderr and input observations, device/session/network identifiers and private paths, malformed versions, credential-bearing URLs, report generation errors and contradictory gameplay status. Verify no upload/publish command is executed.
- [ ] Run `test_reports.py` red. A minimum negative assertion is:

```python
result = public_report({"recipe": {"id": "cyberpunk-mac-2.3-2d-v1", "version": 1},
                        "token": "private-test-secret", "raw_log": "private-test-secret"})
self.assertNotIn("private-test-secret", json.dumps(result))
```

- [ ] Implement schema-aware reconstruction, not regex-only redaction or copying arbitrary dictionaries. Validate coarse versions/counts/enumerated outcomes; human observations are explicit labels, not arbitrary log text. Report writes only to the requested new draft path and refuses replacement of an existing file. Missing/invalid inputs fail without raw-log fallback.
- [ ] Run privacy/status tests plus the whole synthetic automation suite; document local diagnostic locations and privacy review before sharing.
- [ ] Commit `feat: add private status and allowlisted reproduction reports`.

### Task 12: CI, fresh-workspace verification, docs and release gates

**Files:** Create `.github/workflows/automation.yml`, `docs/automation.md`; update engine README/Makefile/.gitignore and companion setup/roadmap links after source publication. Use current repository CI conventions discovered at execution time, keeping proprietary/device jobs outside public CI.

**Interfaces:** `make automation-test`, `make doctor`, `make plan`, `make prepare`, `make verify`, `make build`, `make transfer`, `make install`, `make launch`, `make status`, `make report` invoke the same tested CLI. Explicit GAME/WORKSPACE/DEVICE/TEAM/TRANSPORT variables map to parser options; absent required selectors fail before mutation.

- [ ] Test every Make wrapper with an argument-capturing CLI fixture, including paths with spaces. Check docs examples and invalid/missing selectors; confirm CI contains only synthetic/source checks and publishes no private artifacts.
- [ ] Run the full synthetic suite red for wrapper/CI gaps, then implement wrappers using properly quoted variables and explicit CLI argument validation. Add private-workspace/credential exclusions without untracking existing reviewed source. Public CI executes:

```sh
uv run --no-project python -m unittest discover -s tests/automation -p 'test_*.py' -v
```

Do not invent gameplay/device test success from this command. Read workflow/toolchain conventions before choosing runner versions and actions.
- [ ] Execute a fresh private doctor/plan/prepare/verify run against the user's immutable matching inputs; run signing/build separately with supplied credentials. Check retained originals, output invariants, receipt invalidation/resume and no writes into tracked source.
- [ ] Arrange independent second-Mac/headset reproduction from the published instructions: transfer/update/launch, actual menu/gameplay, movement release/turn/look/fire/scroll, 1280×720 output, audio/save/relaunch and duration/performance limitations. Keep a factual acceptance matrix: passed, failed, skipped or pending. No initial implementation session silently counts as independent acceptance.
- [ ] Self-review security/privacy and run relevant receiver/adapter regression checks for changed native source. Obtain whole-branch independent review under the chosen execution method, resolve findings and confirm CI before public merge. Commit `docs: document verified automation and remaining acceptance gates`; publish only reviewed source/docs, attach any created PR to this chat.

## Plan self-review and completion

The twelve tasks cover all approved commands, complete provider/module preparation, signing, private manifests, intentional input changes, receiver first deployment, authoritative writer exclusion, container ownership, report privacy and independent reproduction. Converter tests cover all representations used by current inputs; real proprietary comparisons are private gates. Spec-defined unsupported paths are explicit errors, not success stubs.

Do not mark automation or user-installation readiness complete merely because the synthetic suite passes. Checkpoint A/B/C completion and independent physical acceptance have separate records. Code publication can precede independent physical acceptance if remaining gates are clearly labeled; do not claim those results happened. Preserve the working 2D/VR research setup throughout.
