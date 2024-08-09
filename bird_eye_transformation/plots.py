from utils import TrackPoint, Point
from position_to_line.line_crossing import add_line_to_frame

import cv2 
import numpy as np 


def add_bird_eye_points_to_frame(frame):
    for point in [tl, bl, tr, br]:
        cv2.circle(frame, point, 10, (0,0,255), -1)
    return frame

def add_bird_eye_line(frame, line_start_point, line_stop_point, projection_matrix):
    points = [
        [int(line_start_point.x),int(line_start_point.y)],
        [int(line_stop_point.x),int(line_stop_point.y)]
    ]
    points_original = np.array(points, dtype=np.float32,).reshape(1, -1, 2)
    points_transformed = cv2.perspectiveTransform(points_original, projection_matrix)[0]
    transformed_line_start_point = Point(int(points_transformed[0][0]), int(points_transformed[0][1]))
    transformed_line_stop_point = Point(int(points_transformed[1][0]), int(points_transformed[1][1]))
    frame = add_line_to_frame(transformed_line_start_point, transformed_line_stop_point, frame)
    return frame