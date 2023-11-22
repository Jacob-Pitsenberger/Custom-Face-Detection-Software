"""
Module: utils.py
Author: Jacob Pitsenberger
Date: 11/22/23

Description:
    This module provides utility functions for the face detection application. It includes functions for
    opening a file explorer dialog, opening a file with the default system player, and handling file operations.

Functions:
- open_file_explorer() -> str: Opens a file explorer dialog to allow the user to select a file.
- open_with_default_player(file_path: str) -> None: Opens a file using the default system application.
- open_file_with_default_player() -> None: Opens a file selected by the user using the default system application.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

from tkinter import filedialog
import os
import subprocess

RED = '#4a020d'
BLUE = '#06003d'

def open_file_explorer() -> str:
    """
    Open a file explorer dialog to allow the user to select a file.

    Returns:
        str: The path of the selected file.
    """
    try:
        initial_dir = os.path.join(os.getcwd())
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All files", "*.*")])
        # `file_path` will contain the path of the selected file.
        print("Selected file:", file_path)
        return file_path
    except Exception as e:
        print(f"Error opening file explorer: {e}")
        return None

def open_with_default_player(file_path: str) -> None:
    """
    Open a file using the default system application.

    Args:
        file_path (str): The path to the file to be opened.

    Returns:
        None
    """
    try:
        if os.name == 'nt':
            os.startfile(file_path)  # Opens the file using the default Windows application
        elif os.name == 'posix':
            subprocess.run(['xdg-open', file_path])  # Opens the file using xdg-open (Linux)
    except Exception as e:
        print(f"Error opening file: {e}")

def open_file_with_default_player() -> None:
    """
    Open a file selected by the user using the default system application.

    Returns:
        None
    """
    try:
        file_path = open_file_explorer()
        if file_path:
            open_with_default_player(file_path)
    except Exception as e:
        print(f"Error opening file with default player: {e}")