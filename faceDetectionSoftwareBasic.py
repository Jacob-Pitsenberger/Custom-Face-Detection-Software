"""
Module: faceDetectionSoftwareBasic.py
Author: Jacob Pitsenberger
Last Updated: 12/19/23

Description:
    This module serves as the entry point for the Face Detection Software application. It initializes the GUI
    as either the post-processing version or the realtime feeds version specified by the input parameter,
    and starts the main event loop.

Usage:
    To run this module, execute the module using a Python interpreter.

Note:
    - Set the version parameter to 'rf' for the realtime feed app or 'pp' for the postprocessing app.
"""

from face_detection_package.gui import App
import logging

if __name__ == "__main__":
    try:
        App(version='rf')
    except Exception as e:
        logging.error(f"Error in main: {e}")

