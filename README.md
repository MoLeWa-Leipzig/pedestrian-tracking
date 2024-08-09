# Pedestrian Detection and Tracking
This project allows the automatic detection and positional tracking of pedestrians.
Positions can be measured in pixel coordinates (using a monocular camera) or in centimeters and relative to a fixed world origin (using a stereo camera).

# Installation
`conda create -n tracking -y python=3.9`
`pip install ultralytics`

## Nvidia Jetson Nano 
Follow the Installtion Manual for the ZED SDK.
OpenCV is already installed.
`python3 -m pip install cython===0.29.34`  dont install cython3, numpy wont install
`python3 -m pip install numpy===0.19.2`
`pip3 install /usr/local/zed/pyzed-4.1-cp36-cp36m-linux_aarch64.whl`

Set `OPENBLAS_CORETYPE=ARMV8` in your .bashrc

Download calibration file under https://calib.stereolabs.com

If there problems with OpenCV, try `sudo apt install libcanberra-gtk-module libcanberra-gtk3-module -y` or `sudo apt install libgtk2.0-dev pkg-config`

# Usage
## Using the ZED 2 stereo camera
`python zed2.py -d 20 -x 10 -y 10`
x: camera position on x axes relative to the world origin (e.g. 10 if the camera is shifted 10 meters to the right)
y: camera position on y axes relative to the world origin (e.g. 10 if the camera is shifted 10 meters upwards/vertically)
d: maximum distance for depth estimation

If the `x` value is not changed, all position will be relative to the camera (regarding the x axes). This means positions to the left of the camera, will get a negative value. This might be annoying when these coordinates are plotted in an image. 