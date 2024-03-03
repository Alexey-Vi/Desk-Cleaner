import json
import logging
import main
import os

templates_file = "templates.json"
log_file = "Logs.log"
logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')


def get_templates_list():
    """
    Loads the template file and returns a list of all the templates along with their appropriate folder.
    :return: returns a dictionary of all the templates.
             returns an error in case it failed reading the file.
    """
    try:
        with open(templates_file, 'r') as config:
            content = json.load(config)
        return content["templates"]
    except Exception as e:
        logging.error("{}\nFailed reading config file.".format(e))
        return "error"


def get_template_folder(param):
    """
    This method gets a specific parameter's state from the given config file.
    :param param: which template path to return.
    :return: returns the requested template path.
    """
    content = get_templates_list()
    if content == "error":
        main.close_app()
    else:
        value = content[param]
        return value


def get_list_of_template_names():
    """
    This method returns a list of all the
    :return:
    """
    try:
        template_list = list(get_templates_list().keys())
        return template_list
    except Exception as e:
        logging.error("{}\nFailed reading template file.".format(e))
        main.close_app()


def get_template_file_list(template):
    try:
        with open(templates_file, 'r') as config:
            content = json.load(config)
        return content["template files"][template]
    except Exception as e:
        logging.error("{}\nFailed reading config file.".format(e))
        return "error"


def add_template(template_name, template_folder, template_files):
    """
    This method adds a new template to the template file.
    :param template_folder: the folder to which the template is pointing
    :param template_name: name of the template
    :param template_files: list of the files to be saved under the template
    :return: Nothing
    """
    try:
        logging.info("Adding new template: \"{}\"".format(template_name))
        with open(templates_file, 'r') as config:
            content = json.load(config)
        content["templates"][template_name] = template_folder
        content["template files"][template_name] = template_files
        with open(templates_file, 'w') as config:
            json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed reading template file.".format(e))
        main.close_app()


def remove_template(template_name):
    """
    This method removes the specified template from the template file.
    :param template_name: name of the template to remove
    :return: Nothing
    """
    if template_name == "":
        return
    try:
        logging.info("Removing template: {}".format(template_name))
        with open(templates_file, 'r') as config:
            content = json.load(config)
        content["templates"].pop(template_name)
        content["template files"].pop(template_name)
        with open(templates_file, 'w') as config:
            json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed reading template file.".format(e))
        main.close_app()


def handle_template_file():
    """
    This method confirms the existence and validity of the 'templates.json' file.
    If it doesn't exist -> create the file with the basic preset.
    if it exists and isn't a valid json, it overrides it to the basic preset.
    :param file: the template file to open
    :return: nothing
    """
    content = {"templates": {},"template files": {}}  # The basic configuration of the file.
    if not os.path.isfile(templates_file):
        with open(templates_file, 'a') as config:
            json.dump(content, config, indent=2)
        return
    else:
        try:
            with open(templates_file, 'r') as config:
                json.load(config)
        except ValueError as e:
            with open(templates_file, 'r') as backup:
                original_file_content = backup.read()
            with open("templates - org.txt", 'a') as backup:
                backup.write(original_file_content)
            with open(templates_file, 'w') as config:
                json.dump(content, config, indent=2)
            logging.error("{}\ntemplate file was invalid.\nCreated new basic 'Template' file.\n"
                          "Original file content may be found in {}".format(e, os.path.abspath("templates - org.txt")))
