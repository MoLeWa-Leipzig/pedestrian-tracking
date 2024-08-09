import os 
from utils import Point

class Logger():
    def __init__(self, path_to_file, three_dimensions=False):
        self.path_to_file = path_to_file
        self.three_dimensions = three_dimensions
        self.__setup_track_file()

    def __setup_track_file(self):
            if not os.path.exists(self.path_to_file):
                with open(self.path_to_file, 'w') as track_file:
                    header = "time,id,class,prob,x,y"
                    if self.three_dimensions:
                        header += ",z"
                    header += "\n"
                    track_file.write(header)
                    track_file.flush()

    def log(self, tracked_point: Point):
        with open(self.path_to_file, 'a') as track_file:
            track_file.write(f"{tracked_point.ts},{tracked_point.track_id},{tracked_point.class_id},{tracked_point.prob},{tracked_point.point.x},{tracked_point.point.y}")
            if self.three_dimensions:
                track_file.write(tracked_point.z)
            track_file.write("\n")
            track_file.flush()
