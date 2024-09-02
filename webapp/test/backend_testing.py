from multiprocessing import Process
from requests import request
from time import sleep

from webapp.rest_app import run_rest_app
from webapp.db_handler import db_connection
from webapp.test.TestUtils import (format_error_assertion_message,
                                   get_testing_endpoint_details)
from webapp.Utils import (OK_RETURN_CODE,
                          UNSUPPORTED_MEDIA_TYPE_CODE,
                          UNPROCESSABLE_ENTITY_CODE,
                          INTERNAL_SERVER_ERROR_CODE)

global endpoint_details
global endpoint_url
global expected_user_name

tests_user_id = -9999
expected_new_user_name = "AmitUpdated"

expected_ok_status = "ok"
expected_ok_return_code = OK_RETURN_CODE

expected_error_status = "error"
expected_no_id_error_reason = "no such id"
expected_internal_server_error_code = INTERNAL_SERVER_ERROR_CODE

expected_id_exists_new_id = tests_user_id + 1

expected_unsupported_format_reason = "payload should be json"
expected_unsupported_media_type_code = UNSUPPORTED_MEDIA_TYPE_CODE

expected_invalid_json_reason = "json does not contain user_name"
expected_unprocessable_entity_code = UNPROCESSABLE_ENTITY_CODE


def before_test_get_user_found():
    with db_connection().cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, NULL)", (tests_user_id, expected_user_name))
        db_connection().commit()


