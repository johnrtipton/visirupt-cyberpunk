# Framework preparation

Use a separate clean engine checkout and private build directory. This guide records source-build commands and the exact proprietary-provider transformations recovered from the working setup. The proprietary converters are still awaiting public packaging; do not assume the commands below complete that missing stage.

## Working directory and tools

From the engine checkout root:

```sh
VISIRUPT_ENGINE_ROOT="$(pwd)"
VISIRUPT_BUILD_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/visirupt-build.XXXXXX")"
VISIRUPT_XROS_SDK="$(xcrun --sdk xros --show-sdk-path)"
VISIRUPT_SIGNING_TEAM="YOUR_OWN_TEAM_ID"
xcodebuild -version
xcrun --sdk xros --show-sdk-version
xcodegen --version
cmake --version
ninja --version
```

The retained binary target is ARM64 visionOS 26.0 with SDK 27.0. Record any SDK change instead of assuming output hashes will match. Keep the private directory until hashes, verification and backups are recorded.

## 1. HostAdapters and the three bridges

The public consolidated XcodeGen spec contains the real source sets, symbol aliases and reexports. Use it rather than reconstructing linker flags from memory. It builds HostAdapters, DisplayBridge, IOKitBridge and MetalBridge together:

```sh
(
  cd "$VISIRUPT_ENGINE_ROOT/scratch/cyberpunk-consolidated-host"
  xcodegen generate --spec project.yml
  xcodebuild -project CyberpunkConsolidatedHost.xcodeproj \
    -scheme HostAdapters -configuration Debug -sdk xros \
    -destination 'generic/platform=visionOS' \
    -derivedDataPath "$VISIRUPT_BUILD_ROOT/Adapters" \
    CODE_SIGNING_ALLOWED=NO build
)
```

This command rebuilt all four targets from the pinned public engine source in an isolated directory on October 13. It produces unsigned framework inputs. Final host embedding uses your normal signing configuration. Before using a private working-copy destination, confirm you have not selected an existing accepted build. Copy the four resulting frameworks from `Adapters/Build/Products/Debug-xros` into the clean checkout's host `Frameworks` directory. All three bridges must accompany the new HostAdapters build.

## 2. NativeSecurity from authored source

The required implementations are `CPClientIdentity.m`, `CPPublicKeyExport.m`, `CPCertificateLabel.m` and `CPDesktopSecurity.m` under `cyberpunk-avp/compat/Security`. The four exported aliases satisfy the scoped desktop Security imports in the adapted Galaxy library. They implement the inspected contracts using native Security/Foundation; they do not replace purchases or account authorization.

This **device** compile was rechecked on October 13 with warnings-as-errors. The earlier experimental `build.sh` used `xrsimulator`; do not copy its target into a device recipe.

```sh
VISIRUPT_SECURITY_SRC="$VISIRUPT_ENGINE_ROOT/cyberpunk-avp/compat/Security"
VISIRUPT_SECURITY_FRAMEWORK="$VISIRUPT_BUILD_ROOT/NativeSecurity.framework"
mkdir -p "$VISIRUPT_SECURITY_FRAMEWORK"
xcrun --sdk xros clang -target arm64-apple-xros26.0 \
  -dynamiclib -fobjc-arc -Wall -Wextra -Werror \
  -I"$VISIRUPT_SECURITY_SRC" \
  "$VISIRUPT_SECURITY_SRC/CPClientIdentity.m" \
  "$VISIRUPT_SECURITY_SRC/CPPublicKeyExport.m" \
  "$VISIRUPT_SECURITY_SRC/CPCertificateLabel.m" \
  "$VISIRUPT_SECURITY_SRC/CPDesktopSecurity.m" \
  -framework Foundation -framework Security \
  -Wl,-alias,_CPDesktopItemImport,_SecItemImport \
  -Wl,-alias,_CPDesktopItemExport,_SecItemExport \
  -Wl,-alias,_CPDesktopIdentityCreateWithCertificate,_SecIdentityCreateWithCertificate \
  -Wl,-alias,_CPDesktopCertificateCopyLongDescription,_SecCertificateCopyLongDescription \
  -install_name @rpath/NativeSecurity.framework/NativeSecurity \
  -o "$VISIRUPT_SECURITY_FRAMEWORK/NativeSecurity"
xcrun vtool -show-build "$VISIRUPT_SECURITY_FRAMEWORK/NativeSecurity"
xcrun nm -gU "$VISIRUPT_SECURITY_FRAMEWORK/NativeSecurity"
```

