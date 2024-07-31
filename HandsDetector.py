import cv2
import math
import mediapipe as mp


class HandsDetector:
    def __init__(
        self,
        model_complexity=1,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        # Hand Detection Settings
        self.model_complexity = model_complexity
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Objects for hand detection
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            self.model_complexity,
            self.max_num_hands,
            self.model_complexity,
            self.min_detection_confidence,
            self.min_tracking_confidence
        )
        self.fingertips = [4, 8, 12, 16, 20]

    def find_hands(self, frame, draw=True):
        '''Hand detection in the frame and drawing of landmarks and connectors'''

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Hand detection
        self.results = self.hands.process(img_rgb)

        # Draw points and connectors of the hands on the frame
        if self.results.multi_hand_landmarks:  # If there is a hand
            for hand_landmarks in self.results.multi_hand_landmarks:  # Get 21 points for each hand
                if draw:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,  # Tracker all connections
                        self.mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2),  # Points
                        self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2),  # Connectors
                    )

        return frame

    def find_position_landmarks(self, frame, hand_no=0, draw=True) -> list:
        '''Detecting the position of each landmark and drawing them'''

        x_list = []
        y_list = []
        self.landmark_list = []
        # bounding_box = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id_landmark, landmark in enumerate(my_hand.landmark):
                h, w, _ = frame.shape

                # Get coordinates of each landmark by hand
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                # Save the coordinates of each landmark by hand in a list
                x_list.append(cx)
                y_list.append(cy)
                # Saves the coordinates of all landmarks at hand
                self.landmark_list.append([id_landmark, cx, cy])

                if draw:
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 0), cv2.FILLED)

                # Get bounding box from the hand landmarks with the lowest and highest points
                # x_min, x_max = min(x_list), max(x_list)
                # y_min, y_max = min(y_list), max(y_list)

                # Saves the coordinates of the bounding box
                # bounding_box = x_min, y_min, x_max, y_max

                # if draw:
                #     cv2.rectangle(frame, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 0, 0), 2)

        # print(self.landmark_list)  # Information of each landmark
        return self.landmark_list

    def fingers_up(self) -> list:
        '''Get the fingers that are up'''

        fingers = []
        # Thumb
        # If the tip of the finger is longer than the tip of the previous finger
        if self.landmark_list[self.fingertips[0]][1] > self.landmark_list[self.fingertips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1, 5):
            # If the tip of the finger is longer than the tip of the previous finger
            if self.landmark_list[self.fingertips[id]][2] < self.landmark_list[self.fingertips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        return fingers

    def distance(self, p1, p2, frame, draw=True, line_width=2):
        '''Gets the distance between two points (landmarks)'''
        x1, y1 = self.landmark_list[p1][1:]
        x2, y2 = self.landmark_list[p2][1:]

        # Average between two points
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Distance between two points
        distance = math.hypot(x2 - x1, y2 - y1)
        linea = [x1, y1, x2, y2, cx, cy]

        if draw:
            # Draw a line between the two points
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 0), line_width)
            # Draw the distance between the two points
            # cv2.putText(frame, str(int(distance)), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        return distance, frame, linea
