# YoutubeUploader

A collection of scripts for compression, merging and uploading videos to youtube.

This is made for groups of videoes (course-videos etc.) that might need to be setup a specific way.

**Currently the scrips are split into:**

### metadata
- This uses exiftool (gives more needed information than hachoir) which will have to be downloaded separately and setup correctly in relation to this script
- Useful for handling of proper mergingsize.
- Important for compression being able to stop and continue at another time (as this takes very long time if you have lots of videos)
- Gives lots of useful and unuseful information about each video. The useful information can be used for data exploration and analysis and makes it easier to scan for anomalies.
- The script should be able to handle generation and updating of metadata (when more videos are added and when not all are compressed)
- The output is a data.csv file (csv was more practical than jsonlines as exiftool can give different attributes per file)
### compression
- This uses FFMPEG compression library (libx264 in veryfast mode) which will have to be downloaded separately and setup in the right place
- This process takes a lot of time so it relies on the data.csv file made by metadata so that compression can stop and continue at another time
### merging
- Uses moviepy for stitching of video and audiofiles. (looked into similar libraries, this seemed suitable for the task)
- This is for handling merging of multiple videos within a group. This is needed as some videoes can be really short and youtube has limitations on upload.
- Currently not implemented but it will take into account filesize and duration to stay within 12 hours mark for youtube upload limit.
- Should also give out chapters and useful data for youtube description.
- Unsure if it should delete original video files (pros: the saved size could be huge, cons: if something goes wrong you would have to download all vids again)

Then I will add the final step for youtube uploading when the current scrips are working well enough.
should include:

- token handling
- chapters, bookmarks and descriptions provided by merging
- perhaps periodical upload if you have huge amounts of videos that need uploading over time


Bugs etc. (important to know as they could lag behind in already used trials of the scrips):
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

## Statistics

#### Compression
Ran compression on about 3100 videos of ~560GB. Compressed to ~160GB in about 15 days (24 hours a day) on a 4 core CPU (1.5-4.5 GHz) laptop.
