import glob
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

do_replace = False

#added to compressed videofiles
suffix = '-d.mp4'

ffmpeg_args = '-vcodec libx264 -preset veryfast -crf 40'

# def compress(filepath):
# 	if do_replace:
# 		subprocess.run('ffmpeg -i "' + filepath + '" -vcodec libx265 -crf '+\
# 			str(compression_level) + ' "' + filepath + '"')
# 	else:
# 		subprocess.run('ffmpeg -i "' + filepath + '" -vcodec libx265 -crf '+\
# 			str(compression_level) + ' "' + filepath[:-4] + suffix + '"')
# 	print(filepath)

def compress(filepath):
	process = 'ffmpeg -i "' + filepath + '" ' + ffmpeg_args + ' "' + filepath[:-4] + suffix + '"'
	subprocess.run(process)

channels = glob.glob('Channels/*')
for channel in channels:
	#iterates all videos in all channels
	vids = glob.glob(channel+'/*.mp4')
	#sort by date
	vids.sort(key=os.path.getmtime)

	with ThreadPoolExecutor(max_workers=1) as exe:
		exe.map(compress,vids)