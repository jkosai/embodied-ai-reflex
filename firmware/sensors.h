#pragma once

struct SensorFrame {
  unsigned long timestamp_ms;
  float raw_sensor_value;
  float filtered_sensor_value;
  float capacitance;
  float force;
  float force_rate;
  float temperature_c;
  float contact_duration_s;
  bool valid;
  bool communication_ok;
  bool manual_stop;
};

void sensors_init();
SensorFrame sensors_read();
bool sensors_valid(const SensorFrame& frame);
