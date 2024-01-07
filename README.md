# YoutubeUploader

This repo contains two scripts:
- One for merging videos and writing metadata
- One for uploading to youtube

This project is primarily for learning purposes and is should not be viewed as robust or efficient.

The main script is the merging script as youtube has restrictions on number of daily uploads, but not on size.
The idea was therefore to merge videos up to the limit of 12 hours and write chapter data such that one can 
upload more videos in a shorter amount of time.

Using the youtube API was limiting both in number of uploads (4 instead of 10 per day, and you steed need to
authenticate per video) so I would suggest to just use `main.py` to merge the videos and manually upload them 
and paste the chapter data. 

This repo has been experimental for a long time and there are potentially multiple places where the 
documentation is outdated.

## Warning
- Backup your files before using, videos might be corrupted or compressed too much.

## Dependencies
- You need to install `FFMPEG` (+`FFMPROBE`) separately.

## Main script
- This uses ffmprobe to find video sizes
- Compresses and merges videos into chunks of up to 12 hours and outputs a file with

- You need to specify input folder and output folder:
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
```
- As I have encountered a lot of errors I have put in some error handling, but if you use this script there
might be cases that I have not encountered.

## Known things to watch out for
- Soring of videos is handeled by numbers then text, however if there are different amount of numbers it is
zero padded up to 5 numbers (can be changed manually)
- If videos are of different aspect ratio, or fps there might be trouble. In the latest version this should
be handeled to some degree, but it might not be fail-safe.
- Be mindful of video names, the script should handle spaces etc., but there might be special characters that
makes it crash
- To handle differing video types (size etc.), I believe one has to decode and encode the videos which is slow
, therefore it is possible to use GPU for this, which you should check out if you have available.
- If the script is stopped mid-way, there are some temp_files and logs saved so that one does not have to
process all files again, however it might not be "fail-safe".

### upload
- Supports chunked upload
- You need to setup youtube api credentials: https://console.cloud.google.com/apis/credentials
- Both OAuth and API keys need to be placed in /Keys folder
- You must enable YouTube Data API v3 in the API project you create

**Libraries**
- os
- glob
- subprocesses
- pandas
- shutil
- time
- moviepy
- regex (removed)
- datetime (removed)
- numpy (removed)
- concurrent.futures (removed)
- json (removed)

- youtube api

**Programs**
- FFMPEG
- Exiftool (no more)
- hachoir (no more)

## Lessions Learned (most important?)
- This project has been super educative and I would advise you to try to make something similar if you want
to learn about working with videos or creating a mid-sizes project.
- This started as my first project where I used python to modify files on my system, as well as the first time
I did that with automation.
- I have learned to work with many libraries I have never used before such as:
    - subprocesses
    - regex
    - datetime
    - FFMPEG
    - exiftool
    ...
- Encountered some basics of working with videos:
    - encoding/decoding, audio track vs video track, videotypes, aspect ratios, sizes, bitsize +++
- Working with real world "messy" videos are super challenging, there are so many bugs one can encounter
- Most of the time after the inital setup was used to either make stuff more efficient or fix bugs
- Worked with exiftool (learned about metadata on videos and other files) and FFMPEG
- Learned a lot about making backwards compatible code, making backup and "fail-safeing"/error handling
- Handling decent amounts of data on a laptop without outside backup (500-1000GB)
- Learned about some data analysis on my "dataset" of metadata about videos.
- Google/youtube API, and API in general

## Statistics
This is outdated, but not too far off.

#### Compression
Ran compression on about 3100 videos of ~560GB. Compressed to ~160GB in about 15 days (24 hours a day) on a 4
core CPU (1.5-4.5 GHz) laptop.
Compressing on a Nvidia 3070 laptop GPU was about 4-8 times faster.  


TODO:
Everything should be f-string, all "/" should be either `/` or `\\\\`, and open should use enconding.
