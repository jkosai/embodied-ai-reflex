#include "responses.h"

RequestedResponse choose_response(ContactEvent event, Condition condition) {
  if (event == ContactEvent::RELEASE) return RequestedResponse::RETURN_TO_BASELINE;
  if (condition == Condition::FIXED) {
    return (event == ContactEvent::PRESS || event == ContactEvent::SUSTAINED_HOLD || event == ContactEvent::STROKE)
        ? RequestedResponse::WARM_SLOW : RequestedResponse::NO_RESPONSE;
  }
  if (condition != Condition::CONTEXT_SENSITIVE) return RequestedResponse::NO_RESPONSE;
  switch (event) {
    case ContactEvent::PRESS: return RequestedResponse::WARM_SLOW;
    case ContactEvent::SUSTAINED_HOLD: return RequestedResponse::MAINTAIN;
    case ContactEvent::STROKE: return RequestedResponse::WARM_MODERATE;
    default: return RequestedResponse::NO_RESPONSE;
  }
}

bool is_heating(RequestedResponse response) {
  return response == RequestedResponse::WARM_SLOW || response == RequestedResponse::WARM_MODERATE
      || response == RequestedResponse::MAINTAIN;
}

const char* response_name(RequestedResponse response) {
  switch (response) {
    case RequestedResponse::WARM_SLOW: return "WARM_SLOW";
    case RequestedResponse::WARM_MODERATE: return "WARM_MODERATE";
    case RequestedResponse::MAINTAIN: return "MAINTAIN";
    case RequestedResponse::RETURN_TO_BASELINE: return "RETURN_TO_BASELINE";
    default: return "NO_RESPONSE";
  }
}

const char* condition_name(Condition condition) {
  return condition == Condition::FIXED ? "fixed" : "context_sensitive";
}
