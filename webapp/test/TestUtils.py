from webapp.db_handler import db_connection


# Generates proper asserting error message with given variable
def format_error_assertion_message(variable_name, expected, actual):
    return f"Error asserting {variable_name} - expected value: {expected}, actual: {actual}"


def get_driver_by_name(driver_name, webdriver):
    match driver_name:
        case "Chrome":
            return webdriver.Chrome
        case "Firefox":
            return webdriver.Firefox
        case "Ie":
            return webdriver.Ie
        case "Edge":
            return webdriver.Edge
        case _:
            raise InvalidDriverName


def get_testing_endpoint_details(endpoint_name):
    # TODO: Finish query and change tests to use the new config table
    with db_connection().cursor() as cursor:
        cursor.execute("SELECT endpoint_name, endpoint_url, endpoint_port, endpoint_api, browser, user_name "
                       "FROM config "
                       "WHERE endpoint_name=%s", endpoint_name)


class InvalidDriverName:
    pass

