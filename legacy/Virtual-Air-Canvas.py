import cv2
import numpy as np
from collections import deque

blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

points = deque(maxlen=1024)

cap = cv2.VideoCapture(0)


cv2.namedWindow("Air Canvas")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, blueLower, blueUpper)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)

        ((x, y), radius) = cv2.minEnclosingCircle(c)

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            points.appendleft(center)

        else:
            pass

        # Draw line

        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            
            #gives thickness of line based on how far back the point is in the deque
            thickness = int(np.sqrt(1024 / float(i + 1)) * 2.5)
            cv2.line(frame, points[i - 1], points[i], (0, 0, 255), thickness)

            cv2.imshow("Air Canvas", frame)

            cv2.imshow("Mask", mask)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            cap.release()
            cv2.destroyAllWindows()