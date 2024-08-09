import zed 

class StereoRecorder():
    # Record images/frames and depth map from a stereo camera for further offline processing
    def __init__(self, save_records=False, output_dir="./data") -> None:
        self.init_params = sl.InitParameters()
        self.init_params.depth_mode = sl.DEPTH_MODE.ULTRA # Use ULTRA depth mode
        self.init_params.coordinate_units = sl.UNIT.MILLIMETER # Use millimeter units (for depth measurements)
        self.save_records = save_records
        self.output_dir = output_dir

    def loop_frames_and_depth_maps(self):
        frame_nr = 0
        while True:
            frame = sl.Mat()
            depth_map = sl.Mat()
            runtime_parameters = sl.RuntimeParameters()
            if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS :
                # A new image and depth is available if grab() returns SUCCESS
                zed.retrieve_image(frame, sl.VIEW.LEFT) # Retrieve left image
                zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH) 

                if self.save_records:
                    self.save(frame, depth_map, frame_nr)
            frame_nr += 1
            yield frame, depth_map, frame_nr

    def save(self, frame, depth_map, frame_nr):
        pass
