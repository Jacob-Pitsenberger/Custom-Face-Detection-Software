"""
Module:settings_frame.py
Author: Jacob Pitsenberger
Date: 12-19-23

Description:
    This module defines the DetectorSettings class, responsible for creating a graphical user interface (GUI) to configure
    settings for face detection, such as enabling/disabling detection bounding boxes and applying blurring effects.
    It uses the customtkinter library for GUI development and incorporates a basic frontal face detector.

Classes:
- DetectorSettings: A class representing the GUI for configuring face detection settings.

Dependencies:
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- face_detection_package.frontal_face_detector: Module containing the FrontalFaceDetector class for face detection.

Attributes:
- draw_box (bool): Indicates whether to display detection bounding boxes.
- draw_blur (bool): Indicates whether to apply blurring effects to detections.
"""

import customtkinter as ctk
from face_detection_package.frontal_face_detector import FrontalFaceDetector


class DetectorSettings(ctk.CTkFrame):
    def __init__(self, parent):
        """
        Initialize the Settings instance.

        Args:
            parent: The parent widget.

        Returns:
            None
        """
        super().__init__(parent)
        self.place(x=0, rely=0.2, relwidth=0.6, relheight=0.8)

        self.parent = parent
        self.gui_red = self.parent.gui_red
        self.gui_blue = self.parent.gui_blue

        # create the widgets
        self.settings_frame = ctk.CTkFrame(self, border_width=2, border_color=self.gui_red)

        self.settings_label = ctk.CTkLabel(self.settings_frame, text='Settings', font=('Roboto', 20, 'bold'),
                                           bg_color=self.gui_red, text_color='white')

        self.detector_label = ctk.CTkLabel(self.settings_frame, text="Basic Frontal Face Detector",
                                           font=('Roboto', 14, 'bold', 'italic'), text_color='white')

        self.effects_label = ctk.CTkLabel(self.settings_frame, text='Effects:', font=('Roboto', 14), text_color='white')

        self.bbox_cb = ctk.CTkCheckBox(self.settings_frame, text='Show Detection Bounding Box', fg_color=self.gui_blue,
                                       font=('Roboto', 12), text_color='white', border_color=self.gui_blue)
        self.bbox_cb.select()

        self.blur_cb = ctk.CTkCheckBox(self.settings_frame, text='Blur Detections', fg_color=self.gui_blue,
                                       font=('Roboto', 12),
                                       text_color='white', border_color=self.gui_blue)

        self.bottom_border_lbl = ctk.CTkLabel(self.settings_frame, text='', bg_color=self.gui_red, text_color='white')

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Set the default effect and face detector settings.
        self.draw_box = True
        self.draw_blur = False

        # Initialize face detector
        self.haar_detector = FrontalFaceDetector(self)

        # Set the default face detector
        self.face_detector = self.haar_detector  # Set the default detector

        # Create IntVar to track the state of checkboxes
        self.bbox_var = ctk.IntVar(value=1)
        self.blur_var = ctk.IntVar(value=0)

        # Connect checkbox variables to their respective callbacks
        self.bbox_cb.configure(variable=self.bbox_var, command=self.update_checkbox)
        self.blur_cb.configure(variable=self.blur_var, command=self.update_checkbox)

        self.static_mode_flag = False  # Default value, change as needed

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create widgets for the Settings frame.

        Returns:
            None
        """
        # settings layout
        self.settings_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))
        self.settings_label.pack(fill='both', pady=(0, 10), ipady=15)
        # Add a label for the detector
        self.detector_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.effects_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.bbox_cb.pack(pady=10, padx=(20, 0), anchor='w')
        self.blur_cb.pack(pady=10, padx=(20, 0), anchor='w')
        self.bottom_border_lbl.pack(fill='both', side='bottom')

    def update_checkbox(self) -> None:
        """
        Update the draw box and draw blur attributes based on checkbox states.

        Returns:
            None
        """
        self.draw_box = bool(self.bbox_var.get())
        self.draw_blur = bool(self.blur_var.get())
        print(f'draw box set to {self.draw_box}')
        print(f'draw blur set to {self.draw_blur}')
