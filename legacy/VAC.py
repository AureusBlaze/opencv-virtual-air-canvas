import cv2
import numpy as np
from collections import deque
import traceback # error handling

try:
    
    blueLower = np.array([100, 60, 60])
    blueUpper = np.array([140, 255, 255])
    points = deque(maxlen=50) # time to forget old points

    prev_center = None

    is_fullscreen = False

    #UI
    def draw_ui(frame):
        # List of instructions: (Text, Position Y-coordinate)
        instructions = [
            ("CONTROLS:", 30),
            (" 'C' - Clear Canvas", 60),
            (" 'Q' - Quit", 90),
            (" 'F' - Toggle Full Screen", 120)
        ]
        
        for text, y in instructions:
        # 1. Draw Black Shadow
            # cv2.putText(frame, text, (12, y + 2), cv2.FONT_HERSHEY_SIMPLEX, 
            #        0.6, (0, 0, 0), 3, cv2.LINE_AA)
        # 2. Draw White Text on top
            cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, (255, 255, 255), 1, cv2.LINE_AA)
        

    # Start webcam
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened
    if not cap.isOpened():
        raise Exception("Camera could not be opened. Try changing index to 1 or -1.")

    print("Camera started! Press 'q' to quit.")

    cv2.namedWindow("Air Canvas", cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, blueLower, blueUpper)
        mask = cv2.erode(mask, None, iterations=10)
        mask = cv2.dilate(mask, None, iterations=5)

        # detecting version to avoid the crash
        contours_info = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # OpenCV 3 returns 3 items, OpenCV 4 returns 2. This handles both:
        cnts = contours_info[0] if len(contours_info) == 2 else contours_info[1]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            raw_center = (int(M["m10"] / (M["m00"] + 1e-5)), int(M["m01"] / (M["m00"] + 1e-5))) # Added +1e-5 to avoid divide by zero

            if radius > 5:
                if prev_center is None:
                    smooth_center = raw_center
                else:
                    alpha = 0.5 
                    sx = int(alpha * raw_center[0] + (1 - alpha) * prev_center[0])
                    sy = int(alpha * raw_center[1] + (1 - alpha) * prev_center[1])
                    smooth_center = (sx, sy)

                prev_center = smooth_center
                points.appendleft(smooth_center)
        
                cv2.circle(frame, smooth_center, int(radius), (0, 0, 255), 2)
            else:
                prev_center = None # Reset if we lose tracking


        # Draw the lines
        for i in range(1, len(points)):
            if points[i - 1] is None or points[i] is None:
                continue
            cv2.line(frame, points[i - 1], points[i], (0, 0, 255), 5)

        draw_ui(frame)

        cv2.imshow("Air Canvas", frame)

        # ... inside the while loop ...

        key = cv2.waitKey(1) & 0xFF
        
        # QUIT
        if key == ord("q"):
            break
            
        # CLEAR CANVAS
        elif key == ord("c"):
            points.clear()
            
        # TOGGLE FULL SCREEN (New Feature)
        elif key == ord("f"):
            # Check current state
            current_state = cv2.getWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN)
            
            if current_state == cv2.WINDOW_FULLSCREEN:
                # If full screen -> Go normal
                cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            else:
                # If normal -> Go full screen
                cv2.setWindowProperty("Air Canvas", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

except Exception:
    # IN CASE OF CRASH:
    print("\n" + "="*40)
    print("!! THE SCRIPT CRASHED !!")
    print("Here is the error message:")
    print("="*40 + "\n")
    traceback.print_exc() # Prints the error
    print("\n" + "="*40)
    input("Press Enter to close this window...") # Keeps window open

finally:
    cap.release()
    cv2.destroyAllWindows()