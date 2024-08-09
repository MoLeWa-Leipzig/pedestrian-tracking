from executor.mono.executor import Executor

class OnlineMonoExecutor(Executor):
    # Use mono camera to retrieve image in real time
    
    def __init__(self, log_path, use_bird_view_transformation=False):
        super().__init__(0, log_path, use_bird_view_transformation)

    
