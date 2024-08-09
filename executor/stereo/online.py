from executor.logging import Logger
from sources.stereo import StereoRecorder
from tracking_detection.run import Detector
from coordinates.transformer import CoordinateTransformer

class OnlineStereoExecutor():
    # Use Zed2 Stereo camera to retrieve image + depth in realtime and to run the whole pipeline
    
    def __init__(self, log_path,):
        self.recorder = StereoRecorder()
        self.logger = Logger(log_path)
        self.detector = Detector()
        intrinsic_matrix, extrinsic_matrix = []
        self.coordinate_transformer = CoordinateTransformer(intrinsic_matrix, extrinsic_matrix)

    def get_current_frame_and_depth_map(self):
        for frame, depth_map, frame_nr in self.recorder.loop_frames_and_depth_maps():
            result = self.detector.run(frame, frame_nr)
            if not result:
                continue
            
            track_positions, annotated_frame = result
            for tracked_point in track_positions:
                converted_point = self.coordinate_transformer.convert_from_image_to_world_frame(depth_map, tracked_point)
                self.logger.log(converted_point)
