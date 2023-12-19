# Face Detection Software
Author: Jacob Pitsenberger
Last Updated: 12/19/2023

Welcome to the Face Detection Software, a powerful software utility designed to facilitate real-time and post-production 
face detection over digital media or internal/external webcam feeds and gain or add key insights and effects in the process.

## Current Features:

- Post-Production Analysis: Analyze pre-recorded video and image files for facial features.
- Realtime-Feed Analysis: Analyze realtime video feeds, from either internal or external webcams, for facial features. 
- Face Blurring: Aside from standard detections, a blur effect can be applied to conceal identities and maintain privacy.
- Intuitive GUI's: Enjoy two user-friendly Graphical User Interfaces (GUI) that simplify interaction with the software's capabilities.

## Future Enhancements
- Real-Time Detection Over CCTV/IP feeds: Instantaneously identify faces in CCTV/IP camera feeds.
- Data Annotation: Create custom datasets by having annotations drawn over media files or realtime camera feeds to create your own custom datasets with ease.
- Timestamp Analysis: Perform deep analysis over recorded media by viewing the exact time stamps faces are detected.
- Supreme Detection Model Option: A custom trained Yolo model detector will be available to optimize these current capabilities to near perfect detection accuracy.
- Model Detection Pipeline: No longer require the need to specify a specific detector model as they all work together under this pipeline to ensure each only returns the most confident detections and builds upon the more basic ones such that the benefits of all can be combined into a single output.
- Detect-Or Custom Software Utilities: This Face Detection Software is just a small part of what is planned to be a complete set of computer vision model utilities that perform similar functionalities but allow for a wider array of object to be detected.

## Getting Started

Before delving into the features and functionality of the Face Detection Software, let's ensure that your system meets the necessary requirements and that the software is correctly installed.

### System Requirements

Before installation, ensure that your system meets the following requirements:
- Operating System: Windows 10 or later
- Memory: 8GB of RAM is recommended for smooth operation.
- Processor: A quad-core processor (or equivalent) with a clock speed of 2.0 GHz or faster is recommended.


## User Guide

The User Guide provides detailed instructions on how to effectively utilize the Face Detection Software.

### Using the GUI

The graphical user interface (GUI) is the primary interface of the software. There are two in which this software is operated which is specified in the entry point module faceDetectionSoftwareBasic.py when initializing the gui with the version as the parameter ('pp' for postprocessing gui, 'rf' for realtime feeds gui)
Both the realtime feed and post-processing GUIs comprise a main window with various buttons facilitating different functions. 
Below are the main features of the GUI:
- Detector Settings: Specify the detector model to use in processing by selecting it from the dropdown menu under the Settings frame.
- Effect Settings: These consist of check boxes that when selected apply standard detection bounding boxes over processed media and/or a blur effect.
- Post-processing Video and Image Files: Under the 'Make Detections' frame in the 'pp' GUI version there are two buttons with the text 'Video', and 'Image'. These buttons allow you to process video and image files for detections respectively.
- Processing realtime internal and external webcam feeds: Under the 'Make Detections' frame in the 'pp' GUI version there are two buttons with the text 'Internal Webcam Feed', and 'External Webcam Feed'. These buttons allow you to process internal or external webcam feeds for detections respectively.
- File Explorer: Opens the file explorer in the project's root directory, enabling you to view files saved with detections.
- Help Button: Provides additional assistance on using the software effectively.

### Face Detection Modes

The Face Detection Software offers various modes for detecting faces with those currently available consisting of:
- Detect Over Video: Select a video file and detect faces within it.
- Detect Over Image: Select an image file and detect faces within it.
- Internal Webcam Feed: Opens the internal webcam feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.
- External Webcam Feed: Opens an external webcam feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.
- Files: Opens the file explorer in the project root folder, allowing you to open a file processed for detections with your system's default media player.

Other modes that will be available soon but are not currently include:
- CCTV Feed: Opens a CCTV/IP camera feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.

## Data Storage

Upon downloading the `Face Detection Software Basic Post Processing Version 1.0.zip` file, the Face Detection Software is placed in the root directory titled "Face Detection Software". This directory includes all the necessary dependencies to run the program, licensing files, and the executable file for launching the software. When the program is launched for the first time, it automatically creates three additional directories in the root directory to organize processed detection files. These directories are:
- `image detections`: Here, you'll find image files that were processed for detections and saved through the software.
- `video detections`: This directory stores video files that have undergone processing for detections. Video files saved from webcam feeds are named with the timestamp at which the feed was initially viewed, followed by the channel number used to access the webcam (0 for internal, 1 for external), and the text “_webcam_recording”. Video files saved from CCTV/IP camera feeds follow a similar naming convention with the timestamp followed by the text “_feed_recording”. Both webcam and CCTV/IP camera feeds are saved as .mp4 files. Videos and images post-processed for detections are saved in the .mp4 and .jpg formats, respectively.

If running the post-processing version in your local IDE, these directories are created in a similar way.

If running the realtime-feed version in your local IDE (currently no .zip download), the following directory is created and placed under the project root directory.
- `recorded detections`: Here, you'll find video files that are recording from internal or external, realtime webcam feeds, processed for detections and saved through the software.


## Data Deletion

All files generated using the Face Detection Software are stored in the software's master root directory titled “Face Detection Software”. To delete these files, you can do so through your file explorer, following the same procedure as you would for deleting other locally stored files on your system. Alternatively, if you prefer to delete these files directly through the software, you can utilize the “Files” button. This button opens a file explorer in the project's root directory, where the generated files can be found in the three directories created by the software for storing images and videos that have been processed for detections.

## Troubleshooting 

To ensure smooth operation of the Face Detection Software, please keep the following points in mind:
- Ensure you use video/image files with valid extensions (.mp4, .mov, .jpg, .png) when making detections.
- Image and video detections are saved to the 'image_detections' and 'video_detections' directories, respectively.
- A message will notify you when detections are being processed and when they are done processing (The GUI will appear unresponsive until the success message appears).
- The detector is initialized when either the 'Video' or 'Image' button is pressed and is done so with the current values specified in the settings frame.

Below notes are only applicable to future enhancements previously described for realtime feed detections.
- Only one feed can be displayed at a time. Attempting to open multiple feeds simultaneously may result in unexpected behavior.
- To exit out of a displayed camera feed, simply press the ‘q’ key on your keyboard. This will close the feed window and return you to the main interface.
- It is strongly advised not to move or delete any files in the root directory that were present prior to the initial use of the software through the executable file. Doing so may disrupt the software's functionality.
- If you are using an external camera, make sure it is correctly connected to your computer's USB port. Additionally, ensure that the proper driver software is installed for streaming from your particular external camera device. This will ensure seamless operation of the software with external feeds.

## License

This software is licensed under the MIT License. By using this software, you agree to comply with the terms outlined in the license.


