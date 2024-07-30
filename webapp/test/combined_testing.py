from multiprocessing import Process
from selenium import webdriver
from time import sleep
from requests import request

from webapp.db_handler import db_connection
from webapp.web_app import run_web_app
from webapp.rest_app import run_rest_app
from webapp.Utils import OK_RETURN_CODE
from webapp.test.TestUtils import format_error_assertion_message

tests_user_id = -9999
expected_user_name = "Amit"
expected_ok_status = "ok"
expected_ok_return_code = OK_RETURN_CODE


def before_test_full_request():
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users "
                       f"WHERE user_id = {tests_user_id}")
        db_connection().commit()


def test_full_request():
    # Create user with backend request
    json_response = request("POST", f"http://localhost:5000/users/{tests_user_id}",
                            json={"user_name": expected_user_name})

    # Get user with backend request
    json_response = request("GET", f"http://localhost:5000/users/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    get_request_actual_status = json_response["status"]
    get_request_actual_user_name = json_response["user_name"]

    assert expected_ok_return_code == actual_return_code, (
        format_error_assertion_message("return_code", expected_ok_return_code, actual_return_code))
    assert expected_ok_status == get_request_actual_status, (
        format_error_assertion_message("status", expected_ok_status, get_request_actual_status))
    assert expected_user_name == get_request_actual_user_name, (
        format_error_assertion_message("user_name", expected_user_name, get_request_actual_user_name))

    # Check user was created in DB
    with db_connection().cursor() as cursor:
        db_connection().commit()
        cursor.execute(f"SELECT user_name "
                       f"FROM users "
                       f"WHERE user_id={tests_user_id}")

        actual_db_user_name = cursor.fetchone()[0]

    assert expected_user_name == actual_db_user_name, (
        format_error_assertion_message("db user_name", expected_user_name, actual_db_user_name))

    driver = webdriver.Chrome()
    driver.get(f"http://localhost:5001/users/get_user_data/{tests_user_id}")

    user_element = driver.find_element(by="id", value="user")

    is_user_name_displayed = user_element.is_displayed()
    actual_user_name = user_element.text

    assert is_user_name_displayed, (
        format_error_assertion_message("user_name visible", "True", is_user_name_displayed))
    assert expected_user_name == actual_user_name, (
        format_error_assertion_message("frontend user_name", expected_user_name, actual_user_name))


def cleanup_tests():
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users "
                       f"WHERE user_id = {tests_user_id}")
        db_connection().commit()


def run_tests():
    before_test_full_request()
    test_full_request()

    cleanup_tests()


if __name__ == '__main__':
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