import tkinter as tk

window = tk.Tk()
window.title("Desk Cleaner")

def start_window(files=0):
    frm_left = tk.Frame(width=25, height=15, padx=5, pady=5)
    frm_right = tk.Frame(width=25, height=15, padx=5, pady=5)
    frm_right_inner = tk.Frame(master=frm_right)

    lbl_available_files_to_delete = tk.Label(text="{} available files to delete".format(files),width=25,
                                              master=frm_right_inner, relief=tk.GROOVE)
    btn_refresh_file_counter = tk.Button(text="0", width=2, master=frm_right_inner)
    btn_run_cleaner = tk.Button(text="Run Cleaner", width=25, height=2, master=frm_left)
    btn_create_template = tk.Button(text="Create Template", width=25, height=2, master=frm_left,
                                    command=create_template_window())
    btn_delete_template = tk.Button(text="Delete Template", width=25, height=2, master=frm_left)

    # btn_create_template.bind(create_template_window())

    lbl_available_files_to_delete.pack(side=tk.LEFT)
    btn_refresh_file_counter.pack(side=tk.RIGHT)
    btn_run_cleaner.pack()
    btn_create_template.pack()
    btn_delete_template.pack()

    frm_left.pack(side=tk.LEFT)
    frm_right.pack(side=tk.RIGHT)
    frm_right_inner.pack()
    window.mainloop()


def create_template_window():
    create_template_window = tk.Toplevel(window)
    create_template_window.title("New Template")

    frm_top = tk.Frame(master= create_template_window,padx=5, pady=5)
    frm_bot = tk.Frame(master= create_template_window, padx=5, pady=5)
    frm_inner_bot = tk.Frame(master=frm_bot, padx=5, pady=5)

    label = tk.Label(text="Template Name", master=frm_top).pack()
    entry = tk.Entry(master=frm_top).pack()
    submit_button = tk.Button(text="Submit", width=25, height=2, master=frm_inner_bot).pack(side=tk.LEFT)
    cancel_button = tk.Button(text="Cancel", width=25, height=2, master=frm_inner_bot).pack(side=tk.RIGHT)

    frm_top.pack()
    frm_bot.pack()
    frm_inner_bot.pack()
