from video_utils import *
import utils

import os
import imageio.v3 as iio

import numpy as np
from glob import glob

# PEA
from PEA.PEA_uniformdimming import UniformDimming
from PEA.PEA_brightnessrolloff import BrightnessRolloff
from PEA.PEA_dichopticdimming import DichopticDimming

# PODs
from PODs.PODs_globalLC import GlobalLC
from PODs.PODs_localLC import LocalLC
from PODs.PODs_oled import OLED

from peapods import PEAPODs

if __name__ == "__main__":

    # define PEA and POD
    #globalLC = GlobalLC(measurements_pth="data/mqp_display/mqp_BLU.csv", name="Global Dimming LC")
    uniformdimming = UniformDimming(color="limegreen", name="Uniform Dimming")
    brightnessrolloff = BrightnessRolloff(color="gold", name="Brightness Rolloff")
    dichopticdimming = DichopticDimming(color="violet", name="Dichoptic Dimming")


    # compute eccentricity map
    H, W = 1080, 1920
    xv, yv = np.meshgrid(np.linspace(0, W, W), np.linspace(0, H, H))
    dist = ((xv - W / 2) ** 2 + (yv - H / 2) ** 2) ** .5

    # define display parameters
    display_params = {
        "ppd": 22,
        "foveal_region": 10,
        "FOV": 110,
        "distance": dist,
        "save_frames": True,
        "resolution": [H, W]
    }


    video_input = "./data/videos/VIDEO.mp4"  # Replace with your video file path
    frames_dir = "./data/output/v_frames"  # Replace with your desired output directory
    video_output = "./data/output/videos"

    pea_pod_out = "./output/frames"
    os.makedirs(frames_dir, exist_ok=True)


    video_to_frames(video_input, frames_dir)

    img_pths = glob(frames_dir + "/*.png")  # list of image paths
    alpha = 0.5
    frame_count = 0

    """
    #compute images using uniform dimming
    for pth in img_pths:
        image = utils.srgb2rgb(iio.imread(pth) / 255)
        image_modulated = uniformdimming.evaluate(image, f"frame_{frame_count:04d}.png", alpha, **display_params)
        frame_count += 1
    print(".")

    frames_to_video(pea_pod_out, video_output + f"/uniform_dimming_alpha_{alpha}.avi")
    clear_dir(pea_pod_out)
    """



    # compute images using brightness rolloff
    for pth in img_pths:
        image = utils.srgb2rgb(iio.imread(pth) / 255)
        image_modulated = brightnessrolloff.evaluate(image, f"frame_{frame_count:04d}.png", alpha, **display_params)
        frame_count += 1
    print(".")

    frames_to_video(pea_pod_out, video_output + f"/brightness_rolloff_alpha_{alpha}.avi")
    clear_dir(pea_pod_out)


    """
    # compute images using Dichoptic Dimming
    for pth in img_pths:
        image = utils.srgb2rgb(iio.imread(pth) / 255)
        image_modulated = dichopticdimming.evaluate(image, f"frame_{frame_count:04d}.png", alpha, **display_params)
        frame_count += 1
    print(".")

    frames_to_video(pea_pod_out, video_output + f"/dichoptic_dimming_alpha_{alpha}.avi")
    """

    clear_dir(frames_dir)
    clear_dir(pea_pod_out)


