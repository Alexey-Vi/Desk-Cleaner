import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import main
import templateHandler

log_file = "Logs.log"
logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                    datefmt='%m/%d/%Y %H:%M:%S')


def deploy_start_window(total_templates=0):
    """
    Main program window. All interactions come and go through here.
    :param total_templates: How many templates are saved currently.
    :return: Nothing
    """
    start_window = tk.Tk()
    start_window.title("Desk Cleaner")
    start_window.resizable(False, False)

    frm_left = tk.Frame(start_window, width=25, height=15, padx=5, pady=5)
    frm_right = tk.Frame(start_window, width=25, height=15, padx=5, pady=5)
    frm_right_inner = tk.Frame(frm_right)

    lbl_available_files_to_delete = tk.Label(frm_right_inner, text="{} available templates to clean."
                                             .format(total_templates), width=25, relief=tk.GROOVE)
    btn_refresh_file_counter = tk.Button(master=frm_right_inner, text="⟲", command=lambda:
                                         [start_window.destroy(), main.create_main_window()])
    lb_files_to_delete = tk.Listbox(frm_right, selectmode=tk.MULTIPLE, width=30)
    template_names = templateHandler.get_list_of_template_names()
    for index in range(len(template_names)):
        lb_files_to_delete.insert(index+1, template_names[index])

    btn_run_cleaner = tk.Button(text="Run Cleaner", width=25, height=2, master=frm_left,
                                command=lambda: deploy_run_cleaner_window(get_listbox_variables(lb_files_to_delete, lb_files_to_delete.curselection())))
    btn_create_template = tk.Button(text="Create Template", width=25, height=2, master=frm_left,
                                    command=deploy_create_template_window)
    btn_edit_template = tk.Button(text="Edit Template", width=25, height=2, master=frm_left,
                                  command=deploy_edit_template_window)
    btn_delete_template = tk.Button(text="Delete Template", width=25, height=2, master=frm_left,
                                    command=deploy_delete_template_window)
    btn_close_window = tk.Button(text="Close", width=25, height=2, master=frm_left, command=start_window.destroy)

    lbl_available_files_to_delete.pack(side=tk.LEFT)
    btn_refresh_file_counter.pack(side=tk.RIGHT)
    lb_files_to_delete.pack(side=tk.BOTTOM)
    btn_run_cleaner.pack()
    btn_create_template.pack()
    btn_edit_template.pack()
    btn_delete_template.pack()
    btn_close_window.pack()

    frm_left.pack(side=tk.LEFT)
    frm_right.pack(side=tk.RIGHT)
    frm_right_inner.pack()
    start_window.mainloop()


def deploy_create_template_window():
    """
    New template creation window. Accessed from start window.
    Receives a name for a template. When pressing 'Submit' will open folder hierarchy to choose which files to save
    as a template.
    :return: Nothing
    """
    create_template_window = tk.Tk()
    create_template_window.title("New Template")
    create_template_window.resizable(False, False)

    entry_input = tk.StringVar(create_template_window)

    frm_top = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_inner_bot = tk.Frame(master=frm_bot, padx=5, pady=5)

    lbl = tk.Label(master=frm_top, text="Template Name")
    ent = tk.Entry(master=frm_top, textvariable=entry_input)
    btn_submit = tk.Button(text="Confirm", width=25, height=2, master=frm_inner_bot,
                           command=lambda: [create_template_window.destroy(),
                                            main.save_template(entry_input.get(), filedialog.askdirectory())])
    btn_cancel = tk.Button(text="Cancel", width=25, height=2, master=frm_inner_bot,
                           command=create_template_window.destroy)

    lbl.pack()
    ent.pack()
    btn_submit.pack(side=tk.LEFT)
    btn_cancel.pack(side=tk.RIGHT)
    frm_top.pack()
    frm_bot.pack()
    frm_inner_bot.pack()


