import moviepy.editor
import glob
import os

channels = glob.glob('Channels/*')
for channel in channels:
    #iterates all videos in all channels
    vids = glob.glob(channel+'/*.mp4')
    #sort by date
    vids.sort(key=os.path.getmtime)

    processed_vids = []
    for vid in vids:
        print(vid)       
        
        clip = moviepy.editor.VideoFileClip(vid)
        audioclip = moviepy.editor.AudioFileClip(vid)
        videoclip = clip.set_audio(audioclip)
        processed_vids.append(videoclip)
    
    final = moviepy.editor.concatenate_videoclips(processed_vids)
    final.write_videofile(channel+"All.mp4")