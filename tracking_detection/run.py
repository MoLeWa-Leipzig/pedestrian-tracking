import cv2 
import datetime 
from utils import Point, TrackPoint
from ultralytics import YOLO

class Detector():
    def __init__(
        self
    ):
        # https://gist.github.com/AruniRC/7b3dadd004da04c80198557db5da4bda
        self.CLASSES = [0, 2, 3, 4, 6, 7]

        self.CONF = 0.8
        self.IOU = 0.9

        # Load an official or custom model
        self.model = YOLO('yolov8m.pt')  # Load an official Detect model

    def run(self, frame, frame_nr):
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = self.model.track(frame, show=False, conf=self.CONF, iou=self.IOU, classes=self.CLASSES, tracker="tracker.yaml", persist=True)[0]  # Tracking with default tracker
        annotated_frame = results.plot()

        if results.boxes.id == None:
            return
                    
        boxes = results.boxes.xywh.cpu()
        class_ids = results.boxes.cls.int().cpu()
        track_ids = results.boxes.id.int().cpu()
        probs = results.boxes.conf.cpu()

        all_tracks = []

        for box, class_id, track_id, prob in zip(boxes, class_ids, track_ids, probs):
            x, y, w, h = box
            point = Point(x.item(), y.item())
            datetimestamp_now = datetime.datetime.now()
            track_point = TrackPoint(point, prob, track_id.item(), class_id, datetimestamp_now, frame_nr)
            all_tracks.append(track_point)

        return all_tracks, annotated_frame

    
