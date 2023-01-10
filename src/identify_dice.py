import cv2
import numpy as np
import time

def startWebcam():
    capture = cv2.VideoCapture(2)
    return capture

def drawShapes(capture):
    while (True):
        result, frame = capture.read()
        frame = getShapes(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def getShapes(frame):

    results = []

    # converting image into grayscale image
    rendered_image = frame[209:370, 72:508]
    gray = cv2.cvtColor(rendered_image, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 70, 1, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0

    # Draw the background for the numbers.
    y_offset = 50
    x_offset = 50
    cv2.rectangle(frame, (0, 0), (x_offset + 300, y_offset + 100), (38, 32, 24), -1)

    for contour in contours:

        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        x, y, w, h = cv2.boundingRect(contour)
        # number_x = int(x + (w / 4))
        # number_y = int(y + (h / 4))
        # number_width = int(w / 2)
        # number_height = int(h / 2)

        number_width = 20
        number_height = 20
        number_x = int(x + (w / 2)) - int(number_width / 2)
        number_y = int(y + (h / 2)) - int(number_height / 2)


        try:
            if 100 > w > 15:
                if 100 > h > 15:
                    # Bounding rect
                    # cv2.rectangle(rendered_image, (x, y), (x + w, y + h), (0, 255, 0), 1)

                    # Number rect
                    cv2.rectangle(rendered_image, (number_x, number_y), (number_x + number_width, number_y + number_height), (0, 0, 255), 1)

                    # Outline
                    cv2.drawContours(rendered_image, [contour], 0, (252, 186, 3), 2)

                    # Display the numbers in the top left
                    frame[
                        y_offset:y_offset + number_height,
                        x_offset:x_offset + number_width
                    ] = rendered_image [
                        number_y:number_y + number_height,
                        number_x:number_x + number_width
                    ]

                    # y_offset = y_offset + number_height
                    x_offset = x_offset + number_width + 5
        except:
            continue

    return frame

def closeStreams(capture):
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture = startWebcam()
    drawShapes(capture)
    closeStreams(capture)