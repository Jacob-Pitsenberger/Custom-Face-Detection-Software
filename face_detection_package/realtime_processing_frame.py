"""
Module: realtime_processing_frame.py
Author: Jacob Pitsenberger
Date: 12-19-23

Description:
    This module defines the ProcessRealtimeDetections class, which is responsible for creating a graphical user
    interface (GUI) to process realtime video feeds from internal or external webcams, detect faces, and display the results.
    It uses face detection algorithms and provides options for internal or external webcams processing.

Classes:
- ProcessRealtimeDetections: A class representing the GUI for processing realtime video feeds from internal or external webcams
  and detecting faces.

Dependencies:
- os: Provides a way to interact with the operating system, such as file path manipulations.
- customtkinter as ctk: A customized version of the tkinter library for GUI development.
- datetime: Offers functionalities for working with dates and times.
- cv2: OpenCV library for computer vision tasks.
"""

import os
import customtkinter as ctk
import datetime
import cv2


class ProcessRealtimeDetections(ctk.CTkFrame):
    def __init__(self, parent):
        """
        Initialize the ProcessRealtimeDetections instance.

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

        self.internal_webcam_btn = ctk.CTkButton(self.detections_frame, text="Internal Webcam Feed",
                                                 fg_color=self.gui_blue, font=('Roboto', 12),
                                                 text_color='white', command=lambda: self.detect_over_webcam(0))

        self.external_webcam_btn = ctk.CTkButton(self.detections_frame, text="External Webcam Feed",
                                                 fg_color=self.gui_blue, font=('Roboto', 12),
                                                 text_color='white', command=lambda: self.detect_over_webcam(1))

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
        print(
            f"in ... before set we have the detector = {self.face_detector} and the staticMode_flag = {staticMode_flag}")
        # Modify the following line to set the detector directly
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
        self.internal_webcam_btn.pack(pady=(40, 20))
        self.external_webcam_btn.pack(pady=(20, 20))
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

    def detect_over_webcam(self, channel: int) -> None:
        """
        Detect faces in the internal or external webcam feed.

        Args:
            channel (int): The channel number of the camera to detect faces over.

        Raises:
            ValueError: If the selected camera channel is unable to be connected to.
            cv2.error: If an OpenCV-related error occurs during realtime feed processing.
            Exception: For other generic exceptions.

        Returns:
            None
        """
        try:
            self.create_detector(staticMode_flag=True)
            print(f"In detect over webcam,\n detector = {self.face_detector}")
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            cap = cv2.VideoCapture(channel)

            if not cap.isOpened():
                # Update the status label after processing
                self.status_lbl.config(
                    text=f"Error opening camera.\n Please check if an external\n camera is connected.")
                # Schedule clearing the label after 5 seconds
                self.after(5000, self.clear_status_label)
                raise ValueError(
                    f"Error opening camera channel {channel}. Please check if an external camera is connected.")

            # Create a VideoWriter object
            out = cv2.VideoWriter(
                os.path.join(self.directory_manager.recordings_dir, f'{timestamp}_{channel}_webcam_recording.mp4'),
                cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (640, 480))

            while True:
                ret, frame = cap.read()
                print("in detect webcam, read capture and calling face detector.detect_faces method on frame")
                self.face_detector.detect_faces(frame)
                print("method called, writing to file and showing...")
                out.write(frame)
                cv2.imshow("Webcam - Press 'q' key to quit.", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        except cv2.error as cve:
            print(f"OpenCV Error in detect_over_webcam: {cve}")
        except Exception as e:
            print(f"Error in detect_over_webcam: {e}")
