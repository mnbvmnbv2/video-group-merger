import glob
import shutil
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

crf = 34

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

	with ThreadPoolExecutor(max_workers=1) as exe:
		exe.map(compress,vids)