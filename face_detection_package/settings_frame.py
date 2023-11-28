# Add these import statements at the beginning of the module
import customtkinter as ctk
from face_detection_package.frontal_face_detector import FrontalFaceDetector
from face_detection_package.mesh_face_detector import FaceMeshDetector

# Inside the Settings class
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

        self.parent = parent
        self.gui_red = self.parent.gui_red
        self.gui_blue = self.parent.gui_blue

        # create the widgets
        self.settings_frame = ctk.CTkFrame(self, border_width=2, border_color=self.gui_red)

        self.settings_label = ctk.CTkLabel(self.settings_frame, text='Settings', font=('Roboto', 20, 'bold'),
                                           bg_color=self.gui_red, text_color='white')

        self.detector_label = ctk.CTkLabel(self.settings_frame, text='Detector:', font=('Roboto', 14),
                                           text_color='white')

        self.detector_options = ['Basic: Frontal Face Detector', 'Advanced: Mesh Face Detector']
        self.detector_menu_var = ctk.StringVar(value=self.detector_options[0])

        self.detector_menu = ctk.CTkOptionMenu(self.settings_frame, values=self.detector_options,
                                               variable=self.detector_menu_var,
                                               fg_color=self.gui_blue, font=('Roboto', 12), text_color='white')

        self.effects_label = ctk.CTkLabel(self.settings_frame, text='Effects:', font=('Roboto', 14), text_color='white')

        self.bbox_cb = ctk.CTkCheckBox(self.settings_frame, text='Show Detection Bounding Box', fg_color=self.gui_blue,
                                       font=('Roboto', 12), text_color='white', border_color=self.gui_blue)
        self.bbox_cb.select()

        self.blur_cb = ctk.CTkCheckBox(self.settings_frame, text='Blur Detections', fg_color=self.gui_blue,
                                       font=('Roboto', 12),
                                       text_color='white', border_color=self.gui_blue)
        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Set the default effect and face detector settings.
        self.draw_box = True
        self.draw_blur = False

        # Initialize face detectors
        # self.haar_detector = FrontalFaceDetector(self.draw_box, self.draw_blur)
        self.haar_detector = FrontalFaceDetector(self)
        # self.mesh_detector_img = FaceMeshDetector(self.draw_box, self.draw_blur, True)
        # self.mesh_detector_vid = FaceMeshDetector(self.draw_box, self.draw_blur, False)
        self.mesh_detector_img = FaceMeshDetector(self, True)
        self.mesh_detector_vid = FaceMeshDetector(self, False)

        # Set the default face detector
        self.face_detector = self.haar_detector  # Set the default detector

        # Create IntVar to track the state of checkboxes
        self.bbox_var = ctk.IntVar(value=1)
        self.blur_var = ctk.IntVar(value=0)

        # Connect the detector menu variable to a callback
        self.detector_menu_var.trace_add('write', self.update_detector)

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
        self.settings_label.pack(fill='both')
        self.detector_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.detector_menu.pack(pady=(0, 20), padx=(20, 20), anchor='w', fill='x')
        self.effects_label.pack(pady=(20, 0), padx=(20, 0), anchor='w')
        self.bbox_cb.pack(pady=10, padx=(20, 0), anchor='w')
        self.blur_cb.pack(pady=10, padx=(20, 0), anchor='w')

    def update_detector(self, *args):
        """
        Update the face detector based on the selected option.

        Returns:
            None
        """
        try:
            self.update_checkbox()  # Update checkboxes first
            if self.detector_menu_var.get() == self.detector_options[0]:
                print("detector version 1 selected")
                self.face_detector = self.haar_detector  # Use the Haar detector
                print(self.face_detector)
            elif self.detector_menu_var.get() == self.detector_options[1]:
                print("detector version 2 selected")
                if self.static_mode_flag:
                    self.face_detector = self.mesh_detector_img
                    print(self.face_detector)
                    print(f'Initialized with staticMode set to True for image detections')
                elif not self.static_mode_flag:
                    self.face_detector = self.mesh_detector_vid
                    print(self.face_detector)
                    print(f'Initialized with staticMode set to False for video and realtime detections')
        except Exception as e:
            print(f"Error setting detector option: {e}")
        finally:
            print(f"Reset Settings To:\n Detector: {self.face_detector}\n draw box: {self.draw_box} "
                  f"\n draw blur: {self.draw_blur} \n staticMode_flag: {self.static_mode_flag}")

    def update_checkbox(self):
        """
        Update the draw box and draw blur attributes based on checkbox states.

        Returns:
            None
        """
        self.draw_box = bool(self.bbox_var.get())
        self.draw_blur = bool(self.blur_var.get())
        print(f'draw box set to {self.draw_box}')
        print(f'draw blur set to {self.draw_blur}')
