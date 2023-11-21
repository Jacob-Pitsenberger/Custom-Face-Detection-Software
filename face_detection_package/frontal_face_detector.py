"""
Module: frontal_face_detector.py
Author: Jacob Pitsenberger
Date: 9-27-23

Description:
    This module provides a FrontalFaceDetector class that handles face detection using the OpenCV library.
"""
from datetime import datetime

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
    # TEXT_THICKNESS = 1//2
    # SCALE = 0.5
    TEXT_THICKNESS = 1
    SCALE = 1

    def __init__(self, draw_box, show_info, draw_blur):
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
        self.show_info = show_info

    def detect_faces(self, frame: np.ndarray, current_time) -> None:
        """
        Detect faces in a given frame using the pre-trained cascade classifier.

        Args:
            frame: The input frame in which faces will be detected.

        Returns:
            None
        """
        try:
            # timestamp = datetime.now().strftime("%d %b %Y  %H:%M:%S.%f")
            # timestamp = datetime.now()
            timestamp = current_time

            # Convert the frame to grayscale
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Get numpy array with values for faces detected by passing in grayscale image, scale factor, and minimum neighbors
            faces = self.face_cascade.detectMultiScale(frame_gray, 1.2, 8)

            # For the x, y coordinates and width, height detected
            for (x, y, w, h) in faces:
                dims = [x, y, w, h]
                self.draw_rectangle(frame, dims)

            # Update the face count with the number of faces detected
            face_count = f'Faces: {len(faces)}'
            effect_text = f'blur: {self.draw_blur}'
            self.draw_info(frame, face_count, effect_text, timestamp)
            # cv2.putText(frame, face_count, (10, 25), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
            # cv2.putText(frame, effect_text, (10, 50), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
            print(face_count)
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

    def draw_info(self, frame, face_count, effect_text, timestamp):
        """These integer hardcoded values were determined when testing over the test image and successfully
        formatted this info box based on this images dimensions. When testing over a video file, the dimensions
        of the draw info box were to large and covered the majority of the video frames so this is not an
        adequate approach.
        For the first release, this feature will be disabled (no button in gui and just leave parameter set to False).
        """
        if self.show_info is True:
            w, h, c = frame.shape
            scale = w//480
            step = (scale*scale) + 10
            print(f'scale_factor: {scale}')
            # Divide dimensions by 8 to get 720x480 res (with dims = 5740, 3840)
            box_end = ((h//scale*2), 7*(w//scale)//4)
            print(f'width {w}\n height {h}')
            # print(f'box end coordinates are {box_end}')
            date = timestamp.strftime("%d %b %Y")
            time = timestamp.strftime("%H:%M:%S")

            # Draw a rectangle to hold the drawn text in the upper left corner of the video stream window.
            # the -1 argument indicates the rectangle is filled.
            # cv2.rectangle(frame, (0, 0), (185, 80), (0, 0, 0), -1)
            cv2.rectangle(frame, (0, 0), box_end, (0, 0, 0), -1)
            cv2.putText(frame, self.version_name, (5, step), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
            cv2.putText(frame, effect_text, (5, step*3), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
            cv2.putText(frame, face_count, (5, step*5), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
            cv2.putText(frame, '-------------------', (5, step*7), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
            cv2.putText(frame, date, (5, step*9), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
            cv2.putText(frame, time, (5, step*11), self.FONT, self.SCALE*scale//2, self.TEXT_COLOR, self.TEXT_THICKNESS*scale//2)
        else:
            pass

