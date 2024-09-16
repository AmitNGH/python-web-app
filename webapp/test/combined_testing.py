from multiprocessing import Process
from selenium import webdriver
from time import sleep
from requests import request

from db_handler import db_connection
from web_app import run_web_app
from rest_app import run_rest_app
from Utils import OK_RETURN_CODE
from test.TestUtils import (format_error_assertion_message,
                                   get_testing_endpoint_details,
                                   get_driver_by_name)

global frontend_endpoint_details
global frontend_endpoint_url
global frontend_expected_user_name
global backend_endpoint_details
global backend_endpoint_url
global backend_expected_user_name

tests_user_id = -9999
expected_ok_status = "ok"
expected_ok_return_code = OK_RETURN_CODE


def before_test_full_request():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_full_request():
    # Create user with backend request
    json_response = request("POST", f"{backend_endpoint_url}/{tests_user_id}",
                            json={"user_name": backend_expected_user_name})

    # Get user with backend request
    json_response = request("GET", f"{backend_endpoint_url}/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    get_request_actual_status = json_response["status"]
    get_request_actual_user_name = json_response["user_name"]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == get_request_actual_status, (
        format_error_assertion_message("status", expected_ok_status, get_request_actual_status))
    assert backend_expected_user_name == get_request_actual_user_name, (
        format_error_assertion_message("user_name", backend_expected_user_name, get_request_actual_user_name))

    # Check user was created in DB
    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute("SELECT user_name "
                       "FROM users "
                       "WHERE user_id=%s", tests_user_id)

        actual_db_user_name = cursor.fetchone()[0]

    assert backend_expected_user_name == actual_db_user_name, (
        format_error_assertion_message("db user_name", backend_expected_user_name, actual_db_user_name))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = get_driver_by_name(frontend_endpoint_details["browser"], webdriver, options=options)
    driver.get(f"{frontend_endpoint_url}/{tests_user_id}")

    user_element = driver.find_element(by="id", value="user")

    is_user_name_displayed = user_element.is_displayed()
    actual_user_name = user_element.text

    assert is_user_name_displayed, (
        format_error_assertion_message("user_name visible", "True", is_user_name_displayed))
    assert frontend_expected_user_name == actual_user_name, (
        format_error_assertion_message("frontend user_name", frontend_expected_user_name, actual_user_name))


def cleanup_tests():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def run_tests():
    before_test_full_request()
    test_full_request()

    cleanup_tests()


if __name__ == '__main__':
    frontend_endpoint_details = get_testing_endpoint_details("frontend")
    frontend_endpoint_url = (f"http://{frontend_endpoint_details['endpoint_url']}:"
                             f"{frontend_endpoint_details['endpoint_port']}"
                             f"{frontend_endpoint_details['endpoint_api']}")
    frontend_expected_user_name = frontend_endpoint_details["user_name"]

    backend_endpoint_details = get_testing_endpoint_details("backend")
    backend_endpoint_url = (f"http://{backend_endpoint_details['endpoint_url']}:"
                            f"{backend_endpoint_details['endpoint_port']}"
                            f"{backend_endpoint_details['endpoint_api']}")
    backend_expected_user_name = backend_endpoint_details["user_name"]

    web_app_process = Process(target=run_web_app)
    web_app_process.start()
    rest_app_process = Process(target=run_rest_app)
    rest_app_process.start()
    sleep(5)

    run_tests()

    web_app_process.terminate()
    web_app_process.join()
    rest_app_process.terminate()
    rest_app_process.join()