def deploy_delete_template_window():
    """
    Template deletion window. Accessed from start window.
    If there are no templates saved it will inform the user with a pop-up. Otherwise, it will open a list of available
    template names and will delete the relevant template from the 'templates.json'.
    :return: None
    """
    delete_template_window = tk.Tk()
    delete_template_window.title("Delete Template")
    delete_template_window.resizable(False, False)

    if len(templateHandler.get_templates_list()) == 0:
        frm_window = tk.Frame(master=delete_template_window, padx=50, pady=50)

        lbl = tk.Label(text="No Templates Found", master=frm_window)
        btn_cancel = tk.Button(text="Close", width=25, height=2, master=frm_window,
                               command=delete_template_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(master=delete_template_window, padx=5, pady=5)
        frm_bot = tk.Frame(master=delete_template_window, padx=5, pady=5)

        combobox_input = tk.StringVar(delete_template_window)

        lbl = tk.Label(text="Template Name", master=frm_window)
        cmb_template_list = ttk.Combobox(frm_window, values=templateHandler.get_list_of_template_names(),
                                         textvariable=combobox_input)
        btn_confirm = tk.Button(text="Confirm", width=25, height=2, master=frm_bot, command=lambda:
                                [delete_template_window.destroy(), templateHandler.remove_template(combobox_input.get())])
        btn_cancel = tk.Button(text="Cancel", width=25, height=2, master=frm_bot,
                               command=delete_template_window.destroy)

        lbl.pack()
        cmb_template_list.pack()
        btn_confirm.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()
        frm_bot.pack()


def deploy_run_cleaner_window(selected_templates):
    """
    Confirmation window before cleaning the folders. Accessed from 'get_listbox_variables'.
    This window confirms whether you wish to clean x files from the selected folders.
    :param selected_templates: The template folders to be cleared.
    :return: Nothing
    """
    run_cleaner_window = tk.Tk()
    run_cleaner_window.title("Run Cleaner")
    run_cleaner_window.resizable(False, False)

    if len(templateHandler.get_templates_list()) == 0:
        frm_window = tk.Frame(master=run_cleaner_window, padx=50, pady=50)

        lbl = tk.Label(text="No Templates Found", master=frm_window)
        btn_cancel = tk.Button(text="Close", width=25, height=2, master=frm_window,
                               command=run_cleaner_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()
    else:
        frm_window = tk.Frame(master=run_cleaner_window, padx=5, pady=5)
        frm_bot = tk.Frame(master=frm_window, padx=5, pady=5)

        lbl_confirmation = tk.Label(frm_window, text="Delete {} files from {} templates?"
                                    .format(main.count_files_to_delete(selected_templates), len(selected_templates)))
        btn_yes = tk.Button(text="Yes", width=25, height=2, master=frm_bot,
                            command=lambda: [run_cleaner_window.destroy(), main.remove_files(selected_templates)])
        btn_no = tk.Button(text="No", width=25, height=2, master=frm_bot,
                           command=run_cleaner_window.destroy)

        lbl_confirmation.pack()
        btn_yes.pack(side=tk.LEFT)
        btn_no.pack(side=tk.RIGHT)
        frm_bot.pack()
        frm_window.pack()


def deploy_edit_template_window():
    """
    Template edit window. Accessed from start window.
    This window allows you to select which template you wish to edit. The 2 edit options are (currently) overwriting the
    whole template, or removing individual files.
    Pressing on the 'overwrite' leads to creating a new template with the same name, deleting the original.
    Pressing the 'remove files' leads to the delete files from template window.
    :return: Nothing.
    """
    edit_template_window = tk.Tk()
    edit_template_window.title("Edit Template")
    edit_template_window.resizable(False, False)

    if len(templateHandler.get_templates_list()) == 0:
        frm_window = tk.Frame(master=edit_template_window, padx=50, pady=50)

        lbl = tk.Label(text="No Templates Found", master=frm_window)
        btn_cancel = tk.Button(text="Close", width=25, height=2, master=frm_window,
                               command=edit_template_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(master=edit_template_window, padx=5, pady=5)
        frm_bot = tk.Frame(master=edit_template_window, padx=5, pady=5)

        combobox_input = tk.StringVar(edit_template_window)

        lbl = tk.Label(text="Template Name", master=frm_window)
        cmb_template_list = ttk.Combobox(frm_window, values=templateHandler.get_list_of_template_names(),
                                         textvariable=combobox_input)
        btn_overwrite_template = tk.Button(master=frm_bot, text="Overwrite Template", width=25, height=2, command=lambda:
                                           [edit_template_window.destroy(), main.save_template(combobox_input.get(), filedialog.askdirectory())])
        btn_remove_files_from_template = tk.Button(master=frm_bot, text="Remove Files", width=25, height=2, command=
                                                   lambda: [edit_template_window.destroy(), deploy_remove_files_from_template_window(combobox_input.get())])
        btn_cancel = tk.Button(text="Cancel", width=25, height=2, master=frm_bot,
                               command=edit_template_window.destroy)

        lbl.pack()
        cmb_template_list.pack()
        btn_overwrite_template.pack(side=tk.LEFT)
        btn_remove_files_from_template.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()
        frm_bot.pack()


def deploy_remove_files_from_template_window(template_name):
    """
    Remove files from template window. Accessed from Edit Template window.
    Allows the selection of individual files
    :param template_name:
    :return:
    """
    remove_files_from_template_window = tk.Tk()
    remove_files_from_template_window.title("Delete Files From Template")
    remove_files_from_template_window.resizable(False, False)

    frm_window = tk.Frame(remove_files_from_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(remove_files_from_template_window, padx=5, pady=5)

    lbl = tk.Label(frm_window, text="Select file to remove, press done when complete.")
    lb_files_to_remove_from_template = tk.Listbox(frm_window, selectmode=tk.MULTIPLE, width=30)
    files_in_template = templateHandler.get_template_file_list(template_name)
    for index in range(len(files_in_template)):
        lb_files_to_remove_from_template.insert(index + 1, files_in_template[index])

    btn_remove_file = tk.Button(frm_bot, text="Remove Files", width=25, height=2, command=lambda:
                                [templateHandler.remove_files_from_template(template_name, get_listbox_variables(lb_files_to_remove_from_template, lb_files_to_remove_from_template.curselection())),
                                 remove_files_from_template_window.destroy()])
    btn_cancel = tk.Button(frm_bot, text="Cancel", width=25, height=2, command=remove_files_from_template_window.destroy)

    lbl.pack()
    lb_files_to_remove_from_template.pack(side=tk.BOTTOM)
    btn_remove_file.pack(side=tk.LEFT)
    btn_cancel.pack(side=tk.RIGHT)
    frm_window.pack()
    frm_bot.pack()


def get_listbox_variables(listbox, listbox_selection):
    listbox_input = []
    for i in listbox_selection:
        listbox_input.append(listbox.get(i))
    return listbox_input
