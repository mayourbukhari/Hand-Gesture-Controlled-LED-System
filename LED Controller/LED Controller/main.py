# Author: Syed Mohsin Bukhari
# Website: https://mayourbukhari.github.io/Personal-Portfolio

import cv2
import mediapipe as mp
import time
import controller as cnt

# Wait for 2 seconds before starting
time.sleep(2.0)

# Initialize Mediapipe modules
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# Define the fingertip IDs
tipIds = [4, 8, 12, 16, 20]

# Open the video camera
video = cv2.VideoCapture(0)

# Use Mediapipe Hands module
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        # Read a frame from the video
        ret, image = video.read()

        # Convert BGR image to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the frame with Mediapipe Hands
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # List to store landmark information
        lmList = []

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            # Take the first hand detected
            myHands = results.multi_hand_landmarks[0]

            # Loop through landmarks and get their coordinates
            for id, lm in enumerate(myHands.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            # Draw landmarks and connections
            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

        # List to store finger state (open or closed)
        fingers = []

        # If landmarks are detected
        if len(lmList) != 0:
            # Check the state of each finger
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Count the number of open fingers
            total = fingers.count(1)

            # Control the LED based on the finger count
            cnt.led(total)

            # Display finger count on the frame
            if total > 0:
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, str(total), (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)
                cv2.putText(image, "LED", (100, 375), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 0, 0), 5)

        # Display the frame
        cv2.imshow("Frame", image)

        # Check for key press to exit the loop
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

# Release video capture and close all windows
video.release()
cv2.destroyAllWindows()
