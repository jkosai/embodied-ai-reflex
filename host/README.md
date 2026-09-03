# Host Logger

The logger can be used before any hardware exists.

## Simulation

```powershell
python logger.py --simulate --condition fixed --session-id session-demo --trial-id trial-A --output ..\data\raw\trial-A.jsonl
python logger.py --simulate --condition context_sensitive --session-id session-demo --trial-id trial-B --output ..\data\raw\trial-B.jsonl
```

This generates schema-v0.4 JSONL from deterministic sensor traces sampled at a virtual 100 ms interval.
Runtime speed does not change contact duration or event classification. It does not simulate heat transfer.

Use `--scenario overtemperature`, `--scenario sensor_fault`, or `--scenario timeout` to exercise rejection paths.
Use at least 80 frames for the default timeout fixture. No scenario physically actuates anything.
`--frames` limits accepted frames in either input mode.

Session/trial IDs default to newly generated values. `--participant-id` is optional and defaults to null;
use a pseudonym only. `--phase calibration` is the default; `--phase formal` identifies scored trials.
`--device-id` and `--operator-note` are optional. Never put private details in a public example or operator note.
Each invocation is one trial/episode (episode index 0). Use distinct trial IDs/output paths per condition.
Existing output files cause an error, preserving original records.

## Serial mode

After the ESP32 is connected:

```powershell
pip install pyserial
python logger.py --serial COM3 --condition context_sensitive --trial-id bench-B --frames 1200 --output ..\data\raw\bench-B.jsonl
```

Replace `COM3` with the actual serial port.

The current firmware still emits simulated measurements even over a real serial connection.
The logger preserves the device's `mode`; serial transport does not imply real hardware data.
Boot/status lines and malformed JSON are skipped. Unversioned/incomplete telemetry, inconsistent execution
flags, and device/host condition mismatches stop recording rather than silently mislabeling a trial.
Upgrade the firmware and logger together; old v0.3 input is not silently converted.

Build `esp32-s3-devkitc-1` for `context_sensitive` or `esp32-s3-fixed` for `fixed` with PlatformIO.
Switching conditions currently requires rebuilding/rebooting the device between trials.
The host condition flag validates telemetry; it is not a command that changes device policy.

## Boundary

The microcontroller emits a compact device-oriented JSON line.

The host logger owns:

- canonical experiment schema
- episode/frame indexing
- session and trial IDs
- file output
- future higher-level context fields

This keeps the firmware small while allowing the experiment schema to evolve.

The firmware owns sensor → event → request → safety → output. `pipeline.py` is the matching non-actuating
reference for host-only tests. Neither path implements an external-agent command channel yet.
