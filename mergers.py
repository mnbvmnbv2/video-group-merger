"""Handles merging of video files"""
import os
import glob
import json

from paths import main_folder


def save_flist(videos: list) -> None:
    """Transforms a list of videos into a text file of videos on FFMPEG format

    Args:
        videos (list): List of videos
    """
    f_data = "file " + "\nfile ".join(videos)

    f_list = "list.txt"
    with open(f_list, "w", encoding="UTF-8") as f:
        f.write(f_data)
    return f_list


def merge_videos(path: str) -> None:
    """Merge videos from descriptions by mergersdata.json file

    Args:
        path (str): path to channel folder
    """

    # get mergerdata json file if it exists
    try:
        f = open(path + "\\\\mergerdata.json")
    except FileNotFoundError:
        print(f"Did not find mergerdata in {path}")
        return

    # load in json as dictionary
    mergersdata = json.load(f)

    # edit path to FFMPEG format
    FFM_path = path.replace("\\", "\\\\")
    FFM_path = FFM_path.replace(" ", "\\ ")

    # iterate over group (videos)
    for idx, group in enumerate(mergersdata):
        # print name and which group out of total number of group is being processed
        print(f"{group['name']}, {idx + 1}/{len(mergersdata)}")

        # get merged status (not set in mergerdata)
        try:
            merged = group["merged"]
        except KeyError:
            merged = False  # if the key does not exist it has not been merged yet
        # if the group is merged then continue
        if not merged:
            # get videos in group
            videos = group["videos"]

            # setup list of videos for moviepy to merge
            processed_videos = []
            # iterate videos
            for video in videos:
                print(video)
                # get video path
                video_path = FFM_path + "\\\\" + video.replace(" ", "\\ ")

                processed_videos.append(video_path)

            # combine videos into final merged videofile
            save_flist(processed_videos)

            FFM_out = group["name"] + ".mp4"

            # only supporte the same video_format, copy and not recode.
            call = (
                f'ffmpeg -f concat -safe 0 -i list.txt -c copy "{path}\\\\{FFM_out}" -y'
            )

            os.system(call)

            # set json group as finished merging
            group["merged"] = True
            # update json-file
            with open(f"{path}\\\\mergerdata.json", "w") as outfile:
                json.dump(mergersdata, outfile)


if __name__ == "__main__":
    # get channels
    channels = glob.glob(main_folder + "Channels/*")

    for channel in channels:
        # print current channel
        print(channel)
        # merge videos in channel
        merge_videos(channel)
