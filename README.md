# VisiRupt · Cyberpunk 2077 on Apple Vision Pro

Documenting how to reproduce native Cyberpunk 2077 on Apple Vision Pro, and researching a VR mod.

**Current baseline:** Cyberpunk's Mac 2.3 build runs locally in a native 2D visionOS window on M2 Vision Pro. John Tipton confirmed gameplay, aiming/firing, WASD movement, arrow-key turning, mouse clicks/dragging and trackpad scrolling. Native output drawables were measured at **1280×720**. This is local execution, without game streaming.

**Current research:** adapting the working game for VR. A separate synthetic immersive scene has demonstrated tracked rendering and user-observed world anchoring/depth on the headset. Integrating headset pose with the game's active camera, true game stereo and spatial controller input remain research milestones.

This repository starts the user workflow documentation. The compatibility engine and host source live in [johnrtipton/visirupt](https://github.com/johnrtipton/visirupt). A [reviewed automation preview](docs/automation.md) now prepares exact matching inputs and source providers in a private workspace. Provisioned signing and independent headset acceptance for that new pipeline remain pending; a complete accepted end-user installer is not available yet. Cloning either repository alone will not launch the game.

## TL;DR: Try the automated install

**Experimental native 2D developer workflow.** You need your own matching **Mac ARM64 Cyberpunk 2077 2.3** copy, an Apple Silicon Mac with Xcode/visionOS SDK **27.0**, XcodeGen, CMake, Ninja and uv, plus your Apple signing team and a paired Vision Pro in Developer Mode. Budget for about **158 GB of game data**, build space and transfer overhead. Signed-device and independent reproduction acceptance remain pending.

```sh
# The automation source is currently in the engine PR branch.
git clone --branch feat/native-cyberpunk-pipeline https://github.com/johnrtipton/visirupt.git
cd visirupt

export GAME='/absolute/path/to/Cyberpunk2077.app'
export WORKSPACE="$HOME/visirupt-private/cyberpunk" # outside the checkout and original game
export TEAM='YOURTEAMID'                          # your 10-character Apple team ID
export DEVICE='YOUR-PAIRED-DEVICE-IDENTIFIER'
export TRANSPORT='foreground'

make doctor
make plan
uv run --no-project python tools/visirupt.py prepare --download-source
make verify
make build

# Explicitly install/launch the receiver and transfer your verified assets.
uv run --no-project python tools/visirupt.py transfer --deploy-receiver --launch-receiver
make install
make launch
```

`--download-source` fetches only the pinned official Curl source; bring your own game. Keep the receiver open during foreground transfer. Retry with the same workspace and `make transfer` to resume, then install/launch after transfer completes.

**Do not uninstall an existing receiver/game as a retry.** Unknown manually installed app ownership stops for a migration decision. Keep the workspace: it retains transfer checkpoints and installation provenance. For background transfer, later host updates and troubleshooting, read the [full automation guide](https://github.com/johnrtipton/visirupt/blob/feat/native-cyberpunk-pipeline/docs/automation.md) and [acceptance status](docs/automation.md).

## Start here

- [Native automation preview](docs/automation.md): reviewed source PR, commands and separate acceptance gates.
- [Setup workflow](docs/setup-workflow.md): prerequisites, local preparation, transfer, signing, installation and acceptance.
- [Build inputs and preparation order](docs/build-inputs.md): exact original identities and the eleven-framework dependency graph.
- [Framework preparation](docs/framework-preparation.md) and [game-module preparation](docs/game-module-preparation.md): recovered build commands, transformations and verification gates.
- [Verified baseline](docs/status.md): tested features, evidence and current limitations.
- [Architecture and source map](docs/architecture.md): which repository owns each component.
- [Troubleshooting](docs/troubleshooting.md): preserve assets and diagnose failed stages.
- [VR research](docs/vr-research.md): the current investigation and ordered validation gates.
- [Roadmap](docs/roadmap.md): what must be packaged for other users.
- [Contributing](CONTRIBUTING.md): reviewed, privacy-safe findings from humans and agents.

Bring your own legitimate compatible Mac game copy. Game executables, assets, proprietary frameworks, complete game configuration files and signing materials are not distributed here. This is an independent research project, unaffiliated with CD PROJEKT RED or Apple.

Research lead: [John Tipton](https://github.com/johnrtipton). AI assisted implementation, analysis and documentation; human testing and review remain explicit. [VisiRupt website](https://visirupt.com) · [Published foundational findings](https://agentcommons.me/pages/page_4636664ccca2f1c8a7f3bdc1).

For repository documentation checks, run `make check` (requires Python 3 and make).
