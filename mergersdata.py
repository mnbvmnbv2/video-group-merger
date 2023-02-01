"""File for creating metadata for merging videos"""
import glob
import json
import datetime

import pandas as pd

from paths import main_folder


def create_mergerdata(folder: str, channel: str) -> None:
    """Create mergersdata json file in the channel folder

    Args:
        folder (str): Path to channel folder
        channel (str): Channel in channel folder
    """

    # read in the data.csv
    try:
        df = pd.read_csv(f"{folder}\\\\data.csv")
    except pd.errors.EmptyDataError:  # if empty csv
        return

    # set time limit and time counter for limiting merge video length
    time_limit = datetime.timedelta(hours=10)
    time_counter = datetime.timedelta()

    # groupings of videos to be merged
    vid_groups = []
    group_counter = 1

    # for individual group
    merge_videos = []
    chapters = []

    for i in range(len(df)):
        # get hours, mins and secs
        try:
            split_time = df.iloc[i]["Duration"].split(":")
        except AttributeError:  # if Duration value is undefined etc.
            continue

        # set as timedelta
        try:
            add_time = datetime.timedelta(
                hours=int(split_time[0]),
                minutes=int(split_time[1]),
                seconds=int(split_time[2]),
            )
        except ValueError:  # cannot handle time in seconds (e.g. 22.99 s), video length must be 1 min+
            continue

        # check if total exceeds limit
        if add_time + time_counter > time_limit:
            # add info about video_group
            merge_vid = {
                "name": f"{channel}-{group_counter}",
                "videos": merge_videos,
                "chapters": chapters,
            }
            vid_groups.append(merge_vid)

            # reset merge_videos and chapters
            merge_videos = []
            chapters = []

            # reset time_counter
            time_counter = datetime.timedelta()

            # increase group counter
            group_counter += 1

        # add current video to group
        merge_videos.append(df.iloc[i]["File Name"])
        chapters.append(
            f"{int(time_counter.seconds/3600):02}:{int(time_counter.seconds/60)%60:02}:{int(time_counter.seconds)%60:02}"
        )

        # add time to counter
        time_counter += add_time

    # add final group
    merge_vid = {
        "name": f"{channel}-{group_counter}",
        "videos": merge_videos,
        "chapters": chapters,
    }
    vid_groups.append(merge_vid)

    with open(f"{folder}\\\\mergerdata.json", "w") as outfile:
        json.dump(vid_groups, outfile)


if __name__ == "__main__":
    # get a list of channels
    channels = glob.glob(main_folder + "Channels/*")
    print(channels)
    # iterate channels
    for channel in channels:
        # print current folder
        channel_name = channel.split("\\")[-1]
        print(channel_name)
        # create metadata for the folder
        create_mergerdata(channel, channel_name)
