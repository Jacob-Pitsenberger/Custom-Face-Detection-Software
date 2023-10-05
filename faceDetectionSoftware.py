"""
Module: faceDetectionSoftware.py
Author: Jacob Pitsenberger
Dates:
    v1: 9-27-23
    v2: 10-2-23

Description:
    This module serves as the entry point for the Face Detection Software application. It initializes the GUI
    version and starts the main event loop.

Versions:
    v1 (1) - Face Detection using Viola-Jones Frontal Face Cascade detector.
    v2 (2) - Face Detection using Google MediaPipe Face Mesh Model.

Usage:
    To run this module, specify the detector version (1 or 2) to use and execute the module using a Python interpreter.
"""

from face_detection_package.gui import GUI


if __name__ == "__main__":
    try:
        # Initialize the GUI
        gui = GUI(version=1)
        # Call the run_app method to run tkinter mainloop
        gui.run_app()
    except Exception as e:
        print(f"Error in main: {e}")

