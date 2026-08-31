# Data

Public, sanitized experiment data only.

Use [`schema.md`](schema.md) for the canonical V0 record.

Do not commit:

- raw conversation
- names or direct identifiers
- credentials or API keys
- biometric templates
- persistent phone/watch identifiers
- raw wearable exports
- unnecessary physiological history
- unpublished calibration thresholds or control parameters

Missing values are `null`, not zero.

Keep original experiment records. Convert to LeRobot or another downstream format with an exporter rather than replacing the source data.

The `examples/` directory may contain generated or sanitized example sessions used to test the logging pipeline.
