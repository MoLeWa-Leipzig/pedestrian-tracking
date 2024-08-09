from visualizations.visualizations import create_frame_with_colored_tracks, resize
from bird_eye_transformation.plots import add_bird_eye_points_to_frame
from position_to_line.line_crossing import add_line_to_frame
import cv2 
from utils import TrackPoint, Point
import numpy as np 
from bird_eye_transformation.bird_eye_transformation import calc_projection_matrix


class Plotter():
    def __init__(self):
        pass 

    def plot_raw_plot_with_detections(self, frame):
        #frame_with_line = add_line_to_frame(line_start_point, line_stop_point, frame)
        #frame = add_bird_eye_points_to_frame(frame)
        frame = resize(frame)
        cv2.imshow("Detection & Tracking", frame) 

    def plot_raw_tracks(self, frame, tracked_objects):
        points = [object for object in tracked_objects]
        frame = create_frame_with_colored_tracks(frame, points)
        #frame = add_line_to_frame(line_start_point, line_stop_point, frame)
        frame = resize(frame)
        cv2.imshow("Tracks in original perspective", frame) 

    def plot_tracks_bird_eye_perspective(self, tracked_objects, frame, bird_eye_config):
        projection_matrix = calc_projection_matrix(bird_eye_config)

        frame = cv2.warpPerspective(frame, projection_matrix, (bird_eye_config.width, bird_eye_config.height))

        points_original = []
        for object in tracked_objects:
            points_original.append([int(object.point.x), int(object.point.y)])

        points_original = np.array(points_original, dtype=np.float32,).reshape(1, -1, 2)
        points_transformed = cv2.perspectiveTransform(points_original, projection_matrix)

        detections = []
        for i, point in enumerate(points_transformed[0]):
            detection = tracked_objects[i]
            detections.append(TrackPoint(Point(point[0], point[1]), detection.prob, detection.track_id, detection.class_id, detection.ts, detection.frame_nr))

        frame = create_frame_with_colored_tracks(frame, detections)
        #frame = add_bird_eye_line(frame, line_start_point, line_stop_point, projection_matrix)
        frame = resize(frame)
        cv2.imshow("Tracks in bird eye perspective", frame)

    def plot_bird_eye(self, annotated_frame, bird_eye_config):
        projection_matrix = calc_projection_matrix(bird_eye_config)
        bird_eye_frame = cv2.warpPerspective(annotated_frame, projection_matrix, (bird_eye_config.width, bird_eye_config.height))
        bird_eye_frame = resize(bird_eye_frame)
        cv2.imshow("Bird Eye View", bird_eye_frame)
        return bird_eye_frame