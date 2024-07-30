from multiprocessing import Process
from selenium import webdriver
from time import sleep

from webapp.web_app import run_web_app
from webapp.db_handler import db_connection
from webapp.test.TestUtils import format_error_assertion_message

tests_user_id = -9999
expected_user_name = "Amit"
expected_error_message = f"no such user with id: {tests_user_id}"


def before_test_id_found():
    with db_connection().cursor() as cursor:
        cursor.execute(f"INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       f"VALUES ({tests_user_id}, '{expected_user_name}', NULL)")
        db_connection().commit()


def test_id_found():
    driver = webdriver.Chrome()
    driver.get(f"http://localhost:5001/users/get_user_data/{tests_user_id}")

    user_element = driver.find_element(by="id", value="user")

    is_user_name_displayed = user_element.is_displayed()
    actual_user_name = user_element.text

    assert is_user_name_displayed, (
        format_error_assertion_message("user_name visible", "True", is_user_name_displayed))
    assert expected_user_name == actual_user_name, (
        format_error_assertion_message("user_name", expected_user_name, actual_user_name))


def before_test_id_not_found():
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users "
                       f"WHERE user_id = {tests_user_id}")
        db_connection().commit()


def test_id_not_found():
    driver = webdriver.Chrome()
    driver.get(f"http://localhost:5001/users/get_user_data/{tests_user_id}")

    error_element = driver.find_element(by="id", value="error")

    is_error_displayed = error_element.is_displayed()
    actual_error_message = error_element.text

    assert is_error_displayed, (
        format_error_assertion_message("error visible", "True", is_error_displayed))
    assert expected_error_message == actual_error_message, (
        format_error_assertion_message("error", expected_error_message, actual_error_message))


def cleanup_tests():
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users "
                       f"WHERE user_id = {tests_user_id}")
        db_connection().commit()


def run_tests():
    before_test_id_found()
    test_id_found()

    before_test_id_not_found()
    test_id_not_found()

    cleanup_tests()


if __name__ == '__main__':
    web_app_process = Process(target=run_web_app)
    web_app_process.start()
    sleep(5)

    run_tests()

    web_app_process.terminate()
    web_app_process.join()
