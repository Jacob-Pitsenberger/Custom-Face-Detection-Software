"""
Module: post_processing_frame.py
Author: Jacob Pitsenberger
Date: 12-19-23

Description:
    This module defines the PostProcessDetections class, which is responsible for creating a graphical user
    interface (GUI) to process video and image files, detect faces, and display the results. It uses face
    detection algorithms and provides options for video and image processing.

Classes:
- PostProcessDetections: A class representing the GUI for processing video and image files and detecting faces.

Dependencies:
- os: Provides a way to interact with the operating system, such as file path manipulations.
- face_detection_package.utils: Contains utility functions and constants used in face detection.
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- datetime: Offers functionalities for working with dates and times.
- cv2: OpenCV library for computer vision tasks.

Constants:
- RED: Hexadecimal color code for red used in the GUI.
- BLUE: Hexadecimal color code for blue used in the GUI.
"""

import os
from face_detection_package.utils import open_file_explorer
import customtkinter as ctk
import datetime
import cv2

class PostProcessDetections(ctk.CTkFrame):
    def __init__(self, parent):
        """
        Initialize the PostProcessDetections instance.

        Args:
            parent: The parent widget.

        Returns:
            None
        """

        super().__init__(parent)
        self.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.8)

        self.parent = parent

        self.gui_red = self.parent.gui_red
        self.gui_blue = self.parent.gui_blue

        self.detections_frame = ctk.CTkFrame(self, border_width=2, border_color=self.gui_red)
        self.detections_label = ctk.CTkLabel(self.detections_frame, text='Make Detections', font=('Roboto', 20, 'bold'),
                                             bg_color=self.gui_red, text_color='white')
        self.video_btn = ctk.CTkButton(self.detections_frame, text='Process Video', fg_color=self.gui_blue, font=('Roboto', 12),
                                       text_color='white', command=self.detect_over_video)
        self.image_btn = ctk.CTkButton(self.detections_frame, text='Process Image', fg_color=self.gui_blue, font=('Roboto', 12),
                                       text_color='white', command=self.detect_over_image)
        self.status_lbl = ctk.CTkLabel(self.detections_frame, text='', font=('Roboto', 16, 'bold'), text_color='white')

        self.bottom_border_lbl = ctk.CTkLabel(self.detections_frame, text='', bg_color=self.gui_red, text_color='white')

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.face_detector = None
        print(self.face_detector)
        self.directory_manager = self.parent.directory_manager

        self.create_widgets()

    def create_detector(self, staticMode_flag: bool = None) -> None:
        """
        Create a face detector using the specified staticMode_flag.

        Args:
            staticMode_flag (bool): A flag indicating whether to use static mode for the face detector (mesh model only).

        Returns:
            None
        """
        print(f"in ... before set we have the detector = {self.face_detector} and the staticMode_flag = {staticMode_flag}")
        # Changed to set the detector directly to the haar_detector
        self.face_detector = self.parent.settings.haar_detector
        print(f"in create detector, set self.face_detector = {self.face_detector}")

    def create_widgets(self) -> None:
        """
        Create widgets for the PostProcessDetections frame.

        Returns:
            None
        """
        self.detections_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))
        self.detections_label.pack(fill='both', pady=(0, 10), ipady=15)
        self.video_btn.pack(pady=(40, 20))
        self.image_btn.pack(pady=(20, 20))
        self.status_lbl.pack()
        self.bottom_border_lbl.pack(fill='both', side='bottom')

    def clear_status_label(self) -> None:
        """
        Clear the status label text.

        Returns:
            None
        """
        try:
            self.status_lbl.configure(text="")
        except Exception as e:
            print(f"Error clearing status label: {e}")

    def detect_over_video(self) -> None:
        """
        Process a video file, detect faces in each frame, and save the output.

        Raises:
            ValueError: If the selected video file has an invalid extension.
            cv2.error: If an OpenCV-related error occurs during video processing.
            Exception: For other generic exceptions.

        Returns:
            None
        """
        try:
            self.create_detector(staticMode_flag=False)
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            video_path = open_file_explorer()
            if video_path:
                valid_extensions = ('.mp4', '.mov')
                if not video_path.lower().endswith(valid_extensions):
                    raise ValueError("Invalid file type. Please select a .mp4 or .mov file.")

                video_path_out = os.path.join(self.directory_manager.videos_dir,
                                              f'{os.path.basename(video_path)}_{timestamp}_detections.mp4')

                cap = cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                H, W, _ = frame.shape
                out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)),
                                      (W, H))

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # Update status label at the beginning of processing
                self.status_lbl.configure(text="Processing video...")
                self.update()

                for frame_count in range(total_frames):
                    ret, frame = cap.read()
                    self.face_detector.detect_faces(frame)
                    out.write(frame)

                self.clear_status_label()

                cap.release()
                out.release()
                cv2.destroyAllWindows()

                # Update status label when processing is done
                self.status_lbl.configure(text="Video detections processed")
                self.after(5000, self.clear_status_label)
        except ValueError as ve:
            print(f"ValueError in detect_over_video: {ve}")
        except cv2.error as cve:
            print(f"OpenCV Error in detect_over_video: {cve}")
        except Exception as e:
            print(f"Error in detect_over_video: {e}")

    def detect_over_image(self) -> None:
        """
        Process an image file, detect faces, and save the output.

        Raises:
            ValueError: If the selected image file has an invalid extension.
            Exception: For other generic exceptions.

        Returns:
            None
        """
        try:
            self.create_detector(staticMode_flag=True)
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            img_path = open_file_explorer()
            if img_path:
                valid_extensions = ('.png', '.jpg')
                if not img_path.lower().endswith(valid_extensions):
                    raise ValueError("Invalid file type. Please select a .png or .jpg file.")

                img_path_out = os.path.join(self.directory_manager.images_dir,
                                            f'{os.path.basename(img_path)}_{timestamp}_detections.jpg')

                img = cv2.imread(img_path)

                # Update status label at the beginning of processing
                self.status_lbl.configure(text="Processing image...")
                self.update()

                self.face_detector.detect_faces(img)
                cv2.imwrite(img_path_out, img)
                cv2.destroyAllWindows()

                # Update status label when processing is done
                self.status_lbl.configure(text="Image detections processed")
                self.after(5000, self.clear_status_label)
        except ValueError as ve:
            print(f"ValueError in detect_over_image: {ve}")
        except Exception as e:
            print(f"Error in detect_over_image: {e}")
