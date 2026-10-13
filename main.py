import cv2
import numpy as np
from collections import deque
import traceback

    # Green: (0, 255, 0)

    # Blue: (255, 0, 0)

    # Red: (0, 0, 255)

    # Yellow: (0, 255, 255)

    # Cyan (Light Blue): (255, 255, 0)

    # Magenta (Pink): (255, 0, 255)

    # White: (255, 255, 255)

    # Black: (0, 0, 0)

try:
    # Color (B, G, R)
    DRAW_COLOR = (0, 255, 255) # Yellow
    # DRAW_COLOR = (255, 0, 255)
    blueLower = np.array([100, 140, 60])
    blueUpper = np.array([140, 255, 255])
    points = deque(maxlen=512) # Memory

    prev_center = None

    # UI Function
    def draw_ui(frame):
        instructions = [
            ("CONTROLS:", 30),
            (" 'C' - Clear Canvas", 60),
            (" 'Q' - Quit", 90),              
            (" 'F' - Toggle Full Screen", 120)
        ]
        
        for text, y in instructions:
            # Shadow
            cv2.putText(frame, text, (12, y + 2), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (0, 0, 0), 3, cv2.LINE_AA)
            # Text
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # Start webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise Exception("Camera could not be opened.")

    print("Camera started! Press 'q' to quit.")

    # Create window before loop
    cv2.namedWindow("Air Canvas", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, blueLower, blueUpper)

        mask = cv2.erode(mask, None, iterations=6)
        mask = cv2.dilate(mask, None, iterations=3)

        contours_info = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = contours_info[0] if len(contours_info) == 2 else contours_info[1]
        
        # Reset center for this frame
        current_center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            
            if M["m00"] > 0: # Check for divide by zero
                raw_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if radius > 5:
                    if prev_center is None:
                        smooth_center = raw_center
                    else:
                        alpha = 0.2
                        sx = int(alpha * raw_center[0] + (1 - alpha) * prev_center[0])
                        sy = int(alpha * raw_center[1] + (1 - alpha) * prev_center[1])
                        smooth_center = (sx, sy)

                    prev_center = smooth_center
                    points.appendleft(smooth_center)
                    cv2.circle(frame, smooth_center, int(radius), DRAW_COLOR, 2)
                else:
                    prev_center = None

        # Draw the lines
        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            cv2.line(frame, points[i - 1], points[i], DRAW_COLOR, 5)

        draw_ui(frame)

        cv2.imshow("Air Canvas", frame)

        # Controls
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break
        elif key == ord("c"):
            points.clear()
            prev_center = None
        elif key == ord("f"):
            # Toggle Full Screen
            current_state = cv2.getWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN)
            if current_state == cv2.WINDOW_FULLSCREEN:
                cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            else:
                cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

except Exception:
    print("\n" + "="*40)
    print("!! THE SCRIPT CRASHED !!")
    traceback.print_exc()
    print("="*40 + "\n")
    input("Press Enter to close this window...")

finally:
    cap.release()
    cv2.destroyAllWindows()