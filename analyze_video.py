import cv2
import numpy as np


# Function to detect potential cracks in a frame
def detect_cracks(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to smooth the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Perform morphological operations to close gaps in edges
    kernel = np.ones((5, 5), np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours of potential cracks
    contours, _ = cv2.findContours(closed_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around potential cracks
    for contour in contours:
        # Filter contours based on area (you may need to adjust these thresholds)
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame

# Process video stream
cap = cv2.VideoCapture('video5.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break

    # Detect potential cracks in the frame
    frame_with_cracks = detect_cracks(frame)

    # Display the resulting frame
    cv2.imshow('Frame', cv2.resize(frame_with_cracks, (640, 360)))


    # Break the loop if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release video capture object and close windows
cap.release()
cv2.destroyAllWindows()
