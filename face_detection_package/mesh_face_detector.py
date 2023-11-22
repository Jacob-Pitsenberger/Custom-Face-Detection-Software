"""
Module: mesh_face_detector.py
Author: Jacob Pitsenberger
Date: 11/22/2023

Description:
    This module provides a FaceMeshDetector class that handles face detection using the OpenCV and
    Google MediaPipe libraries.

Classes:
- FaceMeshDetector: Handles face detection using the MediaPipe face mesh model.

Constants:
- FONT: Font type for text overlay on the frame.
- TEXT_COLOR: Text color for overlay.
- BOX_COLOR: Color of the bounding box around detected faces.
- BOX_THICKNESS: Thickness of the bounding box.
- TEXT_THICKNESS: Thickness of the text overlay.
- SCALE: Scaling factor for text and box dimensions.

Methods:
- __init__(self, draw_box, draw_blur, staticMode, maxFaces=10, refine_landmarks=False,
          minDetectionCon=0.2, minTrackCon=0.2): Initializes the FaceMeshDetector object.
- detect_faces(self, frame: np.ndarray) -> None: Detects facial landmarks in an image.
- draw_rectangle(self, frame: np.ndarray, faceLms: mp.solutions.face_mesh.NamedTuple) -> None:
  Draws a bounding box around the detected face mesh.

Attributes:
- results: Store the results of face detection and landmarks.
- imgRGB: Store the RGB version of the input image.
- staticMode: Flag for static mode.
- maxFaces: Maximum number of faces to detect.
- refine_landmarks: Flag for refining landmarks.
- minDetectionCon: Minimum confidence for face detection.
- minTrackCon: Minimum confidence for face tracking.
- mpDraw: MediaPipe drawing utilities.
- mpFaceMesh: MediaPipe face mesh model.
- faceMesh: Face mesh model.
- drawSpec: Drawing specifications for face landmarks.
- draw_box: Flag indicating whether to draw bounding boxes.
- draw_blur: Flag indicating whether to blur detected faces.
- version_name: Version name of the detector.
"""

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
    # TEXT_THICKNESS = 1//2
    # SCALE = 0.5
    TEXT_THICKNESS = 1
    SCALE = 1

    def __init__(self, draw_box, draw_blur, staticMode, maxFaces=10, refine_landmarks=False, minDetectionCon=0.2,
                 minTrackCon=0.2):
        """
        Constructor method to initialize the FaceMeshDetector object.

        Args:
            staticMode (bool): If True, face landmarks are not refined for every frame
                               (Use True for images and False for video or realtime feeds).
            maxFaces (int): Maximum number of faces to detect.
            refine_landmarks (bool): If True, the face landmarks are refined.
                                     Whether to further refine the landmark coordinates around the eyes and lips,
                                     and output additional landmarks around the irises by applying the Attention Mesh Model.
                                     Default to false.
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

        self.draw_box = draw_box
        self.draw_blur = draw_blur
        self.version_name = 'Advanced: Mesh Face Detector'

    def detect_faces(self, frame: np.ndarray) -> None:
        """
        Detects facial landmarks in an image.

        Args:
            frame (numpy.ndarray): Input image (BGR format).

        Returns:
            None
        """
        try:
            self.imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR image to RGB
            self.results = self.faceMesh.process(self.imgRGB)  # Process the image with the face mesh model

            if self.results.multi_face_landmarks:
                for faceLms in self.results.multi_face_landmarks:
                    self.draw_rectangle(frame, faceLms)
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
            if self.draw_blur:
                blur_img = cv2.blur(frame[y_min:y_max, x_min:x_max], (50, 50))
                frame[y_min:y_max, x_min:x_max] = blur_img
            if self.draw_box:
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), self.BOX_COLOR, self.BOX_THICKNESS)
        except Exception as e:
            print(f"Error in draw rectangle: {e}")

