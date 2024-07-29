from multiprocessing import Process
from requests import request
from time import sleep

from webapp.rest_app import run_rest_app
from webapp.db_handler import db_connection
from webapp.test.TestUtils import format_error_assertion_message
from webapp.Utils import (OK_RETURN_CODE,
                          UNSUPPORTED_MEDIA_TYPE_CODE,
                          UNPROCESSABLE_ENTITY_CODE,
                          INTERNAL_SERVER_ERROR_CODE)

tests_user_id = -9999
expected_ok_status = "ok"
expected_error_status = "error"
expected_user_name = "Amit"
expected_ok_return_code = OK_RETURN_CODE


def before_test_get_user_found():
    with db_connection().cursor() as cursor:
        cursor.execute(f"INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       f"VALUES ({tests_user_id}, '{expected_user_name}', NULL)")
        db_connection().commit()


def test_get_user_found():
    json_response = request("GET", f"http://localhost:5000/users/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_name = json_response["user_name"]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert expected_user_name == actual_user_name, (
        format_error_assertion_message("user_name", expected_user_name, actual_user_name))


def run_tests():
    before_test_get_user_found()
    test_get_user_found()


if __name__ == '__main__':
    rest_app_process = Process(target=run_rest_app)
    rest_app_process.start()
    sleep(5)

    run_tests()

    rest_app_process.terminate()
    rest_app_process.join()
