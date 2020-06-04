import time

def wait(wait_time):
    time_end = time.time() + wait_time  
    while time.time() < time_end:
        pass