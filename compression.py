"""Handles compression of video files"""
import time
import glob
import shutil
import subprocess

import pandas as pd
from pandas.errors import EmptyDataError

from paths import main_folder


def compress_video(filepath: str, crf=34) -> None:
    """Compresses video with predefined settings

    Args:
        filepath: str, string to videofile
    """

    # compression with ffmpeg to a separate temp video file
    # (temp file to avoid corrupting main if process is cancelled)
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            filepath,
            "-vcodec",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            str(crf),
            filepath + "_compressing_.mp4",
        ],
        text=True,
        input="y",
    )
    # overwrite the main file with the temp file
    shutil.move(filepath + "_compressing_.mp4", filepath)


def compress_in_folder(path: str) -> None:
    """Compress videos in folder based on dataframe in the folder

    Args:
        path: path of csv file and videos
    """
    # get df in channel if not empty
    try:
        df = pd.read_csv(path + "/data.csv")
    except EmptyDataError:
        # if emtpy return out of function
        print("Empty CSV")
        return

    # iterate the rows
    for i in range(df.shape[0]):
        # Check every video in dataframe if it is compressed
        if not df.iloc[i]["Compressed"]:
            # runs the compression of the video
            try:
                compress_video(df.iloc[i]["Directory"] + "/" + df.iloc[i]["File Name"])
            except:
                print("Failed to compress")

            # set compression to true
            df.at[i, "Compressed"] = True

            # Gets the current time
            mod_time = time.strftime("%Y:%m:%d %H:%M:%S%z", time.gmtime())
            # add : to the local time difference to get correct format
            mod_time = mod_time[:-2] + ":" + mod_time[-2:]
            # update time in dataframe
            df.at[i, "File Modification Date/Time"] = mod_time
            # update the csv after each compression
            df.to_csv(path + "/data.csv", index=False)


if __name__ == "__main__":
    # get a list of channels
    channels = glob.glob(main_folder + "Channels/*")
    # iterate channels
    for channel in channels:
        # output current channel
        print(channel)
        # compress videos in folder
        compress_in_folder(channel)
