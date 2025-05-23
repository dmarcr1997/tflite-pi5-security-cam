from picamera2 import Picamera2
import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter
from my_server.notify_discord import send_image_to_discord
from utils import check_tf_version

#Load model
interpreter = Interpreter("models/detect.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
boxes_idx, classes_idx, scores_idx = check_tf_version(output_details)

#load labels
labels = []
with open("models/labelmap.txt", 'r') as f:
    labels = [line.strip() for line in f.readlines()]
if labels[0] == '???':
       labels.pop(0)

#start camera   
frame_height = 1640
frame_width = 1232
picam2 = Picamera2()
picam2.preview_configuration.main.size = (frame_height, frame_width)
picam2.preview_configuration.main.format = "RGB888"

# Align configuration parameters based on camera sensor details.
picam2.preview_configuration.align()
picam2.start()

time.sleep(1) # Give camera buffer time to wake up

#Detection debounce state
detection_time = None
detected = False
alert_cooldown = 10
last_alert_time = 0

def check_for_detection(c_time, frame):
    global detection_time, detected, last_alert_time
    if detected:
        if detection_time is None:
            detection_time = c_time
        elif c_time - detection_time >= 2:
            if c_time - last_alert_time > alert_cooldown:
                image_path = f"person_{int(c_time)}.jpg"
                cv2.imwrite(image_path, frame)
                send_image_to_discord(image_path, f"Person detected (2s) @ {c_time}")
                last_alert_time = c_time
            detection_time = None
    else: 
        detection_time = None



def detect(frame):

    global detected

    image = cv2.resize(frame.copy(), (width, height))
    input_data = np.expand_dims(image, axis=0)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    
    frame_height, frame_width, _ = frame.shape
    detected = False
    for i in range(len(scores)):
        if scores[i] > 0.5 and int(classes[i]) == 0:
            ymin = int(boxes[i][0] * frame_height)
            xmin = int(boxes[i][1] * frame_width)
            ymax = int(boxes[i][2] * frame_height)
            xmax = int(boxes[i][3] * frame_width)
            timestamp = int(time.time())
            image_path = f"person_{timestamp}.jpg"
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255,0), 2)

            detected = True
    current_time = time.time()
    check_for_detection(current_time, frame)
    return frame

print("Startin detection.... Press Ctrl+C to exit.")
try:
    while True:
        frame = picam2.capture_array() 
        annotated_frame = detect(frame)
        cv2.imshow("Security Camera Feed", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Stopping Camera...")

cv2.destroyAllWindows()