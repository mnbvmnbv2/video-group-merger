# YoutubeUploader

A collection of scripts for compression, merging and uploading of videos to youtube.

This is made for groups of videoes (course-videos etc.) that will be combined to reduce the 
total amount of files to make it easier to upload to youtube.

This repo has been experimental for a long time and the structure of the files have changed multiple times. 
Using what I have learned I have found that the current setup with one main file to compress, merge videos 
and add a summary text-file for chapters, to be most practical. 

## Table of contents
- [Features](Features)

**Currently the scrips are split into:**

### metadata
- This uses exiftool (gives more needed information than hachoir) which will have to be downloaded separately and setup correctly in relation to this script
- Useful for handling of proper mergingsize.
- Important for compression being able to stop and continue at another time (as this takes very long time if you have lots of videos)
- Gives lots of useful and unuseful information about each video. The useful information can be used for data exploration and analysis and makes it easier to scan for anomalies.
- The script should be able to handle generation and updating of metadata (when more videos are added and when not all are compressed)
- The output is a data.csv file (csv was more practical than jsonlines as exiftool can give different attributes per file?)
### compression
- This uses FFMPEG compression library (libx264 in veryfast mode) which will have to be downloaded separately and setup in the right place
- This process takes a lot of time so it relies on the data.csv file made by metadata so that compression can stop and continue at another time
- Can handle empty folders/data.csvs

#### mergerdata
- like metadata but for info before merging that will be used when uploading to youtube

### merging
- Uses moviepy for stitching of video and audiofiles. (looked into similar libraries, this seemed suitable for the task)
- This is for handling merging of multiple videos within a group. This is needed as some videoes can be really short and youtube has limitations on upload.
- Currently not implemented but it will take into account filesize and duration to stay within 12 hours mark for youtube upload limit.
- Should also give out chapters and useful data for youtube description.
- Unsure if it should delete original video files (pros: the saved size could be huge, cons: if something goes wrong you would have to download all vids again)

### upload
- Supports chunked upload
- You need to setup youtube api credentials: https://console.cloud.google.com/apis/credentials
- Both OAuth and API keys need to be placed in /Keys folder
- You must enable YouTube Data API v3 in the API project you create


Then I will add the final step for youtube uploading when the current scrips are working well enough.
should include:
- perhaps periodical upload if you have huge amounts of videos that need uploading over time


##### Bugs etc. 
(important to know as they could lag behind in already used trials of the scrips):
- Metadata could overwrite compressed videoes.
- Metadata can contain Error message row
- Metadata has inconsistent notation for some columns (Duration hh:mm:ss or xx S.)
- Metadata did not have index=False which lead to a huge amount of unnamed index columns over time
- Merges could happen on group of incomplete videos
- Metadata is not 100% correct on file creation and modification as files are overwritten and deleted for practical puropses
- Metadata updating is slow.
- There could be mismatched between data.csv and actual metadata that could propagate if the order of the scrips run is wrong or outdated (ex: a file could be deleted, but if metadata is not run compression could try to compress non-existing files)
- There could be tempfiles from compression (or download/insertion) that could end up in metadata data.csv file if not disposed of.
- There is no handling for removal of data/actual files to be handeled correctly 

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
- Exiftool
- hachoir (no more)

## Lessions Learned (most important?)
- This started as my first project where I used python to modify files on my system, as well as the first time I did that in any automed fashion.
- I have learned to work with many libraries I have never used before as:
    - subprocesses
    - regex
    - datetime
    ...
- Encountered some basics of working with videos (encoding/decoding, audio track vs video track etc.)
- Working with real world "messy" videos are super challenging
- Most of my time after inital setup was to either make stuff more efficient or locate bugs of corruping videos
- Worked with different video formats
- Worked with exiftool (learned about metadata on videos and other files) and FFMPEG
- Learned a lot about making backwards compatible code, making backup and "fail-safeing"/error handling
- Handling slightly big amounts of data (just on a laptop) 500-1000GB
- Learned about some data analysis on my "dataset" of metadata about videos.
- Google/youtube API, and API in general

## Statistics

#### Compression
Ran compression on about 3100 videos of ~560GB. Compressed to ~160GB in about 15 days (24 hours a day) on a 4 core CPU (1.5-4.5 GHz) laptop.

#### Mergers
Using FFMPEG instead of moviepy resulted in about 1000x speedup, not sure why.
All videos (3100) took some hours to merge.


## Guide

First of all, this is not optimal.
All of these scrips have been part of a journey where I have learned a lot, and now that it works for its intended purpose I will discontinue updates.
And processing videos takes A LOT of time, wow.

The goal was also to learn so I have used different tools where perhaps only one should be used and not all edge cases and redunandacy is assured.
For example the scripts have to be run in order and it is not failsafe to run out of order, details below.

Step by step:
1. Create the appropriate folders
2. Put videos in folders (NB: Naming)
3. Run metadata.py
4. 

5. NB: Cannot go back and rerun from 3. now!!

9. Added sorting in mergersdata, but filenames should be named 01 if numbers go above 9 for example

Do not run mergersdata after mergers, or upload as it overwrites the json-file.

KNown bug, sorting (by date etc) is not always correct.
The final metadata is not correct, but it can still be fun to use for data analysis/exploration.

There might be temp files from compressing or merging ling (?) about. Be careful about reruns of metadata and mergersdata etc.

Be careful about space. While compression is meant to save space, mergers increases it by 2x so be sure to either remove merged videos (or when uploaded to youtube), or have enough space.

TODO:
Everything should be f-string, all "/" should be either `/` or `\\\\`, and open should use enconding.

Mergers is superslow. Maybe speedup with FFMPEG or GPU?

In heindsight:
Compression might be too intense. Audio is a bit distorted...


Mergerdata does not sort! Videos comes in wrong order...