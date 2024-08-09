import cv2 
import numpy as np 

def resize(frame):
    original_height, original_width, orignal_channels = frame.shape
    new_width = 1000
    aspect_ratio = original_height/original_width
    new_height = aspect_ratio * new_width
    frame = cv2.resize(frame, (int(new_width), int(new_height)))
    return frame

def object_id_to_color(object_id):
    colors = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0)]
    if object_id > len(colors):
        return (230, 25, 75)
    return colors[object_id-1] # ids start with 1

def create_frame_with_colored_tracks(old_frame, detections):
    original_height, original_width, orignal_channels = old_frame.shape
    frame = np.zeros((original_height, original_width, orignal_channels), np.uint8)
    
    for detection in detections:
        point = [int(detection.point.x), int(detection.point.y)]
        cv2.circle(frame, point, 5, object_id_to_color(detection.track_id), -1)

    return frame