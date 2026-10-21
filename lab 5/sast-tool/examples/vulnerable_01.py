"""Intentionally vulnerable demo source; never use these patterns in production."""

import pickle

password = "123456"


def evaluate_user_expression(user_data):
    return eval(user_data)  # SAST should flag eval.


def load_untrusted_payload(payload):
    return pickle.loads(payload)  # SAST should flag unsafe deserialization.
