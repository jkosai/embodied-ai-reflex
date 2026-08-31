#include <Arduino.h>
#include "outputs.h"

void outputs_init() {
  // Real GPIO initialization goes here after the hardware is selected.
}

RequestedResponse choose_local_demo_response(ContactEvent event) {
  // Deterministic placeholder logic, not the future AI policy.
  switch (event) {
    case ContactEvent::SUSTAINED_CONTACT:
      return RequestedResponse::WARM_LOW;
    case ContactEvent::RAPID_OR_HIGH_FORCE:
      return RequestedResponse::MOTOR_AWAY;
    default:
      return RequestedResponse::NONE;
  }
}

ExecutedResponse outputs_execute(const SafetyDecision& decision) {
  // Pre-hardware: no physical actuation.
  ExecutedResponse result;
  result.response = decision.approved_response;
  result.executed = false;
  return result;
}

const char* response_name(RequestedResponse response) {
  switch (response) {
    case RequestedResponse::WARM_LOW: return "warm_low";
    case RequestedResponse::WARM_MEDIUM: return "warm_medium";
    case RequestedResponse::MOTOR_AWAY: return "motor_away";
    default: return "none";
  }
}

void emit_serial_frame(
  const SensorFrame& frame,
  ContactEvent event,
  RequestedResponse requested,
  const SafetyDecision& decision,
  const ExecutedResponse& executed
) {
  Serial.print("{\"capacitance\":");
  Serial.print(frame.capacitance, 3);
  Serial.print(",\"force\":");
  Serial.print(frame.force, 3);
  Serial.print(",\"force_rate\":");
  Serial.print(frame.force_rate, 3);
  Serial.print(",\"temperature_c\":");
  Serial.print(frame.temperature_c, 2);
  Serial.print(",\"contact_duration_s\":");
  Serial.print(frame.contact_duration_s, 3);

  Serial.print(",\"event\":\"");
  Serial.print(contact_event_name(event));
  Serial.print("\"");

  Serial.print(",\"requested_response\":\"");
  Serial.print(response_name(requested));
  Serial.print("\"");

  Serial.print(",\"approved_response\":\"");
  Serial.print(response_name(decision.approved_response));
  Serial.print("\"");

  Serial.print(",\"safety_intervention\":");
  Serial.print(decision.intervention ? "true" : "false");

  Serial.print(",\"safety_reason\":");
  if (decision.reason) {
    Serial.print("\"");
    Serial.print(decision.reason);
    Serial.print("\"");
  } else {
    Serial.print("null");
  }

  Serial.print(",\"physically_executed\":");
  Serial.print(executed.executed ? "true" : "false");
  Serial.println("}");
}
