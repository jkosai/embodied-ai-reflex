#include "events.h"

static bool was_touching = false;
static float last_duration = 0;

ContactEvent classify_contact(const SensorFrame& frame) {
  if (!sensors_valid(frame)) {
    was_touching = false;
    last_duration = 0;
    return ContactEvent::INVALID_INPUT;
  }

  bool touching = frame.filtered_sensor_value > 0.05f;

  if (!touching && was_touching) {
    was_touching = false;
    return last_duration < 0.3f ? ContactEvent::TAP : ContactEvent::RELEASE;
  }

  if (!touching) {
    was_touching = false;
    return ContactEvent::NONE;
  }

  bool started = !was_touching;
  was_touching = true;
  last_duration = frame.contact_duration_s;

  if (frame.filtered_sensor_value > 0.80f || frame.force_rate > 0.45f)
    return ContactEvent::EXCESSIVE_INPUT;

  if (started) return ContactEvent::CONTACT_START;

  if (frame.contact_duration_s >= 1.0f)
    return ContactEvent::SUSTAINED_HOLD;

  return ContactEvent::PRESS;
}

const char* contact_event_name(ContactEvent event) {
  switch (event) {
    case ContactEvent::CONTACT_START: return "CONTACT_START";
    case ContactEvent::TAP: return "TAP";
    case ContactEvent::PRESS: return "PRESS";
    case ContactEvent::SUSTAINED_HOLD: return "SUSTAINED_HOLD";
    case ContactEvent::STROKE: return "STROKE";
    case ContactEvent::EXCESSIVE_INPUT: return "EXCESSIVE_INPUT";
    case ContactEvent::INVALID_INPUT: return "INVALID_INPUT";
    case ContactEvent::RELEASE: return "RELEASE";
    default: return "NONE";
  }
}
