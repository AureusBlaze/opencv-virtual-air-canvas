import cv2
import numpy as np

def nothing(x):
    pass

# Create a window with sliders
cv2.namedWindow("Color Detector")
cv2.createTrackbar("Hue Min", "Color Detector", 90, 179, nothing) # Start at 90
cv2.createTrackbar("Hue Max", "Color Detector", 130, 179, nothing) # Start at 130
cv2.createTrackbar("Sat Min", "Color Detector", 50, 255, nothing)
cv2.createTrackbar("Sat Max", "Color Detector", 255, 255, nothing)
cv2.createTrackbar("Val Min", "Color Detector", 50, 255, nothing)
cv2.createTrackbar("Val Max", "Color Detector", 255, 255, nothing)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    # convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get values from trackbars
    h_min = cv2.getTrackbarPos("Hue Min", "Color Detector")
    h_max = cv2.getTrackbarPos("Hue Max", "Color Detector")
    s_min = cv2.getTrackbarPos("Sat Min", "Color Detector")
    s_max = cv2.getTrackbarPos("Sat Max", "Color Detector")
    v_min = cv2.getTrackbarPos("Val Min", "Color Detector")
    v_max = cv2.getTrackbarPos("Val Max", "Color Detector")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Create the mask
    mask = cv2.inRange(hsv, lower, upper)

    # Show the original camera and the "Mask" side by side
    # The mask is what the computer "sees". 
    # Adjust sliders until your object is WHITE and background is BLACK.
    cv2.imshow("Original", frame)
    cv2.imshow("The Mask (Adjust Sliders!)", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        print(f"--- YOUR NEW NUMBERS ---")
        print(f"blueLower = np.array([{h_min}, {s_min}, {v_min}])")
        print(f"blueUpper = np.array([{h_max}, {s_max}, {v_max}])")
        print(f"------------------------")
        break

cap.release()
cv2.destroyAllWindows()