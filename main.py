import cv2
import numpy as np
from HandsDetector import HandsDetector

# Libraries for controlling the volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


Devices = AudioUtilities.GetSpeakers()  # Get all audio devices
interface = Devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)  # Activate the interface
volume = cast(interface, POINTER(IAudioEndpointVolume))  # Casting
vol_range = volume.GetVolumeRange()  # Volume range
min_vol = vol_range[0]  # Minimum volume
max_vol = vol_range[1]  # Maximum volume


cap = cv2.VideoCapture(1)
detector = HandsDetector(max_num_hands=1)  # Single hand detection

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    frame = detector.find_hands(frame, draw=True)
    landmark_list = detector.find_position_landmarks(frame, draw=False)

    if len(landmark_list) != 0:  # If there are landmarks
        fingers = detector.fingers_up()

        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            distance, frame, linea = detector.distance(4, 8, frame)
            vol = np.interp(distance, [25, 200], [min_vol, max_vol])  # Linear interpolation
            volume.SetMasterVolumeLevel(vol, None)  # Changing the volume


    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()