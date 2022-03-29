import os
import glob
import json
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

#Path to exiftool for file metadata
exe = 'C:\\Users\Ferdi\\Desktop\\exiftool\\exiftool'

def compress(filepath):
	subprocess.run(['ffmpeg', '-i', filepath, '-vcodec', 'libx264', '-preset', 'veryfast', '-crf', str(crf), filepath+'cpr.mp4'], text=True, input="y")
	shutil.move(filepath+'cpr.mp4', filepath)
	os.remove(filepath+'cpr.mp4')

channels = glob.glob('Channels/*')
for channel in channels:
    #iterates all videos in all channels
    vids = glob.glob(channel+'/*.mp4')
    #sort by date
    vids.sort(key=os.path.getmtime)

    #write summary of metadata for videos in channel
    #strip the file to write metadata
    f = open(channel+ "\\summary.json", "w")
    f.write('')
    f.close()

    for vid in vids:
        #getting the metadata for a video
        process = subprocess.Popen([exe, vid],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        keys = []
        vals = []
        for o in process.stdout:
            #process key values for the metadata
            a = o.strip().split(':', 1)
            keys.append(a[0].strip())
            vals.append(a[1].strip())
            vid_data = dict(zip(keys,vals))
            #add the video as a line to be written to file
        with open(channel+ "\\summary.json", "a") as outfile:
            #add json lines
            json.dump(vid_data, outfile)
            outfile.write('\n')

    with ThreadPoolExecutor(max_workers=1) as exe:
        exe.map(compress,vids)