import shutil
import subprocess
import pandas as pd

crf = 34

def compress_file(filepath):
    subprocess.run(['ffmpeg', '-i', filepath, '-vcodec', 'libx264', '-preset', 'veryfast', '-crf', str(crf), filepath+'cpr.mp4'], text=True, input="y")
    shutil.move(filepath+'cpr.mp4', filepath)
    
def compress(df):
    for i in range(df.shape[0]):
        if df.iloc[i, df.columns.get_loc('Compressed')] == False:
            compress_file(df.iloc[i, df.columns.get_loc('Directory')] + '/' + df.iloc[i, df.columns.get_loc('File Name')])
            df.iloc[i, df.columns.get_loc('Compressed')] = True
            df.to_csv('data.csv')

df = pd.read_csv('data.csv')
compress(df)