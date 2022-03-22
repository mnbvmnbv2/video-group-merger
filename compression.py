import subprocess
from importlib_metadata import metadata
import moviepy.editor
import glob
import subprocess
import os

do_compression = False
do_threading = False


#added to compressed videofiles
suffix = '-d.mp4'

channels = glob.glob('Channels/*')
for channel in channels:
    #iterates all videos in all channels
    vids = glob.glob(channel+'/*.mp4')
    #sort by date
    vids.sort(key=os.path.getmtime)

    processed_vids = []
    for vid in vids:
        print(vid)       

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