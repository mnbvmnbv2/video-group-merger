"""Handles merging of video files"""
import glob
import json

import moviepy.editor

from paths import main_folder


def merge_videos(path: str) -> None:
    """Merge videos in folder and create a summary file"""

    # get mergerdata json file if it exists
    try:
        f = open(path + "\\\\mergerdata.json")
    except FileNotFoundError:
        return

    # load in json as dictionary
    mergersdata = json.load(f)

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
                video_path = path + "\\\\" + video

                # combine video and audio
                clip = moviepy.editor.VideoFileClip(video_path)
                audioclip = moviepy.editor.AudioFileClip(video_path)
                videoclip = clip.set_audio(audioclip)
                processed_videos.append(videoclip)

            # combine videos into final merged videofile
            final = moviepy.editor.concatenate_videoclips(processed_videos)
            # set name of file
            final.write_videofile(path + "/" + group["name"] + ".mp4")

            # set json group as finished merging
            group["merged"] = True
            # update json-file
            with open(f"{folder}\\\\mergerdata.json", "w") as outfile:
                json.dump(mergersdata, outfile)


if __name__ == "__main__":
    # get channels
    channels = glob.glob(main_folder + "Channels/*")

    for channel in channels:
        # print current channel
        print(channel)
        # merge videos in channel
        merge_videos(channel)
