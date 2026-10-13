# Exact-build Cyberpunk module preparation

This is the recovered preparation specification for the working native 2D module. It is intended for implementing/reviewing a reproducible converter. The historical scripts remain local experimental tools; no public one-command converter is available yet. Read the [input identities](build-inputs.md) first.

## 1. Convert a separate executable copy

Require the tested original SHA-256 and ARM64 Mach-O `MH_EXECUTE` header. Parse bounded load commands and all file-backed sections; reject malformed lengths, insufficient header padding and an unsupported identity.

The retained original header/load-command area ends at file offset 5328; the first file-backed section starts at 19664. The experiment verified intervening padding was zero before repacking commands. This is build-specific space, not an invitation to grow headers into code.

- Change file type to `MH_DYLIB`; clear `MH_PIE`.
- Remove `LC_MAIN` and `LC_LOAD_DYLINKER`; the native host later invokes the verified original entrypoint explicitly.
- Keep segment indices; neutralize the `__PAGEZERO` virtual reservation rather than deleting its segment.
- Add `LC_ID_DYLIB` with identity `@rpath/CyberpunkModule.framework/CyberpunkModule`.
- Retarget `LC_BUILD_VERSION` to visionOS 26.0 / SDK 27.0 and create a valid XROS framework Info.plist.

`vtool` changes platform metadata only; it does not perform the executable conversion or API adaptation:

```sh
xcrun vtool -set-build-version visionos 26.0 27.0 -replace \
  -output "$VISIRUPT_MODULE_COPY" "$VISIRUPT_MODULE_COPY"
```

Set `VISIRUPT_MODULE_COPY` to the prepared **private copy**, never the original. The old code signature is invalid after modification; normally sign the final framework/app through your own build.

## 2. Route dependencies without corrupting bindings

The tested original has 24 dependency commands. Remove only its unused Cocoa umbrella after confirming no chained or external undefined nlist import is bound to it. It is original dependency ordinal 4 in this build. Decrement later positive ordinals in both chained-import records and external undefined nlist records. Preserve special ordinals, names, indices, weak flags, addends and non-ordinal descriptor bits. Verify each logical provider before/after, allowing only the declared routing changes.

The audited recipe inspects 57,963 chained-import records and 68,639 total nlist records. A header-only path rewrite cannot substitute for ordinal verification after removing a provider.

| Original provider | Prepared provider |
| --- | --- |
| `/usr/lib/libcurl.4.dylib` | `@rpath/Curl.framework/Curl` |
| `@executable_path/../Frameworks/libBink2MacArm64.dylib` | `@rpath/Bink.framework/Bink` |
| `@executable_path/../Frameworks/libGameServicesAppStore.dylib` | `@rpath/AppStoreServices.framework/AppStoreServices` |
| `@rpath/libREDGalaxy64.dylib` | `@rpath/GalaxyServices.framework/GalaxyServices` |
| Desktop AppKit | `@rpath/HostAdapters.framework/HostAdapters` |
| Desktop CoreGraphics | `@rpath/DisplayBridge.framework/DisplayBridge` |
| Desktop IOKit | `@rpath/IOKitBridge.framework/IOKitBridge` |
| Desktop Metal | `@rpath/MetalBridge.framework/MetalBridge` |
| `/usr/lib/libSystem.B.dylib` | `@rpath/MemoryTrace.framework/MemoryTrace` |

Normalize the remaining audited native Apple framework paths to their actual visionOS image paths; do not blindly strip every `Versions` component. The active module's remaining native frameworks include MetricKit, MetalFX, GameKit, Foundation, QuartzCore, AudioToolbox, CoreAudio, GameController, CoreHaptics, AVFAudio and CoreFoundation, plus libbz2/libobjc/libc++.

Keep client current/compatibility version fields as audited. Curl's original client requirement and upstream dylib version fields differ; record actual loading behavior rather than forging compatibility metadata. Preserve all 29 section payloads at this stage.

## 3. Apply only the audited capacity changes

For the identified original, the working initial engine pools are **16/8/8 GiB**. Only two ARM64 instruction words change:

| Unslid virtual address | Original word | Final word | Capacity |
| --- | --- | --- | --- |
| `0x100012358` | `0xd2c00209` | `0xd2c00049` | 64 → 8 GiB |
| `0x10001239c` | `0xd2c00109` | `0xd2c00049` | 32 → 8 GiB |

The first 16-GiB pool and three later 4-GiB world-pool instructions remain unchanged. Map addresses through Mach-O section/segment metadata; they are not file offsets or live ASLR addresses. Verify original instruction words before writing; reject another build or an already modified input. The historical investigation tested an intermediate 16/16/16 variant first; recreating that intermediate is unnecessary for a reviewed converter producing the final recipe.

The October 13 comparison found exactly four differing section bytes across these two words, all 28 other sections unchanged and the initializer section unchanged. The earlier independent verifier counted **6,538 original initializer entries**. Virtual reservations are distinct from physical memory usage; passing startup does not validate every gameplay allocator requirement.

## 4. Include the pass-through memory/file provider

The current module redirects the original libSystem dependency at retained ordinal 20 to `MemoryTrace`. This is part of the actual working recipe, not merely optional console logging. The host project's MemoryTrace framework reexports libSystem and supplies native mmap/madvise/file wrappers. Its file adapter maps logical app-bundle `Data` accesses to `Application Support/GameData/Data` while retaining genuine native failure/errno semantics.

That path mapping must be configured before original engine startup. Preserve the actual copied provider names and linking layout, including the three bridges. Do not replace native failures with fabricated success.

## 5. Verify before device use

- Recheck the immutable original hash and record the prepared copy hash.
- Require ARM64, `MH_DYLIB`, VISIONOS/minimum 26.0/SDK 27.0 and expected framework identity.
- Require exactly the declared dependencies and correct logical import providers.
- Require all section sizes/addresses unchanged, with only the two allowed instruction replacements.
- Verify the complete original initializer data remains intact.
- Build and normally sign the host with supported memory entitlements and your own signing team; verify signature and provisioning acceptance.
- Confirm actual staged data access, original entrypoint guards, menu and gameplay using the [setup acceptance](setup-workflow.md).

Historical provenance: `cyberpunk-game-host-native-probe/prepare.py` handled exact-format/provider conversion; the pool/startup capacity experiments established the final instruction words; `cyberpunk-memory-trace-probe/prepare-module.py` routed libSystem. These names describe local research stages under the engine's scratch layout, not scripts promised in the public repository. Their scripts must be parameterized and reviewed before publication as user tools.
