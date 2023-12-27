import argparse
import datetime
import json
import re
import shutil
import subprocess
import typing
from collections import namedtuple
from pathlib import Path

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
    with open(filename, "w", encoding="UTF-8") as f:
        for i, c in enumerate(chapters):
            timestamp = f"{int(c.time_start.seconds/3600):02}:{int(c.time_start.seconds/60)%60:02}:{int(c.time_start.seconds)%60:02}"
            f.write(f"{timestamp} - {c.name}\n")


def save_flist(video_paths: typing.List[Path]) -> None:
    """Transforms a list of video_paths into a text file of videos on FFMPEG format

    Args:
        video_paths (typing.List[Path]): List of video_paths on format [Path(video1), Path(video2), ...]
    """
    videos = [p.name for p in video_paths]
    f_data = "file '" + "'\nfile '".join(videos) + "'"

    f_list = "temp/list.txt"
    with open(f_list, "w", encoding="UTF-8") as f:
        f.write(f_data)


def run_command(command: str, verbose: bool) -> None:
    """Helper function to run a shell command."""
    command = command if verbose else command + " -loglevel fatal"
    try:
        if not verbose:
            subprocess.run(command, shell=True, stderr=subprocess.PIPE, check=True)
        else:
            subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as error:
        print(f"Command failed: {error.cmd}")
        print(error.stderr.decode())
        raise


