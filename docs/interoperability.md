# Interoperability Strategy

## Goal

Keep the embodiment interface independent from any one model vendor, investor, robot platform, or training stack.

The physical prototype should expose a stable boundary:

**observations out → policy/logic → bounded actions in**

The implementation behind either side of that boundary may change.

## Why LeRobot is relevant

LeRobot is an open-source robotics framework maintained in the Hugging Face ecosystem. It provides:

- hardware abstractions for custom robots;
- standardized observation/action interfaces;
- dataset tooling;
- multiple policy implementations rather than a single model family.

The project is using LeRobot as a **compatibility target**, not as a hard dependency.

A future patch implementation may expose itself through a custom LeRobot `Robot` interface, but the patch should remain usable without LeRobot.

## MolmoAct 2 position

MolmoAct 2 is one candidate learned policy.

Ai2 has released MolmoAct 2 code, training data, and LeRobot integration so it can be adapted to new hardware and tasks. That makes it useful for experimentation, especially while the project is physically small.

However:

- MolmoAct 2 is not part of the V0 safety loop.
- The project does not require MolmoAct 2 to function.
- The observation/action boundary should support evaluation of other policies.
- Model-specific transformations belong in adapters, not in the physical-device API.

## Anti-lock-in rules

1. **Device API first.** Define the patch in terms of its own observations, safe capabilities, and limits.
2. **Adapters second.** LeRobot, MolmoAct 2, or another policy stack connects through an adapter.
3. **Canonical raw data stays ours.** Store the original experiment representation and export into downstream formats.
4. **Do not encode a model's quirks into firmware.**
5. **Safety remains local and model-independent.**
6. **Keep policy comparisons possible.** A future experiment should be able to compare deterministic logic, MolmoAct 2, or another policy over the same embodiment interface.

## Investor framing

The company/research thesis is not:

> We are building a MolmoAct 2 application.

It is:

> We are developing a safe embodiment and reflex interface for persistent AI agents, with open compatibility across embodied-policy ecosystems.

Using LeRobot and MolmoAct 2 demonstrates that the prototype can plug into modern open robotics infrastructure. It should be presented as evidence of interoperability and execution speed, not as strategic dependence on Ai2.

## Data portability

LeRobotDataset v3 is currently a useful export target because it standardizes multimodal time-series data, actions, timestamps, task descriptions, and episode metadata.

The canonical V0 dataset remains project-owned and schema-versioned. Conversion to LeRobotDataset v3 should be an exporter. If a different ecosystem becomes strategically important later, another exporter can be added without re-running the original experiment.
