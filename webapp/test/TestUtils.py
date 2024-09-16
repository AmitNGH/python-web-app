from db_handler import db_connection


# Generates proper asserting error message with given variable
def format_error_assertion_message(variable_name, expected, actual):
    return f"Error asserting {variable_name} - expected value: {expected}, actual: {actual}"


def get_driver_by_name(driver_name, webdriver, options=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    match driver_name:
        case "Chrome":
            return webdriver.Chrome(options=options)
        case "Firefox":
            return webdriver.Firefox()
        case "Ie":
            return webdriver.Ie()
        case "Edge":
            return webdriver.Edge()
        case _:
            raise InvalidDriverName


def get_testing_endpoint_details(endpoint_name) -> dict:
    with db_connection().cursor() as cursor:
        cursor.execute("SELECT endpoint_name, endpoint_url, endpoint_port, endpoint_api, browser, user_name "
                       "FROM config "
                       "WHERE endpoint_name=%s", endpoint_name)
        endpoint_details = cursor.fetchone()

    return {"endpoint_name": endpoint_details[0],
            "endpoint_url": endpoint_details[1],
            "endpoint_port": endpoint_details[2],
            "endpoint_api": endpoint_details[3],
            "browser": endpoint_details[4],
            "user_name": endpoint_details[5]}


class InvalidDriverName:
    pass
