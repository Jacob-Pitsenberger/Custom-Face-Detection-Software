"""
Module: frontal_face_detector.py
Author: Jacob Pitsenberger
Date: 11/28/23

Description:
    This module provides a FrontalFaceDetector class that handles face detection using the OpenCV library.

Classes:
- FrontalFaceDetector: Handles face detection using a pre-trained cascade classifier.

Constants:
- FONT: Font type for text overlay on the frame.
- TEXT_COLOR: Text color for overlay.
- BOX_COLOR: Color of the bounding box around detected faces.
- BOX_THICKNESS: Thickness of the bounding box.
- TEXT_THICKNESS: Thickness of the text overlay.
- SCALE: Scaling factor for text and box dimensions.

Methods:
- __init__(self, draw_box, draw_blur): Initializes the FrontalFaceDetector.
- detect_faces(self, frame: np.ndarray) -> None: Detects faces in a given frame.
- draw_rectangle(self, frame, dims): Draws rectangles around detected faces.

Attributes:
- face_cascade: Cascade classifier for face detection.
- version_name: Version name of the detector.
- draw_box: Flag indicating whether to draw bounding boxes.
- draw_blur: Flag indicating whether to blur detected faces.
"""
import cv2
import os
import numpy as np


class FrontalFaceDetector:
    """
    Provides a FrontalFaceDetector class that handles face detection using the OpenCV library.
    """
    FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
    TEXT_COLOR = (0, 255, 255)
    BOX_COLOR = (0, 0, 255)
    BOX_THICKNESS = 2
    TEXT_THICKNESS = 1
    SCALE = 1

    def __init__(self, draw_box, draw_blur):
        """
        Initialize the FrontalFaceDetector with a pre-trained cascade classifier for face detection.
        """
        # Get the current file directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the path to haarcascade file
        cascade_path = os.path.join(current_dir, 'data-files', 'haarcascade_frontalface_default.xml')

        # Create a cascade
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        self.version_name = "Basic: Frontal Face Detector"
        self.draw_box = draw_box
        self.draw_blur = draw_blur

    def detect_faces(self, frame: np.ndarray) -> None:
        """
        Detect faces in a given frame using the pre-trained cascade classifier.

        Args:
            frame: The input frame in which faces will be detected.

        Returns:
            None
        """
        try:
            # Convert the frame to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Changing scaleFactor value to 1.2 as to speed up detection time for post-processing video files (was 1.05 causing this issue).
            faces = self.face_cascade.detectMultiScale(image=frame_gray, scaleFactor=1.2, minNeighbors=5)

            # For the x, y coordinates and width, height detected
            for (x, y, w, h) in faces:
                dims = [x, y, w, h]
                self.draw_rectangle(frame, dims)

        except Exception as e:
            print(f"Error in detect faces: {e}")

    def draw_rectangle(self, frame, dims):
        try:
            x, y, w, h = dims
            if self.draw_blur is True:
                # Instead of drawing a rectangle we will first calculate the end coordinates using its boxes start coordinates
                x2 = x + w
                y2 = y + h
                # Then we create a blured image for this area of the original frame
                blur_img = cv2.blur(frame[y:y2, x:x2], (50, 50))
                # And lastly we set detected area of the frame equal to the blurred image that we got from the area
                frame[y:y2, x:x2] = blur_img
            if self.draw_box is True:
                # Draw a rectangle around the face using these values
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.BOX_COLOR, self.BOX_THICKNESS)
        except Exception as e:
            print(f"Error in draw rectangle: {e}")



