import cv2 
import numpy as np 
from dataclasses import dataclass

@dataclass
class BirdEyeConfig():
    height: float
    width: float
    top_left: float
    top_right: float 
    bottom_left: float
    bottom_right: float

def calc_projection_matrix(config: BirdEyeConfig):
    pts1 = np.float32([config.top_left, config.bottom_left, config.top_right, config.bottom_right])
    pts2 = np.float32([[0,0], [0, config.height], [config.width, 0], [config.width, config.height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return matrix


