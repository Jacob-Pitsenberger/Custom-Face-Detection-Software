"""
Module: gui_custom.py
Author: Jacob Pitsenberger
Date: 11/22/23

Description:
    This module defines the Application class, which serves as the main entry point for the face detection
    application. It creates the main window, initializes the navigation menu, and manages the overall structure
    of the application.

Classes:
- Application: A class representing the main face detection application.

Dependencies:
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- Navigation: Module containing the Navigation class.
- PostProcessDetections: Module containing the PostProcessDetections class.
- Settings: Module containing the Settings class.
- face_detection_package.directory_manager: Module containing the DirectoryManager class for managing directories.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

import customtkinter as ctk
from face_detection_package.nav_frame import Nav
from face_detection_package.settings_frame import Settings
from face_detection_package.post_processing_frame import PostProcessDetections
from face_detection_package.directory_manager import DirectoryManager

class App(ctk.CTk):
    def __init__(self):
        """
        Initialize the main application.

        Args:
            None

        Returns:
            None
        """
        # main setup
        super().__init__()

        # Create and configure the directory manager
        self.directory_manager = DirectoryManager()
        self.directory_manager.create_directories()

        size = (600, 370)
        self.title('FACE DETECTION SOFTWARE')
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Create widgets
        self.nav = Nav(self)
        self.settings = Settings(self)
        self.detections = PostProcessDetections(self)

        # Run the application
        self.mainloop()


def main():
    App()


if __name__ == "__main__":
    main()
