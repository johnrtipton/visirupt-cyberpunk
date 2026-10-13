# Architecture and source ownership

`visirupt-cyberpunk` owns the Cyberpunk setup guide, compatibility recipe, evidence summaries and research roadmap. [visirupt](https://github.com/johnrtipton/visirupt) owns the compatibility engine, native host, transfer tools and implementation tests. Link to upstream code instead of maintaining a second divergent copy.

```text
User-owned Mac ARM64 game + assets
          | local, exact-build preparation
          v
Native visionOS host + adapters + dependency providers
          | reads verified data in preserved app container
          v
Cyberpunk running in a native 2D window
          |
          +-- Separate VR research: camera ownership, pose, stereo, input
```

| Engine source location | Purpose |
| --- | --- |
| `cyberpunk-avp/compat` | Authored platform/API adapters |
| `cyberpunk-avp/resumable` | Asset receiver, foreground/background transport and tests |
| `scratch/cyberpunk-consolidated-host` | Adapter framework project and display bridge |
| `scratch/cyberpunk-staged-startup` | Active native game host and project specification |
| `scratch/cyberpunk-window-init-simulator` | Source-only adapter controls |
| `checkpoint/2026-10-12` | Sanitized baseline acceptance and reproduction boundaries |

The locally developed `native-vr` work contains the immersive foundation and camera investigation. Its latest state was not present in the public engine main revision checked when this guide was initialized. Publish reviewed updates upstream before treating them as publicly reproducible source.

Selected adapters may help other native Mac ports. This recipe validates Cyberpunk only; reusable code does not establish compatibility for another game. Game binaries and compiled proprietary providers stay outside these repositories.