Require all four `_Sec…` alias exports and a VISIONOS build command. Add a framework Info.plist declaring executable/name `NativeSecurity`, package type `FMWK`, supported platform `XROS`, minimum 26.0, version 1/1.0 and a bundle identifier under your control. A bare dylib without framework metadata is not the completed framework package. Copy that package into the clean host's `Frameworks` directory before signing the app.

## 3. Historical native Curl build

The accepted experiment source-built official **curl 8.14.1** with Secure Transport. Source archive SHA-256 is `f4619a1e2474c4bbfedc88a7c2191209c8334b48fa1f4e53fd584cc12e9120dd`; provenance records verified the detached release signature. Obtain the [official archive](https://curl.se/download/curl-8.14.1.tar.xz) and follow [curl's signature verification procedure](https://curl.se/docs/verify.html). Set `VISIRUPT_CURL_SOURCE` to the verified extracted source directory.

This pins historical reproduction. Upstream [removed Secure Transport in 8.15.0](https://curl.se/ch/8.15.0.html); a maintained curl/TLS backend and its feature/ABI tests remain a release decision. Do not label the archival dependency as a current production recommendation.

The recovered CMake driver is Darwin with an explicit visionOS clang target. The old installed CMake lacked a visionOS platform module. The command below expresses its settings without developer-specific toolchain paths:

```sh
cmake -S "$VISIRUPT_CURL_SOURCE" -B "$VISIRUPT_BUILD_ROOT/Curl" -G Ninja \
  -DCMAKE_SYSTEM_NAME=Darwin -DCMAKE_SYSTEM_VERSION=26.0 \
  -DCMAKE_OSX_DEPLOYMENT_TARGET:STRING= \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_OSX_SYSROOT="$VISIRUPT_XROS_SDK" \
  -DCMAKE_C_COMPILER="$(xcrun --sdk xros --find clang)" \
  -DCMAKE_C_COMPILER_TARGET=arm64-apple-xros26.0 \
  -DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
  -DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
  -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY \
  -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY \
  -DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON -DBUILD_CURL_EXE=OFF -DBUILD_TESTING=OFF \
  -DCURL_USE_SECTRANSP=ON -DCURL_USE_OPENSSL=OFF \
  -DCURL_USE_LIBPSL=OFF -DCURL_USE_LIBSSH2=OFF \
  -DCURL_ZLIB=OFF -DCURL_BROTLI=OFF -DCURL_ZSTD=OFF \
  -DUSE_NGHTTP2=OFF -DUSE_LIBIDN2=OFF \
  -DCURL_DISABLE_LDAP=ON -DCURL_DISABLE_LDAPS=ON -DHAVE_PIPE2=FALSE
cmake --build "$VISIRUPT_BUILD_ROOT/Curl" --parallel 2
```

`HAVE_PIPE2=FALSE` selects the actual upstream fallback for the 26.0 deployment target; optional host Homebrew libraries are disabled. This records the recovered options and replaces fixed compiler/SDK paths with `xcrun`; that portable form completed a fresh isolated build on October 13, with VISIONOS/minimum 26.0/SDK 27.0, all 16 required exports and no Homebrew runtime dependencies. This used the existing verified source tree, not a new archive download, and did not exercise network/TLS behavior.

Package the resulting real `lib/libcurl.4.8.0.dylib` as `Curl.framework/Curl`, with an XROS framework Info.plist. Change only its install identity to the framework path, retaining the real version metadata:

```sh
VISIRUPT_CURL_FRAMEWORK="$VISIRUPT_BUILD_ROOT/Curl.framework"
mkdir -p "$VISIRUPT_CURL_FRAMEWORK"
cp "$VISIRUPT_BUILD_ROOT/Curl/lib/libcurl.4.8.0.dylib" \
  "$VISIRUPT_CURL_FRAMEWORK/Curl"
xcrun install_name_tool -id @rpath/Curl.framework/Curl \
  "$VISIRUPT_CURL_FRAMEWORK/Curl"
xcrun vtool -show-build "$VISIRUPT_CURL_FRAMEWORK/Curl"
xcrun otool -L "$VISIRUPT_CURL_FRAMEWORK/Curl"
xcrun nm -gU "$VISIRUPT_CURL_FRAMEWORK/Curl"
```

Require VISIONOS and no accidental Homebrew or macOS-only runtime paths. The game's 16 required exports are easy_cleanup/getinfo/init/perform/setopt/strerror; global_cleanup/init_mem; multi_add_handle/cleanup/info_read/init/perform/remove_handle; slist_append/free_all, each with the `curl_` prefix. Verify ARM64 LP64 layouts and actual behavior, including callback/varargs contracts, rather than treating names alone as ABI proof.

The game's original curl dependency declares compatibility 7.0.0/current 9.0.0; the upstream-built library declares compatibility 4.0.0/current 4.8.0. Earlier physical loading advanced with real metadata preserved. Do not forge either field or infer full network/TLS parity from that load result.

## 4. User-owned Bink library

Require the [original Bink identity](build-inputs.md). The recovered device sequence was:

1. Work on a separate local copy; rewrite its identity to `@rpath/Bink.framework/Bink` and retarget to VISIONOS/minimum 26.0/SDK 27.0.
2. Normalize only the audited CoreAudio and AudioToolbox image paths.
3. Align the original symbol-string pool to an 8-byte boundary, preserving every string byte. Update its LC_SYMTAB string offset and LINKEDIT sizes with zero padding and checked bounds.
4. Remove AudioUnit and Carbon only after confirming they contribute no imports to the inspected legacy bind/weak/lazy streams or external undefined nlist records. Remap surviving ordinals **2→1, 3→2, 5→3** in each affected representation; preserve special ordinals and logical providers.
5. Verify all ten original file-backed sections, retained payload invariants and framework metadata before normal signing.

The active Bink image depends only on native CoreAudio, AudioToolbox and libSystem, plus its own identity. Historical provenance is the local `cyberpunk-native-bink-pruned` preparation/alignment/pruning/verification sequence. Its paths are not public preparation commands. Earlier incomplete copies still contained unavailable AudioUnit/Carbon paths; do not use them as the final provider.

## 5. User-owned AppStoreServices library

Start from the matching original `libGameServicesAppStore.dylib`. The **device** adaptation retains all 24 original file-backed sections and initializer bytes:

- Remove its first AppKit dependency and append HostAdapters. Normalize audited native framework paths and set the framework identity.
- Redirect exactly `_NSApp`, `_NSApplicationDidBecomeActiveNotification`, `_NSApplicationWillResignActiveNotification`, `_syslog$DARWIN_EXTSN` and `_OBJC_CLASS_$_GKDialogController` to appended provider ordinal 7.
- Remap other surviving positive dependency ordinals in both chained imports and external undefined nlist records; preserve names, flags, addends and special ordinals.
- Retarget to **VISIONOS platform 11**, not XRSimulator platform 12; package with XROS metadata and verify all 65 chained records.

The final provider retains native GameKit, Foundation, CoreFoundation, libobjc/libc++/libSystem and HostAdapters. This adapts platform API imports; original game-service implementation remains. Historical device provenance is `cyberpunk-appstore-device-probe/prepare.py`; the similarly named native-probe script actually targeted a simulator and must not be substituted blindly.

## 6. User-owned GalaxyServices library

Start from matching `libREDGalaxy64.dylib`; retain its 15 original file-backed sections and initializers:

- Remove its first unused Cocoa dependency after verifying the import boundary; append NativeSecurity.
- Redirect exactly `_SecItemImport`, `_SecItemExport`, `_SecIdentityCreateWithCertificate` and `_SecCertificateCopyLongDescription` to appended provider ordinal 6.
- Remap surviving positive ordinals in chained-import and external undefined nlist records, preserving their other fields and special ordinals.
- Normalize audited native paths, set `@rpath/GalaxyServices.framework/GalaxyServices`, retarget to VISIONOS platform 11 and use XROS metadata.
- Verify all 667 chained records and the original code/data payloads before normal signing.

Galaxy retains its own embedded curl/TLS implementation; the separately built Curl framework does not replace that embedded code. Source-built adapters and successful service-library loading do not establish account/TLS feature parity. Historical device provenance is `cyberpunk-galaxy-device-probe/prepare.py` and its independent verifier.

## Framework metadata for source-built providers

After creating both NativeSecurity and Curl directories, create their framework Info.plists in your **private build directory**. This example uses local research identifiers; configure identifiers appropriate to your signing setup. It refuses to replace existing metadata.

```sh
uv run --no-project python - "$VISIRUPT_SECURITY_FRAMEWORK" "$VISIRUPT_CURL_FRAMEWORK" <<'PYTHON'
from pathlib import Path
import plistlib
import sys

for value in sys.argv[1:]:
    framework = Path(value)
    name = framework.stem
    if name not in {"NativeSecurity", "Curl"} or not (framework / name).is_file():
        raise SystemExit("Expected an existing source-built framework executable")
    info = {
        "CFBundleExecutable": name,
        "CFBundleIdentifier": "local.research." + name.lower(),
        "CFBundleName": name,
        "CFBundlePackageType": "FMWK",
        "CFBundleShortVersionString": "1.0",
        "CFBundleVersion": "1",
        "CFBundleSupportedPlatforms": ["XROS"],
        "MinimumOSVersion": "26.0",
    }
    with (framework / "Info.plist").open("xb") as destination:
        plistlib.dump(info, destination)
PYTHON
```

Inspect the files with `plutil -lint` before staging. This supplies package metadata, not a code signature or entitlement grant. The final host build must normally embed/sign these frameworks.

## 7. Assemble the host after all inputs pass

Prepare [CyberpunkModule](game-module-preparation.md) and place it with all nine other prebuilt frameworks in the clean engine host's `Frameworks` directory. The host itself builds MemoryTrace. Its project requests both the supported [Extended Virtual Addressing](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.kernel.extended-virtual-addressing) and [Increased Memory Limit](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.kernel.increased-memory-limit) entitlements; provisioning must accept them under your own team.

Generate the host project and normally build/sign it only after external preparation is complete:

```sh
(
  cd "$VISIRUPT_ENGINE_ROOT/scratch/cyberpunk-staged-startup"
  xcodegen generate --spec project.yml
  xcodebuild -project CyberpunkStartupFileProbe.xcodeproj \
    -scheme CyberpunkStartupFileProbe -configuration Debug -sdk xros \
    -destination 'generic/platform=visionOS' \
    -derivedDataPath "$VISIRUPT_BUILD_ROOT/Host" \
    DEVELOPMENT_TEAM="$VISIRUPT_SIGNING_TEAM" \
    CODE_SIGN_STYLE=Automatic -allowProvisioningUpdates build
)
VISIRUPT_HOST_APP="$VISIRUPT_BUILD_ROOT/Host/Build/Products/Debug-xros/CyberpunkStartupFileProbe.app"
codesign --verify --deep --strict --verbose=2 "$VISIRUPT_HOST_APP"
codesign -d --entitlements :- "$VISIRUPT_HOST_APP"
```

Do not publish signing output or provisioning profiles. This command overrides the retained local team setting without claiming the project's defaults are portable. Installation, asset transfer and live acceptance remain separate [workflow steps](setup-workflow.md); building does not establish a successful device update or gameplay.
