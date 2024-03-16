import os
import shutil
import logging
import sys

import templateHandler
import userInterface

desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
log_file = "Logs.log"
logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')


def close_app():
    logging.info("Closing app...\n")
    sys.exit()


def save_template(template_name, template_folder):
    """
    Creates a new template with the given template name and the requested folder.
    :param template_name: Name of the new template.
    :param template_folder: The folder to which the template refers.
    :return: Nothing
    """
    if template_name == "":
        return
    file_list = os.listdir(template_folder)
    templateHandler.add_template(template_name, template_folder, file_list)


def scan_files_to_remove(templates):
    """
    Scans the saved template folders for any unapproved files.
    :return: a list of all the files not approved by the template.
    """
    files_to_delete = []
    for template in list(templates):
        template_folder = templateHandler.get_template_folder(template)
        template_folder_current_files = os.listdir(template_folder)
        approved_template_files = templateHandler.get_template_file_list(template)
        for file in template_folder_current_files:
            if os.path.basename(file.casefold()) not in (index.casefold() for index in approved_template_files):
                full_file_path = os.path.join(template_folder, file)
                files_to_delete.append(full_file_path)
    return files_to_delete


def count_files_to_delete(templates_to_clean):
    """
    Counts the amount of available files to delete.
    :return: an integer representing the amount of file to delete.
    """
    return len(scan_files_to_remove(templates_to_clean))


def remove_files(templates_to_clean):
    """
    Delete all files that don't belong in the templates.
    :return: Nothing
    """
    logging.info("Beginning file cleaning cycle.")
    if len(templates_to_clean) == 0:
        logging.info("No Templates were selected.")
        return

    files_to_delete = scan_files_to_remove(templates_to_clean)
    for file in files_to_delete:
        try:
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)
        except Exception as e:
            logging.error("{}\nFailed to remove file: {}".format(e, file))


def create_main_window():
    userInterface.deploy_start_window(len(templateHandler.get_list_of_template_names()))


if __name__ == '__main__':
    logging.info("Script started.")
    templateHandler.handle_template_file()
    create_main_window()
    close_app()
