"""
Module: faceDetectionSoftware.py
Author: Jacob Pitsenberger
Last Updated: 11/21/23

Description:
    This module serves as the entry point for the Face Detection Software application. It initializes the GUI
    starting the main event loop.

Usage:
    To run this module, execute the module using a Python interpreter.
"""

from face_detection_package.gui_basic import GUI
from face_detection_package.gui_custom import App


if __name__ == "__main__":
    try:
        # Initialize the GUI
        # gui = GUI()
        App()
        # Call the run_app method to run tkinter mainloop
        # gui.run_app()
    except Exception as e:
        print(f"Error in main: {e}")


