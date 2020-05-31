"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from rest_framework_jwt.settings import api_settings


def get_token_for_user(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
