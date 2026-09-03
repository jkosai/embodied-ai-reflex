# V0 Touch + Warmth Test Protocol

Version 0.1, recorded 2026-09-03. Status: **pre-hardware software scaffold**.

## Question and boundary

Does context-sensitive response selection feel more responsive, intentional, and connected to a person's
touch than a fixed response? V0 tests this narrow comparison on one benchtop touch/thermal zone.
It does not demonstrate emotional understanding, persistent relationship memory, or safe robotic hugging.
No physical results are claimed. Motion and higher-level agent integration remain future work.

## Executable pipeline

```text
sensor input -> classified event -> requested response -> safety evaluation -> executed response -> log
```

Firmware implements these stages in `sensors`, `events`, `responses`, `safety`, `outputs`, then serial telemetry.
The host logger adds trial metadata and canonical JSONL. `host/pipeline.py` provides a non-actuating reference.
All sampled frames are logged, including idle, rejection, and invalid-input frames.

## Conditions

| Event | A: `fixed` | B: `context_sensitive` |
|---|---|---|
| NONE / CONTACT_START / TAP | NO_RESPONSE | NO_RESPONSE |
| PRESS | WARM_SLOW | WARM_SLOW |
| SUSTAINED_HOLD | WARM_SLOW | MAINTAIN |
| STROKE (reserved) | WARM_SLOW | WARM_MODERATE |
| RELEASE | RETURN_TO_BASELINE | RETURN_TO_BASELINE |
| EXCESSIVE_INPUT / INVALID_INPUT | NO_RESPONSE | NO_RESPONSE |

Fixed mode requests the same warmth for every qualifying ongoing contact regardless of class.
Both conditions still classify and log all input. Contact-start waits for the next sample to qualify;
a short contact can briefly enter PRESS before TAP is recognized on release.
The single force-channel fixture cannot establish strokes; do not claim stroke detection from this build.
The vocabulary and mapping are calibration starting points, not a claim of perceptible thermal differences.

Hold the hardware, surface, starting-temperature range, room conditions, duration, participant instructions,
and independent safety limits constant. Only response-selection logic changes. The host refuses to record
a condition that differs from the device-reported condition. Rebuild/reboot firmware between conditions.

## Calibration gate (not scored)

1. Record untouched baselines and repeated short touches, presses, holds, and releases.
2. Inspect raw/filtered traces, classification stability, drift, and false detections. Preserve calibration logs privately.
3. Establish at least three repeatable interaction classes; validate additional sensing before enabling stroke detection.
4. Characterize heating/cooling, sensor lag, overshoot, and perceptibility off-body.
5. Verify closed-loop control, manual shutdown, invalid/stale sensor handling, heating timeout, communication-loss behavior
   if a remote controller is used, and an independent hardware cutoff before human-contact tests.
6. Freeze the tested thresholds, response profiles, and safety configuration for a formal run; reference the private
   calibration record in the operator's private trial notes. Do not publish withheld thresholds or gains.

The current software passes none of the hardware readiness gates by itself. The 35°C/5-second guard fixtures
are only for exercising code paths, not validated human-contact settings. GPIO outputs are absent. Real sensor
freshness, shutdown wiring, heartbeat monitoring, thermal profiles, and physical execution feedback remain unimplemented.

## Trial procedure

Use one trial ID per condition and a common session ID per paired run. Mark calibration separately from formal trials.
Assign A/B order before testing, randomized or counterbalanced across participants, and keep the active condition
hidden from participants where practical. Keep assignment/pseudonym records private.

1. Return the surface to the calibrated starting-temperature range.
2. Begin a new log with trial ID, actual condition, phase, and optional participant pseudonym.
3. Ask the participant to interact naturally, including brief touch, press, hold, and release; request strokes only
   after that sensing capability has been established.
4. Allow approximately 2–3 minutes; end the log and collect ratings immediately.
5. Reset to the same baseline and run the other condition with a different trial ID/output file.
6. Record failures, exclusions, unexpected thermal behavior, and comparative feedback; never discard failed trials silently.

## Ratings and interpretation

After each condition, rate 1 (not at all) to 7 (very strongly): responsive; intentional; connected to how I touched it;
meaningfully predictable; alive/agent-like; affected by my actions; and desire to continue.
Ask: “What, if anything, did you think the object was responding to?”
After both, ask which felt more responsive, intentional, natural, and preferable, and what pattern they noticed.
Avoid explaining the mapping or introducing companion/relationship framing beforehand.

Define criteria before examining results: reliable classification, repeatable bounded physical responses, correct
requested-versus-executed logs, and context-sensitive improvement on the combined responsive/intentional/action-connected
ratings. Preference and unprompted recognition of touch-dependent behavior provide secondary evidence.
Small exploratory samples do not establish statistical significance. Variation perceived as randomness is not success.

## Required record

Log time, trial ID, condition, raw/filtered input, classified event, confidence (null until calibrated), contact duration,
intensity, surface-temperature channel, requested response, safety approval, executed response, clamp/rejection reason,
and heater output. See [`../data/schema.md`](../data/schema.md) for exact paths and units.

Never overwrite a request with the safety fallback. Never label a safety approval as physical execution.
Synthetic examples must remain clearly marked.
