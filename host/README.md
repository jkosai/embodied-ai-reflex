# Host Logger

The logger can be used before any hardware exists.

## Simulation

```powershell
python logger.py --simulate --output ..\data\examples\v0_simulated_session.jsonl
```

This generates schema-v0.3 JSONL using fake touch events.

## Serial mode

After the ESP32 is connected:

```powershell
pip install pyserial
python logger.py --serial COM3 --output v0_real_session.jsonl
```

Replace `COM3` with the actual serial port.

## Boundary

The microcontroller emits a compact device-oriented JSON line.

The host logger owns:

- canonical experiment schema
- episode/frame indexing
- session and trial IDs
- file output
- future higher-level context fields

This keeps the firmware small while allowing the experiment schema to evolve.
