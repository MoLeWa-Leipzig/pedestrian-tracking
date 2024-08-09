import argparse
from executor.stereo.zed2 import Zed2Executor

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', help="max depth", type=int, default=5)
	parser.add_argument('-x', help="camera position on x axes relative to world origin", type=int, default=5)
	parser.add_argument('-y', help="camera position on y axes relative to world origin", type=int, default=5)
	args = vars(parser.parse_args())
	return args 

if __name__ == "__main__":
    args = parse_args()
    max_depth = args['d']
    cam_pos_x = args['x']
    cam_pos_y = args['y']
    e = Zed2Executor(max_depth, cam_pos_x, cam_pos_y)
    e.run()