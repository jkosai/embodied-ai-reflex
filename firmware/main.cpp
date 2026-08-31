#include "sensors.h"
#include "events.h"
#include "outputs.h"
#include "safety.h"

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
  RequestedResponse requested = choose_local_demo_response(event);
  SafetyDecision decision = safety_validate(requested, frame);
  ExecutedResponse executed = outputs_execute(decision);

  emit_serial_frame(frame, event, requested, decision, executed);
  delay(100);
}
