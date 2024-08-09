from executor.mono.online import OnlineMonoExecutor

# Postprocessing
def add_position_relative_to_line():
    # 2.1 Optional: loop through csv
    # add column indicating position realtive to line 
    # end result: 
    pass 

def create_bird_eye_paths():
    # 2.2 loop thorugh csv and change perspective
    # transform position to bird eye position and save as column
    # end result -> tracked positions
    pass

def detect():
    # 1. Run detection and save to file
    pass

if __name__ == "__main__":
    e = OnlineMonoExecutor("log.log", False)
    e.run()