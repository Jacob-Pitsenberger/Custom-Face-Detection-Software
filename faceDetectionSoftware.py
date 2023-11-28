"""
Module: faceDetectionSoftware.py
Author: Jacob Pitsenberger
Last Updated: 11/28/23

Description:
    This module serves as the entry point for the Face Detection Software application. It initializes the GUI,
    starting the main event loop.

Usage:
    To run this module, execute the module using a Python interpreter.
"""

from face_detection_package.gui_custom import App


if __name__ == "__main__":
    try:
        App()
    except Exception as e:
        print(f"Error in main: {e}")

