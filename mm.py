import cv2
import numpy as np
import time
from pyfirmata import Arduino, util

# Establish serial connection with Arduino
board = Arduino("COM15")  # Adjust the port according to your setup

# LED pins on Arduino
led_pins = [8, 9, 10, 11, 12]
for pin in led_pins:
    board.digital[pin].mode = 1


# Function to count fingers
def count_fingers(thresholded, drawing):
    contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return 0
    max_contour = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(max_contour, returnPoints=False)
    defects = cv2.convexityDefects(max_contour, hull)

    if defects is not None:
        count = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(max_contour[s][0])
            end = tuple(max_contour[e][0])
            far = tuple(max_contour[f][0])

            a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))

            if angle <= np.pi / 2:
                count += 1
                cv2.circle(drawing, far, 3, [255, 0, 0], -1)
        return count + 1


# Main function
def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame
        frame = cv2.flip(frame, 1)

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Threshold the image
        _, thresholded = cv2.threshold(
            blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # Create a black image for drawing
        drawing = np.zeros(frame.shape, dtype=np.uint8)

        # Count fingers
        fingers = count_fingers(thresholded, drawing)

        # Control LEDs based on finger count
        for pin in range(8, 13):
            if pin - 7 <= fingers:
                board.digital[pin].write(1)
            else:
                board.digital[pin].write(0)

        # Display the count
        cv2.putText(
            drawing,
            str(fingers),
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
        )

        # Display the frames
        cv2.imshow("Original", frame)
        cv2.imshow("Thresholded", thresholded)
        cv2.imshow("Drawing", drawing)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
