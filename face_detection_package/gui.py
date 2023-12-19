"""
Module: gui.py
Author: Jacob Pitsenberger
Date: 12/19/23

Description:
    This module defines the Application class, which serves as the main entry point for the face detection
    application. It creates the main window, initializes the navigation menu, and manages the overall structure
    of the application.

Classes:
- Application: A class representing the main face detection application.

Dependencies:
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- face_detection_package.nav_frame: Module containing the Navigation class.
- face_detection_package.realtime_processing_frame: Module containing the ProcessRealtimeDetections class.
- face_detection_package.post_processing_frame: Module containing the PostProcessDetections class
- face_detection_package.setting_frame: Module containing the Settings class.
- face_detection_package.directory_manager: Module containing the DirectoryManager class for managing directories.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

import customtkinter as ctk
from face_detection_package.directory_manager import DirectoryManager
from face_detection_package.nav_frame import Nav
from face_detection_package.post_processing_frame import PostProcessDetections
from face_detection_package.realtime_processing_frame import ProcessRealtimeDetections
from face_detection_package.setting_frame import DetectorSettings
from face_detection_package.utils import CUSTOM_RED, CUSTOM_BLUE

class App(ctk.CTk):
    def __init__(self, version):
        """
        Initialize the main application.

        Args:
            None

        Returns:
            None
        """
        # main setup
        super().__init__()

        self.version = version
        # Create and configure the directory manager
        self.directory_manager = DirectoryManager(self.version)
        self.directory_manager.create_directories()

        size = (600, 370)
        self.title('FACE DETECTION SOFTWARE')
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        self.resizable(False, False)

        # Define custom colors
        self.gui_red = CUSTOM_RED
        self.gui_blue = CUSTOM_BLUE

        # Create widgets
        self.nav = Nav(self)

        self.settings = DetectorSettings(self)

        if self.version == 'pp':
            self.detections = PostProcessDetections(self)
        elif self.version == 'rf':
            self.detections = ProcessRealtimeDetections(self)

        # Run the application
        self.mainloop()



