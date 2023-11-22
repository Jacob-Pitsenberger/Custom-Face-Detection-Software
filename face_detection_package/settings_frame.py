"""
Module: settings_frame.py
Author: Jacob Pitsenberger
Date: 11/22/23

Description:
    This module defines the Settings class, responsible for creating a graphical user interface (GUI) to adjust
    settings related to face detection. Users can choose the face detection algorithm, toggle visualization
    effects, and configure additional options.

Classes:
- Settings: A class representing the GUI for adjusting face detection settings.

Dependencies:
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- face_detection_package.frontal_face_detector: Module containing the FrontalFaceDetector class.
- face_detection_package.mesh_face_detector: Module containing the FaceMeshDetector class.
- face_detection_package.utils: Contains utility functions and constants used in face detection.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

import customtkinter as ctk
from face_detection_package.frontal_face_detector import FrontalFaceDetector
from face_detection_package.mesh_face_detector import FaceMeshDetector
from face_detection_package.utils import RED, BLUE

class Settings(ctk.CTkFrame):
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

        # create the widgets
        self.settings_frame = ctk.CTkFrame(self, border_width=2, border_color=RED)

        self.settings_label = ctk.CTkLabel(self.settings_frame, text='Settings', font=('Roboto', 20, 'bold'),
                                           bg_color=RED, text_color='white')

        self.detector_label = ctk.CTkLabel(self.settings_frame, text='Detector:', font=('Roboto', 14), text_color='white')

        self.detector_options = ['Basic: Frontal Face Detector', 'Advanced: Mesh Face Detector']
        self.detector_menu_var = ctk.StringVar(value=self.detector_options[0])

        self.detector_menu = ctk.CTkOptionMenu(self.settings_frame, values=self.detector_options,
                                               variable=self.detector_menu_var,
                                               fg_color=BLUE, font=('Roboto', 12), text_color='white')

        self.effects_label = ctk.CTkLabel(self.settings_frame, text='Effects:', font=('Roboto', 14), text_color='white')

        self.bbox_cb = ctk.CTkCheckBox(self.settings_frame, text='Show Detection Bounding Box', fg_color=BLUE,
                                       font=('Roboto', 12), text_color='white', border_color=BLUE)
        self.bbox_cb.select()

        self.blur_cb = ctk.CTkCheckBox(self.settings_frame, text='Blur Detections', fg_color=BLUE, font=('Roboto', 12),
                                       text_color='white', border_color=BLUE)
        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.parent = parent

        # Set the default effect and face detector settings.
        self.draw_box = True
        self.draw_feed_info = False
        self.draw_blur = False
        self.face_detector = None
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create widgets for the Settings frame.

        Returns:
            None
        """
        # settings layout
        self.settings_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))
        self.settings_label.pack(fill='both')
        self.detector_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.detector_menu.pack(pady=(0, 20), padx=(20, 20), anchor='w', fill='x')
        self.effects_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.bbox_cb.pack(pady=10, padx=(20, 0), anchor='w')
        self.blur_cb.pack(pady=10, padx=(20, 0), anchor='w')

    def set_draw_box(self) -> None:
        """
        Set the draw box attribute based on the checkbox state.

        Returns:
            None
        """
        state: int = self.bbox_cb.get()
        self.draw_box = state == 1
        print(f'draw box set to {self.draw_box}')
        """
        if self.bbox_cb.get() == 1:
            print('draw box set to True')
            self.draw_box = True
        elif self.bbox_cb.get() == 0:
            print('draw box set to False')
            self.draw_box = False
        """

    def set_draw_blur(self) -> None:
        """
        Set the draw blur attribute based on the checkbox state.

        Returns:
            None
        """
        state: int = self.blur_cb.get()
        self.draw_blur = state == 1
        print(f'draw blur set to {self.draw_blur}')
        """
        if self.blur_cb.get() == 1:
            print('draw blur set to True')
            self.draw_blur = True
        elif self.blur_cb.get() == 0:
            print('draw blur set to False')
            self.draw_blur = False
        """

    def set_detector(self, staticMode_flag: bool) -> None:
        """
        Set the face detector based on the selected option and settings.

        Args:
            staticMode_flag (bool): A flag indicating whether to use static mode for the face detector (mesh model only).

        Returns:
            None
        """
        try:
            self.set_draw_box()
            self.set_draw_blur()
            if self.detector_menu_var.get() == self.detector_options[0]:
                print("detector version 1 selected")
                self.face_detector = FrontalFaceDetector(self.draw_box, self.draw_blur)
                print(self.face_detector)
            elif self.detector_menu_var.get() == self.detector_options[1]:
                print("detector version 2 selected")
                if staticMode_flag:
                    self.face_detector = FaceMeshDetector(self.draw_box, self.draw_blur, True)
                    print(self.face_detector)
                    print(f'Initialized with staticMode set to True for image detections')
                elif staticMode_flag is False:
                    self.face_detector = FaceMeshDetector(self.draw_box, self.draw_blur, False)
                    print(self.face_detector)
                    print(f'Initialized with staticMode set to False for video and realtime detections')
        except Exception as e:
            print(f"Error setting detector option: {e}")
        finally:
            print(f"Reset Settings To:\n Detector: {self.face_detector}\n draw box: {self.draw_box} "
                  f"\n draw blur: {self.draw_blur} \n staticMode_flag: {staticMode_flag}")


