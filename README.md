# video-group-merger

Youtube uploading script is moved to [youtube-uploader](https://github.com/mnbvmnbv2/youtube-uploader), but 
it is not that useful.

---

This repo now only contains one script for merging videos and writing metadata.

This project is primarily for learning purposes and is should not be viewed as robust or efficient.

The aim is to merge videos before uploading to youtube as youtube has restrictions on number of daily uploads,
but little restriction on size. The idea is therefore to merge videos up to the limit of 12 hours and use
video chapters to separate videos such that one can upload more videos in a shorter amount of time.
The main script is designed for groups of many smaller videos (e.g. lectures) to be combined and numerated.

Use `main.py` to merge the videos and manually upload them to youtube and then paste the chapter data. 

This repo has been experimental for a long time and there are potentially multiple places where the 
documentation is outdated.

## Warning
- Backup your files before using, videos might be corrupted or compressed too much.

## Dependencies
- You need to install `FFMPEG` (+`FFMPROBE`) separately.

## Main script
- This uses ffmprobe to find video sizes
- Compresses and merges videos into chunks of up to 12 hours.

- You need to specify input folder and output folder
- The input folder should be divided by folders per "related group" for example courses if you use it for
lecture videos. The combined length inside a folder can exceed 12 hours. If one folder named `example` has
14 videos that are a combined length of 14 hours, then the output videos will be named `example-1.mp4` and 
`example-2.mp4`.
- It is generated a textfile alongside the video with timestamps for the original videos. This can be pasted
as the youtube description of the merged video to make it easy to find the orignial videos.

- Input folder should be on format
```
- Input_folder
    - Group1
        - Video1.mp4
        - Video2.mp4
        - ...
    - Group2
        - ...
```
- The output should be the following:
```
- Output_folder
    - Group1-1.mp4
    - Group1-1.txt
    - Group1-2-mp4
    - Group1-2.txt
    - Group2-1.mp4
    - Group2-1.txt
    - ...
```
- I have added support for merging (encoding/decoding) with nvidia GPUs which should be faster.
- If the script is stopped mid-way, there are some temp_files and logs saved so that should be able to 
continue from where it was stopped, however it might not be "fail-safe".

### Known things to watch out for
- As I have encountered a lot of errors I have put in some error handling, but there are probably plenty more
edge cases that could cause errors. Some things to consider are the following:
- The merged videos tries to sort the order by numbers appearing in the name however if there are more than
5 numbers appearing with separation you need to change the `extract_numbers` function argument `max_length`.
- If videos are of different aspect ratio, or fps there might be trouble. In the latest version of the script
this should be handeled to some degree, but it might not be fail-safe.
- Be mindful of video names, the script should handle spaces and some other special characters, but there 
might be some characters that makes the script crash

## Tools used
**Libraries**
- subprocesses
- shutil
- argparse
- os (removed)
- glob (removed)
- pandas (removed)
- moviepy (removed)
- regex (removed)
- time (removed)
- datetime (removed)
- numpy (removed)
- concurrent.futures (removed)
- json (removed)

**Programs**
- FFMPEG + FMMPROBE
- Exiftool (no more)
- hachoir (no more)

## Lessions Learned (most important?)
- This project has been super educative and I would advise you to try to make something similar if you want
to learn about working with videos or creating a mid-sized project.
- This started as my first project where I used python to modify files on my system.
- I have learned to work with many libraries I have never used before (see Libraries list).
- I encountered some basics of working with videos:
    - encoding/decoding, audio track vs video track, videotypes, aspect ratios, sizes, bitsize +++
- Working with real world "messy" videos are super challenging, there are so many bugs one can encounter
- Most of the time after the inital setup was used to either make stuff more efficient or fix bugs
- Worked with exiftool (learned about metadata on videos and other files) and created some datasets and
visualisations with the data I had (separately)
- Learned a lot about making backwards compatible code, making backup and "fail-safeing"/error handling as
I worked with decent amounts of data on a laptop without outside backup (500-1000GB)
- Learned about the Google/youtube API, and APIs in general

## Statistics
This is outdated, but not too far off.

#### Compression
Ran compression on about 3100 videos of ~560GB. Compressed to ~160GB in about 15 days (24 hours a day) on a 4
core CPU (1.5-4.5 GHz) laptop.
Compressing on a Nvidia 3070 laptop GPU was about 4-8 times faster.
