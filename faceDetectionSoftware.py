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
1. 11/2/23
- added a variable for the only effect currently functional (face blur). This is used when initializing
             the GUI instance and can be set to 'None' for standard detection rectangles.

2. 11/10/23
	Initiated the GUI class with the frontal face detector as the default and introduced an option menu for users to switch between detector versions.
	Implemented widgets allowing users to specify the detector and effects, with a button to save these settings.
	Added functionality to update the GUI class's detector and effects parameters upon pressing the save settings button.
	Ensured proper cleanup of resources from default or previous option window settings. (No changes needed)
*Note: a bug caused for the if statement in mesh detectors draw box method checking for effect is None to fail.
    - to overcome this, edited so the only if statement checks if the self.effect is set to blur and if not just draws box.

NEXT STEP - I still need to test and ensure these changes work for postprocessing detections and once confirmed
            work on styling and formatting the GUI to be more appealing and so that it is easy to add more widgets
            seamlessly if needed.
"""

from face_detection_package.gui import GUI


if __name__ == "__main__":
    try:
        # Initialize the GUI
        gui = GUI()
        # Call the run_app method to run tkinter mainloop
        gui.run_app()
    except Exception as e:
        print(f"Error in main: {e}")