def test_get_user_found():
    json_response = request("GET", f"{endpoint_url}/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_name = json_response["user_name"]

    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute("SELECT user_name "
                       "FROM users "
                       "WHERE user_id=%s", tests_user_id)

        actual_db_user_name = cursor.fetchone()[0]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert expected_user_name == actual_user_name, (
        format_error_assertion_message("user_name", expected_user_name, actual_user_name))
    assert expected_user_name == actual_db_user_name, (
        format_error_assertion_message("db user_name", expected_user_name, actual_db_user_name))


def before_test_get_user_not_found():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_get_user_not_found():
    json_response = request("GET", f"{endpoint_url}/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_internal_server_error_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_internal_server_error_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_no_id_error_reason == actual_reason, (
        format_error_assertion_message("reason", expected_no_id_error_reason, actual_reason))


def before_test_create_user_success():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_create_user_success():
    json_response = request("POST", f"{endpoint_url}/{tests_user_id}",
                            json={"user_name": expected_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_added = json_response["user_added"]
    actual_user_id = json_response["user_id"]

    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute("SELECT user_name "
                       "FROM users "
                       "WHERE user_id=%s", tests_user_id)

        actual_db_user_name = cursor.fetchone()[0]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert expected_user_name == actual_user_added, (
        format_error_assertion_message("user_added", expected_user_name, actual_user_added))
    assert tests_user_id == actual_user_id, (
        format_error_assertion_message("user_id", expected_id_exists_new_id, actual_user_id))
    assert expected_user_name == actual_db_user_name, (
        format_error_assertion_message("db user_name", expected_user_name, actual_db_user_name))


def before_test_create_user_already_exists():
    with db_connection().cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, NULL)", (tests_user_id, expected_user_name))
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", expected_id_exists_new_id)
        db_connection().commit()


def test_create_user_already_exists():

    json_response = request("POST", f"{endpoint_url}/{tests_user_id}",
                            json={"user_name": expected_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_added = json_response["user_added"]
    actual_user_id = json_response["user_id"]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert expected_user_name == actual_user_added, (
        format_error_assertion_message("user_added", expected_user_name, actual_user_added))
    assert expected_id_exists_new_id == actual_user_id, (
        format_error_assertion_message("user_id", expected_id_exists_new_id, actual_user_id))


def test_create_user_unsupported_format():
    json_response = request("POST", f"{endpoint_url}/{tests_user_id}",
                            data={"user_name": expected_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_unsupported_media_type_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_unsupported_media_type_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_unsupported_format_reason == actual_reason, (
        format_error_assertion_message("reason", expected_unsupported_format_reason, actual_reason))


def test_create_user_invalid_json_format():
    json_response = request("POST", f"{endpoint_url}/{tests_user_id}",
                            json={"testField": expected_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_unprocessable_entity_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_unprocessable_entity_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_invalid_json_reason == actual_reason, (
        format_error_assertion_message("reason", expected_invalid_json_reason, actual_reason))


def before_test_update_user_success():
    with db_connection().cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, NULL)", (tests_user_id, expected_user_name))
        db_connection().commit()


def test_update_user_success():
    json_response = request("PUT", f"{endpoint_url}/{tests_user_id}",
                            json={"user_name": expected_new_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_name_updated = json_response["user_updated"]

    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute("SELECT user_name "
                       "FROM users "
                       "WHERE user_id=%s", tests_user_id)

        actual_db_user_name = cursor.fetchone()[0]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert expected_new_user_name == actual_user_name_updated, (
        format_error_assertion_message("user_updated", expected_new_user_name, actual_user_name_updated))
    assert expected_new_user_name == actual_db_user_name, (
        format_error_assertion_message("db user_name", expected_new_user_name, actual_db_user_name))


def before_test_update_user_not_found():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_update_user_not_found():
    json_response = request("PUT", f"{endpoint_url}/{tests_user_id}",
                            json={"user_name": expected_new_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_internal_server_error_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_internal_server_error_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_no_id_error_reason == actual_reason, (
        format_error_assertion_message("reason", expected_no_id_error_reason, actual_reason))


def test_update_user_unsupported_format():
    json_response = request("PUT", f"{endpoint_url}/{tests_user_id}",
                            data={"user_name": expected_new_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_unsupported_media_type_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_unsupported_media_type_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_unsupported_format_reason == actual_reason, (
        format_error_assertion_message("reason", expected_unsupported_format_reason, actual_reason))


def test_update_user_invalid_json_format():
    json_response = request("PUT", f"{endpoint_url}/{tests_user_id}",
                            json={"testField": expected_new_user_name})

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_unprocessable_entity_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_unprocessable_entity_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_invalid_json_reason == actual_reason, (
        format_error_assertion_message("reason", expected_invalid_json_reason, actual_reason))


def before_test_delete_user_found():
    with db_connection().cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, NULL)", (tests_user_id, expected_user_name))
        db_connection().commit()


def test_delete_user_found():
    json_response = request("DELETE", f"{endpoint_url}/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_user_id = json_response["user_deleted"]

    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute("SELECT user_name "
                       "FROM users "
                       "WHERE user_id=%s", tests_user_id)

        query_results = cursor.fetchall()

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == actual_status, (
        format_error_assertion_message("status", expected_ok_status, actual_status))
    assert tests_user_id == actual_user_id, (
        format_error_assertion_message("user_deleted", tests_user_id, actual_user_id))
    assert len(query_results) == 0, (
        format_error_assertion_message("number of query results", "0", len(query_results)))


def before_test_delete_user_not_found():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_delete_user_not_found():
    json_response = request("DELETE", f"{endpoint_url}/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    actual_status = json_response["status"]
    actual_reason = json_response["reason"]

    assert expected_internal_server_error_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_internal_server_error_code, actual_return_code))
    assert expected_error_status == actual_status, (
        format_error_assertion_message("status", expected_error_status, actual_status))
    assert expected_no_id_error_reason == actual_reason, (
        format_error_assertion_message("reason", expected_no_id_error_reason, actual_reason))


def cleanup_tests():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def run_tests():
    # GET method tests
    before_test_get_user_found()
    test_get_user_found()

    before_test_get_user_not_found()
    test_get_user_not_found()

    # POST method tests
    before_test_create_user_success()
    test_create_user_success()

    before_test_create_user_already_exists()
    test_create_user_already_exists()

    test_create_user_unsupported_format()

    test_create_user_invalid_json_format()

    # PUT method tests
    before_test_update_user_success()
    test_update_user_success()

    before_test_update_user_not_found()
    test_update_user_not_found()

    test_update_user_unsupported_format()

    test_update_user_invalid_json_format()

    # DELETE method tests
    before_test_delete_user_found()
    test_delete_user_found()

    before_test_delete_user_not_found()
    test_delete_user_not_found()

    cleanup_tests()


if __name__ == '__main__':
    endpoint_details = get_testing_endpoint_details("backend")
    endpoint_url = (f"http://{endpoint_details['endpoint_url']}:"
                    f"{endpoint_details['endpoint_port']}"
                    f"{endpoint_details['endpoint_api']}")
    expected_user_name = endpoint_details['user_name']

    rest_app_process = Process(target=run_rest_app)
    rest_app_process.start()
    sleep(5)

    run_tests()

    rest_app_process.terminate()
    rest_app_process.join()
