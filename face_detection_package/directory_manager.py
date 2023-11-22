"""
Module: directory_manager.py
Author: Jacob Pitsenberger
Date: 11-22-23

Description:
    This module provides a DirectoryManager class that manages directory paths for the Face Detection Software application.
    It includes methods to initialize directory paths and create necessary directories.

Notes:
    - 11/21/23: Commented out code to create the recordings directory since this will only be utilized for the
                post-processing detections for the initial release.
"""

import os

class DirectoryManager:
    """
    Manages directory paths for the application.
    """
    def __init__(self):
        """
        Initialize directory paths.
        """
        # Path to the root directory (current working directory).
        self.root_dir = os.getcwd()

        # Path to the different detections Directories.
        # self.recordings_dir = os.path.join(self.root_dir, 'recorded_detections')
        self.videos_dir = os.path.join(self.root_dir, 'video_detections')
        self.images_dir = os.path.join(self.root_dir, 'image_detections')
        # self.directories = [self.root_dir, self.recordings_dir, self.videos_dir, self.images_dir]
        self.directories = [self.root_dir, self.videos_dir, self.images_dir]

    def create_directories(self) -> None:
        """
        Create necessary directories if they don't exist.
        """
        try:
            for directory in self.directories:
                if not os.path.exists(directory):
                    os.makedirs(directory)
        except Exception as e:
            print(f"Error creating directories: {e}")
