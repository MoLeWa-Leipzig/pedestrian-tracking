import time
import signal 
import sys 
import traceback
import math 
from copy import deepcopy
import numpy as np
import cv2
import pyzed.sl as sl 
import cv_viewer.tracking_viewer as cv_viewer
from executor.logging import Logger 

INTERRUPTED = False 

class Detection():
	def __init__(self, pos, idx):
		self.position = pos
		self.id = idx	

id_colors = [[232,176,59],
             [175,208,59],
             [102,205,105],
             [185,0,255],
             [99,107,252]]

class Zed2Executor():
    # Use the Zed2 stereo camera and its builtin detection/tracking 

    def __init__(self, max_depth, cam_pos_x, cam_pos_y, log_path="./log.log") -> None:
        self.max_depth = max_depth
        self.cam_pos_x = cam_pos_x
        self.cam_pos_y = cam_pos_y
        self.logger = Logger(log_path)
    
    def setup_camera(self):
        self.init_params = sl.InitParameters()
        self.init_params.camera_resolution = sl.RESOLUTION.HD1080
        self.init_params.camera_fps = 30
        self.init_params.coordinate_units = sl.UNIT.METER
        self.init_params.depth_minimum_distance = 1.0 #recommended for long range 
        self.init_params.depth_maximum_distance = self.max_depth
        self.init_params.coordinate_system = sl.COORDINATE_SYSTEM.LEFT_HANDED_Y_UP

        err = self.zed.open(self.init_params)

        if err != sl.ERROR_CODE.SUCCESS:
            exit(-1)

    def setup_object_detection(self):
        detection_params = sl.ObjectDetectionParameters()
        detection_params.enable_tracking = True
        detection_params.detection_model = sl.OBJECT_DETECTION_MODEL.MULTI_CLASS_BOX_FAST

        positional_parameters = sl.PositionalTrackingParameters()
        # Setting position of camera did not work ?
        #initial_position = sl.Transform()
        #initial_translation = sl.Translation()
        #initial_translation.init_vector(5,-10, 0)
        #initial_position.set_translation(initial_translation)
        #positional_parameters.set_initial_world_transform(initial_position)
        self.zed.enable_positional_tracking(positional_parameters)

        err = self.zed.enable_object_detection(detection_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print("Could not enable object detection: " + err)
            self.zed.close()
            exit(-1)

    def get_current_objects(self):
        objs = sl.Objects()
        grab_params = sl.RuntimeParameters()
        grab_params.measure3D_reference_frame = sl.REFERENCE_FRAME.WORLD
        err = self.zed.grab() 
        if err != sl.ERROR_CODE.SUCCESS:
            print(f"Could not grab image: {err}")
        
        detection_params_rt = sl.ObjectDetectionRuntimeParameters()
        detection_params_rt.detection_confidence_threshold = 20
        detection_params_rt.object_class_filter = [sl.OBJECT_CLASS.VEHICLE, sl.OBJECT_CLASS.PERSON]

        self.zed.retrieve_objects(objs, detection_params_rt)
        return objs

    def get_objects_positions(self):
        global INTERRUPTED 
        while True and not INTERRUPTED:	
            objs = self.get_current_objects()
            for obj in objs.object_list:
                print(f"Id: {obj.id} Pos: {obj.position} Class: {obj.label} Sub: {obj.sublabel} Conf: {obj.confidence} 2D: {obj.bounding_box_2d} 3D: {obj.bounding_box}")
            time.sleep(1)

    def handle_signal(self):
        def handler(a,b):
            global INTERRUPTED
            INTERRUPTED = True
        signal.signal(signal.SIGINT, handler)

    def draw_tracks(self, track_positions, objects, tracks_resolution):
        # Draw tracks (relative to the flat streets)

        image_track_ocv = np.zeros((tracks_resolution.height, tracks_resolution.width, 4), np.uint8)

        for obj in objects.object_list:
            pos = obj.position
            if math.isnan(pos[0]) or math.isnan(pos[1]) or math.isnan(pos[2]):
                continue
            camera_point = np.array([pos[0], pos[1], pos[2], 1])
            world_point = self.convert_point_from_camera_to_world(camera_point)
            x_world = world_point[0]
            z_world = world_point[2]
            
            image_point = np.array([x_world, z_world])
            image_point_scaled = 100 * image_point
            print(tuple(image_point_scaled))
            pos = tuple(image_point_scaled.astype(int))
            track_positions.append(Detection(pos, obj.id))

        for detection in track_positions:
            color = self.generateColorID_u(detection.id)
            cv2.circle(image_track_ocv, detection.position, 5, color, -1)

        track_image_copy_flip = cv2.flip(image_track_ocv, 0)

        return track_positions, track_image_copy_flip 

    def convert_point_from_camera_to_world(self, point):
        print(f"Point wrt Camera: {point}")
        cam_pose_matrix = self.get_camera_pose_matrix()
        world_point = cam_pose_matrix.dot(point)
        print(f"Point wrt World: {world_point}")
        return world_point

    def resize(self, frame, new_width=None, new_height=None):
        height, width, c = frame.shape
        aspect_ratio = height/width
        if new_width:
            new_height = aspect_ratio*new_width
        elif new_height:
            new_width = aspect_ratio*new_height
        frame = cv2.resize(frame, (int(new_width), int(new_height)))
        return frame

    def setup_track_frame(self):
        # 1px=1cm
        # max_depth == image height
        track_height = self.max_depth * 100 # if max depth is 20m then the track image shall be 2000px high 
        resolution = sl.Resolution(track_height, track_height)
        image_track_ocv2 = np.zeros((resolution.height, resolution.width, 4), np.uint8)
        return image_track_ocv2, resolution

    def setup_resolution(self):
        camera_config = self.zed.get_camera_information().camera_configuration
        DISPLAY_WIDTH = 1000	
        image_aspect_ratio = camera_config.resolution.width/camera_config.resolution.height
        DISPLAY_RESOLUTION = sl.Resolution(DISPLAY_WIDTH, DISPLAY_WIDTH/image_aspect_ratio)
        return DISPLAY_RESOLUTION

    def show_cv_image(self):
        camera_config = self.zed.get_camera_information().camera_configuration
        DISPLAY_RESOLUTION = self.setup_resolution()
        image_track_ocv2, track_resolution = self.setup_track_frame()
        image_scale = (DISPLAY_RESOLUTION.width/camera_config.resolution.width, DISPLAY_RESOLUTION.height/camera_config.resolution.height)
        print(f"Max Depth: {self.init_params.depth_maximum_distance}")
        track_view_generator = cv_viewer.TrackingViewer(track_resolution, camera_config.fps, self.init_params.depth_maximum_distance*1000, 3)
        track_view_generator.set_camera_calibration(camera_config.calibration_parameters)

        image = sl.Mat()
        cam_w_pose = sl.Pose()

        track_positions = []

        global INTERRUPTED 
        while True and not INTERRUPTED:	
            self.zed.retrieve_image(image, sl.VIEW.LEFT, sl.MEM.CPU, DISPLAY_RESOLUTION)
            image_np = image.get_data()
            self.zed.get_position(cam_w_pose, sl.REFERENCE_FRAME.WORLD)
            objects = self.get_current_objects()

            # Draw frame with detections
            track_view_generator.generate_view(objects, image_np, image_scale, cam_w_pose, image_track_ocv2, objects.is_tracked)
            
            # Draw tracks
            track_positions, image_track_ocv = self.draw_tracks(track_positions, objects, track_resolution)
            image_track_ocv = self.resize(image_track_ocv, new_width=DISPLAY_RESOLUTION.width)
            print(image_np.shape)
            print(image_track_ocv.shape)	
            global_image = cv2.vconcat([image_np, image_track_ocv])
            cv2.imshow("", global_image)
            cv2.waitKey(10)

    def get_camera_pose_matrix(self):
        trans_y = self.cam_pos_y # office:1 outside: 15
        trans_x = self.cam_pos_x # office: 2.5 outside: #10
        return np.array([[1,0,0,trans_x], [0,1,0,trans_y], [0,0,1,0], [0, 0, 0, 1]])

    def print_camera_position(self):
        pose = sl.Pose()
        self.zed.get_position(pose, sl.REFERENCE_FRAME.WORLD)
        trans = sl.Translation()
        pose.get_translation(trans)
        orien = sl.Orientation()
        pose.get_orientation(orien)
        trans_x = trans.get()[0]
        trans_y = trans.get()[1]
        trans_z = trans.get()[2]

        o_x = orien.get()[0]
        o_y = orien.get()[1]
        o_z = orien.get()[2]
        o_w = orien.get()[3]

        print(f"{o_x} {o_w}")

    def generateColorID_u(self, idx):
        if idx < 0:
            return (236, 184, 36, 255)
        
        color_idx = idx % 5
        return (id_colors[color_idx][0], id_colors[color_idx][1], id_colors[color_idx][2], 255)


    def run(self):
        self.handle_signal()	
        self.zed = sl.Camera()	
        try:
            self.setup_camera()
            self.setup_object_detection()
            #get_objects_positions()
            self.show_cv_image()
        except Exception as e:
            print("Error occured: " + str(e))
            print(traceback.format_exc())
            self.zed.disable_object_detection()
            self.zed.disable_positional_tracking()
            self.zed.close()





