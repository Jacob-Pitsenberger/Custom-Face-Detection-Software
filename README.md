# Face Detection Software

Welcome to the Face Detection Software, a powerful tool designed to facilitate real-time and post-production face detection on various camera feeds, including internal and external webcams, as well as CCTV/IP camera streams.

## Key Features:

- Real-Time Detection: Instantaneously identify faces in live webcam and CCTV/IP camera feeds.
- Post-Production Analysis: Analyze pre-recorded video and image files for facial features.
- Intuitive GUI: Enjoy a user-friendly Graphical User Interface (GUI) that simplifies interaction with the software's capabilities.

## Getting Started

Before delving into the features and functionality of the Face Detection Software, let's ensure that your system meets the necessary requirements and that the software is correctly installed.

### System Requirements

Before installation, ensure that your system meets the following requirements:
- Operating System: Windows 10 or later
- Memory: 8GB of RAM is recommended for smooth operation.
- Processor: A quad-core processor (or equivalent) with a clock speed of 2.0 GHz or faster is recommended.

## License

This software is licensed under the MIT License. By using this software, you agree to comply with the terms outlined in the license.

## User Guide

The User Guide provides detailed instructions on how to effectively utilize the Face Detection Software.

### Using the GUI

The graphical user interface (GUI) is the primary interface of the software. It comprises a main window with various buttons facilitating different functions. Below are the main features of the GUI:
- Real-time Video Feed: This button allows you to open a live video feed. You can choose between the internal webcam, external webcam, or CCTV/IP camera feeds, each accessible through separate buttons on the GUI. After viewing the feed, you can save it with any detections made by pressing the 'q' key after ensuring the feed window is in focus. To bring the window into focus, click on it with your left mouse button.
- Post-processing Video and Image Files: These buttons allow you to process video and image files for detections.
- File Explorer: Opens the file explorer in the project's root directory, enabling you to view files saved with detections.
- Help Button: Provides additional assistance on using the software effectively.

### Face Detection Modes

The Face Detection Software offers various modes for detecting faces:
- Internal Webcam Feed: Opens the internal webcam feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.
- External Webcam Feed: Opens an external webcam feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.
- CCTV Feed: Opens a CCTV/IP camera feed for real-time face detection. Close the feed window by pressing the 'q' key after ensuring the window is in focus.
- Detect Over Video: Select a video file and detect faces within it.
- Detect Over Image: Select an image file and detect faces within it.
- Files: Opens the file explorer in the project root folder, allowing you to open a file processed for detections with your system's default media player.

## Data Storage

Upon installation, the Face Detection Software is placed in the root directory titled "Face Detection Software". This directory includes all the necessary dependencies to run the program, licensing files, and the executable file for launching the software. When the program is launched for the first time, it automatically creates three additional directories in the root directory to organize processed detection files. These directories are:

- `recorded detections`: This directory contains recorded video files from internal, external, and CCTV/IP camera feeds that were viewed using the software.
- `image detections`: Here, you'll find image files that were processed for detections and saved through the software.
- `video detections`: This directory stores video files that have undergone processing for detections. Video files saved from webcam feeds are named with the timestamp at which the feed was initially viewed, followed by the channel number used to access the webcam (0 for internal, 1 for external), and the text “_webcam_recording”. Video files saved from CCTV/IP camera feeds follow a similar naming convention with the timestamp followed by the text “_feed_recording”. Both webcam and CCTV/IP camera feeds are saved as .mp4 files. Videos and images post-processed for detections are saved in the .mp4 and .jpg formats, respectively.

## Data Deletion

All files generated using the Face Detection Software are stored in the software's master root directory titled “Face Detection Software”. To delete these files, you can do so through your file explorer, following the same procedure as you would for deleting other locally stored files on your system. Alternatively, if you prefer to delete these files directly through the software, you can utilize the “Files” button. This button opens a file explorer in the project's root directory, where the generated files can be found in the three directories created by the software for storing images and videos that have been processed for detections.

## Troubleshooting

To ensure smooth operation of the Face Detection Software, please keep the following points in mind:

- Only one feed can be displayed at a time. Attempting to open multiple feeds simultaneously may result in unexpected behavior.
- To exit out of a displayed camera feed, simply press the ‘q’ key on your keyboard. This will close the feed window and return you to the main interface.
- It is strongly advised not to move or delete any files in the root directory that were present prior to the initial use of the software through the executable file. Doing so may disrupt the software's functionality.
- If you are using an external camera, make sure it is correctly connected to your computer's USB port. Additionally, ensure that the proper driver software is installed for streaming from your particular external camera device. This will ensure seamless operation of the software with external feeds.




