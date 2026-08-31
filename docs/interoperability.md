# Interoperability

## Device boundary

The physical prototype should expose a simple boundary:

```text
observations out -> policy or logic -> bounded actions in
```

The device API should describe the patch itself: what it can sense, what it can safely do, and what limits apply.

## LeRobot

LeRobot is a useful compatibility target because it supports custom robot interfaces, datasets, and multiple policy families.

A future adapter may expose the patch through LeRobot's robot interface.

The patch should still work without LeRobot.

## MolmoAct 2

MolmoAct 2 is one policy candidate for later testing.

It is not part of the V0 safety loop and should not require changes to the device firmware or canonical data model.

## Anti-lock-in test

If replacing a policy requires changing the patch firmware, safety architecture, or canonical experiment format, the integration is too tightly coupled.

If replacing it requires only a new adapter or exporter, the boundary is doing its job.
