import logging
import tkinter as tk
import main
import configHandler


def start_window(files=0):
    """
    Main program window. All interactions come and go through here.
    :param files: How many files are currently available to be deleted.
    :return: None
    """
    window = tk.Tk()
    window.title("Desk Cleaner")
    frm_left = tk.Frame(width=25, height=15, padx=5, pady=5)
    frm_right = tk.Frame(width=25, height=15, padx=5, pady=5)
    frm_right_inner = tk.Frame(master=frm_right)

    lbl_available_files_to_delete = tk.Label(text="{} available files to delete".format(files), width=25,
                                              master=frm_right_inner, relief=tk.GROOVE)
    btn_refresh_file_counter = tk.Button(text="⟲", font=10, width=2, master=frm_right_inner)
    btn_run_cleaner = tk.Button(text="Run Cleaner", width=25, height=2, master=frm_left)
    btn_create_template = tk.Button(text="Create Template", width=25, height=2, master=frm_left,
                                    command=create_template_window)
    btn_delete_template = tk.Button(text="Delete Template", width=25, height=2, master=frm_left,
                                    command=delete_template_window)
    btn_close_window = tk.Button(text="Close", width=25, height=2, master=frm_left, command=window.destroy)

    lbl_available_files_to_delete.pack(side=tk.LEFT)
    btn_refresh_file_counter.pack(side=tk.RIGHT)
    btn_run_cleaner.pack()
    btn_create_template.pack()
    btn_delete_template.pack()
    btn_close_window.pack()

    frm_left.pack(side=tk.LEFT)
    frm_right.pack(side=tk.RIGHT)
    frm_right_inner.pack()
    window.mainloop()


def create_template_window():
    """
    New template creation window. Accessed from the main window. Receives a name for a template.
    When pressing 'Submit' will open folder hierarchy to choose which files to save as a template.
    :return: None
    """
    create_template_window = tk.Tk()
    create_template_window.title("New Template")

    frm_top = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_inner_bot = tk.Frame(master=frm_bot, padx=5, pady=5)

    lbl = tk.Label(text="Template Name", master=frm_top).pack()
    ent = tk.Entry(master=frm_top).pack()
    btn_submit = tk.Button(text="Submit", width=25, height=2, master=frm_inner_bot)
    btn_cancel = tk.Button(text="Cancel", width=25, height=2, master=frm_inner_bot,
                              command=create_template_window.destroy)

    btn_submit.pack(side=tk.LEFT)
    btn_cancel.pack(side=tk.RIGHT)
    frm_top.pack()
    frm_bot.pack()
    frm_inner_bot.pack()


def delete_template_window():
    """
    Template deletion window. If there are no templates saved it will inform the user with a pop-up.
    Otherwise, it will open a list of available template names and will delete the relevant template from the
    'templates.json'.
    :return: None
    """
    delete_template_window = tk.Tk()
    delete_template_window.title("Delete Template")

    if len(configHandler.get_config_parameter("templates.json", "templates")) == 0 and False:
        frm_window = tk.Frame(master=delete_template_window, padx=50, pady=50)

        lbl = tk.Label(text="No Templates Found", master=frm_window).pack()
        btn_cancel = tk.Button(text="Close", width=25, height=2, master=frm_window,
                               command=delete_template_window.destroy)

        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()

    else:
        frm_window = tk.Frame(master=delete_template_window, padx=5, pady=5)
        frm_bot = tk.Frame(master=delete_template_window, padx=5, pady=5)

        lbl = tk.Label(text="Template Name", master=frm_window).pack()
        # TODO add area for a interactive template list
        btn_configm = tk.Button(text="Confirm", width=25, height=2, master=frm_bot)
        btn_cancel = tk.Button(text="Cancel", width=25, height=2, master=frm_bot,
                               command=delete_template_window.destroy)

        btn_configm.pack(side=tk.LEFT)
        btn_cancel.pack(side=tk.RIGHT)
        frm_window.pack()
        frm_bot.pack()
