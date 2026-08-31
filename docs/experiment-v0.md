# V0 Experiment Plan

## Scope

V0 tests a small touch/thermal system, not a full robot.

Planned hardware:

- one touch surface
- force / pressure sensing
- capacitive or proximity sensing
- temperature sensing
- one regulated thermal zone
- optional one-axis motor output
- local controller
- host-side logging

## Stage 1 — sensor characterization

Collect repeated examples of:

- light contact
- sustained contact
- rapid / high-force contact
- release

Record raw measurements first. Do not assign social meaning to the contact classes.

Questions:

- Are the signals stable enough to distinguish these events?
- Does capacitive sensing add useful information beyond force?
- How much variation appears across repeated trials?

## Stage 2 — bounded motor response

Add one simple motor response after event classification is repeatable.

Log:

- detected event
- requested response
- executed response
- latency
- any safety clamp or rejection

## Stage 3 — thermal response

Characterize the thermal zone off-body before human-contact testing.

Measure:

- warm-up time
- steady-state behavior
- overshoot
- cool-down time
- sensor lag
- cutoff behavior

Human-contact heating comes later.

## Stage 4 — higher-level agent

Expose semantic interaction events to a higher-level agent.

The agent may request only responses allowed by the local controller.

Raw conversation does not go to the embedded controller.

## Planned perception comparison

After the hardware is stable, compare:

- **fixed mapping** — the same valid contact gets the same thermal behavior
- **context-sensitive mapping** — thermal behavior depends on the interpreted interaction state

Primary measure:

> The system's physical responses felt intentional.

This experiment tests the response mapping, not whether one condition is simply warmer.

## Not in V0

- whole-body actuation
- unrestricted model control
- emotional-state detection
- identity authentication from touch alone
- learned low-level safety control
- human lifting
