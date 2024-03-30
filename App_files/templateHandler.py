import json
import logging
import main
import os

templates_file = "Desk-Cleaner\\templates.json"


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
    :return: List of template names
    """
    try:
        template_list = list(get_templates_list().keys())
        return template_list
    except Exception as e:
        logging.error("{}\nFailed reading template file.".format(e))


def get_template_file_list(template):
    """
    This method returns all the files that are saved in a template.
    :param template: Template name
    :return: List of files saved to template
    """
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
        logging.error("{}\nFailed adding template.".format(e))


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
        logging.error("{}\nFailed removing template.".format(e))


def add_files_to_template(template_name, files):
    if template_name == "" or not files:
        return
    try:
        with open(templates_file, 'r') as config:
            content = json.load(config)
        for file in files:
            logging.info("Adding file: {}\tto template: {}".format(file, template_name))
            content["template files"][template_name].append(os.path.basename(file))
        with open(templates_file, 'w') as config:
            json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed adding file to template.".format(e))


def remove_files_from_template(template_name, files):
    """
    This method removes a single file from the template listing.
    If the template is empty at the end of the removal it also deletes the template.
    :param template_name: The name of the template to access.
    :param files: The files to remove.
    :return: Nothing.
    """
    if template_name == "":
        return
    try:
        with open(templates_file, 'r') as config:
            content = json.load(config)
        for file in files:
            logging.info("Removing file: {}\tfrom template: {}".format(file, template_name))
            content["template files"][template_name].remove(file)
        if len(content["template files"][template_name]) == 0:
            remove_template(template_name)
        else:
            with open(templates_file, 'w') as config:
                json.dump(content, config, indent=2)
    except Exception as e:
        logging.error("{}\nFailed removing file from template.".format(e))


def handle_template_file():
    """
    This method confirms the existence and validity of the 'templates.json' file.
    If it doesn't exist -> create the file with the basic preset.
    if it exists and isn't a valid json, it overrides it to the basic preset.
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
