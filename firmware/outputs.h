#pragma once
#include "events.h"

enum class RequestedResponse {
  NONE,
  WARM_LOW,
  WARM_MEDIUM,
  MOTOR_AWAY
};

struct SafetyDecision {
  RequestedResponse approved_response;
  bool intervention;
  const char* reason;
};

struct ExecutedResponse {
  RequestedResponse response;
  bool executed;
};

void outputs_init();
RequestedResponse choose_local_demo_response(ContactEvent event);
ExecutedResponse outputs_execute(const SafetyDecision& decision);
const char* response_name(RequestedResponse response);

void emit_serial_frame(
  const SensorFrame& frame,
  ContactEvent event,
  RequestedResponse requested,
  const SafetyDecision& decision,
  const ExecutedResponse& executed
);
