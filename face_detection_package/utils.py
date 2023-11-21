from tkinter import filedialog
import os

def open_file_explorer() -> str:
    """
    Open a file explorer dialog to allow the user to select a file.

    Returns:
        str: The path of the selected file.
    """
    try:
        # initial_dir = os.path.join(os.getcwd(), '../Face Detection Software')
        initial_dir = os.path.join(os.getcwd())
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All files", "*.*")])
        # `file_path` will contain the path of the selected file.
        print("Selected file:", file_path)
        return file_path
    except Exception as e:
        print(f"Error opening file explorer: {e}")
        return None