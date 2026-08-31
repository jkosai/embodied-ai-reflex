#pragma once

struct SensorFrame {
  float capacitance;
  float force;
  float force_rate;
  float temperature_c;
  float contact_duration_s;
  bool valid;
};

void sensors_init();
SensorFrame sensors_read();
