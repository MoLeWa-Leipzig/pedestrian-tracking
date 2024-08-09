from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-seg.pt')  # load an official model

# Predict with the model
results = model.track(source=0, show=True)  # Tracking with default tracker
