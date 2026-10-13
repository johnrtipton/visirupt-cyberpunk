# Setup workflow

Goal: reproduce the working native 2D baseline on another Mac and Apple Vision Pro, then offer a dependable end-user guide. This is the first documented workflow; external-framework preparation and parts of deployment still need packaging. The [native automation preview](automation.md) now supplies reviewed parameterized commands in an engine draft PR; its provisioned signing and independent headset acceptance remain pending. The sections below preserve the architectural/acceptance context of the earlier manual workflow.

## 1. Prepare your own environment

- A legitimate **Mac ARM64 Cyberpunk 2077 2.3** installation matching the supported recipe. The Windows executable is a different target.
- An Apple Silicon Mac with Xcode and the visionOS SDK, XcodeGen for source projects, make, uv for Python development checks, and CMake/Ninja for the recovered Curl build.
- An Apple Vision Pro paired for development, with Developer Mode and your own normal Apple signing/provisioning setup.
- A keyboard and pointing device for the currently validated controls.
- Storage for your original game, local build/staging and headset data. The tested original Data set had **110 files / 158,461,863,365 bytes** (about 158.46 GB / 147.58 GiB). Sizes vary with the game build; this is not the complete required free-space budget.

Record the actual Xcode, SDK, visionOS, hardware and game build versions for your reproduction. M2 Vision Pro is the accepted hardware baseline; other devices/builds need their own result. Follow Apple's current development/signing guidance for your installed Xcode version.

## 2. Obtain and identify the compatibility source

```sh
git clone https://github.com/johnrtipton/visirupt.git
cd visirupt
git rev-parse HEAD
```

Read its `CHECKPOINT.md` before building. A published reference is `7bd937d683beee6d27336ec3eeb29ca43ab88d89`; newer source can differ. Keep an immutable original game copy and local hashes. Match any adaptation to the exact game build; never apply unverified offsets from another release.

The existing source checkpoint expects separately prepared native provider frameworks and a locally adapted game module. The [build-input inventory](build-inputs.md) now identifies all ten prebuilt frameworks, the host-built MemoryTrace provider and exact original hashes. [Framework preparation](framework-preparation.md) and [game-module preparation](game-module-preparation.md) recover the commands and transformations. The proprietary conversion tools still need public packaging; record actual input/output identities before claiming a fresh-machine reproduction. Do not download an unofficial game package to fill missing dependencies.

## 3. Prepare the native host locally

The working host combines authored UIKit/AppKit compatibility adapters, native dependency providers, an adapted local ARM64 module, asset-root mapping and audited engine memory-capacity changes. Supported memory entitlements use normal provisioning. Reservations are virtual address space, not a claim that the headset has that much physical RAM.

Regenerate source projects from XcodeGen specs and configure your own signing team. The checkpoint's host Makefile builds the adapters and host **once its external prerequisites exist**; it is not a standalone build pipeline. Use the preparation guides for project-generation/build commands, Security aliases, native Curl options and exact module changes. The metadata converters described there are specifications awaiting parameterized public tools, so this remains a developer workflow.

Keep a distinct known-working 2D build. Never use a VR/debugger experiment as the default user build. Do not alter purchases, entitlement checks or DRM to make startup advance.

## 4. Stage and transfer your own assets

Use the engine repository's `cyberpunk-avp/resumable` receiver and transfer source. Hash original files; verify received chunks and final whole-file hashes. Keep checkpoints durable and resume from native receipts, rather than guessing an offset from host progress.

The tested receiver and game host preserve the bundle identifier `local.games.cyberpunk.assetreceiver`. Its `Application Support/GameData` container holds the transferred game data; host updates must preserve access to that container. **Do not uninstall the receiver as a retry:** that deletes its data container. Review identifier/signing changes before deployment.

Two transport paths have been tested: foreground developer-copy packets and authenticated background URLSession chunks. Use only one writer at a time. Background transfer needs the Mac awake and reachable on the same network; the OS controls scheduling. Plans contain bearer credentials and remain private. Budget for temporary chunks as well as final files; initial background scheduling conservatively requires twice planned remaining bytes plus 512 MiB.

This section still needs an independently verified first-run sequence covering receiver install, checkpoint export, plan creation, background scheduling and completion verification. Use the engine source README to distinguish older proposals from later implemented transport.

## 5. Build, sign, update and launch

Build for the physical visionOS device, verify signatures and requested supported entitlements, then perform a normal app update that preserves the asset container. Confirm installation completion before launching. Avoid simultaneous installs/transfers; the first monolithic full-bundle attempt generated substantial temporary disk usage.

The engine's active host lives under `scratch/cyberpunk-staged-startup` in its retained source layout. Despite the directory name, it is the checkpointed host source. Its game asset root must resolve to the verified external data container. Confirm actual file opens, not just a configured path string.

Use the native window with its real interaction area. During earlier startup the host waited for a genuine pointer sample before entering the engine; a transparent plain window blocked pointer admission until the full black rectangular interaction area was restored. Do not bypass readiness with fake input.

Record build/source identity, successful install, launch, asset-root access and output resolution. Keep raw launch logs private.

## 6. Verify the 2D baseline

- Reach menu and actual gameplay; intro playback or original-main return alone is insufficient.
- Hold/release W/A/S/D and verify movement starts/stops. Test mouse look/fire, clicks, dragging and scrolling.
- Test left/right-arrow camera yaw. The accepted setup added those buttons to `RightX_Axis` in one local `inputUserMappings.xml`; keep a backup and distinguish its modified hash from original transfer hashes.
- Confirm Space/Return/Escape where the test scenario permits and record missing bindings.
- Measure actual output drawables. The accepted baseline is 1280×720; saved settings and window dimensions alone are not proof.
- Exercise normal relaunch and saves before claiming reliability. Record failures and duration; extended stability, complete save handling and measured performance remain reproduction work.

Submit a sanitized [reproduction report](../CONTRIBUTING.md). Only call the workflow ready for end users after another setup passes it with the published source and complete external-input instructions.

## 7. Keep VR research separate

After recording the 2D baseline, follow [VR research](vr-research.md). Game camera observation and immersive synthetic rendering are distinct experiments. Preserve the playable build and original assets throughout.
