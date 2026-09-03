#include <Arduino.h>
#include <math.h>
#include "outputs.h"

void outputs_init() {
  // No hardware pins are configured; this build cannot actuate a heater.
}

ExecutedResponse outputs_execute(const SafetyDecision& decision) {
  // Approval is not execution. The simulated output remains off.
  return {RequestedResponse::NO_RESPONSE, false, 0.0f, decision.intervention};
}

static void number(float value, int digits = 3) {
  if (isfinite(value)) Serial.print(value, digits);
  else Serial.print("null");
}

void emit_serial_frame(const SensorFrame& frame, Condition condition, ContactEvent event,
                       RequestedResponse requested, const SafetyDecision& decision,
                       const ExecutedResponse& executed) {
  Serial.print("{\"record_type\":\"frame\",\"mode\":\"simulated-prehardware\",\"condition\":\"");
  Serial.print(condition_name(condition));
  Serial.print("\",\"device_timestamp_s\":"); number(frame.timestamp_ms / 1000.0f);
  Serial.print(",\"capacitance\":"); number(frame.capacitance);
  Serial.print(",\"force\":"); number(frame.force);
  Serial.print(",\"raw_sensor_value\":"); number(frame.raw_sensor_value);
  Serial.print(",\"filtered_sensor_value\":"); number(frame.filtered_sensor_value);
  Serial.print(",\"force_rate\":"); number(frame.force_rate);
  Serial.print(",\"temperature_c\":"); number(frame.temperature_c, 2);
  Serial.print(",\"contact_duration_s\":"); number(frame.contact_duration_s);
  Serial.print(",\"valid\":"); Serial.print(sensors_valid(frame) ? "true" : "false");
  Serial.print(",\"classified_event\":\""); Serial.print(contact_event_name(event));
  Serial.print("\",\"event_confidence\":null,\"interaction_intensity\":");
  if (sensors_valid(frame)) number(frame.filtered_sensor_value); else Serial.print("null");
  Serial.print(",\"requested_response\":\""); Serial.print(response_name(requested));
  Serial.print("\",\"approved_response\":\""); Serial.print(response_name(decision.approved_response));
  Serial.print("\",\"safety_clamp\":"); Serial.print(decision.intervention ? "true" : "false");
  Serial.print(",\"safety_reason\":");
  if (decision.reason) {
    Serial.print("\""); Serial.print(decision.reason); Serial.print("\"");
  } else Serial.print("null");
  Serial.print(",\"executed_response\":");
  if (executed.executed) {
    Serial.print("\""); Serial.print(response_name(executed.response)); Serial.print("\"");
  } else Serial.print("null");
  Serial.print(",\"physically_executed\":"); Serial.print(executed.executed ? "true" : "false");
  Serial.print(",\"heater_output\":"); number(executed.heater_output);
  Serial.print(",\"safe_state_entered\":"); Serial.print(executed.safe_state_entered ? "true" : "false");
  Serial.println("}");
}
