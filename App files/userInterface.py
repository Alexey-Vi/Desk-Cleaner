import logging
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import main
import templateHandler


def deploy_start_window():
    """
    Main program window. All interactions come and go through here.
    :return: Nothing
    """

    start_window = tk.Tk()
    start_window.title("Desk Cleaner")
    start_window.resizable(False, False)

    frm_left = tk.Frame(start_window, width=25, height=15, padx=5, pady=5)
    frm_right = tk.Frame(start_window, width=25, height=15, padx=5, pady=5)
    frm_right_inner = tk.Frame(frm_right)

    lbl_available_files_to_delete = tk.Label(frm_right, text="{} available templates to clean."
                                             .format(len(templateHandler.get_list_of_template_names())), relief=tk.GROOVE)

    template_names = templateHandler.get_list_of_template_names()
    lb_values = tk.Variable(value=template_names)
    lb_template_names = tk.Listbox(frm_right_inner, selectmode=tk.MULTIPLE, width=30, listvariable=lb_values)
    scrollbar = ttk.Scrollbar(frm_right_inner, orient=tk.VERTICAL, command=lb_template_names.yview)
    lb_template_names['yscrollcommand'] = scrollbar.set

    btn_run_cleaner = tk.Button(frm_left, text="Run Cleaner", width=25, height=2, command=lambda:
                                deploy_run_cleaner_window(get_listbox_variables(lb_template_names, lb_template_names.curselection())))
    btn_create_template = tk.Button(frm_left, text="Create Template", width=25, height=2,
                                    command=lambda: deploy_create_template_window(lbl_available_files_to_delete, lb_template_names))
    btn_edit_template = tk.Button(frm_left, text="Edit Template", width=25, height=2,
                                  command=lambda: deploy_edit_template_window(lbl_available_files_to_delete, lb_template_names))
    btn_delete_template = tk.Button(frm_left, text="Delete Template", width=25, height=2,
                                    command=lambda: deploy_delete_template_window(lbl_available_files_to_delete, lb_template_names))
    btn_close_window = tk.Button(frm_left, text="Close", width=25, height=2, command=start_window.destroy)

    lbl_available_files_to_delete.pack(side=tk.TOP)
    lb_template_names.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    btn_run_cleaner.pack()
    btn_create_template.pack()
    btn_edit_template.pack()
    btn_delete_template.pack()
    btn_close_window.pack()

    frm_left.pack(side=tk.LEFT)
    frm_right.pack(side=tk.RIGHT)
    frm_right_inner.pack(side=tk.BOTTOM)

    start_window.protocol("WM_DELETE_WINDOW", start_window.iconify)

    start_window.mainloop()


