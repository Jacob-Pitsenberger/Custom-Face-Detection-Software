import os
import subprocess
from face_detection_package.utils import open_file_explorer
import customtkinter as ctk

RED = '#4a020d'
BLUE = '#06003d'


class Nav(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relwidth=1, relheight=0.2)

        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        title_frame = ctk.CTkFrame(self, border_width=2, border_color=RED, fg_color=RED)

        label = ctk.CTkLabel(title_frame, text='FACE DETECTION SOFTWARE', font=('Roboto', 28, 'bold'),
                             text_color='white')
        files_btn = ctk.CTkButton(title_frame, text='Files', width=75, fg_color=BLUE, font=('Roboto', 12),
                                  text_color='white',
                                  command=self.open_file_with_default_player)
        help_btn = ctk.CTkButton(title_frame, text='Help', width=75, fg_color=BLUE, font=('Roboto', 12),
                                 text_color='white',
                                 command=lambda: self.show_help())

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # toggle layout
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
            help_window = ctk.CTk()
            help_window.title("Help")

            help_label = ctk.CTkLabel(help_window, text=help_text, font=("Courier", 10), justify='left')
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
            file_path = open_file_explorer()
            if file_path:
                self.open_with_default_player(file_path)
        except Exception as e:
            print(f"Error opening file with default player: {e}")

