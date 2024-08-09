import cv2
import numpy as np
import os 
from .bird_eye_transformation import BirdEyeConfig

pts = [(0, 0), (0, 0), (0, 0), (0, 0), ()]
pointIndex = 0
image = None

def select_source_points_from_frame(video_path):
    print("Select four points for bird eye transformation. 1. Bottom-Left 2. Bottom-Right 3. Top-Right 4. Top-Left")
    video = cv2.VideoCapture(video_path)
    show_window(video)
    return BirdEyeConfig(height=0, width=0, bottom_left=pts[0], bottom_right=pts[1], top_right=pts[2], top_left=pts[3])

# function to select four points on a image to capture desired region
def draw_circle(event, x, y, flags, param):
    global image
    global pointIndex
    global pts
    global n_clicks

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        pts[pointIndex] = (x, y)
        # print(pointIndex)
        if pointIndex == 3:
            cv2.line(image, pts[0], pts[1], (0, 255, 0), thickness=2)
            cv2.line(image, pts[1], pts[2], (0, 255, 0), thickness=2)
            cv2.line(image, pts[2], pts[3], (0, 255, 0), thickness=2)
            cv2.line(image, pts[3], pts[0], (0, 255, 0), thickness=2)
        pointIndex = pointIndex + 1


def show_window(cap):
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            # Display the resulting frame
            cv2.imwrite(os.path.join(".", "data", 'image.png'), frame)
            break 
    
        # Break the loop
        else: 
            break

    # When everything done, release the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()
    
    
    global image
    global n_clicks
    image = cv2.imread("data/image.png")

    cv2.namedWindow("img")
    cv2.setMouseCallback("img", draw_circle)

    while True:
        cv2.imshow("img", image)

        if pointIndex == 5 or (cv2.waitKey(1) & 0xFF == ord("q")):
            break
    
    cv2.destroyAllWindows()

        



