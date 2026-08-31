# V0 Wiring Plan — Pre-Hardware Draft

Status: **provisional / pre-purchase**

This is a wiring plan, not a final schematic. Exact GPIOs, supply voltage, heater rating, driver, temperature sensor, and thermal cutoff must be confirmed from the actual parts before power is applied.

## Block diagram

```text
                        USB
                         |
                         v
                    +---------+
                    | ESP32-S3|
                    +---------+
                      |   |   \
                      |   |    \ digital / I2C
                      |   |     \
                      |   |      +-----------------> temperature sensor
                      |   |
                      |   +------------------------> capacitive sensor / electrode
                      |
                      +----------------------------> force / pressure sensor input

ESP32 GPIO (bounded request)
          |
          v
   +----------------+
   | MOSFET / driver| <--------- separate low-voltage heater supply
   +----------------+
          |
          v
   +----------------+
   | flexible heater|
   +----------------+
          |
          +----> surface temperature measured independently

Heater power path:
power source -> fuse / independent thermal cutoff -> heater driver -> heater
```

## Provisional signal map

Do **not** assign final GPIOs until the actual board and modules are in hand.

| Function | Interface | ESP32 connection | Status |
|---|---|---|---|
| Force / pressure sensor | analog or divider | `ADC_TBD` | TBD after sensor selection |
| Capacitive touch | I2C or digital | `I2C_TBD` / `GPIO_TBD` | TBD after module selection |
| Temperature sensor | I2C / 1-wire / analog | `BUS_TBD` | TBD after sensor selection |
| Heater enable / PWM | digital output to MOSFET driver | `GPIO_TBD` | TBD after driver selection |
| Independent thermal cutoff | hardware power path | **not software-controlled** | required before human-contact heating |

## Power rules

- Do not power the heater directly from an ESP32 GPIO.
- Do not assume the ESP32 USB rail can safely supply the heater.
- Heater voltage/current must come from the actual heater specification.
- If the heater uses a separate supply and the driver is non-isolated, confirm the required ground reference from the selected topology.
- Add an independent thermal cutoff in the heater power path before human-contact tests.
- First thermal tests are off-body.

## First bench bring-up order

1. ESP32 only.
2. Add force sensor; verify raw readings.
3. Add capacitive sensor; verify raw readings.
4. Add temperature sensor; compare with room temperature.
5. Connect driver **without heater power** and verify control logic.
6. Add heater power with the heater off-body.
7. Verify software cutoff behavior.
8. Verify independent cutoff behavior.
9. Only after measured thermal behavior is stable should human-contact testing be considered.

## Open hardware questions

- Which exact ESP32-S3 board?
- Which force sensor / FSR?
- Which capacitive module?
- Which temperature sensor?
- Heater rated voltage, resistance, and maximum current?
- MOSFET/driver model and gate-drive requirements?
- Independent thermal cutoff type and trip point?
- Heater power source and fuse rating?
