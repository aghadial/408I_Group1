import cv2
import numpy as np

def detectLine(frame):
    """
    Process the given frame to detect and track the center of a white line.
    
    Args:
        frame (numpy.ndarray): The input frame from the webcam.
    
    Returns:
        lineCenter: A number between [-1, 1] denoting where the center of the line is relative to the frame.
        newFrame: Processed frame with the detected line marked using cv2.rectangle() and center marked using cv2.circle().
    """

    height, width, channels = frame.shape

    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_img, 300, 400)

    y_coords, x_coords = np.nonzero(edges)

    center_coord = [width, 0.0, height, 0.0]
    for x in x_coords:
        if x < center_coord[0]:
            center_coord[0] = x
        if x > center_coord[1]:
            center_coord[1] = x

    for y in y_coords:
            if y < center_coord[2]:
                center_coord[2] = y
            if y > center_coord[3]:
                center_coord[3] = y

    center = (int((center_coord[1] - center_coord[0]) / 2), int(height / 2))

    lineCenter = 1 - 2 * (width - center[0]) / width
    newFrame = cv2.circle(frame, center=center, radius=10, color=(0, 0, 255), thickness=-1)
    newFrame = cv2.rectangle(newFrame, (int(center_coord[0]), int(center_coord[3])), (int(center_coord[1]), int(center_coord[2])), thickness=2, color=(0, 0, 255))

    return lineCenter, newFrame

def main():
    cam = cv2.VideoCapture(1)  # Open webcam

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break

        lineCenter, newFrame = detectLine(frame)

        cv2.imshow('NewFrame', newFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
