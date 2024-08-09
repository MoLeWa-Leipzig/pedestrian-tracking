from executor.mono.executor import Executor

class OfflineMonoExecutor(Executor):
    def __init__(self, video_path, log_path, use_bird_view_transformation=False):
        super().__init__(video_path, log_path, use_bird_view_transformation)
        # ../data/video_1.mp4