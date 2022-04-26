import os
import math
import copy
import codecs
import numpy as np
import srt
import subprocess
import pandas as pd
from progress.bar import Bar
from utilis import mkdir, basename_without_ext


class GetSub:
    def binary_array_from_srt(self, srt_path):
        common_encodings = ["utf-8", "utf-16", "cp1252"]

        for encoding in common_encodings:
            try:
                srt_file = codecs.open(srt_path, "r", encoding=encoding)
                srt_string = srt_file.read()
                srt_file.close()

                subs = list(srt.parse(srt_string))

                break
            except BaseException as error:
                print("An exception occurred: {}".format(error))

        start_end_pairs = [
            (self.timedelta_to_frame(sub.start), self.timedelta_to_frame(sub.end))
            for sub in subs
        ]

        # convert seconds and microseconds to milliseconds
        first_sub_frame = start_end_pairs[0][0]
        last_sub_frame = start_end_pairs[-1][1]

        bin_array = np.zeros(last_sub_frame)

        with Bar("Creating Binary Array from SRT", max=len(start_end_pairs)) as bar:
            for start_frame, end_frame in start_end_pairs:
                for i in range(start_frame, end_frame):
                    bin_array[i] = 1
                bar.next()

        # TODO
        five_second_delay = int(5 * 1000 / self.vad.frame_duration_ms)

        # set max delay to 5% of video
        max_delay = max(five_second_delay, int(len(bin_array) * 0.05))

        return bin_array, -first_sub_frame, max_delay

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

    def align(self, video_file_path, srt_path, file_dir, original_name):
        bin_arr1 = list(self.vad.detect(video_file_path))
        bin_arr2, delay_range_start, delay_range_end = self.binary_array_from_srt(
            srt_path
        )
