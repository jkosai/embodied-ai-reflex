# Embodied AI Reflex Layer

Experimental hardware/software for testing context-sensitive physical responses from persistent AI agents.

## What V0 is

V0 is a small benchtop touch/thermal prototype.

```text
touch sensors -> local event classification -> bounded response -> log
                                      ^
                                      |
                         higher-level agent request
```

The local controller owns actuator safety limits. A higher-level agent may request from a restricted response set, but it does not directly control heater power, motor torque, or other unrestricted actuator values.

## Current status

**Pre-hardware implementation / procurement.**

The repository now includes:

- a provisional wiring plan
- an ESP32 firmware skeleton with simulated sensor input
- separated sensing, event classification, safety, and output modules
- a host-side Python logger
- a schema-v0.3 simulated JSONL session

No physical hardware results are claimed yet.

Current V0 scope:

- one touch surface
- force / pressure sensing
- capacitive or proximity sensing
- surface temperature sensing
- one low-voltage thermal zone
- optional single-axis motor response
- structured event logging
- later higher-level agent integration

Whole-body robotics, learned reflex control, and autonomous humanoid behavior are out of scope for V0.

## Run the pre-hardware logger

No hardware is required:

```powershell
cd host
python logger.py --simulate --output ..\data\examples\v0_simulated_session.jsonl
```

The logger writes canonical schema-v0.3 records.

See [`host/README.md`](host/README.md).

## First questions

1. Can the selected sensors distinguish a small set of contact events repeatably?
2. Can the local controller execute bounded motor and thermal responses reliably?
3. Can requested and executed responses be logged separately?
4. Once the hardware is stable, does context-sensitive response mapping change how intentional or responsive the system feels?

## Safety boundary

Local code owns thermal, motion, force, timeout, and fault limits.

Conversation context, identity signals, and wearable physiology may influence higher-level response selection later, but they do not relax local safety limits.

See [`docs/safety.md`](docs/safety.md).

## Data

The canonical experiment format is project-owned and versioned in [`data/schema.md`](data/schema.md).

It keeps episode/frame structure, observations, requested behavior, executed behavior, timestamps, and safety interventions. A later exporter may convert the data to LeRobotDataset v3 or another robotics format.

## Interoperability

LeRobot is a compatibility target, not a dependency. MolmoAct 2 is one possible policy to evaluate later.

The device should remain usable with deterministic logic or other policy stacks through adapters.

See [`docs/interoperability.md`](docs/interoperability.md).

## Repository layout

```text
.
├── README.md
├── firmware/
│   ├── platformio.ini
│   ├── main.cpp
│   ├── sensors.*
│   ├── events.*
│   ├── outputs.*
│   └── safety.*
├── host/
│   ├── README.md
│   └── logger.py
├── data/
│   ├── README.md
│   ├── schema.md
│   └── examples/
│       └── v0_simulated_session.jsonl
└── docs/
    ├── experiment-v0.md
    ├── interoperability.md
    ├── log.md
    ├── prior-art.md
    ├── research-principles.md
    ├── safety.md
    └── wiring-v0.md
```

## Related work

This project does not claim novelty for tactile sensing, warm robot surfaces, robot reflexes, or learned manipulation individually.

Current references include:

- Zhou et al. (2026), tactile-reactive grippers  
  https://doi.org/10.1038/s44182-026-00079-y
- EmArm, whole-arm tactile sensing and adaptive manipulation  
  https://www.nature.com/articles/s44460-026-00097-1
- Del Dottore et al. (2026), distributed local reflex-like behavior  
  https://doi.org/10.1038/s42256-026-01230-y
- Hugging Face LeRobot  
  https://huggingface.co/docs/lerobot
- Ai2 MolmoAct 2  
  https://allenai.org/blog/molmoact2

See [`docs/prior-art.md`](docs/prior-art.md) for the preliminary tactile-HRI map.
