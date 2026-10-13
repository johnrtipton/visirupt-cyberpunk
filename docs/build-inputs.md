# Build inputs and preparation order

Audited October 13, 2026 against the framework inputs used by the retained native host. This records the working 2D recipe and identifies the preparation tools still absent from the public engine checkpoint. See [framework preparation](framework-preparation.md) and [game-module preparation](game-module-preparation.md).

## Original game identity

The tested Mac ARM64 2.3 copy has these SHA-256 identities, relative to its app's `Contents` directory:

| Original input | SHA-256 |
| --- | --- |
| `MacOS/Cyberpunk2077` | `22c0d58bffe932fd3f78dacf5fe4e0378900b25a1a52d10f376d3e19764a4cd7` |
| `Frameworks/libBink2MacArm64.dylib` | `7d2cb4078e4e4da68df40a8f3c50fce79ca3d230a8d66a92f66d8d9bb2a3da6f` |
| `Frameworks/libGameServicesAppStore.dylib` | `eb79ae75b22adf7e923d5bd75f5c51928cfdb392f43ee8de15273ce9e8038891` |
| `Frameworks/libREDGalaxy64.dylib` | `9a2603656e8d5db4cbfcbb2b325c4629c9d0a6b096e1d3ccc97d6c48cbdf0023` |

These hashes identify the exact experiment, not publisher authenticity or proof of ownership. A mismatched build needs an independently audited recipe. Keep originals immutable; all adaptation happens on separate local copies.

## Framework inventory

The active host specification embeds ten pre-existing frameworks and builds one additional framework target:

| Framework | Origin | Preparation / dependency |
| --- | --- | --- |
| `HostAdapters` | Authored source | Consolidated XcodeGen project; UIKit-backed desktop/API adapters |
| `DisplayBridge` | Authored source | Reexports HostAdapters for scoped CoreGraphics provider routing |
| `IOKitBridge` | Authored source | Reexports HostAdapters for scoped IOKit routing |
| `MetalBridge` | Authored source | Reexports HostAdapters for scoped Metal routing |
| `NativeSecurity` | Authored source | Four Security implementation files; four desktop-symbol aliases |
| `Curl` | Official open-source curl 8.14.1 | Native source build with Secure Transport; historical tested dependency |
| `Bink` | User's `libBink2MacArm64.dylib` | Local platform/path adaptation, symbol-pool alignment and audited unused-dependency removal |
| `AppStoreServices` | User's `libGameServicesAppStore.dylib` | Local platform/path and five selected import-provider changes; HostAdapters required |
| `GalaxyServices` | User's `libREDGalaxy64.dylib` | Local platform/path and four selected Security provider changes; NativeSecurity required |
| `CyberpunkModule` | User's original executable | Exact-build conversion, dependency routing and two pool-capacity instructions |
| `MemoryTrace` | Authored source, built by host project | Reexports native libSystem; file-path translation and memory/file diagnostics |

Do not obtain proprietary providers from another user's compiled app. They are prepared locally from your compatible game copy; the repository distributes authored source and reviewed recipe information.

## Dependency order

1. Identify the original game and create private working copies.
2. Build HostAdapters and the three forwarding bridges; build NativeSecurity.
3. Source-build and package Curl; prepare local Bink, AppStoreServices and GalaxyServices copies.
4. Prepare CyberpunkModule using the complete conversion recipe, including the MemoryTrace dependency.
5. Stage all ten frameworks into `scratch/cyberpunk-staged-startup/Frameworks` in a clean engine checkout.
6. Generate the host project; it builds MemoryTrace and embeds/signs the provider frameworks.
7. Verify platform, dependencies, signatures, section invariants and assets before a device update. Preserve the receiver's data container.

## Audit result and scope

All ten current framework inputs are ARM64 `MH_DYLIB`, with `LC_BUILD_VERSION` platform **VISIONOS**, minimum 26.0 and SDK 27.0. This is artifact metadata, not a claim that every visionOS 26 device/runtime has been tested.

Compared with immutable originals, all 24 AppStoreServices, 10 Bink and 15 GalaxyServices file-backed sections are unchanged. CyberpunkModule has 29 file-backed sections; only `__text` differs, with four changed bytes across the two declared pool-capacity instruction words. The other 28 sections match. Header/LINKEDIT metadata and normal signatures are intentionally outside that section-equality claim. Full binding-provider validation is a separate gate.

The source-only NativeSecurity command in the framework guide was rebuilt with warnings-as-errors and produced VISIONOS/minimum 26.0/SDK 27.0 on October 13. HostAdapters and all three bridges also rebuilt from the pinned public source in an isolated checkout; the documented portable Curl command completed a fresh build from the retained official source tree and exported all 16 required names with the correct device target. No game launch, device update, archive re-download, TLS/network test or clean-machine game reproduction was performed for this documentation audit.

## Remaining packaging gates

The public engine checkpoint contains the host, adapters and transfer source, but not the historical exact-build conversion scripts or a standalone NativeSecurity/Curl preparation target. The original experimental scripts contain fixed local paths, earlier probes and simulator variants. Do not treat their names as available fresh-checkout commands.

Next implementation work is to publish parameterized, fail-closed preparation tools upstream, test them on synthetic binaries, and independently verify their outputs against these originals. A complete first-run transfer/signing/container procedure and second-machine reproduction must follow. These documents recover the recipe; they do not claim those packaging gates have passed.
