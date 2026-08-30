# V0 Experiment Plan

## Primary question

Can multimodal touch sensing support repeatable classification of physical contact events and trigger bounded local reflexes without a large model in the fast control loop?

## Independent variables

Initial physical-contact classes:
- light contact
- sustained gentle contact
- rapid/high-force contact
- release

Later extension:
- person identity label / confidence
- compact conversation-context state

## Outputs

Log at minimum:
- timestamp
- raw capacitance
- raw force
- force rate of change
- contact duration
- measured temperature
- semantic event
- requested response
- executed response
- safety intervention / clamp, if any

## Initial procedure

1. Characterize sensor baselines and noise.
2. Collect repeated examples of each contact class.
3. Establish deterministic thresholds / simple classifier for V0.
4. Verify classification repeatability before enabling motor or heat output.
5. Add bounded single-axis motor response.
6. Characterize thermal response off-body.
7. Add thermal feedback and independent cutoff.
8. Only then evaluate human-contact thermal behavior.

## Planned human-perception comparison

Once the hardware behavior is repeatable, compare a fixed response mapping against a context-sensitive mapping using the same hardware and comparable safe thermal exposure. Primary perception measure: whether the system's physical response feels intentional. Secondary measures can include responsiveness, agent-likeness, appropriateness, physical presence, pleasantness, and predictability.
