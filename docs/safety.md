# Safety Boundary

The local controller owns all physical safety limits.

## Local-only limits

Examples include:

- maximum surface temperature
- heater power / duty-cycle limits
- motor speed and travel
- force / torque limits where applicable
- timeouts
- sensor plausibility checks
- fault handling
- safe-stop behavior

These limits do not change because of model output, identity, conversation context, or physiological data.

## Higher-level agent

A higher-level agent may request only approved semantic responses.

It may not directly set unrestricted actuator values.

Requested and executed responses are logged separately so clamps, substitutions, and rejections remain visible.

The public V0 pipeline also preserves `safety.approved_response` between request and execution.
The non-actuating output adapter reports `executed_response: null`, `physically_executed: false`, and
`heater_output: 0` even when safety approves a warming request. The logger never substitutes approval for execution.

## Current simulation guards

The firmware and host reference reject invalid/non-finite/out-of-range sensor data, excessive input,
temperature at or above a simulation fixture limit, continuous heating intent beyond a fixture timeout,
manual-stop input, and unavailable communication. `MAINTAIN` counts as heating, and changing heating
response names cannot reset the timeout. Faults latch until explicit controller reinitialization.
Safety does not receive the experimental condition and its limits are identical in both modes.

The 35°C temperature threshold and five-second intent timeout are public simulation fixtures only.
They are not validated contact limits or unpublished calibration values. The output adapter has no heater GPIO.
Manual-stop and communication flags are injected test inputs; the firmware currently has no shutdown wiring,
sensor freshness watchdog, remote-agent transport, or heartbeat monitor. No software test verifies physical safety.

Real hardware integration must implement and measure those inputs, closed-loop thermal control and output
feedback, startup-off behavior, independent cutoff, and off-body fault tests before human-contact trials.
Resetting a latched fault requires operator investigation; response selection cannot authorize a reset.

## Identity

Recognition and authorization are separate.

A nearby phone, watch, touch pattern, face, voice, or other signal may contribute to identity confidence. No single signal automatically grants privileged access.

Someone carrying or wearing the primary user's device must not automatically inherit that user's permissions.

## Physiology

Wearable measurements such as heart rate may be passed to the higher-level agent as context.

They are not:

- proof of emotion
- proof of identity
- medical diagnosis
- inputs that change actuator safety limits

Stale or missing wearable data is treated as unavailable.

## Thermal testing

Thermal testing starts off-body.

Human-contact heating requires closed-loop temperature measurement and independent protection appropriate to the measured heater/surface behavior.
