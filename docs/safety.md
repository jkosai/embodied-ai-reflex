# Safety Boundary

This project intentionally separates high-level AI policy from safety-critical execution.

## Immutable local constraints

The local controller owns:
- maximum heater temperature
- maximum heater duty cycle / power
- maximum motor speed
- maximum motor travel
- maximum force / torque where applicable
- response timeout
- fault handling
- sensor plausibility checks
- emergency stop / safe-stop behavior as hardware matures

These limits do not change based on identity, relationship, conversational state, or model output.

## Identity and authorization

Recognition and authorization are separate concepts.

A system may estimate who is interacting using multiple signals, but **recognition confidence does not automatically grant privileges**.

Public design principles:

- **Proximity is not authentication.** A nearby watch, phone, or other possession-based signal may contribute evidence, but must not by itself grant sensitive access.
- **No single signal is definitive.** Touch characteristics, wearable proximity, face, voice, or future credential mechanisms should be treated as inputs to a confidence-based identity process rather than as automatic proof.
- **Possession does not imply identity.** Another person wearing or carrying the primary user's device must not inherit the primary user's privileged access.
- **Social personalization and security authorization are separate.** The system may allow low-risk personalized behavior at a lower confidence threshold than it allows private-context access, configuration changes, account actions, or other privileged functions.
- **Identity uncertainty should degrade safely.** If identity confidence drops, privileged behavior should reduce or stop rather than silently remain unlocked.

Specific multimodal fusion logic, thresholds, credential methods, and authorization policies are intentionally not specified in the public repository at this stage.

## Agent permissions

A higher-level agent may request only approved semantic responses from a bounded vocabulary. It may not directly set unrestricted actuator values.

## Fail-safe expectations

Invalid command, missing sensor data, implausible data, communication loss, overtemperature, or controller fault should resolve to a safe state locally.

## Thermal testing

Thermal characterization begins off-body. Human-contact heating requires closed-loop measurement plus independent hardware protection selected from measured heater/surface behavior.
