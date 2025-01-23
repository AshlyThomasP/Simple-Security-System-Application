import cv2
import json
import os
import logging
from datetime import datetime

# Configuration
EVENT_LOG_FILE = "event_log.json"
ERROR_LOG_FILE = "error_log.log"

# Setup logging
logging.basicConfig(filename=ERROR_LOG_FILE, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(event_type, image_filename):
    """Logs an event with details such as timestamp, event type, and image filename."""
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "image_filename": image_filename
    }

    try:
        # If event log file doesn't exist, create it
        if not os.path.exists(EVENT_LOG_FILE):
            with open(EVENT_LOG_FILE, 'w') as file:
                json.dump([], file)

        #  Read existing events from the log file
        with open(EVENT_LOG_FILE, 'r') as file:
            events = json.load(file)

        #  Append the new event to the list of events
        events.append(event)

        # Save the updated list of events back to the log file
        with open(EVENT_LOG_FILE, 'w') as file:
            json.dump(events, file, indent=4)
    except Exception as e:
        logging.error(f"Failed to log event: {e}")

def capture_image(camera):
    """Captures an image using the computer's camera and saves it with a timestamped filename."""
    
    ret, frame = camera.read() # Capture a frame from the camera

    # If capturing the frame fails, log the error and exit
    if not ret:
        logging.error("Failed to capture image from the camera.")
        camera.release()
        raise IOError("Failed to capture image from the camera.")
    
    # Generate a filename for the captured image based on the current timestamp
    image_filename = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")

    # Save the captured image to a file
    cv2.imwrite(image_filename, frame)

    return image_filename

def main():
    try:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow

        # Check if the camera was opened successfully
        if not camera.isOpened():
            logging.error("Cannot access the camera.")
            raise IOError("Cannot access the camera.")
        
        print("Press 'Enter' to capture an image. Press 'q' to quit.")

        # Start the loop to continuously capture and display frames from the camera
        while True:
            ret, frame = camera.read()
            if not ret:
                logging.error("Failed to capture image from the camera.")
                break

            # Display the frame 
            cv2.imshow("Camera", frame)

            # Wait for key press to capture image
            key = cv2.waitKey(1) & 0xFF

            if key == 13:  # Enter key to capture
                image_filename = capture_image(camera)
                log_event("Button Pressed Capture", image_filename)
                break
            elif key == ord('q'):  # Press 'q' to quit
                break

        camera.release()
        cv2.destroyAllWindows()

    except Exception as e:
        logging.error(f"Error occurred: {e}")

main()
