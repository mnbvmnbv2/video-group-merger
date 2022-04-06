import shutil
import subprocess
import pandas as pd
import time

crf = 34

def compress_file(filepath):
    subprocess.run(['ffmpeg', '-i', filepath, '-vcodec', 'libx264', '-preset', 'veryfast', '-crf', str(crf), filepath+'cpr.mp4'], text=True, input="y")
    shutil.move(filepath+'cpr.mp4', filepath)
    
def compress(df):
    for i in range(df.shape[0]):
        if df.iloc[i, df.columns.get_loc('Compressed')] == False:
            compress_file(df.iloc[i, df.columns.get_loc('Directory')] + '/' + df.iloc[i, df.columns.get_loc('File Name')])
            df.iloc[i, df.columns.get_loc('Compressed')] = True
            mod_time = time.strftime("%Y:%m:%d %H:%M:%S%z", time.gmtime())
            mod_time = ":".join(mod_time.split("00", 1)) + '00'
            df.iloc[i, df.columns.get_loc('File Modification Date/Time')] = mod_time
            df.to_csv('data.csv', index=False)

df = pd.read_csv('data.csv')
compress(df)