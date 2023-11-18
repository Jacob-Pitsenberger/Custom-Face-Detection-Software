"""
Module: gui.py
Author: Jacob Pitsenberger
Date: 9-27-23

Description:
    This module contains the GUI class for the Face Detection Software.
    It provides a graphical user interface with buttons to interact with
    the systems internal webcam, video files, image files, in addition to
    CCTV (ip) camera and external webcam feeds for face detection.
"""

import datetime
import subprocess
import cv2
from tkinter import Tk, Button, Label, filedialog, Radiobutton, IntVar, StringVar, OptionMenu, Checkbutton
import os
from face_detection_package.directory_manager import DirectoryManager
from face_detection_package.frontal_face_detector import FrontalFaceDetector
from face_detection_package.mesh_face_detector import FaceMeshDetector


class GUI:
    """
    Handles the Graphical User Interface.
    """
    PRIMARY_TEXT_FONT = ("Roboto", 14, "bold")
    SECONDARY_TEXT_FONT = ("Roboto", 10)
    BUTTON_BG = "white"
    BUTTON_FG = "black"
    BUTTON_ACTIVE_BG = "gray"
    FEED_BUTTON_WIDTH = 20
    OTHER_BUTTON_WIDTH = 10
    WINDOW_DIMS = '440x480'

    def __init__(self):
        """
        Initialize the GUI and directories.
        """
        self.directory_manager = DirectoryManager()
        self.directory_manager.create_directories()

        self.detector_options = ['Basic: Frontal Face Detector', 'Advanced: Mesh Face Detector']
        self.effect_options = ['None', 'Blur']

        self.root = Tk()
        self.root.title("Face Detection Software")
        self.root.configure(padx=25, pady=25)
        # Set the windows dimensions to hold all widgets in a clean looking format.
        self.root.geometry(self.WINDOW_DIMS)
        # Don't allow the screen to be resized
        self.root.resizable(0, 0)

        self.settings_lbl = Label(self.root, text="Settings", font=self.PRIMARY_TEXT_FONT)

        # Create StringVars for the settings menus.
        self.detector_selected = StringVar()
        self.effect_selected = StringVar()
        self.feed_info_var = IntVar()

        # Create the menus for selecting the detector and effect settings.
        self.detector_menu = OptionMenu(self.root, self.detector_selected, *self.detector_options)
        self.effect_menu = OptionMenu(self.root, self.effect_selected, *self.effect_options)

        # Configure the two menus current selection text font style.
        self.detector_menu.config(font=self.SECONDARY_TEXT_FONT)
        self.effect_menu.config(font=self.SECONDARY_TEXT_FONT)

        # Configure the two menus drop down text font style
        self.detector_submenu = self.root.nametowidget(self.detector_menu.menuname)  # Get menu widget.
        self.detector_submenu.config(font=self.SECONDARY_TEXT_FONT)  # Set the dropdown menu's font
        self.effect_submenu = self.root.nametowidget(self.effect_menu.menuname)
        self.effect_submenu.config(font=self.SECONDARY_TEXT_FONT)

        self.feed_info_cb = Checkbutton(self.root, text="Show Feed Info", variable=self.feed_info_var, onvalue=1,
                                        offvalue=0, height=2, width=20, font=self.SECONDARY_TEXT_FONT)
        # Set the checkbox selected by default.
        self.feed_info_cb.select()

        # Set the default effect and face detector settings.
        self.effect = None
        self.draw_feed_info = True
        self.face_detector = FrontalFaceDetector(self.effect, self.draw_feed_info)

        self.title_lbl = Label(self.root, text="Face Detection Software", font=self.PRIMARY_TEXT_FONT, pady=10)

        self.detector_lbl = Label(self.root, text="Detector Version: ", font=self.SECONDARY_TEXT_FONT)

        self.effect_lbl = Label(self.root, text="Effect: ", font=self.SECONDARY_TEXT_FONT)

        self.realtime_feeds_lbl = Label(self.root, text="Realtime Feeds", font=self.PRIMARY_TEXT_FONT)

        self.internal_webcam_btn = Button(self.root, text="Internal Webcam Feed", font=self.SECONDARY_TEXT_FONT,
                                          bg=self.BUTTON_BG,
                                          fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                                          activeforeground=self.BUTTON_FG,
                                          relief="groove", width=self.FEED_BUTTON_WIDTH,
                                          command=lambda: self.detect_over_webcam(0))

        self.external_webcam_btn = Button(self.root, text="External Webcam Feed", font=self.SECONDARY_TEXT_FONT,
                                          bg=self.BUTTON_BG,
                                          fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                                          activeforeground=self.BUTTON_FG,
                                          relief="groove", width=self.FEED_BUTTON_WIDTH,
                                          command=lambda: self.detect_over_webcam(1))

        self.post_process_media_lbl = Label(self.root, text="Post-Process Media", font=self.PRIMARY_TEXT_FONT)

        self.video_btn = Button(self.root, text="Detect Over Video", font=self.SECONDARY_TEXT_FONT, bg=self.BUTTON_BG,
                                fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                                activeforeground=self.BUTTON_FG,
                                relief="groove", width=self.FEED_BUTTON_WIDTH,
                                command=self.detect_over_video)

        self.image_btn = Button(self.root, text="Detect Over Image", font=self.SECONDARY_TEXT_FONT, bg=self.BUTTON_BG,
                                fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                                activeforeground=self.BUTTON_FG,
                                relief="groove", width=self.FEED_BUTTON_WIDTH,
                                command=self.detect_over_image)

        self.files_btn = Button(self.root, text="Files", font=self.SECONDARY_TEXT_FONT, bg=self.BUTTON_BG,
                                fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                                activeforeground=self.BUTTON_FG,
                                relief="groove", width=self.OTHER_BUTTON_WIDTH,
                                command=self.open_file_with_default_player)

        self.help_btn = Button(self.root, text="Help", font=self.SECONDARY_TEXT_FONT, bg=self.BUTTON_BG,
                               fg=self.BUTTON_FG, activebackground=self.BUTTON_ACTIVE_BG,
                               activeforeground=self.BUTTON_FG,
                               relief="groove", width=self.OTHER_BUTTON_WIDTH,
                               command=self.show_help)

        self.status_lbl = Label(self.root, text="", font=self.SECONDARY_TEXT_FONT)

        self.save_options_btn = Button(self.root, text='Save Settings', font=self.SECONDARY_TEXT_FONT,
                                       command=self.set_detector_option)

    def set_draw_info(self):
        if self.feed_info_var.get() == 1:
            self.draw_feed_info = True
        elif self.feed_info_var.get() == 0:
            self.draw_feed_info = False

    def set_effect_option(self):
        if self.effect_selected.get() == self.effect_options[0]:
            print("None selected")
            self.effect = 'None'
            print(self.effect)
        elif self.effect_selected.get() == self.effect_options[1]:
            print("Blur selected")
            self.effect = 'Blur'
            print(self.effect)

    def set_detector_option(self):
        """
        Set the selected detector option.

        Returns:
            None
        """
        print("options set")
        try:
            self.set_effect_option()
            self.set_draw_info()
            if self.detector_selected.get() == self.detector_options[0]:
                print("detector version 1 selected")
                self.face_detector = FrontalFaceDetector(self.effect, self.draw_feed_info)
                print(self.face_detector)
            elif self.detector_selected.get() == self.detector_options[1]:
                print("detector version 2 selected")
                self.face_detector = FaceMeshDetector(self.effect, self.draw_feed_info)
                print(self.face_detector)
        except Exception as e:
            print(f"Error setting detector option: {e}")
        finally:
            print(f"Reset Settings To:\n Detector: {self.face_detector}\n Effect: {self.effect}")

    @staticmethod
    def show_help() -> None:
        """
        Display help information in a separate window.
        """
        try:
            help_text = """
            Welcome to the Face Detection Software!

            Instructions:
            1. Internal Webcam Feed: Click this button to open the webcam feed and detect faces in real-time.
            2. External Webcam Feed: Click this button to use an external webcam and detect faces in real-time.
            3. CCTV Feed: Click this button to open a CCTV feed and detect faces in real-time.
            4. Detect Over Video: Click this button to select a video file and detect faces in it.
            5. Detect Over Image: Click this button to select an image file and detect faces in it.
            6. Files: Click this button to open the file explorer to select a file to view.
            7. Help: Click this button to view instructions on how to use the program.

            Notes:
            - Make sure to use video/image files with valid extensions (.mp4, .mov, .jpg, .png) when making detections.
            - All real-time feeds viewed by a user are saved to a video file in the recorded_detections directory.
            - Image and Video detections are saved to the image_/video_detections directories respectively.
            - A message will notify you when detections are done being made over a video or image file.

            Enjoy using the Face Detection Software!
            """
            help_window = Tk()
            help_window.title("Help")

            help_label = Label(help_window, text=help_text, font=("Courier", 10), justify='left')
            help_label.pack(padx=10)

            help_window.mainloop()
        finally:
            help_window.quit()

    @staticmethod
    def open_with_default_player(file_path: str) -> None:
        """
        Open a file using the default system application.

        Args:
            file_path (str): The path to the file to be opened.

        Returns:
            None
        """
        try:
            if os.name == 'nt':
                os.startfile(file_path)  # Opens the file using the default Windows application
            elif os.name == 'posix':
                subprocess.run(['xdg-open', file_path])  # Opens the file using xdg-open (Linux)
        except Exception as e:
            print(f"Error opening file: {e}")

    def open_file_with_default_player(self) -> None:
        """
        Open a file selected by the user using the default system application.

        Returns:
            None
        """
        try:
            file_path = self.open_file_explorer()
            if file_path:
                self.open_with_default_player(file_path)
        except Exception as e:
            print(f"Error opening file with default player: {e}")

    @staticmethod
    def open_file_explorer() -> str:
        """
        Open a file explorer dialog to allow the user to select a file.

        Returns:
            str: The path of the selected file.
        """
        try:
            # initial_dir = os.path.join(os.getcwd(), '../Face Detection Software')
            initial_dir = os.path.join(os.getcwd())
            file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All files", "*.*")])
            # `file_path` will contain the path of the selected file.
            print("Selected file:", file_path)
            return file_path
        except Exception as e:
            print(f"Error opening file explorer: {e}")
            return None

    def clear_status_label(self) -> None:
        """
        Clear the status label text.

        Returns:
            None
        """
        try:
            self.status_lbl.config(text="")
        except Exception as e:
            print(f"Error clearing status label: {e}")

    def run_app(self) -> None:
        """
        Run the main application loop.

        Returns:
            None
        """
        try:
            self.title_lbl.grid(column=0, row=0, sticky='w', padx=(0, 10), pady=(0, 10))

            self.files_btn.grid(column=1, row=0, pady=(0, 17))
            self.help_btn.grid(column=2, row=0, pady=(0, 17))

            self.settings_lbl.grid(column=0, row=3, sticky='w', columnspan=2, pady=(0, 10))

            self.detector_lbl.grid(column=0, row=4, sticky='w')
            self.detector_selected.set(self.detector_options[0])
            # pad bottom of menus 30px
            self.detector_menu.grid(column=0, row=5, sticky='w', columnspan=2, pady=(0, 30))

            self.effect_lbl.grid(column=0, row=6, sticky='w')
            self.effect_selected.set(self.effect_options[0])
            self.effect_menu.grid(column=0, row=7, sticky='w', columnspan=2, pady=(0, 30))

            self.feed_info_cb.grid(column=0, row=8, sticky='w')

            self.save_options_btn.grid(column=1, row=8, columnspan=2)

            self.realtime_feeds_lbl.grid(column=1, row=10, columnspan=2, pady=(10, 10))
            self.internal_webcam_btn.grid(column=1, row=11, columnspan=2)
            self.external_webcam_btn.grid(column=1, row=12, columnspan=2)

            self.post_process_media_lbl.grid(column=0, row=10, pady=(10, 10))
            self.video_btn.grid(column=0, row=11)
            self.image_btn.grid(column=0, row=12)
            self.status_lbl.grid(column=0, row=13)

            # Start the tkinter main loop
            self.root.mainloop()
        except Exception as e:
            print(f"Error running the application: {e}")
        finally:
            self.cleanup()

    def detect_over_webcam(self, channel: int) -> None:
        """
        Detect faces in the internal or external webcam feed.

        Args:
            channel (int): The channel number of the camera to detect faces over.

        Returns:
            None
        """
        print(f"In detect over webcam,\n detector = {self.face_detector} \n effect = {self.effect}")
        try:
            # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            cap = cv2.VideoCapture(channel)

            if not cap.isOpened():
                # Update the status label after processing
                self.status_lbl.config(
                    text=f"Error opening camera.\n Please check if an external\n camera is connected.")
                # Schedule clearing the label after 5 seconds
                self.root.after(5000, self.clear_status_label)
                raise ValueError(
                    f"Error opening camera channel {channel}. Please check if an external camera is connected.")

            # Create a VideoWriter object
            out = cv2.VideoWriter(
                os.path.join(self.directory_manager.recordings_dir, f'{timestamp}_{channel}_webcam_recording.mp4'),
                cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (640, 480))

            while True:
                ret, frame = cap.read()
                print("in detect webcam, read capture and calling face detector.detect_faces method on frame")
                self.face_detector.detect_faces(frame, current_time)
                print("method called, writing to file and showing...")
                out.write(frame)
                cv2.imshow("Webcam - Press 'q' key to quit.", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error detecting faces over webcam: {e}")

    def detect_over_video(self) -> None:
        """
        Detect faces in a selected video file.

        Returns:
            None
        """
        try:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            video_path = self.open_file_explorer()
            if video_path:
                # Check if the selected file has a valid extension
                valid_extensions = ('.mp4', '.mov')
                if not video_path.lower().endswith(valid_extensions):
                    raise ValueError("Invalid file type. Please select a .mp4 or .mov file.")

                # Specify the path to save the video with found detections in the 'video_detections' directory.
                video_path_out = os.path.join(self.directory_manager.videos_dir,
                                              f'{os.path.basename(video_path)}_{timestamp}_detections.mp4')

                # Create a video capture object for the video to predict upon.
                cap = cv2.VideoCapture(video_path)
                # Start reading the video.
                ret, frame = cap.read()
                # Get the dimensions of the video frames.
                H, W, _ = frame.shape
                # Initialize our video writer for saving the output video.
                out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)),
                                      (W, H))

                # Loop through frames read from the video file.
                while ret:
                    self.face_detector.detect_faces(frame, current_time)
                    # Write the frame to the output file.
                    out.write(frame)
                    # Keep reading the frames from the video file until they have all been processed.
                    ret, frame = cap.read()
                self.clear_status_label()

                # Release resources when the video is done being processed.
                cap.release()
                out.release()
                cv2.destroyAllWindows()

                # Update the status label after processing
                self.status_lbl.config(text="Video detections processed")
                # Schedule clearing the label after 5 seconds
                self.root.after(5000, self.clear_status_label)
        except Exception as e:
            print(f"Error detecting faces over video: {e}")

    def detect_over_image(self) -> None:
        """
        Detect faces in a selected image file.

        Returns:
            None
        """
        try:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            img_path = self.open_file_explorer()
            if img_path:
                # Check if the selected file has a valid extension
                valid_extensions = ('.png', '.jpg')
                if not img_path.lower().endswith(valid_extensions):
                    raise ValueError("Invalid file type. Please select a .png or .jpg file.")

                # Specify the path to save the image with found detections.
                img_path_out = os.path.join(self.directory_manager.images_dir,
                                            f'{os.path.basename(img_path)}_{timestamp}_detections.jpg')

                # Read the image.
                img = cv2.imread(img_path)

                self.face_detector.detect_faces(img, current_time)
                cv2.imwrite(img_path_out, img)
                cv2.destroyAllWindows()

                # Update the status label after processing
                self.status_lbl.config(text="Image detections processed")
                # Schedule clearing the label after 5 seconds
                self.root.after(5000, self.clear_status_label)
        except Exception as e:
            print(f"Error detecting faces over image: {e}")

    def cleanup(self) -> None:
        """
        Perform cleanup operations.

        Returns:
            None
        """
        try:
            # Release any resources
            print("Cleaning up resources...")
            self.root.quit()
            exit()
        except Exception as e:
            print(f"Error performing cleanup: {e}")
