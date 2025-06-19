import cv2  # Import OpenCV library for camera operations

# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Failed to open camera (index 0). Try another index or check camera permissions.")
    exit(1)

print("Press 'q' to quit.")
# Main loop to read frames from the camera
while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        print("Failed to read frame from camera.")
        break
    cv2.imshow('Camera Test', frame)  # Display the frame in a window
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resource
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows() 