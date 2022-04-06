import glob
import subprocess
import os
import pandas as pd


#Path to exiftool for file metadata
exe = 'C:\\Users\Ferdi\\Desktop\\exiftool\\exiftool'

vids_json = []

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
        vid_data['Compressed'] = False
        vids_json.append(vid_data)

new_df = pd.DataFrame.from_dict(vids_json)
if os.path.exists('data.csv'):
    old_df = pd.read_csv('data.csv')
    new_vids = new_df[~new_df[['File Name', 'Directory']].isin(old_df).any(axis=1)]
    complete_df = pd.concat((old_df, new_vids))
    complete_df.to_csv('data.csv')