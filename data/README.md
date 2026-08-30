# Data

This directory contains **public, sanitized experiment data only**.

The canonical V0 collection format is project-owned and versioned in [`schema.md`](schema.md). It is designed to retain episode/frame, observation, action, timestamp, and task concepts so data can later be exported into LeRobotDataset v3 or other robot-learning formats.

## Rules

Do not commit:

- raw conversation logs
- names or direct identifiers
- API keys or authentication tokens
- biometric templates
- private relationship data
- unpublished calibration thresholds or control parameters
- unreviewed raw dumps from connected services or wearables

Do not discard original measurements simply to match a downstream ML format. Conversion into LeRobot or another ecosystem should happen through an exporter.

Large raw logs should remain outside the public repository unless they have been explicitly reviewed for privacy, safety, and IP disclosure.
