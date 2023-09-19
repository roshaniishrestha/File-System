
# Student ID:220084
# Student Name:Roshani Shrestha
# Module: Platforms and operating system
# file system


import os
import tkinter as tk
import customtkinter as ct
from tkinter import messagebox, simpledialog, filedialog, scrolledtext, Image
from PIL import Image, ImageTk
import shutil
import sys #read function
import subprocess #readfunction
appearance_mode = 'dark'

file_listbox = None
current_dir_label = None

# Switch for apperance mode light and dark
def switch_mode():
    global appearance_mode
    if appearance_mode == 'dark':
        appearance_mode = 'light'
        ct.set_appearance_mode('light')
    else:
        appearance_mode = 'dark'
        ct.set_appearance_mode('dark')


def create_file():
    try:
        file_name = simpledialog.askstring(
            "Create File", "Enter the file name:")
        if file_name:
            file_path = os.path.join(current_dir, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write("This is a new file.")
                update_file_list()
            else:
                messagebox.showerror("Error", "File already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating file: {e}")


def create_folder():
    try:
        folder_name = simpledialog.askstring(
            "Create Folder", "Enter the folder name:")
        if folder_name:
            folder_path = os.path.join(current_dir, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                update_file_list()
            else:
                messagebox.showerror("Error", "Folder already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating folder: {e}")


def set_permissions(path, perms):
    try:
        os.chmod(path, perms)
        print("Permissions set successfully")
    except Exception as e:
        print(f"Error setting permissions: {e}")

import os

def set_file_permission():
    try:
        file_path = filedialog.askopenfilename(title="Select File")
        if file_path:
            if os.path.exists(file_path):
                # Check if the current user has write access
                if os.access(file_path, os.W_OK):
                    perm_string = simpledialog.askstring(
                        "Set File Permission", "Enter file permission (e.g., 555):")
                    if perm_string:
                        if len(perm_string) == 3 and perm_string.isdigit():
                            try:
                                perms = int(perm_string, 8)
                                # Set the desired permission
                                os.chmod(file_path, perms)

                                # Additional check to ensure the permission is correctly set
                                current_perms = os.stat(file_path).st_mode & 0o777
                                if current_perms == perms:
                                    messagebox.showinfo(
                                        "Success", "File permission set successfully.")
                                else:
                                    messagebox.showerror(
                                        "Error", "Error setting file permission.")
                            except ValueError:
                                messagebox.showerror(
                                    "Error", "Invalid input. Please enter a valid three-digit number.")
                        else:
                            messagebox.showerror(
                                "Error", "Invalid input. Please enter a valid three-digit number.")
                    else:
                        messagebox.showerror(
                            "Error", "File permission not provided.")
                else:
                    messagebox.showerror(
                        "Error", "You don't have write permission on this file.")
            else:
                messagebox.showerror("Error", "File not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Error setting file permission: {e}")


# def set_file_permission():
#     try:
#         file_path = filedialog.askopenfilename(title="Select File")
#         if file_path:
#             if os.path.exists(file_path):
#                 # Get the current file permissions
#                 current_perms = os.stat(file_path).st_mode & 0o777

#                 perm_string = simpledialog.askstring(
#                     "Set File Permission", "Enter file permission (e.g., 777):")
#                 if perm_string:
#                     if len(perm_string) == 3 and perm_string.isdigit():
#                         try:
#                             perms = int(perm_string, 8)

#                             # Check if the current user has write access
#                             if current_perms & 0o200 == 0:
#                                 messagebox.showerror(
#                                     "Error", "You don't have write permission on this file.")
#                                 return

#                             # Reset permission inheritance before setting new permission
#                             # Set initial permission to 600
#                             set_permissions(file_path, 0o600)
#                             # Set the desired permission
#                             set_permissions(file_path, perms)
#                             messagebox.showinfo(
#                                 "Success", "File permission set successfully.")
#                         except ValueError:
#                             messagebox.showerror(
#                                 "Error", "Invalid input. Please enter a valid three-digit number.")
#                     else:
#                         messagebox.showerror(
#                             "Error", "Invalid input. Please enter a valid three-digit number.")
#                 else:
#                     messagebox.showerror(
#                         "Error", "File permission not provided.")
#             else:
#                 messagebox.showerror("Error", "File not found!")
#     except Exception as e:
#         messagebox.showerror("Error", f"Error setting file permission: {e}")


def copy_item():
    try:
        selected_item = file_listbox.get(file_listbox.curselection())
        if selected_item:
            item_path = os.path.join(current_dir, selected_item)
            if os.path.exists(item_path):
                dest_folder = filedialog.askdirectory(
                    title="Select a destination folder")
                if dest_folder:
                    dest_path = os.path.join(
                        dest_folder, os.path.basename(item_path))
                    if os.path.exists(dest_path):
                        messagebox.showerror(
                            "Error", "File/folder with the same name already exists in the destination folder.")
                        return

                    if os.path.isfile(item_path):
                        shutil.copy(item_path, dest_path)
                    else:
                        shutil.copytree(item_path, dest_path)

                    update_file_list()
                    messagebox.showinfo("Success", "Item copied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error copying item: {e}")


def rename_item():
    try:
        selected_item = file_listbox.get(file_listbox.curselection())
        if selected_item:
            item_path = os.path.join(current_dir, selected_item)
            new_name = simpledialog.askstring(
                "Rename Item", "Enter the new name for the item:")
            if new_name:
                new_path = os.path.join(current_dir, new_name)
                if not os.path.exists(new_path):
                    os.rename(item_path, new_path)
                    update_file_list()
                else:
                    messagebox.showerror(
                        "Error", "An item with the new name already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error renaming item: {e}")


def delete_file():
    try:
        selected_file = file_listbox.get(file_listbox.curselection())
        if selected_file:
            file_path = os.path.join(current_dir, selected_file)
            if os.path.exists(file_path):
                result = messagebox.askokcancel(
                    "Confirm Delete", f"Are you sure you want to delete '{selected_file}'?")
                if result:
                    os.remove(file_path)
                    update_file_list()
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {e}")


def delete_folder():
    try:
        selected_folder = file_listbox.get(file_listbox.curselection())
        if selected_folder:
            folder_path = os.path.join(current_dir, selected_folder)
            if os.path.exists(folder_path):
                result = messagebox.askokcancel(
                    "Confirm Delete", f"Are you sure you want to delete '{selected_folder}'?")
                if result:
                    if os.path.isdir(folder_path):
                        # Use shutil.rmtree() to delete folders with contents.
                        shutil.rmtree(folder_path)
                        update_file_list()
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {e}")


def move_item():
    try:
        selected_item = file_listbox.get(file_listbox.curselection())
        if selected_item:
            item_path = os.path.join(current_dir, selected_item)
            if os.path.exists(item_path):
                new_location = filedialog.askdirectory(
                    title="Select a destination folder")
                if new_location:
                    new_path = os.path.join(
                        new_location, os.path.basename(item_path))
                    try:
                        shutil.move(item_path, new_path)
                        update_file_list()
                        messagebox.showinfo(
                            "Success", "Item moved successfully.")
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Error moving item: {e}")
                else:
                    messagebox.showerror(
                        "Error", "No destination folder selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Error moving item: {e}")


def read_file():
    try:
        selected_file = file_listbox.get(file_listbox.curselection())
        if selected_file:
            file_path = os.path.join(current_dir, selected_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    file_content = f.read()

                # Create a custom dialog with a scrollbar
                dialog = tk.Toplevel()
                dialog.iconbitmap('3.ico')
                dialog.title("File Content")

                text_widget = scrolledtext.ScrolledText(
                    dialog, wrap=tk.WORD, width=80, height=80)
                text_widget.insert(tk.END, file_content)
                text_widget.pack(fill=tk.BOTH, expand=True)

                dialog.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")






def open_text_editor(file_path):
    try:
        # Open the file in the default text editor based on the operating system
        if sys.platform.startswith('win'):
            subprocess.Popen(['notepad.exe', file_path])
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', file_path])
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', '-t', file_path])
    except Exception as e:
        print(f"Error opening text editor: {e}")

def write_file():
    try:
        selected_file = file_listbox.get(file_listbox.curselection())
        if selected_file:
            file_path = os.path.join(current_dir, selected_file)
            if os.path.exists(file_path):
                # Open the text editor with the file
                open_text_editor(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening file: {e}")



def update_file_list():
    global file_listbox
    try:
        file_listbox.delete(0, tk.END)
        files = os.listdir(current_dir)
        for file in files:
            file_listbox.insert(tk.END, file)
    except Exception as e:
        messagebox.showerror("Error", f"Error updating file list: {e}")


def change_directory():
    global current_dir, currret_dir_label
    try:

        new_dir = filedialog.askdirectory()
        if new_dir:
            current_dir = new_dir
            current_dir_label.configure(
                text=f"Current Directory: {current_dir}")
            update_file_list()
    except Exception as e:
        messagebox.showerror("Error", f"Error changing directory: {e}")


def secondwin():
    global current_dir, current_dir_label, file_listbox, status_label
    try:
        current_dir = os.getcwd()

        root = ct.CTk()
        root.title("File Manager")
        root.wm_iconbitmap('3.ico')
        frame = ct.CTkFrame(root)
        frame.pack(padx=10, pady=10)

        # Top Frame for change_dir_button and current_dir_label
        top_frame = ct.CTkFrame(frame)
        top_frame.grid(row=0, column=0, columnspan=4)

        # Create the status_label widget
        status_label = ct.CTkLabel(top_frame, text="", text_color="red")
        status_label.pack(side=tk.BOTTOM, pady=5)

        label = ct.CTkLabel(
            top_frame, text="Created By Roshani Shrestha")
        label.pack(pady=15)

        label = ct.CTkLabel(
            top_frame, text="Platforms and Operating System")
        label.pack()

        change_dir_button = ct.CTkButton(
            top_frame, text="Change Directory", fg_color="red",
            hover_color=("maroon"),
            text_color=("white"), command=change_directory)
        change_dir_button.pack(pady=10)

        current_dir_label = ct.CTkLabel(
            top_frame, text=f"Current Directory: {current_dir}")
        current_dir_label.pack()

        file_listbox = tk.Listbox(
            frame, selectmode=tk.SINGLE, width=120, height=10)

        scrollbar = tk.Scrollbar(
            frame, orient=tk.VERTICAL, command=file_listbox.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")
        file_listbox.configure(yscrollcommand=scrollbar.set)
        file_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Buttons Frame
        buttons_frame = ct.CTkFrame(frame)
        buttons_frame.grid(row=2, column=0, columnspan=4, pady=5)

        create_file_button = ct.CTkButton(
            buttons_frame, text="Create File",
            fg_color="#95BF39",
            hover_color=("maroon"),
            text_color=("white"), command=create_file)
        create_file_button.grid(row=0, column=0, padx=5, pady=5)

        create_folder_button = ct.CTkButton(
            buttons_frame, text="Create Folder", fg_color="#2099B4",
            hover_color=("maroon"),
            text_color=("white"), command=create_folder)
        create_folder_button.grid(row=0, column=1, padx=5)

        set_file = ct.CTkButton(
            buttons_frame, text="Set File Permissions",
            fg_color="#FB3F03",
            hover_color=("maroon"),
            text_color=("white"), command=set_file_permission)
        set_file.grid(row=0, column=2, padx=5)

        read_button = ct.CTkButton(buttons_frame, text="Read File", fg_color="purple",
                                   hover_color=("maroon"),
                                   text_color=("white"), command=read_file)
        read_button.grid(row=0, column=3, padx=5)

        write_button = ct.CTkButton(
            buttons_frame, text="Write", fg_color="orange",
            hover_color=("maroon"),
            text_color=("white"),
            command=write_file)
        write_button.grid(row=0, column=4, padx=5)

        delete_button = ct.CTkButton(
            buttons_frame, text="Delete File", fg_color="#FD2F7B",
            hover_color=("maroon"),
            text_color=("white"), command=delete_file)
        delete_button.grid(row=1, column=0, padx=5)

        delete_btn = ct.CTkButton(
            buttons_frame, text="Delete Folder", fg_color="#DE4249",
            hover_color=("maroon"),
            text_color=("white"), command=delete_folder)
        delete_btn.grid(row=1, column=1, padx=5)

        copy_file_folder_button = ct.CTkButton(
            buttons_frame, text="Copy/Paste",
            fg_color="#5313E6",
            hover_color=("maroon"),
            text_color=("white"), command=copy_item)
        copy_file_folder_button.grid(row=1, column=2, padx=5)

        rename = ct.CTkButton(
            buttons_frame, text="Rename", fg_color="blue",
            hover_color=("maroon"),
            text_color=("white"), command=rename_item)
        rename.grid(row=1, column=3, padx=5)

        move = ct.CTkButton(
            buttons_frame, text="Move", fg_color="#00813C",
            hover_color=("maroon"),
            text_color=("white"),
            command=move_item)
        move.grid(row=1, column=4, padx=5)

        switch = ct.CTkSwitch(root, text="Mode", command=switch_mode)
        switch.pack(pady=5)

        update_file_list()

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error occurred: {e}")


def validate_admin_password():
    admin_password = "roshani"  # Replace this with your actual admin password
    password = password_entry.get()
    re_password = re_password_entry.get()

    if password == admin_password and password == re_password:
        login_window.destroy()
        secondwin()
    else:
        messagebox.showerror("Error", "Passwords do not match!")


# Login window
if __name__ == "__main__":
    login_window = ct.CTk()
    login_window.wm_iconbitmap('3.ico')
    login_window.title("Login")
    login_window.geometry("600x350")

    admin_label = ct.CTkLabel(
        login_window, text="File Managing System")
    admin_label.pack(pady=15)

# logo
    picture_image = Image.open("Simple Document Folder Logo (1).ico")
    picture_image = picture_image.resize((50, 50))

    # Create a PhotoImage object from the PIL Image
    picture_ctk_image = ImageTk.PhotoImage(picture_image)

    # Create a label to display the image
    picture_label = tk.Label(login_window, image=picture_ctk_image)
    picture_label.image = picture_ctk_image
    picture_label.pack(pady=5)
# logo ends

    password_label = ct.CTkLabel(login_window, text="Enter Admin Password:")
    password_label.pack(pady=5)

    password_entry = ct.CTkEntry(login_window, show="*")
    password_entry.pack(pady=5)

    re_admin_label = ct.CTkLabel(login_window, text="Re-enter Admin Password:")
    re_admin_label.pack(pady=5)

    re_password_entry = ct.CTkEntry(login_window, show="*")
    re_password_entry.pack(pady=5)

    submit_button = ct.CTkButton(login_window, text="Submit", fg_color="#DE4249",
                                 hover_color="maroon", text_color="white", command=validate_admin_password)
    submit_button.pack(pady=4)

    switch = ct.CTkSwitch(login_window, text="Mode", command=switch_mode)
    switch.pack(pady=5)

    login_window.mainloop()
