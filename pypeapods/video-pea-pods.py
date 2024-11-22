from video_utils import *
import utils
import statistics

import os
from os.path import basename
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
    globalLC = GlobalLC(measurements_pth="data/mqp_display/mqp_BLU.csv", name="Global Dimming LC")
    localLC = LocalLC(measurements_pth="data/mqp_display/mqp_BLU.csv", name="Local Dimming LC")
    oled = OLED(name="OLED")
    pods = [globalLC, localLC, oled]

    uniformdimming = UniformDimming(color="limegreen", name="Uniform_Dimming")
    brightnessrolloff = BrightnessRolloff(color="gold", name="Brightness_Rolloff")
    dichopticdimming = DichopticDimming(color="violet", name="Dichoptic_Dimming")
    peas = [uniformdimming, brightnessrolloff, dichopticdimming]


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


    video_input = "./data/videos"  # Replace with your video file path
    frames_dir = "./data/output/v_frames"  # Replace with your desired output directory
    video_output = "./data/output/videos"

    pea_pod_out = "./output/frames"
    os.makedirs(frames_dir, exist_ok=True)

    vid_pths = glob(video_input + "/*.mp4")  # list of video paths
    alpha = 0.5
    vid_num = 1

    for vid in vid_pths:
        savings_dict = {}
        base_name, _ = os.path.splitext(basename(vid))
        # compute images using brightness rolloff
        video_to_frames(vid, frames_dir)
        img_pths = glob(frames_dir + "/*.png")  # list of image paths
        for pea in peas:
            frame_count = 0
            for pod in pods:
                savings_dict[pod.name] = []
            vid_name = f"/{base_name}_{pea.name}_Alpha_{alpha}.mp4"
            for pth in img_pths:
                image = utils.srgb2rgb(iio.imread(pth) / 255)
                image_modulated = pea.evaluate(image, f"frame_{frame_count:04d}", alpha, **display_params)
                if pea.name == brightnessrolloff.name:
                    for pod in pods:
                        # compute dynamic power consumption for modulated and reference image
                        _, power_reference = pod.evaluate(image)
                        _, power_modulated = pod.evaluate(image_modulated)
                        # compute savings
                        savings = (1 - power_modulated / power_reference) * 100
                        savings_dict[pod.name].append(savings)
                frame_count += 1

            if pea.name == brightnessrolloff.name:
                for pod in pods:
                    print(f"{vid_name} has average->{statistics.mean(savings_dict[pod.name]):.2f}% savings on {pod.name}")

            frames_to_video(pea_pod_out, video_output + vid_name)
            clear_dir(pea_pod_out)
        clear_dir(frames_dir)
        vid_num += 1


