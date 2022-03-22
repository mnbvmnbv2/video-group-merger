import subprocess
from importlib_metadata import metadata
import moviepy.editor
import glob
import subprocess
import os
import json

do_metadata = True
do_compression = False
do_threading = False


#added to compressed videofiles
suffix = '-d.mp4'
#Path to exiftool for file metadata
exe = 'C:\\Users\Ferdi\\Desktop\\exiftool\\exiftool'


channels = glob.glob('Channels/*')
for channel in channels:
    #iterates all videos in all channels
    vids = glob.glob(channel+'/*.mp4')
    #sort by date
    vids.sort(key=os.path.getmtime)

    processed_vids = []

    #write summary of metadata for videos in channel
    if do_metadata:
        #to store each metadata line
        #metadata = []
        #strip the file to write metadata
        f = open(channel+ "\\summary.json", "w")
        f.write('')
        f.close()
    for vid in vids:
        print(vid)

        if do_metadata:
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
                

        if do_compression:
          subprocess.run('ffmpeg -i "' + vid + '" -vcodec libx265 -crf 40 "' + vid + suffix + '"')
        
        # clip = moviepy.editor.VideoFileClip(vid)
        # audioclip = moviepy.editor.AudioFileClip(vid)
        # videoclip = clip.set_audio(audioclip)
        # processed_vids.append(videoclip)

    #if do_metadata:
    #    f.write(','.join(keys)+'\n')
    #    for line in metadata:
    #        f.write(line)
    
    #f.close()
    
    #final = moviepy.editor.concatenate_videoclips(processed_vids)
    #final.write_videofile(channel+"All.mp4")
    #final.ipython_display()