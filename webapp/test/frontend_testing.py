from multiprocessing import Process
from selenium import webdriver
from time import sleep

from webapp.web_app import run_web_app
from webapp.db_handler import db_connection

expected_user_name = "Amit"


def before_test():
    with db_connection().cursor() as cursor:
        cursor.execute(f"INSERT IGNORE INTO users (user_id, user_name, creation_date) "
                       f"VALUES (-1, '{expected_user_name}', NULL)")
        db_connection().commit()


def test():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5001/users/get_user_data/-1")

    is_user_name_displayed = driver.find_element(by="id", value="user").is_displayed()
    user_name_displayed = driver.find_element(by="id", value="user").text

    assert is_user_name_displayed and expected_user_name == user_name_displayed


if __name__ == '__main__':
    web_app_thread = Process(target=run_web_app)
    web_app_thread.start()

    sleep(5)

    before_test()
    test()

    web_app_thread.terminate()
    web_app_thread.join()
