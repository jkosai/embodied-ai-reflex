#include <Arduino.h>
#include "sensors.h"
#include "events.h"
#include "outputs.h"
#include "safety.h"

// Rebuild/reboot between conditions; the host checks this device-reported value.
#ifdef V0_FIXED_CONDITION
static const Condition condition = Condition::FIXED;
#else
static const Condition condition = Condition::CONTEXT_SENSITIVE;
#endif

void setup() {
  Serial.begin(115200);
  sensors_init();
  outputs_init();
  safety_init();
  Serial.println("{\"status\":\"boot\",\"mode\":\"simulated-prehardware\"}");
}

void loop() {
  SensorFrame frame = sensors_read();
  ContactEvent event = classify_contact(frame);
  RequestedResponse requested = choose_response(event, condition);
  SafetyDecision decision = safety_validate(requested, frame);
  ExecutedResponse executed = outputs_execute(decision);

  emit_serial_frame(frame, condition, event, requested, decision, executed);
  delay(100);
}
