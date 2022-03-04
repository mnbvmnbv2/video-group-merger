import moviepy.editor
import os
import glob

channels = glob.glob('Channels/*')
for channel in channels:
    vids = glob.glob(channel+'/*')
    print(vids)
    output = moviepy.editor.CompositeVideoClip(vids)
    output.write_videofile(channel+"All.mp4")