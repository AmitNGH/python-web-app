# Generates proper asserting error message with given variables
def format_error_assertion_message(variable_name, expected, actual):
    return f"Error asserting {variable_name} - expected value: {expected}, actual: {actual}"
