# Research Principles

Five rules for the project:

1. **Local code owns physical safety limits.**
2. **Record requested and executed behavior separately.**
3. **Do not infer emotion, intent, identity, or diagnosis directly from sensor measurements.**
4. **Preserve raw measurements, timestamps, hardware/protocol versions, and failed trials.**
5. **Treat novelty claims as provisional until prior art has been reviewed.**

Additional working assumptions:

- LeRobot is an export/integration target, not the internal source of truth.
- Missing sensor or wearable values are `null`, not zero.
- Raw conversation does not go to the embedded controller.
- Public documentation should distinguish planned behavior from demonstrated behavior.
