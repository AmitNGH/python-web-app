from multiprocessing import Process
from selenium import webdriver
from time import sleep

from webapp.web_app import run_web_app
from webapp.db_handler import db_connection

tests_user_id = -1
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
    user_name_displayed = user_element.text

    assert is_user_name_displayed and expected_user_name == user_name_displayed


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
    displayed_error = error_element.text

    assert is_error_displayed and expected_error_message == displayed_error


def run_tests():

    before_test_id_found()
    test_id_found()

    before_test_id_not_found()
    test_id_not_found()


if __name__ == '__main__':
    web_app_thread = Process(target=run_web_app)
    web_app_thread.start()
    sleep(5)

    run_tests()

    web_app_thread.terminate()
    web_app_thread.join()
