import json
import logging
import main
import os


def get_configuration_list(file):
    """
    Loads the requested configuration file and returns a list with all the parameters.
    Returns 'error' if it failed to find the file.
    :param file: which config file to load
    :return: returns a list of all the configurations from the requested file.
             returns an error in case it failed reading the file.
    """
    try:
        with open(file, 'r') as config:
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
        with open(file, 'r') as config:
            content = json.load(config)
        content[param] = setting
        with open(file, 'w') as config:
            json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed reading config file.".format(e))
        main.close_app()


def handle_template_file(file):
    """
    This method confirms the existence and validity of the 'templates.json' file.
    If it doesn't exist -> create the file with the basic preset.
    if it exists and isn't a valid json, it overrides it to the basic preset.
    :param file: the template file to open
    :return: nothing
    """
    content = {"templates": [],"template files": {}}  # The basic configuration of the file.
    if not os.path.isfile(file):
        with open(file, 'a') as config:
            json.dump(content, config, indent=2)
        return
    else:
        try:
            with open(file, 'r') as config:
                json.load(config)
        except ValueError as e:
            with open(file, 'r') as backup:
                original_file_content = backup.read()
            with open("templates - org.txt", 'a') as backup:
                backup.write(original_file_content)
            with open(file, 'w') as config:
                json.dump(content, config, indent=2)
            logging.error("{}\ntemplate file was invalid.\nCreated new basic 'Template' file.\n"
                          "Original file content may be found in {}".format(e, os.path.abspath("templates - org.txt")))
