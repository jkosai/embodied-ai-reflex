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
- Added a provisional pre-hardware wiring plan.
- Added an ESP32 firmware skeleton with simulated sensing and separated sensor/event/safety/output modules.
- Added a host-side Python logger and generated a schema-v0.3 simulated session.
- Hardware has not been purchased or physically tested yet.

### Open questions

- Does capacitive sensing add useful information beyond force for V0?
- What thermal response range is noticeable without becoming uncomfortable?
- What response vocabulary is useful before the action space is frozen?
- Which tactile-HRI systems already combine context, history, learned response selection, and physical reciprocity?
- Which exact board, sensors, heater, driver, and independent cutoff will be used for the first physical build?
