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
    This method gets a specific parameter's state from the given config file.
    :param file: the configuration file to read
    :param param: which parameter to read
    :return: returns the requested parameter's state
    """
    content = get_configuration_list(file)
    if content == "error":
        main.close_app()
    else:
        value = content[param]
        return value


def set_config_parameter(file, param, setting):
    """
    This method sets a specific parameter's state in the given config file.
    :param file: the configuration file to read
    :param param: which parameter to read
    :param setting: what to change the parameter to
    """
    try:
        logging.info("Changing configuration '{}' to '{}'".format(param, setting))
        with open(file, "r") as config:
            content = json.load(config)
        content[param] = setting
        with open(file, "w") as config:
            json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed reading config file.".format(e))
        main.close_app()
