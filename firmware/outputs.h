#pragma once
#include "responses.h"

struct ExecutedResponse {
  RequestedResponse response;
  bool executed;
  float heater_output;
  bool safe_state_entered;
};

void outputs_init();
ExecutedResponse outputs_execute(const SafetyDecision& decision);

void emit_serial_frame(
  const SensorFrame& frame,
  Condition condition,
  ContactEvent event,
  RequestedResponse requested,
  const SafetyDecision& decision,
  const ExecutedResponse& executed
);
