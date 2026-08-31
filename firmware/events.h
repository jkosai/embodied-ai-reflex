#pragma once
#include "sensors.h"

enum class ContactEvent {
  NONE,
  LIGHT_CONTACT,
  SUSTAINED_CONTACT,
  RAPID_OR_HIGH_FORCE,
  RELEASE
};

ContactEvent classify_contact(const SensorFrame& frame);
const char* contact_event_name(ContactEvent event);
