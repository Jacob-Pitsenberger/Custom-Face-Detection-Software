import customtkinter as ctk
from face_detection_package.nav_frame import Nav
from face_detection_package.settings_frame import Settings
from face_detection_package.post_processing_frame import PostProcessDetections
from face_detection_package.directory_manager import DirectoryManager
from face_detection_package.frontal_face_detector import FrontalFaceDetector
from face_detection_package.mesh_face_detector import FaceMeshDetector

RED = '#4a020d'
BLUE = '#06003d'

class App(ctk.CTk):
    def __init__(self):
        # main setup
        super().__init__()

        self.directory_manager = DirectoryManager()
        self.directory_manager.create_directories()

        size = (600, 370)
        self.title('FACE DETECTION SOFTWARE')
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # widgets
        self.nav = Nav(self)
        self.settings = Settings(self)
        self.detections = PostProcessDetections(self)

        # run
        self.mainloop()


def main():
    App()


if __name__ == "__main__":
    main()
