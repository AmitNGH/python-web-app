from multiprocessing import Process
from selenium import webdriver
from time import sleep

from web_app import run_web_app
from db_handler import db_connection
from test.TestUtils import (get_driver_by_name,
                                   get_testing_endpoint_details,
                                   format_error_assertion_message)

global endpoint_details
global endpoint_url
global expected_user_name
global driver

tests_user_id = -9999
expected_error_message = f"no such user with id: {tests_user_id}"


def before_test_id_found():
    with db_connection().cursor() as cursor:
        cursor.execute("INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       "VALUES (%s, %s, NULL)", (tests_user_id, expected_user_name))
        db_connection().commit()


def test_id_found():
    driver.get(f"{endpoint_url}/{tests_user_id}")

    user_element = driver.find_element(by="id", value="user")

    is_user_name_displayed = user_element.is_displayed()
    actual_user_name = user_element.text

    assert is_user_name_displayed, (
        format_error_assertion_message("user_name visible", "True", is_user_name_displayed))
    assert expected_user_name == actual_user_name, (
        format_error_assertion_message("user_name", expected_user_name, actual_user_name))


def before_test_id_not_found():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def test_id_not_found():
    driver.get(f"{endpoint_url}/{tests_user_id}")

    error_element = driver.find_element(by="id", value="error")

    is_error_displayed = error_element.is_displayed()
    actual_error_message = error_element.text

    assert is_error_displayed, (
        format_error_assertion_message("error visible", "True", is_error_displayed))
    assert expected_error_message == actual_error_message, (
        format_error_assertion_message("error", expected_error_message, actual_error_message))


def cleanup_tests():
    with db_connection().cursor() as cursor:
        cursor.execute("DELETE FROM users "
                       "WHERE user_id = %s", tests_user_id)
        db_connection().commit()


def run_tests():
    before_test_id_found()
    test_id_found()

    before_test_id_not_found()
    test_id_not_found()

    cleanup_tests()


if __name__ == '__main__':
    endpoint_details = get_testing_endpoint_details("frontend")
    endpoint_url = (f"http://{endpoint_details['endpoint_url']}:"
                    f"{endpoint_details['endpoint_port']}"
                    f"{endpoint_details['endpoint_api']}")
    expected_user_name = endpoint_details["user_name"]

    web_app_process = Process(target=run_web_app)
    web_app_process.start()
    sleep(5)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = get_driver_by_name(endpoint_details["browser"], webdriver, options=options)

    run_tests()

    web_app_process.terminate()
    web_app_process.join()
