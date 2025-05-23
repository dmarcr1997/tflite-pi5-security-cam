from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()


# Set desired frame dimensions for capturing video.
# Note: Adjust these dimensions based on your camera's capability.
frame_height = 1640
frame_width = 1232
picam2.preview_configuration.main.size = (frame_height, frame_width)
picam2.preview_configuration.main.format = "RGB888"

# Align configuration parameters based on camera sensor details.
picam2.preview_configuration.align()

# Start the camera (without configuring a specific mode like "preview" if not needed).
picam2.start()

time.sleep(2)

frame = picam2.capture_array()
cv2.imwrite("debug_frame.jpg", frame)
cv2.imshow("Debug Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()