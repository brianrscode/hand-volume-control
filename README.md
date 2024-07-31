# Hand Volume Control

This project uses the MediaPipe library to detect hands and control the system volume through finger gestures. Detection is performed via the webcam and adjusts the volume based on the distance between the thumb and index finger.

Requirements
- Python 3.7+
- OpenCV
- MediaPipe
- NumPy
- pycaw
- comtypes


## Installation

1. Clone this repository:
````bash
git clone https://github.com/brianrscode/hand-volume-control.git
````
````bash
cd hand-volume-control
````

2. Install the dependencies:
````bash
pip install -r requirements.txt
````

## Usage
1. Run the main script:
````bash
python main.py
````
2. Make sure your webcam is on and visible.
3. Adjust the volume by bringing the thumb and index finger together and moving them apart or closer.

## Project Structure
- `HandsDetector.py`: Contains the HandsDetector class for hand detection and tracking using MediaPipe.

- `main.py`: Main script to run hand detection and volume control.

## Code Description
### HandsDetector
The `HandsDetector` class provides methods to:
- Detect hands in a video frame.
- Find positions of hand landmarks.
- Determine which fingers are up.
- Calculate the distance between two specific landmarks.

### main.py
The main script:
- Sets up video capture from the webcam.
- Uses the `HandsDetector` class to detect hands and get landmark positions.
- Calculates the distance between the thumb and index finger to adjust the system volume.
