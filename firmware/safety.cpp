#include "safety.h"

// Simulation-only placeholder. Not a validated human-contact limit.
static const float SIMULATED_MAX_TEMP_C = 35.0f;

void safety_init() {
}

SafetyDecision safety_validate(
  RequestedResponse requested,
  const SensorFrame& frame
) {
  SafetyDecision d;
  d.approved_response = requested;
  d.intervention = false;
  d.reason = nullptr;

  if (!frame.valid) {
    d.approved_response = RequestedResponse::NONE;
    d.intervention = true;
    d.reason = "invalid_sensor_data";
    return d;
  }

  if ((requested == RequestedResponse::WARM_LOW ||
       requested == RequestedResponse::WARM_MEDIUM) &&
      frame.temperature_c >= SIMULATED_MAX_TEMP_C) {
    d.approved_response = RequestedResponse::NONE;
    d.intervention = true;
    d.reason = "simulated_temperature_limit";
  }

  return d;
}
