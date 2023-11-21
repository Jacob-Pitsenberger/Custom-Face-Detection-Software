import os
from face_detection_package.utils import open_file_explorer
import customtkinter as ctk
import datetime
import cv2

RED = '#4a020d'
BLUE = '#06003d'


class PostProcessDetections(ctk.CTkFrame):
    def __init__(self, parent, detector, directory_manager):
        super().__init__(parent)
        self.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.8)

        self.detections_frame = ctk.CTkFrame(self, border_width=2, border_color=RED)
        self.detections_label = ctk.CTkLabel(self.detections_frame, text='Make Detections', font=('Roboto', 20, 'bold'),
                                             bg_color=RED, text_color='white')
        self.video_btn = ctk.CTkButton(self.detections_frame, text='Process Video', fg_color=BLUE, font=('Roboto', 12),
                                       text_color='white', command=self.detect_over_video)
        self.image_btn = ctk.CTkButton(self.detections_frame, text='Process Image', fg_color=BLUE, font=('Roboto', 12),
                                       text_color='white', command=self.detect_over_image)
        self.status_lbl = ctk.CTkLabel(self.detections_frame, text='', font=('Roboto', 16, 'bold'), text_color='white')

        self.bottom_border_lbl = ctk.CTkLabel(self.detections_frame, text='', bg_color=RED, text_color='white')

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.parent = parent
        self.face_detector = detector
        self.directory_manager = directory_manager

        self.create_widgets()

    def update_face_detector(self, new_detector):
        """
        Updates the face detector used for face detection.

        Args:
            new_detector: The new face detector.

        Returns:
            None
        """
        try:
            self.face_detector = new_detector
        except Exception as e:
            print(f"Error updating face detector: {e}")

    def create_widgets(self):
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
        try:
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
                    self.face_detector.detect_faces(frame, current_time)
                    out.write(frame)

                self.clear_status_label()

                cap.release()
                out.release()
                cv2.destroyAllWindows()

                # Update status label when processing is done
                self.status_lbl.configure(text="Video detections processed")
                self.after(5000, self.clear_status_label)

        except Exception as e:
            print(f"Error detecting faces over video: {e}")

    def detect_over_image(self) -> None:
        try:
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

                self.face_detector.detect_faces(img, current_time)
                cv2.imwrite(img_path_out, img)
                cv2.destroyAllWindows()

                # Update status label when processing is done
                self.status_lbl.configure(text="Image detections processed")
                self.after(5000, self.clear_status_label)

        except Exception as e:
            print(f"Error detecting faces over image: {e}")
    """
    def detect_over_video(self) -> None:
        try:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            video_path = open_file_explorer()
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
                self.status_lbl.configure(text="Video detections processed")
                # Schedule clearing the label after 5 seconds
                self.after(5000, self.clear_status_label)
        except Exception as e:
            print(f"Error detecting faces over video: {e}")

    def detect_over_image(self) -> None:
        try:
            current_time = datetime.datetime.now()
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")
            img_path = open_file_explorer()
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
                self.status_lbl.configure(text="Image detections processed")
                # Schedule clearing the label after 5 seconds
                self.after(5000, self.clear_status_label)
        except Exception as e:
            print(f"Error detecting faces over image: {e}")
    """