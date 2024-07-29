from multiprocessing import Process
from selenium import webdriver
from time import sleep
from requests import request

from webapp.db_handler import db_connection
from webapp.web_app import run_web_app
from webapp.rest_app import run_rest_app

tests_user_id = -9999
expected_user_name = "Amit"


def before_test_id_found():
    with db_connection().cursor() as cursor:
        cursor.execute(f"DELETE FROM users "
                       f"WHERE user_id = {tests_user_id}")
        db_connection().commit()


def test_full_request():
    # Create user with backend request
    json_response = request("POST", f"http://localhost:5000/users/{tests_user_id}",
                            json={"user_name": expected_user_name})

    json_response = request("GET", f"http://localhost:5000/users/{tests_user_id}")

    actual_return_code = json_response.status_code

    json_response = json_response.json()
    get_request_actual_status = json_response["status"]
    get_request_actual_user_name = json_response["user_name"]

    # user_element = driver.find_element(by="id", value="user")
    #
    # is_user_name_displayed = user_element.is_displayed()
    # actual_user_name = user_element.text
    #
    # assert is_user_name_displayed, (
    #     format_error_assertion_message("user_name visible", "True", is_user_name_displayed))
    # assert expected_user_name == actual_user_name, (
    #     format_error_assertion_message("user_name", expected_user_name, actual_user_name))


def run_tests():
    print()


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
