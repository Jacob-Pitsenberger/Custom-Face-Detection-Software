"""
Module: nav_frame.py
Author: Jacob Pitsenberger
Date: 12/19/23

Description:
    This module defines the Navigation class, which handles the navigation menu for the face detection application.
    It includes options to navigate between different sections of the application, such as post-processing and settings.

Classes:
- Nav: A class representing the navigation menu for the face detection application.

Dependencies:
- customtkinter as ctk: A customized version of the tkinter library for GUI development.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

import customtkinter as ctk
from face_detection_package.utils import open_file_with_default_player


class Nav(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.2)
        self.parent = parent
        self.gui_red = self.parent.gui_red
        self.gui_blue = self.parent.gui_blue
        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        title_frame = ctk.CTkFrame(self, border_width=2, border_color=self.gui_red, fg_color=self.gui_red)

        label = ctk.CTkLabel(title_frame, text='FACE DETECTION SOFTWARE - BASIC', font=('Roboto', 20, 'bold'),
                             text_color='white')
        files_btn = ctk.CTkButton(title_frame, text='Files', width=75, fg_color=self.gui_blue, font=('Roboto', 12),
                                  text_color='white',
                                  command=open_file_with_default_player)
        help_btn = ctk.CTkButton(title_frame, text='Help', width=75, fg_color=self.gui_blue, font=('Roboto', 12),
                                 text_color='white',
                                 command=lambda: self.show_help())

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Add the widgets
        title_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(5, 5), padx=(5, 5))
        label.pack(expand=True, side='left', fill='both', padx=(10, 40), pady=10)
        files_btn.pack(side='right', padx=5)
        help_btn.pack(side='right', padx=5)

    @staticmethod
    def show_help() -> None:
        """
        Display help information in a separate window.
        """
        try:
            help_text = """
                Welcome to the Face Detection Software!

                Instructions:
                1. Specify the detector version by selecting it from the drop-down menu in the settings frame.
                2. Check the boxes in the settings frame for the effects you want applied to detections.
                3. In the post-processing frame, press the 'Video' button to open the file explorer and select a video file for detections.
                4. In the post-processing frame, press the 'Image' button to open the file explorer and select an image file for detections.
                5. After selecting either post-processing button, text will appear on the interface indicating that the selected file is 
                   being processed for detections. When detections are done processing, this message will update indicating success.

                Buttons:
                - Files Button: Click this button to open the file explorer and select a file to view.
                - Help Button: Click this button to view instructions on how to use the program.

                Notes:
                - Ensure you use video/image files with valid extensions (.mp4, .mov, .jpg, .png) when making detections.
                - Image and video detections are saved to the 'image_detections' and 'video_detections' directories, respectively.
                - A message will notify you when detections are being processed and when they are done processing.
                  (Note: The GUI will appear unresponsive until the success message appears.)
                - The detector is initialized when either the 'Video' or Image' detection button is pressed and is 
                  done so with the current values specified in the settings frame.

                Enjoy using the Face Detection Software!
                """
            help_window = ctk.CTk()
            help_window.title("Help")

            help_label = ctk.CTkLabel(help_window, text=help_text, font=('Roboto', 12), justify='left')
            help_label.pack(padx=10)

            help_window.mainloop()
        finally:
            help_window.quit()



