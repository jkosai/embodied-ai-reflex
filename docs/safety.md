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

## Agent permissions

A higher-level agent may request only approved semantic responses from a bounded vocabulary. It may not directly set unrestricted actuator values.

## Fail-safe expectations

Invalid command, missing sensor data, implausible data, communication loss, overtemperature, or controller fault should resolve to a safe state locally.

## Thermal testing

Thermal characterization begins off-body. Human-contact heating requires closed-loop measurement plus independent hardware protection selected from measured heater/surface behavior.
