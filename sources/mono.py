import cv2 

class MonoRecorder():
    # Record images/frames from mono camera for further offline processing
    def __init__(self, video_path) -> None:
        self.video_path = video_path
        self.video = cv2.VideoCapture(video_path)

    def loop_frames(self):
        frame_nr = 0
        cap = self.video

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                yield frame, frame_nr

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            frame_nr +=1 