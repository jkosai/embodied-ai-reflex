#include <Arduino.h>
#include "sensors.h"

static float simulated_force = 0.0f;
static float previous_force = 0.0f;
static unsigned long contact_start_ms = 0;

void sensors_init() {
  // Replace with real sensor initialization after hardware selection.
}

SensorFrame sensors_read() {
  // Pre-hardware simulation:
  // no contact -> contact -> sustained contact -> release.
  unsigned long phase = (millis() / 2000UL) % 4UL;

  if (phase == 0) simulated_force = 0.0f;
  if (phase == 1) simulated_force = 0.25f;
  if (phase == 2) simulated_force = 0.55f;
  if (phase == 3) simulated_force = 0.0f;

  bool touching = simulated_force > 0.05f;

  if (touching && contact_start_ms == 0) contact_start_ms = millis();
  if (!touching) contact_start_ms = 0;

  SensorFrame f;
  f.capacitance = touching ? 0.7f : 0.1f;
  f.force = simulated_force;
  f.force_rate = simulated_force - previous_force;
  f.temperature_c = 22.0f;
  f.contact_duration_s = touching && contact_start_ms
      ? (millis() - contact_start_ms) / 1000.0f
      : 0.0f;
  f.valid = true;

  previous_force = simulated_force;
  return f;
}
