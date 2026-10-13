# VisiRupt · Cyberpunk 2077 on Apple Vision Pro

Documenting how to reproduce native Cyberpunk 2077 on Apple Vision Pro, and researching a VR mod.

**Current baseline:** Cyberpunk's Mac 2.3 build runs locally in a native 2D visionOS window on M2 Vision Pro. John Tipton confirmed gameplay, aiming/firing, WASD movement, arrow-key turning, mouse clicks/dragging and trackpad scrolling. Native output drawables were measured at **1280×720**. This is local execution, without game streaming.

**Current research:** adapting the working game for VR. A separate synthetic immersive scene has demonstrated tracked rendering and user-observed world anchoring/depth on the headset. Integrating headset pose with the game's active camera, true game stereo and spatial controller input remain research milestones.

This repository starts the user workflow documentation. The compatibility engine and host source live in [johnrtipton/visirupt](https://github.com/johnrtipton/visirupt). Its published developer checkpoint still depends on locally prepared external frameworks; a complete fresh-machine installer is not available yet. Cloning either repository alone will not launch the game.

## Start here

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
