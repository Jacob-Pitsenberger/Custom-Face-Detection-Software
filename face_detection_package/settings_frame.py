import customtkinter as ctk

RED = '#4a020d'
BLUE = '#06003d'

class Settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, rely=0.2, relwidth=0.6, relheight=0.8)
        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        toggle_frame = ctk.CTkFrame(self, border_width=2, border_color=RED)

        settings_label = ctk.CTkLabel(toggle_frame, text='Settings', font=('Roboto', 20, 'bold'),
                                      bg_color=RED, text_color='white')

        detector_label = ctk.CTkLabel(toggle_frame, text='Detector:', font=('Roboto', 14), text_color='white')

        detector_options = ['Basic: Frontal Face Detector', 'Advanced: Mesh Face Detector']
        detector_menu_var = ctk.StringVar(value=detector_options[0])

        detector_menu = ctk.CTkOptionMenu(toggle_frame, values=detector_options, variable=detector_menu_var,
                                          fg_color=BLUE, font=('Roboto', 12), text_color='white')

        effects_label = ctk.CTkLabel(toggle_frame, text='Effects:', font=('Roboto', 14), text_color='white')

        bbox_cb = ctk.CTkCheckBox(toggle_frame, text='Show Detection Bounding Box', fg_color=BLUE, font=('Roboto', 12), text_color='white', border_color=BLUE)
        info_cb = ctk.CTkCheckBox(toggle_frame, text='Show Detection Info', fg_color=BLUE, font=('Roboto', 12), text_color='white', border_color=BLUE)
        blur_cb = ctk.CTkCheckBox(toggle_frame, text='Blur Detections', fg_color=BLUE, font=('Roboto', 12), text_color='white', border_color=BLUE)
        save_btn = ctk.CTkButton(toggle_frame, text='Save Settings', fg_color=BLUE, font=('Roboto', 12), text_color='white', border_color=BLUE)

        # create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # toggle layout
        toggle_frame.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=(0, 5), padx=(5, 5))
        settings_label.pack(fill='both')
        detector_label.pack(pady=(10, 0), padx=(20, 0), anchor='w')
        detector_menu.pack(pady=(0, 10), padx=(20, 20), anchor='w', fill='x')
        effects_label.pack(padx=(20, 0), anchor='w')
        bbox_cb.pack(pady=5, padx=(20, 0), anchor='w')
        info_cb.pack(pady=5, padx=(20, 0), anchor='w')
        blur_cb.pack(pady=5, padx=(20, 0), anchor='w')
        save_btn.pack(pady=5, anchor='center')