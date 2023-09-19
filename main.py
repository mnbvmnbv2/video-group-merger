import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import typing
from collections import namedtuple

ChapterInfo = namedtuple("ChapterInfo", ["name", "path", "time_start", "time_end", "duration"])


def get_duration(filename: str) -> datetime.timedelta:
    """Get duration of video. From: https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python

    Args:
        filename (str): Path to video

    Returns:
        datetime.timedelta: Duration of video
    """
    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"', shell=True
    ).decode()
    fields = json.loads(result)["streams"][0]

    duration = float(fields["duration"])
    return datetime.timedelta(seconds=duration)


def write_chapters(filename: str, chapters: typing.List[ChapterInfo]) -> None:
    """Write chapters to a text file

    Args:
        filename (str): Path to file
        chapters (typing.List[ChapterInfo]): List of chapters on format [(name, path, time_start, time_end, duration), ...]
    """
    with open(filename, "w") as f:
        for i, c in enumerate(chapters):
            timestamp = f"{int(c.time_start.seconds/3600):02}:{int(c.time_start.seconds/60)%60:02}:{int(c.time_start.seconds)%60:02}"
            f.write(f"{timestamp} - {c.name}\n")


def save_flist(videos: typing.List[str]) -> None:
    """Transforms a list of videos into a text file of videos on FFMPEG format

    Args:
        videos (typing.List[str]): List of videos on format [video1, video2, ...]
    """
    f_data = "file '" + "'\nfile '".join(videos) + "'"

    f_list = "temp/list.txt"
    with open(f_list, "w", encoding="UTF-8") as f:
        f.write(f_data)


def merge_videos(
    merged_filename: str, chapters: typing.List[ChapterInfo], verbose: bool = False, gpu: bool = True
) -> None:
    """Merge videos from chapters list to merged_filename.

    Process:
        1. Remove and create new temp_videos folder
        2. Iterate over group (videos)
            2.1. Set output video path
            2.2. Process video
            2.3. Append video to processed_videos
        3. Combine videos into final merged videofile

    Args:
        merged_filename (str): Path to merged video
        chapters (typing.List[ChapterInfo]): List of chapters on format [(name, path, time_start, time_end, duration), ...]
        verbose (bool, optional): Verbose ffmpeg. Defaults to False.
        gpu (bool, optional): Use GPU for encoding. Defaults to True.
    """
    # TODO get merged status (not set in mergerdata)

    encoder = "h264_nvenc" if gpu else "libx264"

    # remove and create new temp_videos folder
    shutil.rmtree("temp", ignore_errors=True)
    os.mkdir("temp")
    # setup list of videos for merge
    processed_videos = []

    # iterate over group (videos)
    for idx, c in enumerate(chapters):
        # set output video path
        out_video_path = f"temp\{c.name[:-4]}.mp4"

        print(f"Processing '{c.name}', {idx+1}/{len(chapters)}, {c.time_start} - {c.time_end}, {c.duration}")

        call = f'ffmpeg -y -i "{c.path}" -max_interleave_delta 0 -vf "scale=-1:720" -c:v {encoder} -b:v 250k -r 15 "{out_video_path}"'
        if not verbose:
            call += " -loglevel fatal"
        os.system(call)

        processed_videos.append(out_video_path[5:])
        # TODO intermediate saving to avoid duplicate processing if error occurs

    # combine videos into final merged videofile
    save_flist(processed_videos)

    # only support the same video_format, copy and not recode.
    call = f'ffmpeg -f concat -safe 0 -i temp\\list.txt -c copy "{merged_filename}" -y'
    os.system(call)

    # TODO update that the group has been merged


def extract_numbers(string: str) -> tuple[int, str]:
    """Extract numbers from string. Used for sorting.

    Args:
        string (str): String

    Returns:
        tuple: Tuple of integers and string
    """
    # Extract all numbers
    numbers = re.findall(r"\d+", string)
    # Convert to integers, and append the original string for textual comparison
    return tuple(map(int, numbers)) + (string,)


def main(root_dir: str, time_limit_hours: int = 12, verbose_ffmpeg: bool = False, gpu: bool = True):
    """Main function.

    For each folder in root_dir, merge all videos in the folder to a single video. The merged videos will be saved in the output folder.

    Args:
        root_dir (str): Path to root directory
        time_limit_hours (int, optional): Time limit for each merged video in hours. Defaults to 12.
        verbose_ffmpeg (bool, optional): Verbose ffmpeg. Defaults to False.
        gpu (bool, optional): Use GPU for encoding. Defaults to True.
    """
    # Create output directory
    os.makedirs("output", exist_ok=True)

    time_limit = datetime.timedelta(hours=time_limit_hours)

    # Walk through all files in the directory that contains the videos
    folders = glob.glob(root_dir + "/*")

    for folder in folders:
        folder_name = folder.split("\\")[-1]
        print(f"Folder: {folder_name}")
        video_paths = glob.glob(folder + "/*")
        files = [f for f in video_paths if f.endswith(".mp4")]
        sorted_files = sorted(files, key=extract_numbers)
        merged_videos = 1
        chapters = []
        time_counter = datetime.timedelta()

        for filepath in sorted_files:
            filename = filepath.split("\\")[-1]
            duration = get_duration(filepath)

            print(f"Name: {filename} Duration: {duration}")

            # check if total exceeds limit
            if time_counter + duration > time_limit:
                # merge videos
                print(f"Chapters: {chapters}")
                merge_videos(
                    f"output\\\\{folder_name}-{merged_videos}.mp4", chapters, verbose=verbose_ffmpeg, gpu=gpu
                )

                # write chapters
                write_chapters(f"output\\\\{folder_name}-{merged_videos}.txt", chapters)

                # reset merge_videos and chapters
                chapters = []

                # reset time_counter
                time_counter = datetime.timedelta()

                # increment merged_videos counter
                merged_videos += 1
            else:
                chapters.append(
                    ChapterInfo(filename, filepath, time_counter, time_counter + duration, duration)
                )

                # add time to counter
                time_counter += duration

        # merge last group of videos
        print(f"Chapters: {chapters}")
        merge_videos(
            f"output\\\\{folder_name}-{merged_videos}.mp4", chapters, verbose=verbose_ffmpeg, gpu=gpu
        )

        # write chapters
        write_chapters(f"output\\\\{folder_name}-{merged_videos}.txt", chapters)


if __name__ == "__main__":
    main(
        "C:\Channels",
        time_limit_hours=12,
        verbose_ffmpeg=True,
        gpu=True,
    )
