#pragma once
#include "sensors.h"

enum class ContactEvent {
  NONE,
  CONTACT_START,
  TAP,
  PRESS,
  SUSTAINED_HOLD,
  STROKE, // Reserved; current single-force classifier cannot establish strokes.
  EXCESSIVE_INPUT,
  INVALID_INPUT,
  RELEASE
};

ContactEvent classify_contact(const SensorFrame& frame);
const char* contact_event_name(ContactEvent event);
