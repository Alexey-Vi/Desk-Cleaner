import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import main
import templateHandler

log_file = "Logs.log"
logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO,
                        datefmt='%m/%d/%Y %H:%M:%S')


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
    btn_refresh_file_counter = tk.Button(text="⟲", font=10, width=2, master=frm_right_inner, command=lambda:
                                         [window.destroy(), main.create_main_window()])
    btn_run_cleaner = tk.Button(text="Run Cleaner", width=25, height=2, master=frm_left, command=run_cleaner_window)
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

    entry_input = tk.StringVar(create_template_window)

    frm_top = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_bot = tk.Frame(master=create_template_window, padx=5, pady=5)
    frm_inner_bot = tk.Frame(master=frm_bot, padx=5, pady=5)

    lbl = tk.Label(text="Template Name", master=frm_top)
    ent = tk.Entry(master=frm_top, textvariable=entry_input)
    btn_submit = tk.Button(text="Submit", width=25, height=2, master=frm_inner_bot,
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


def delete_template_window():
    """
    Template deletion window. If there are no templates saved it will inform the user with a pop-up.
    Otherwise, it will open a list of available template names and will delete the relevant template from the
    'templates.json'.
    :return: None
    """
    delete_template_window = tk.Tk()
    delete_template_window.title("Delete Template")

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


def run_cleaner_window():
    run_cleaner_window = tk.Tk()
    run_cleaner_window.title("Run Cleaner")

    frm_window = tk.Frame(master=run_cleaner_window, padx=5, pady=5)
    frm_bot = tk.Frame(master=frm_window, padx=5, pady=5)

    lbl_confirmation = tk.Label(text="Delete unapproved files?", master=frm_window)
    btn_yes = tk.Button(text="Yes", width=25, height=2, master=frm_bot,
                           command=lambda: [run_cleaner_window.destroy(), main.remove_files()])
    btn_no = tk.Button(text="No", width=25, height=2, master=frm_bot,
                           command=run_cleaner_window.destroy)

    lbl_confirmation.pack()
    btn_yes.pack(side=tk.LEFT)
    btn_no.pack(side=tk.RIGHT)
    frm_bot.pack()
    frm_window.pack()
