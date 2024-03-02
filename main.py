import os
import shutil
import datetime
import logging
import configHandler
# import Template
import userInterface

templates_file = "templates.json"
desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
downloads_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
log_file = "Logs.log"
logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')


def close_app():
    logging.info("Closing app...\n")
    quit()


def remove_files(file_list, daily_remove_flag=False):
    """
    Function receives a file list and deletes all files that were modified more than a week ago.
    :param file_list: the list of files in the wanted directory
    :param daily_remove_flag: flag meant for files that require daily cleaning instead of weekly.
    """
    try:
        cycle_rate = configHandler.get_config_parameter(config_file, "none daily cycle rate")
        current_time = datetime.datetime.now()
        for file in file_list:
            creation_time = os.path.getctime(file)
            creation_stamp = datetime.datetime.fromtimestamp(creation_time)
            time_diff = current_time - creation_stamp
            if time_diff.days > cycle_rate or daily_remove_flag:
                if os.path.isfile(file):
                    os.remove(file)
                    logging.info('File successfully removed: {}.'.format(file))
                else:
                    shutil.rmtree(file)
                    logging.info('Folder successfully removed: {}.'.format(file))
            else:
                logging.debug("No files older than {} days.".format(cycle_rate))
    except Exception as e:
        logging.error('{}\nFailed to remove files: {}.'.format(e, file_list))


def file_reformat(files):
    reformat_list = configHandler.get_config_parameter(config_file, 'file reformat')
    for file in files:
        for i in reformat_list:
            file = file.strip(i)
    return files


# def clean_folder():  # TODO need to refactor whole method
#     """
#     Takes the file list of the desktop folder and compares it to the list of allowed files from the template file.
#     Any files that do not exist in the template will get deleted on a daily basis.
#     """
#     logging.info("Starting 'desktop' cleaning cycle.")
#     try:
#         template_files = file_reformat(configHandler.get_config_parameter(templates_file, machine_type))
#         desktop_files = file_reformat(glob.glob(desktop_folder + '\\*'))
#         files_to_delete = []
#         for file in desktop_files:
#             if os.path.basename(file.casefold()) not in (index.casefold() for index in template_files):
#                 files_to_delete.append(file)
#         if len(files_to_delete) == 0:
#             logging.info("No files to delete from 'desktop' folder.")
#         else:
#             logging.info("Removing redundant files.")
#             remove_files(files_to_delete, True)
#             logging.error("Finished cleaning 'desktop' folder.")
#     except Exception as e:
#         logging.error("{}\nFailed cleaning 'desktop' folder.".format(e)


def manage_template_files():
    template_list = []
    config_keys = list(dict.keys(configHandler.get_configuration_list(config_file)))
    for key in config_keys:
        key = key.strip(' ', 'run')
        template_name = key
        template_files = configHandler.get_config_parameter(templates_file, key)
        template_list.append(Template.Template(name=template_name, file_list=template_files))
    return template_list


if __name__ == '__main__':
    # logging.info("Script started.")
    configHandler.handle_template_file(templates_file)
    userInterface.start_window()
    # available_templates = manage_template_files()
    close_app()
