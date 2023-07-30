"""Creates csv for metadata of video files"""
import os
import glob
import subprocess

import pandas as pd

from paths import main_folder


def create_metadata(path: str):
    """Create a csv with metadata and compression status for videos in folder

    Args:
        path: str, path to folder
    """
    # create a list for each video with metadata
    metadata_list = []
    # iterates all videos in all channels
    videos = glob.glob(path + "/*.mp4")
    # sort by date
    videos.sort(key=os.path.getmtime)

    for video in videos:
        # getting the metadata for a video with subprocess running exiftool
        process = subprocess.Popen(
            ["exiftool", video],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        keys = []
        vals = []
        for o in process.stdout:
            # process key values for the metadata
            a = o.strip().split(":", 1)
            keys.append(a[0].strip())
            vals.append(a[1].strip())
            video_data = dict(zip(keys, vals))
            # add the video as a line to be written to file
        video_data["Compressed"] = False
        metadata_list.append(video_data)

    # create a dataframe from the metadata list
    new_df = pd.DataFrame.from_dict(metadata_list)

    # if there is already a data file, then update with new videos
    if os.path.exists(path + "/data.csv"):
        # Load the current data
        old_df = pd.read_csv(path + "/data.csv")
        # Take the difference between the fetched and the old data (based on filename)
        # This is to avoid changing when Compression and date is changed
        new_vids = new_df[~new_df[["File Name", "Directory"]].isin(old_df).any(axis=1)]
        complete_df = pd.concat((old_df, new_vids))
        # save it back as data.csv
        complete_df.to_csv(path + "/data.csv", index=False)
    else:
        new_df.to_csv(path + "/data.csv", index=False)


if __name__ == "__main__":
    # get a list of channels
    channels = glob.glob(main_folder + "Channels/*")
    # iterate channels
    for channel in channels:
        # print current folder
        print(channel)
        # create metadata for the folder
        create_metadata(channel)
