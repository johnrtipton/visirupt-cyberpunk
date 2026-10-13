# VR research track

The 2D game is working. Current research is adapting that baseline into native VR on Apple Vision Pro.

## Progress

A separate synthetic Compositor Services/Metal scene builds and renders. Physical M2 Vision Pro testing observed two runtime views and tracked ARKit poses; the user accepted visual world anchoring/depth and improved edges after MSAA work. Simulator, host-pixel and geometry checks cover narrower contracts. These findings belong to the synthetic scene, not Cyberpunk stereo.

Static game analysis identified camera cache/setup/getter paths and projection-related data. Bounded hardware-breakpoint observation has produced a camera-shaped setup sample. One unlabeled sample and generic matrix hits do not establish ownership of the visible gameplay camera. Current work correlates labeled observations with actual player look/turn behavior. No validated game-pose write hook or second-eye render is claimed.

## Ordered milestones

1. **Observe the active gameplay camera.** Verify exact module identity and actual load slide; correlate bounded read-only samples with stationary/turning gameplay and distinguish menus/cutscenes and other views.
2. **Validate coordinate and projection contracts.** Confirm transforms, units, handedness, FOV, depth, culling and timing against actual consumers. Static names and PC offsets are discovery hints.
3. **Opt-in head-tracked mono.** Integrate a validated pose path with explicit original behavior/rollback, while preserving movement and gameplay camera semantics.
4. **True stereo.** Establish independent per-eye engine views and textures, asymmetric projections, depth/lighting/temporal consistency and compositor submission.
5. **Spatial input.** Validate controller actions, UI interaction and recentering against real gameplay.
6. **Acceptance.** Measure frame times, stability and tracking-loss recovery; test scenes, menus, cutscenes and save/reload. Publish measured results and remaining failures.

Preserve a separate accepted 2D build. Never patch a generic matrix helper globally without identifying player/render ownership. Upstream PC VR approaches use Windows/DX12/RED4ext/OpenXR contracts that require independent Mac ARM64/Metal validation.

Contributions should state the exact source/game identity, observed behavior, evidence, limitations and a bounded reproduction protocol. Keep proprietary binaries, disassembly dumps and private debugger logs local. Synthetic success, a module load or a valid quaternion cannot establish working game VR.
