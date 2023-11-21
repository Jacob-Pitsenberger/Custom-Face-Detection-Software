import customtkinter as ctk
from face_detection_package.frontal_face_detector import FrontalFaceDetector
from face_detection_package.mesh_face_detector import FaceMeshDetector

RED = '#4a020d'
BLUE = '#06003d'


class Settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, rely=0.2, relwidth=0.6, relheight=0.8)

        # create the widgets
        self.toggle_frame = ctk.CTkFrame(self, border_width=2, border_color=RED)

        self.settings_label = ctk.CTkLabel(self.toggle_frame, text='Settings', font=('Roboto', 20, 'bold'),
                                           bg_color=RED, text_color='white')

        self.detector_label = ctk.CTkLabel(self.toggle_frame, text='Detector:', font=('Roboto', 14), text_color='white')

        self.detector_options = ['Basic: Frontal Face Detector', 'Advanced: Mesh Face Detector']
        self.detector_menu_var = ctk.StringVar(value=self.detector_options[0])

        self.detector_menu = ctk.CTkOptionMenu(self.toggle_frame, values=self.detector_options,
                                               variable=self.detector_menu_var,
                                               fg_color=BLUE, font=('Roboto', 12), text_color='white')

        self.effects_label = ctk.CTkLabel(self.toggle_frame, text='Effects:', font=('Roboto', 14), text_color='white')

        self.bbox_cb = ctk.CTkCheckBox(self.toggle_frame, text='Show Detection Bounding Box', fg_color=BLUE,
                                       font=('Roboto', 12), text_color='white', border_color=BLUE)
        self.bbox_cb.select()
        # self.info_cb = ctk.CTkCheckBox(self.toggle_frame, text='Show Detection Info', fg_color=BLUE,
        # font=('Roboto', 12), text_color='white', border_color=BLUE)

        self.blur_cb = ctk.CTkCheckBox(self.toggle_frame, text='Blur Detections', fg_color=BLUE, font=('Roboto', 12),
                                       text_color='white', border_color=BLUE)
        self.save_btn = ctk.CTkButton(self.toggle_frame, text='Save Settings', fg_color=BLUE, font=('Roboto', 12),
                                      text_color='white', border_color=BLUE, command=self.set_detector)

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.parent = parent
        # Set the default effect and face detector settings.
        self.draw_box = True
        self.draw_feed_info = False
        self.draw_blur = False
        self.face_detector = FrontalFaceDetector(self.draw_box, self.draw_feed_info, self.draw_blur)
        self.create_widgets()

    def create_widgets(self):
        # toggle layout
        self.toggle_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))
        self.settings_label.pack(fill='both')
        self.detector_label.pack(pady=(10, 0), padx=(20, 0), anchor='w')
        self.detector_menu.pack(pady=(0, 10), padx=(20, 20), anchor='w', fill='x')
        self.effects_label.pack(padx=(20, 0), anchor='w')
        self.bbox_cb.pack(pady=10, padx=(20, 0), anchor='w')
        # self.info_cb.pack(pady=5, padx=(20, 0), anchor='w')
        self.blur_cb.pack(pady=10, padx=(20, 0), anchor='w')
        self.save_btn.pack(pady=10, anchor='center')

    def set_draw_box(self):
        if self.bbox_cb.get() == 1:
            print('draw box set to True')
            self.draw_box = True
        elif self.bbox_cb.get() == 0:
            print('draw box set to False')
            self.draw_box = False

    """
    def set_draw_info(self):
        if self.info_cb.get() == 1:
            print('draw info set to True')
            self.draw_feed_info = True
        elif self.info_cb.get() == 0:
            print('draw info set to False')
            self.draw_feed_info = False
    """

    def set_draw_blur(self):
        if self.blur_cb.get() == 1:
            print('draw blur set to True')
            self.draw_blur = True
        elif self.blur_cb.get() == 0:
            print('draw blur set to False')
            self.draw_blur = False

    def set_detector(self):
        try:
            self.set_draw_box()
            self.set_draw_blur()
            # self.set_draw_info()
            if self.detector_menu_var.get() == self.detector_options[0]:
                print("detector version 1 selected")
                # self.face_detector = FrontalFaceDetector(self.draw_box, self.draw_feed_info, self.draw_blur)
                self.face_detector = FrontalFaceDetector(self.draw_box, self.draw_feed_info, self.draw_blur)
                print(self.face_detector)
            elif self.detector_menu_var.get() == self.detector_options[1]:
                print("detector version 2 selected")
                self.face_detector = FaceMeshDetector(self.draw_box, self.draw_feed_info, self.draw_blur)
                print(self.face_detector)

            # Add these lines for debugging
            print(f"Before updating face detector in PostProcessDetections: {self.parent.detections.face_detector}")
            self.parent.detections.update_face_detector(self.face_detector)
            print(f"After updating face detector in PostProcessDetections: {self.parent.detections.face_detector}")
        except Exception as e:
            print(f"Error setting detector option: {e}")
        finally:
            print(f"Reset Settings To:\n Detector: {self.face_detector}\n draw box: {self.draw_box} "
                  f"\n draw info: {self.draw_feed_info} \n draw blur: {self.draw_blur}")
