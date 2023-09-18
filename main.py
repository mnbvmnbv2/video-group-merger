import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import typing


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


def write_chapters(filename: str, chapters: list) -> None:
    """Write chapters to a text file

    Args:
        filename (str): Path to file
        chapters (list): List of chapters on format [(name, path, duration), ...]
    """
    with open(filename, "w") as f:
        for i, (name, path, duration) in enumerate(chapters):
            timestamp = f"{int(duration.seconds/3600):02}:{int(duration.seconds/60)%60:02}:{int(duration.seconds)%60:02}"
            f.write(f"{timestamp} - {name}\n")


def save_flist(videos: typing.List[str]) -> None:
    """Transforms a list of videos into a text file of videos on FFMPEG format

    Args:
        videos (typing.List[str]): List of videos on format [video1, video2, ...]
    """
    f_data = "file '" + "'\nfile '".join(videos) + "'"

    f_list = "temp/list.txt"
    with open(f_list, "w", encoding="UTF-8") as f:
        f.write(f_data)


def merge_videos(merged_filename: str, chapters: list, verbose: bool = False) -> None:
    """Merge videos from chapters list to merged_filename

    Args:
        merged_filename (str): Path to merged video
        chapters (list): List of chapters on format [(name, path, duration), ...]
        verbose (bool, optional): Verbose ffmpeg. Defaults to False.
    """
    # TODO get merged status (not set in mergerdata)

    # remove and create new temp_videos folder
    shutil.rmtree("temp", ignore_errors=True)
    os.mkdir("temp")
    # setup list of videos for merge
    processed_videos = []

    # iterate over group (videos)
    for idx, (filename, filepath, duration) in enumerate(chapters):
        # set output video path
        out_video_path = f"temp\{filename[:-4]}.mp4"

        print(f"Processing '{filename}', {idx+1}/{len(chapters)}, {duration}")

        call = f'ffmpeg -y -i "{filepath}" -max_interleave_delta 0 -vf "setpts=1.00*PTS, fps=24" -c:v h264_nvenc -r 15 "{out_video_path}"'
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


def main(
    root_dir: str, time_limit: datetime.timedelta = datetime.timedelta(hours=12), verbose_ffmpeg: bool = False
):
    """Main function.

    For each folder in root_dir, merge all videos in the folder to a single video. The merged videos will be saved in the output folder.

    Args:
        root_dir (str): Path to root directory
        time_limit (datetime.timedelta, optional): Time limit for each merged video. Defaults to datetime.timedelta(hours=12).
        verbose_ffmpeg (bool, optional): Verbose ffmpeg. Defaults to False.
    """
    # Create output directory
    os.makedirs("output", exist_ok=True)

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
                merge_videos(f"output\\\\{folder_name}-{merged_videos}.mp4", chapters, verbose=verbose_ffmpeg)

                # write chapters
                write_chapters(f"output\\\\{folder_name}-{merged_videos}.txt", chapters)

                # reset merge_videos and chapters
                chapters = []

                # reset time_counter
                time_counter = datetime.timedelta()

                # increment merged_videos counter
                merged_videos += 1
            else:
                chapters.append((filename, filepath, time_counter))

                # add time to counter
                time_counter += duration

        # merge last group of videos
        merged_videos += 1
        print(f"Chapters: {chapters}")
        merge_videos(f"output\\\\{folder_name}-{merged_videos}.mp4", chapters, verbose=verbose_ffmpeg)

        # write chapters
        write_chapters(f"output\\\\{folder_name}-{merged_videos}.txt", chapters)


if __name__ == "__main__":
    main("C:\Channels")