def deploy_create_template_window(label, listbox):
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

    frm_top = tk.Frame(create_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(create_template_window, padx=5, pady=5)
    frm_inner_bot = tk.Frame(frm_bot, padx=5, pady=5)

    lbl = tk.Label(frm_top, text="Template Name")
    ent = tk.Entry(frm_top, textvariable=entry_input)
    btn_confirm = tk.Button(frm_inner_bot, text="Confirm", width=25, height=2, command=lambda:
                           [main.save_template(entry_input.get(), filedialog.askdirectory()), update_main_window(label, listbox), create_template_window.destroy()])
    btn_cancel = tk.Button(frm_inner_bot, text="Cancel", width=25, height=2, command=create_template_window.destroy)

    # ent.bind('<Return>', btn_confirm.invoke())

    lbl.pack()
    ent.pack()
    btn_confirm.pack(side=tk.LEFT)
    btn_cancel.pack(side=tk.RIGHT)
    frm_top.pack()
    frm_bot.pack()
    frm_inner_bot.pack()


def deploy_delete_template_window(label, listbox):
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

        lbl = tk.Label(frm_window, text="No Templates Found")
        btn_cancel = tk.Button(frm_window, text="Close", width=25, height=2, command=delete_template_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(master=delete_template_window, padx=5, pady=5)
        frm_bot = tk.Frame(master=delete_template_window, padx=5, pady=5)

        combobox_input = tk.StringVar(delete_template_window)

        lbl = tk.Label(frm_window, text="Template Name")
        cmb_template_list = ttk.Combobox(frm_window, values=templateHandler.get_list_of_template_names(),
                                         textvariable=combobox_input)
        btn_confirm = tk.Button(frm_bot, text="Confirm", width=25, height=2, command=lambda:
                                [templateHandler.remove_template(combobox_input.get()), update_main_window(label, listbox), delete_template_window.destroy()])
        btn_cancel = tk.Button(frm_bot, text="Cancel", width=25, height=2, command=delete_template_window.destroy)

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

    if len(selected_templates) == 0:
        frm_window = tk.Frame(run_cleaner_window, padx=50, pady=50)

        lbl = tk.Label(frm_window, text="No Templates Selected")
        btn_cancel = tk.Button(frm_window, text="Close", width=25, height=2, command=run_cleaner_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(run_cleaner_window, padx=5, pady=5)
        frm_bot = tk.Frame(frm_window, padx=5, pady=5)

        toggle_smart_cleaning = tk.BooleanVar(run_cleaner_window)

        lbl_confirmation = tk.Label(frm_window, text="Delete {} files from {} templates?"
                                    .format(main.count_files_to_delete(selected_templates), len(selected_templates)))
        checkbox_smart_cleaning = ttk.Checkbutton(frm_window, text="Enable Smart Cleaning", onvalue=True, offvalue=False,
                                                  variable=toggle_smart_cleaning)
        btn_yes = tk.Button(frm_bot, text="Yes", width=25, height=2, command=lambda:
                            [main.remove_files(selected_templates),
                             deploy_smart_cleaning_window(toggle_smart_cleaning.get(), selected_templates),
                             run_cleaner_window.destroy()])
        btn_no = tk.Button(frm_bot, text="No", width=25, height=2, command=run_cleaner_window.destroy)

        lbl_confirmation.pack()
        checkbox_smart_cleaning.pack()
        btn_yes.pack(side=tk.LEFT)
        btn_no.pack(side=tk.RIGHT)
        frm_bot.pack()
        frm_window.pack()


def deploy_smart_cleaning_window(enable_window, selected_templates):
    """
    Smart cleaning window. Accessed from the 'run cleaner' window.
    If the checkbox for the smart cleaning was enabled, this method will check whether there are more files saved in
    the template than in the actual folder.
    If so this window will appear and allow the user to overwrite the template files with the existing files in the
    folder.
    :param selected_templates:
    :param enable_window:
    :return: Nothing
    """
    if not enable_window:
        return
    for template in selected_templates:
        template_folder_actual_files = os.listdir(templateHandler.get_template_folder(template))
        if len(templateHandler.get_template_file_list(template)) > len(template_folder_actual_files):
            smart_cleaning_window = tk.Tk()
            smart_cleaning_window.title("Edit Template?")
            smart_cleaning_window.resizable(False, False)

            frm_top = tk.Frame(smart_cleaning_window, padx=5, pady=5)
            frm_bot = tk.Frame(smart_cleaning_window, padx=5, pady=5)

            lbl_notice = tk.Label(frm_top, text="In '{}' There are more files in the template than inside the actual folder.".format(template))
            lbl_question = tk.Label(frm_top, text="Would you like you overwrite template with existing files?")
            btn_yes = tk.Button(frm_bot, text="Yes", width=25, height=2, command=lambda:
                                [main.save_template(template, templateHandler.get_template_folder(template)),
                                 smart_cleaning_window.destroy()])
            btn_no = tk.Button(frm_bot, text="No", width=25, height=2, command=smart_cleaning_window.destroy)

            lbl_notice.pack()
            lbl_question.pack()
            btn_yes.pack()
            btn_no.pack()
            frm_top.pack()
            frm_bot.pack()

            smart_cleaning_window.wait_window(smart_cleaning_window)


def deploy_edit_template_window(label, listbox):
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
        frm_window = tk.Frame(edit_template_window, padx=50, pady=50)

        lbl = tk.Label(text="No Templates Found", master=frm_window)
        btn_cancel = tk.Button(frm_window, text="Close", width=25, height=2, command=edit_template_window.destroy)

        lbl.pack()
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(edit_template_window, padx=5, pady=5)
        frm_bot = tk.Frame(edit_template_window, padx=5, pady=5)

        combobox_input = tk.StringVar(edit_template_window)

        lbl = tk.Label(frm_window, text="Template Name")
        cmb_template_list = ttk.Combobox(frm_window, values=templateHandler.get_list_of_template_names(),
                                         textvariable=combobox_input)
        btn_overwrite_template = tk.Button(frm_bot, text="Overwrite Template", width=25, height=2, command=lambda:
                                           [main.save_template(combobox_input.get(), filedialog.askdirectory()), edit_template_window.destroy()])
        btn_remove_files_from_template = tk.Button(frm_bot, text="Remove Files", width=25, height=2, command=lambda:
                                                   [deploy_remove_files_from_template_window(label, listbox, combobox_input.get()), edit_template_window.destroy()])
        btn_cancel = tk.Button(frm_bot, text="Cancel", width=25, height=2, command=edit_template_window.destroy)

        lbl.pack()
        cmb_template_list.pack()
        btn_overwrite_template.pack(side=tk.LEFT)
        btn_remove_files_from_template.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()
        frm_bot.pack()


def deploy_remove_files_from_template_window(label, listbox, template_name):
    """
    Remove files from template window. Accessed from Edit Template window.
    Allows the selection of individual files
    :param listbox:
    :param label:
    :param template_name:
    :return:
    """
    remove_files_from_template_window = tk.Tk()
    remove_files_from_template_window.title("Delete Files From Template")
    remove_files_from_template_window.resizable(False, False)

    frm_window = tk.Frame(remove_files_from_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(remove_files_from_template_window, padx=5, pady=5)

    lbl = tk.Label(remove_files_from_template_window, text="Select file to remove, press done when complete.")
    lb_files_to_remove_from_template = tk.Listbox(frm_window, selectmode=tk.MULTIPLE, width=30)
    files_in_template = templateHandler.get_template_file_list(template_name)
    for index in range(len(files_in_template)):
        lb_files_to_remove_from_template.insert(index + 1, files_in_template[index])
    scrollbar = ttk.Scrollbar(frm_window, orient=tk.VERTICAL, command=lb_files_to_remove_from_template.yview)
    lb_files_to_remove_from_template['yscrollcommand'] = scrollbar.set

    btn_remove_file = tk.Button(frm_bot, text="Remove Files", width=25, height=2, command=lambda:
                                [templateHandler.remove_files_from_template(template_name, get_listbox_variables(lb_files_to_remove_from_template, lb_files_to_remove_from_template.curselection())),
                                 update_main_window(label, listbox), remove_files_from_template_window.destroy()])
    btn_cancel = tk.Button(frm_bot, text="Cancel", width=25, height=2, command=remove_files_from_template_window.destroy)

    lbl.pack()
    lb_files_to_remove_from_template.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    btn_remove_file.pack(side=tk.LEFT)
    btn_cancel.pack(side=tk.RIGHT)
    frm_window.pack()
    frm_bot.pack()


def get_listbox_variables(listbox, listbox_selection):
    """
    This method reads the selected contents of a listbox, and returns a list with all of its values.
    :param listbox: The listbox we're reading from.
    :param listbox_selection: User's selection from listbox.
    :return: List of selected values in listbox.
    """
    listbox_input = []
    for i in listbox_selection:
        listbox_input.append(listbox.get(i))
    return listbox_input


def update_main_window(label, listbox):
    label.config(text="{} available templates to clean.".format(len(templateHandler.get_list_of_template_names())))
    template_names = templateHandler.get_list_of_template_names()
    lb_values = tk.Variable(value=template_names)
    listbox.config(listvariable=lb_values)
