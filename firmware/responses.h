#pragma once
#include "events.h"

enum class Condition { FIXED, CONTEXT_SENSITIVE };
enum class RequestedResponse { NO_RESPONSE, WARM_SLOW, WARM_MODERATE, MAINTAIN, RETURN_TO_BASELINE };

RequestedResponse choose_response(ContactEvent event, Condition condition);
const char* response_name(RequestedResponse response);
const char* condition_name(Condition condition);
bool is_heating(RequestedResponse response);

struct SafetyDecision {
  RequestedResponse approved_response;
  bool intervention;
  const char* reason;
};
