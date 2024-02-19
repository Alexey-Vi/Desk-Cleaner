import json
import logging
import main


def get_configuration_list(file):
    """
    Loads the requested configuration file and returns a list with all the parameters.
    Returns 'error' if it failed to find the file.
    :param file: which config file to load
    :return: returns a list of all the configurations from the requested file.
             returns an error in case it failed reading the file.
    """
    try:
        with open(file, "r") as config:
            content = json.load(config)
        return content
    except:
        logging.error("Failed reading config file.")
        return "error"


def get_config_parameter(file, param):
    """

    :param file:
    :param param:
    :return:
    """
    content = get_configuration_list(file)
    if content == "error":
        main.close_app()
    else:
        value = content[param]
        return value
