"""
Module: mesh_face_detector.py
Author: Jacob Pitsenberger
Date: 10-2-23

Description:
    This module provides a FaceMeshDetector class that handles face detection using the OpenCV and
    Google MediaPipe libraries.
"""
from datetime import datetime

import cv2
import mediapipe as mp
import numpy as np


class FaceMeshDetector:
    """
    FaceMeshDetector class for detecting facial landmarks using Mediapipe.
    """
    FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
    TEXT_COLOR = (0, 255, 255)
    BOX_COLOR = (0, 0, 255)
    BOX_THICKNESS = 2
    TEXT_THICKNESS = 1//2
    SCALE = 0.5

    def __init__(self, draw_box, show_info, draw_blur, staticMode=False, maxFaces=10, refine_landmarks=True, minDetectionCon=0.4,
                 minTrackCon=0.5):
        """
        Constructor method to initialize the FaceMeshDetector object.

        Args:
            staticMode (bool): If True, face landmarks are not refined for every frame.
            maxFaces (int): Maximum number of faces to detect.
            refine_landmarks (bool): If True, the face landmarks are refined.
            minDetectionCon (float): Minimum confidence value for a face detection to be considered successful.
            minTrackCon (float): Minimum confidence value for a face to be considered successfully tracked.
        """
        self.results = None  # Store the results of face detection and landmarks
        self.imgRGB = None  # Store the RGB version of the input image
        self.staticMode = staticMode  # Flag for static mode
        self.maxFaces = maxFaces  # Maximum number of faces to detect
        self.refine_landmarks = refine_landmarks  # Flag for refining landmarks
        self.minDetectionCon = minDetectionCon  # Minimum confidence for face detection
        self.minTrackCon = minTrackCon  # Minimum confidence for face tracking

        # Initialize Mediapipe drawing utilities and face mesh model
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, self.refine_landmarks,
                                                 self.minDetectionCon, self.minTrackCon)

        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)

        # self.effect = effect
        self.draw_box = draw_box
        self.draw_blur = draw_blur
        self.show_info = show_info
        self.version_name = 'Advanced: Mesh Face Detector'

    def detect_faces(self, frame: np.ndarray, current_time) -> None:
        """
        Detects facial landmarks in an image.

        Args:
            frame (numpy.ndarray): Input image (BGR format).

        Returns:
            None
        """
        try:
            # timestamp = datetime.now()
            timestamp = current_time

            self.imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR image to RGB
            self.results = self.faceMesh.process(self.imgRGB)  # Process the image with the face mesh model

            if self.results.multi_face_landmarks:
                for faceLms in self.results.multi_face_landmarks:
                    print("in mesh detector, calling draw rect method")
                    self.draw_rectangle(frame, faceLms)
                # Update the face count with the number of faces detected
                face_count = f'Faces: {len(self.results.multi_face_landmarks)}'
                effect_text = f'blur: {self.draw_blur}'
                self.draw_info(frame, face_count, effect_text, timestamp)
                # cv2.putText(frame, face_count, (10, 25), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
                # cv2.putText(frame, effect_text, (10, 50), self.FONT, self.SCALE, self.TEXT_COLOR, self.THICKNESS)
                print(face_count)
        except Exception as e:
            print(f"Error in detect faces: {e}")

    def draw_rectangle(self, frame: np.ndarray, faceLms: mp.solutions.face_mesh.NamedTuple) -> None:
        """
        Draws a bounding box around the detected face mesh.

        Args:
            frame (numpy.ndarray): Input image (BGR format).
            faceLms (typing.NamedTuple): Detected face landmarks.

        Returns:
            None
        """
        try:
            print("in mesh detector, trying to get bounding box")
            # Get bounding box coordinates
            ih, iw, ic = frame.shape
            x_min, x_max, y_min, y_max = iw, 0, ih, 0

            for id, lm in enumerate(faceLms.landmark):
                x, y = int(lm.x * iw), int(lm.y * ih)
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
            """
            print(f"bbox calculated, checking effect and drawing result...\n self.effect is {self.effect}")
            print("if this is none then I dont know why this if statement is failing....ah")
            if self.effect is None:
                # Draw the bounding box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), self.BOX_COLOR, self.THICKNESS)
                print("in draw rectangle, found self.effect is None so should draw default box...")
            """
            if self.draw_blur:
                # Instead of drawing a rectangle we will first calculate the end coordinates using its boxes start coordinates
                # Then we create a blured image for this area of the original frame
                blur_img = cv2.blur(frame[y_min:y_max, x_min:x_max], (50, 50))
                # And lastly we set detected area of the frame equal to the blurred image that we got from the area
                frame[y_min:y_max, x_min:x_max] = blur_img
            if self.draw_box:
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), self.BOX_COLOR, self.BOX_THICKNESS)
        except Exception as e:
            print(f"Error in draw rectangle: {e}")

    def draw_info(self, frame, face_count, effect_text, timestamp):
        if self.show_info is True:
            date = timestamp.strftime("%d %b %Y")
            time = timestamp.strftime("%H:%M:%S")

            # Draw a rectangle to hold the drawn text in the upper left corner of the video stream window.
            # the -1 argument indicates the rectangle is filled.
            cv2.rectangle(frame, (0, 0), (195, 80), (0, 0, 0), -1)
            cv2.putText(frame, self.version_name, (5, 20), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
            cv2.putText(frame, effect_text, (5, 30), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
            cv2.putText(frame, face_count, (5, 40), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
            cv2.putText(frame, '--------------------', (5, 50), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
            cv2.putText(frame, date, (5, 60), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
            cv2.putText(frame, time, (5, 70), self.FONT, self.SCALE, self.TEXT_COLOR, self.TEXT_THICKNESS)
        else:
            pass

