# Development Log

## 2026-08-30

- Narrowed V0 to a small touch/thermal benchtop prototype.
- Chose local deterministic safety limits with higher-level bounded response requests.
- Added requested-vs-executed response logging.
- Adopted an episode/frame data model that can later be exported to LeRobot-style datasets.
- Kept the numeric action space unresolved until actuator testing.
- Added optional identity and wearable physiology as higher-level context only.
- Explicitly separated recognition from authorization.
- Started a deeper tactile-HRI prior-art review.
- Hardware has not been purchased or tested yet.

### Open questions

- Does capacitive sensing add useful information beyond force for V0?
- What thermal response range is noticeable without becoming uncomfortable?
- What response vocabulary is useful before the action space is frozen?
- Which tactile-HRI systems already combine context, history, learned response selection, and physical reciprocity?
