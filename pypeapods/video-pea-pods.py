from video_utils import *

import numpy as np
from glob import glob

# PEA
from PEA.PEA_uniformdimming import UniformDimming
from PEA.PEA_luminanceclipping import LuminanceClipping
from PEA.PEA_brightnessrolloff import BrightnessRolloff
from PEA.PEA_dichopticdimming import DichopticDimming
from PEA.PEA_colorfoveation import ColorFoveation
from PEA.PEA_whitepointshift import WhitepointShift

if __name__ == "__main__":
    video_input = "./data/videos/VIDEO.mp4"  # Replace with your video file path
    frames_dir = "./data/output/v_frames"         # Replace with your desired output directory
    #make sure to make this dir or it wont write
    video_output = "./data/output/videos/VIDEO_OUTPUT.avi"
    video_to_frames(video_input, frames_dir)







    frames_to_video(frames_dir, video_output)
    clear_dir(frames_dir)

