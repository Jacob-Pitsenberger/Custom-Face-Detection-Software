import customtkinter as ctk

RED = '#4a020d'
BLUE = '#06003d'

class PostProcessDetections(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.8)
        self.create_widgets()

    def create_widgets(self):
        detections_frame = ctk.CTkFrame(self, border_width=2, border_color=RED)
        detections_label = ctk.CTkLabel(detections_frame, text='Make Detections', font=('Roboto', 20, 'bold'),
                                        bg_color=RED, text_color='white')
        video_btn = ctk.CTkButton(detections_frame, text='Video', fg_color=BLUE, font=('Roboto', 12), text_color='white')
        image_btn = ctk.CTkButton(detections_frame, text='Image', fg_color=BLUE, font=('Roboto', 12), text_color='white')
        status_lbl = ctk.CTkLabel(detections_frame, text='', font=('Roboto', 16, 'bold'), text_color='white')

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        detections_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))

        detections_label.pack(fill='both', pady=(0, 10))
        video_btn.pack(pady=10)
        image_btn.pack(pady=10)
        status_lbl.pack(pady=(10, 20))
