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
