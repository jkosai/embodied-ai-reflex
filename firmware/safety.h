#pragma once
#include "sensors.h"
#include "responses.h"

void safety_init();
SafetyDecision safety_validate(
  RequestedResponse requested,
  const SensorFrame& frame
);
