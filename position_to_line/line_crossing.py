from utils import Point

import cv2 

def isLeftorUp(a: Point, b: Point, c: Point):
  return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x) > 0

def add_line_to_frame(LINE_START, LINE_STOP, frame):
    color = (0, 255, 0)
    thickness = 5
    annotated_frame = cv2.line(frame, (LINE_START.x, LINE_START.y), (LINE_STOP.x, LINE_STOP.y), color, thickness)
    return annotated_frame

LINE_START = Point(0, 900)
LINE_STOP = Point(1900, 900)

# point_is_left_or_up_line = isLeftorUp(LINE_START, LINE_STOP, tracked_point.point)
