import os
import math
import copy
import codecs
import numpy as np
import srt
import subprocess
import pandas as pd
from utilis import mkdir, basename_without_ext


class GetSub:
    def download(self, video_file_path, language):
        # get the directory name from the video file path
        file_dir = os.path.dirname(video_file_path)
        temp_dir = "temp/"
        # create a directory named temp and file_dir
        mkdir(temp_dir)
        mkdir(file_dir)

        command1 = (
            "python OpenSubtitlesDownload.py --cli --auto {} --output {} --lang {}"
        )
        command1_list = command1.format(video_file_path, temp_dir, language).split(" ")
        subprocess.call(command1_list)

        original_name = basename_without_ext(video_file_path)
        srt_path = os.path.join(temp_dir, original_name + ".srt")

        # save original file as 'filename_unsynced.srt'
        out_path_unsynced = os.path.join(file_dir, original_name + "_unsynced.srt")
        command2 = "srt fixed-timeshift --input {} --output {} --seconds 0"
        command2_list = command2.format(srt_path, out_path_unsynced).split(" ")
        subprocess.call(command2_list)

        print("downloaded subs:", srt_path)

        self.align(video_file_path, srt_path, file_dir, original_name)
