import glob
import subprocess
import os
import json

#Path to exiftool for file metadata
exe = 'C:\\Users\Ferdi\\Desktop\\exiftool\\exiftool'

#strip the file to write metadata
f = open("big.json", "w")
f.write('[')
f.close()
f = open("small.json", "w")
f.write('[')
f.close()

channels = glob.glob('Channels/*')
for channel in channels:
    #iterates all videos in all channels
    vids = glob.glob(channel+'/*.mp4')
    #sort by date
    vids.sort(key=os.path.getmtime)

    for idx, vid in enumerate(vids):
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
        with open("big.json", "a") as outfile:
            #add json lines
            json.dump(vid_data, outfile)
            #write for every file except last
            if idx != len(vids) - 1:
                outfile.write(',\n')

        #for small format
        small_format = {k:vid_data[k] for k in ('File Name','File Size','Duration') if k in vid_data}
        small_format['Compressed'] = False
        with open("small.json", "a") as outfile:
            #add json lines
            json.dump(small_format, outfile)
            #write for every file except last
            if idx != len(vids) - 1:
                outfile.write(',\n')

f = open("big.json", "a")
f.write(']')
f.close()
f = open("small.json", "a")
f.write(']')
f.close()