from tracking_detection.run import Detector
from executor.logging import Logger
from bird_eye_transformation.source_points import select_source_points_from_frame
from plots.plots import Plotter
from sources.mono import MonoRecorder

class Executor():
    def __init__(self, video_path, log_path, use_bird_view_transformation=False):
        self.detector = Detector()
        self.video_path = video_path
        self.logger = Logger(log_path)
        self.use_bird_view_transformation = use_bird_view_transformation
        self.plotter = Plotter()
        self.recorder = MonoRecorder(video_path)

    def __init_bird_eye(self):
        self.bird_eye_config = select_source_points_from_frame(self.video_path)
        self.bird_eye_config.height = 500
        self.bird_eye_config.width = 500
    
    def run(self):
        # TODO create Plotter class that can store state 
        if self.use_bird_view_transformation:
            self.__init_bird_eye()

        track_positions_over_time = []

        for frame, frame_nr in self.recorder.loop_frames():
            result = self.detector.run(frame, frame_nr)
            if not result:
                continue
                
            track_positions, annotated_frame = result
            for tracked_point in track_positions:
                track_positions_over_time.append(tracked_point)
                self.logger.log(tracked_point)
            
            if not self.use_bird_view_transformation:
                self.plotter.plot_raw_tracks(annotated_frame, track_positions_over_time)
                self.plotter.plot_raw_plot_with_detections(annotated_frame)
            else:
                print(f"Use bird eye config: {self.bird_eye_config}")
                self.plotter.plot_bird_eye(annotated_frame, self.bird_eye_config)
                self.plotter.plot_tracks_bird_eye_perspective(track_positions_over_time, annotated_frame, self.bird_eye_config)

