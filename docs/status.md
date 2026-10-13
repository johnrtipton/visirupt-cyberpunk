# Verified baseline

Updated October 13, 2026. Physical 2D acceptance recorded October 12; John Tipton reconfirmed working 2D mode on October 13. Earlier October 10–11 loader/startup notes are historical and do not describe the current gameplay baseline.

| Area | Evidence | Limit |
| --- | --- | --- |
| Native 2D gameplay | Human played Cyberpunk Mac 2.3 on M2 Vision Pro | One developer setup; independent reproduction pending |
| Input | Aiming/firing, WASD hold/release, left/right arrows for camera yaw, click/drag/scroll confirmed | Complete bindings, controllers and later-build input regressions need testing |
| Window | Plain, resizable window with working interaction area | Enlarging the window does not dynamically increase backing resolution |
| Output | Actual native drawables measured at 1280×720, versus earlier 640×360 | Internal scene render resolution, FPS and frame times unmeasured |
| Assets | Original archives preserved; resumable receiver validates chunks and whole files | Full transfer reproduction on another setup pending; one active input XML was intentionally changed |
| Synthetic immersive renderer | Physical tracked scene and world anchoring/depth received user acceptance | This scene does not render Cyberpunk or establish game stereo |
| Game VR | Camera metadata/call paths mapped; bounded read-only observation underway | Active player-camera ownership, safe pose integration and second-eye rendering unvalidated |

Some later camera-debugging sessions had intermittent launch/attachment failures and keyboard delivery problems. Preserve the accepted 2D build as a baseline and test each research build separately. A passing adapter fixture or simulator renderer is not a gameplay benchmark.

## Evidence provenance

The public engine [checkpoint](https://github.com/johnrtipton/visirupt/blob/7bd937d683beee6d27336ec3eeb29ca43ab88d89/CHECKPOINT.md) records the accepted 2D behavior, source boundary and 95 adapter controls. That pinned public revision provides a stable reference; it does not include every later local VR experiment.

This summary also incorporates reviewed local physical acceptance records and current research notes. Private logs and device/session identifiers remain local. Later VR findings should be published with a sanitized evidence summary and source revision after review. Report independent replication separately from the original developer acceptance.
