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

REVISIONS
1. 11/2/23 - added a variable for the only effect currently functional (face blur). This is used when initializing
             the GUI instance and can be set to 'None' for standard detection rectangles.

    FUTURE ENHANCEMENT
    * Add a styling button to open a window that allows a user to set the effect parameter of the GUI class
    by specifying the effect to apply with a radio or check button.
    If this is not used, the default effect is set to None.
"""

from face_detection_package.gui import GUI


if __name__ == "__main__":
    effect = 'blur'
    try:
        # Initialize the GUI
        gui = GUI(version=1, effects=effect)
        # Call the run_app method to run tkinter mainloop
        gui.run_app()
    except Exception as e:
        print(f"Error in main: {e}")