def merge_videos(
    output_folder: str,
    merged_filename: str,
    chapters: typing.List[ChapterInfo],
    verbose: bool = False,
    gpu: bool = True,
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
        output_folder (str): Path to output folder
        merged_filename (str): Path to merged video
        chapters (typing.List[ChapterInfo]): List of chapters on format [(name, path, time_start, time_end, duration), ...]
        verbose (bool, optional): Verbose ffmpeg. Defaults to False.
        gpu (bool, optional): Use GPU for encoding. Defaults to True.
    """
    # check if videos are already merged
    merge_check = Path(output_folder) / "merged.txt"
    if merge_check.exists():
        merged_videos = merge_check.read_text(encoding="UTF-8").splitlines()
        if merged_filename in merged_videos:
            print(f"Skipping '{merged_filename}', already merged")
            return

    encoder = "h264_nvenc" if gpu else "libx264"

    temp_path = Path("temp")
    processed_file_path = temp_path / "processed_videos.txt"
    processed = set()
    if processed_file_path.exists():
        with processed_file_path.open(encoding="UTF-8") as f:
            processed = set(f.read().splitlines())

    # check if any videos have been processed
    video_paths = [c.path for c in chapters]
    if not any(p in processed for p in video_paths):
        # remove and create new temp_videos folder if no videos have been processed
        if temp_path.exists():
            shutil.rmtree(temp_path)
        temp_path.mkdir()

    # setup list of videos for merge
    processed_videos = []

    # iterate over group (videos)
    for idx, c in enumerate(chapters):
        # set output video path
        out_video_path = temp_path / f"{c.name[:-4]}.mp4"

        # check if video has been processed
        if c.path in processed:
            print(f"Skipping '{c.name}', {idx+1}/{len(chapters)} {c.time_start}-{c.time_end} {c.duration}")
        else:
            print(f"Processing '{c.name}', {idx+1}/{len(chapters)} {c.time_start}-{c.time_end} {c.duration}")

            # process video
            run_command(
                f'ffmpeg -y -i "{c.path}" -max_interleave_delta 0 -c:v {encoder} -b:v 250k -r 15 "{out_video_path}"',  # -vf "scale=-1:720"
                verbose,
            )
            with processed_file_path.open("a", encoding="UTF-8") as f:
                f.write(f"{c.path}\n")

        processed_videos.append(out_video_path)

    # combine videos into final merged videofile
    save_flist(processed_videos)

    # only support the same video_format, copy and not recode.
    run_command(f'ffmpeg -f concat -safe 0 -i temp\\list.txt -c copy "{merged_filename}" -y', verbose)

    # update that the group has been merged
    with merge_check.open("a", encoding="UTF-8") as f:
        f.write(f"{merged_filename}\n")


def extract_numbers(string: str, fill_value: int = 0, max_length: int = 5) -> tuple[int, str]:
    """Extract numbers from string. Used for sorting.

    Args:
        string (str): String
        fill_value (int, optional): Fill value. Defaults to 0.
        max_length (int, optional): Max length of extracted numbers. Defaults to 5.

    Returns:
        tuple: Tuple of integers and string
    """
    # Extract all numbers and convert them to integers
    numbers = [int(num) for num in re.findall(r"\d+", string)]
    # If the number of extracted numbers is less than max_length, fill in the rest
    numbers += [fill_value] * (max_length - len(numbers))
    # Convert to integers, and append the original string for textual comparison
    return tuple(map(int, numbers)) + (string,)


def process_folder(
    output_folder: str, folder: Path, time_limit: datetime.timedelta, verbose: bool, gpu: bool
) -> None:
    """Process a single folder and merge its videos."""
    folder_name = folder.name
    print(f"Folder: {folder_name}")

    print([file for file in folder.iterdir() if file.suffix == ".mp4"])

    files = sorted(
        [file for file in folder.iterdir() if file.suffix == ".mp4"], key=lambda f: extract_numbers(f.name)
    )

    merged_videos = 1
    chapters = []
    time_counter = datetime.timedelta()

    for filepath in files:
        filename = filepath.name
        duration = get_duration(str(filepath))

        print(f"Name: {filename} Duration: {duration}")

        # If the total duration exceeds the limit, merge the videos
        if time_counter + duration > time_limit:
            output_name = f"{output_folder}/{folder_name}-{merged_videos}"
            merge_and_write_chapters(output_folder, output_name, chapters, verbose, gpu)

            # Reset chapters and time_counter
            chapters.clear()
            time_counter = datetime.timedelta()
            merged_videos += 1
        else:
            chapters.append(
                ChapterInfo(filename, str(filepath), time_counter, time_counter + duration, duration)
            )
            time_counter += duration

    # Merge remaining videos
    if chapters:
        output_name = f"{output_folder}/{folder_name}-{merged_videos}"
        merge_and_write_chapters(output_folder, output_name, chapters, verbose, gpu)


def merge_and_write_chapters(
    output_folder: str, output_name: str, chapters: typing.List[ChapterInfo], verbose: bool, gpu: bool
) -> None:
    """Helper function to merge videos and write chapters."""
    merge_videos(output_folder, f"{output_name}.mp4", chapters, verbose=verbose, gpu=gpu)
    write_chapters(f"{output_name}.txt", chapters)


def main(
    root_dir: str,
    output_folder: str,
    time_limit_hours: int = 12,
    verbose_ffmpeg: bool = False,
    gpu: bool = True,
):
    """Main function.

    For each folder in root_dir, merge all videos in the folder to a single video. The merged videos will be saved in the output folder.

    Args:
        root_dir (str): Path to root directory
        output_folder (str): Path to output folder
        time_limit_hours (int, optional): Time limit for each merged video in hours. Defaults to 12.
        verbose_ffmpeg (bool, optional): Verbose ffmpeg. Defaults to False.
        gpu (bool, optional): Use GPU for encoding. Defaults to True.
    """
    # Create output directory
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)

    time_limit = datetime.timedelta(hours=time_limit_hours)

    # Process each folder
    for folder in Path(root_dir).iterdir():
        if folder.is_dir():
            process_folder(output_folder, folder, time_limit, verbose_ffmpeg, gpu)


# Add command-line argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Merge videos in folders.")
    parser.add_argument("root_dir", type=str, help="Path to root directory containing videos.")
    parser.add_argument("output_folder", type=str, help="Path to output folder.")
    parser.add_argument(
        "--time_limit_hours", type=int, default=12, help="Time limit for each merged video in hours."
    )
    parser.add_argument("--verbose_ffmpeg", action="store_true", help="Enable verbose output for ffmpeg.")
    parser.add_argument("--gpu", action="store_true", help="Use GPU for video encoding.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    main(
        root_dir=args.root_dir,
        output_folder=args.output_folder,
        time_limit_hours=args.time_limit_hours,
        verbose_ffmpeg=args.verbose_ffmpeg,
        gpu=args.gpu,
    )
