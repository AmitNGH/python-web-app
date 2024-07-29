from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.routing import IntegerConverter

OK_RETURN_CODE = 200
UNSUPPORTED_MEDIA_TYPE_CODE = 415
UNPROCESSABLE_ENTITY_CODE = 422
INTERNAL_SERVER_ERROR_CODE = 500

USER_ID_INDEX_IN_DB = 1
USER_NAME_INDEX_IN_DB = 2
CREATION_DATE_INDEX_IN_DB = 3


def ok_response_template() -> tuple[dict, int]:
    return {'status': 'ok'}, OK_RETURN_CODE


def unprocessable_entity_response_template() -> tuple[dict, int]:
    return {'status': 'error'}, UNPROCESSABLE_ENTITY_CODE


def unsupported_media_type_response_template() -> tuple[dict, int]:
    return {'status': 'error'}, UNSUPPORTED_MEDIA_TYPE_CODE


def internal_server_error_response_template() -> tuple[dict, int]:
    return {'status': 'error'}, INTERNAL_SERVER_ERROR_CODE


# Attempts to extract json object from given request -
# Returns tuple containing if the operation was successful and the extracted json object
def extract_json_from_request(json_request) -> tuple[bool, dict]:
    try:
        request_json = json_request.get_json()
    except UnsupportedMediaType:
        return False, {}

    return True, request_json


class SignedIntConverter(IntegerConverter):
    regex = r'-?\d+'
