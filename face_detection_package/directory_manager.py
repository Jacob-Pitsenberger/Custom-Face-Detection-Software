"""
Module: directory_manager.py
Author: Jacob Pitsenberger
Date: 12-19-23

Description:
    This module provides a DirectoryManager class that manages directory paths for the Face Detection Software application.
    It includes methods to initialize directory paths and create necessary directories.
"""

import os

class DirectoryManager:
    """
    Manages directory paths for the application.
    """

    def __init__(self, version):
        """
        Initialize directory paths.
        """
        # Path to the root directory (current working directory).
        self.root_dir = os.getcwd()
        self.version = version
        # Path to the different detections Directories.
        self.recordings_dir = os.path.join(self.root_dir, 'recorded_detections')
        self.videos_dir = os.path.join(self.root_dir, 'video_detections')
        self.images_dir = os.path.join(self.root_dir, 'image_detections')
        self.directories = []  # initialize to an empty list
        self.initialize_version()

    def initialize_version(self):
        try:
            if self.version == 'pp':
                self.directories = [self.root_dir, self.videos_dir, self.images_dir]
                print('Created directories for pp version')
            elif self.version == 'rf':
                self.directories = [self.root_dir, self.recordings_dir]
                print('Created directories for rf version')
        except Exception as e:
            print(f"Error initializing directories: {e}")

    def create_directories(self) -> None:
        """
        Create necessary directories if they don't exist.
        """
        try:
            for directory in self.directories:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directories: {e}")