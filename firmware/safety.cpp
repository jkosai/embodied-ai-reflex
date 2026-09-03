#include "safety.h"

// Simulation fixtures, NOT validated human-contact limits.
static const float SIMULATED_MAX_TEMP_C = 35.0f;
static const unsigned long SIMULATED_MAX_HEATING_MS = 5000UL;
static bool heating = false;
static unsigned long heating_start_ms = 0;
static const char* fault = nullptr;

void safety_init() {
  heating = false;
  heating_start_ms = 0;
  fault = nullptr;
}

SafetyDecision safety_validate(RequestedResponse requested, const SensorFrame& frame) {
  if (!fault) {
    if (frame.manual_stop) fault = "manual_stop_or_unknown";
    else if (!frame.communication_ok) fault = "communication_lost_or_unknown";
    else if (!sensors_valid(frame)) fault = "invalid_sensor_data";
    else if (frame.temperature_c >= SIMULATED_MAX_TEMP_C) fault = "simulated_temperature_limit";
    else if (frame.filtered_sensor_value > 0.8f || frame.force_rate > 0.45f) fault = "excessive_input";
    else if (requested != RequestedResponse::NO_RESPONSE && requested != RequestedResponse::RETURN_TO_BASELINE
             && !is_heating(requested)) fault = "invalid_request";
    else if (is_heating(requested)) {
      if (!heating) {
        heating = true;
        heating_start_ms = frame.timestamp_ms;
      }
      // Unsigned elapsed-time subtraction also handles millis() rollover.
      if (frame.timestamp_ms - heating_start_ms >= SIMULATED_MAX_HEATING_MS)
        fault = "simulated_heating_timeout";
    } else heating = false;
  }
  // Faults latch until safety_init at boot. Policy/condition cannot clear them.
  return {fault ? RequestedResponse::NO_RESPONSE : requested, fault != nullptr, fault};
}
