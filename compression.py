import shutil
import subprocess
import pandas as pd
import time

def compress_file(filepath, crf=34):
    subprocess.run(['ffmpeg', '-i', filepath, '-vcodec', 'libx264', '-preset', 'veryfast', '-crf', str(crf), filepath+'cpr.mp4'], text=True, input="y")
    shutil.move(filepath+'cpr.mp4', filepath)
    
def compress(df):
    for i in range(df.shape[0]):
        #Check every video in dataframe if it is comrpessed
        if df.iloc[i, df.columns.get_loc('Compressed')] == False:
            # runs the compression of the time
            compress_file(df.iloc[i, df.columns.get_loc('Directory')] + '/' + df.iloc[i, df.columns.get_loc('File Name')])

            df.iloc[i, df.columns.get_loc('Compressed')] = True

            #Gets the current time
            mod_time = time.strftime("%Y:%m:%d %H:%M:%S%z", time.gmtime())
            #add : to the local time difference to get correct format
            mod_time = mod_time[:-2] + ':' + mod_time[-2:]
            df.iloc[i, df.columns.get_loc('File Modification Date/Time')] = mod_time
            #update the csv after each compression
            df.to_csv('data.csv', index=False)

df = pd.read_csv('data.csv')
compress(df)