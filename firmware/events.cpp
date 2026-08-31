#include "events.h"

static bool was_touching = false;

ContactEvent classify_contact(const SensorFrame& frame) {
  if (!frame.valid) return ContactEvent::NONE;

  bool touching = frame.force > 0.05f;

  if (!touching && was_touching) {
    was_touching = false;
    return ContactEvent::RELEASE;
  }

  if (!touching) {
    was_touching = false;
    return ContactEvent::NONE;
  }

  was_touching = true;

  if (frame.force > 0.80f || frame.force_rate > 0.45f)
    return ContactEvent::RAPID_OR_HIGH_FORCE;

  if (frame.contact_duration_s >= 1.0f)
    return ContactEvent::SUSTAINED_CONTACT;

  return ContactEvent::LIGHT_CONTACT;
}

const char* contact_event_name(ContactEvent event) {
  switch (event) {
    case ContactEvent::LIGHT_CONTACT: return "light_contact";
    case ContactEvent::SUSTAINED_CONTACT: return "sustained_contact";
    case ContactEvent::RAPID_OR_HIGH_FORCE: return "rapid_or_high_force";
    case ContactEvent::RELEASE: return "release";
    default: return "none";
  }
}
