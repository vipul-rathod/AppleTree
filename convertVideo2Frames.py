import sys, os

from PIL import Image

shotPath = 'D:/new_project/'

ffmpegPath = '//192.168.5.253/BBB_main/bbb/t/dev_installers/ffmpeg/bin/ffmpeg.exe -i "D:/new_project/ep103_sh003_BOARD.v000.mov" -vf scale=480:270  -r 25 D:/new_project/frames/ep103_sh003_BOARD.v000.%03d.jpg'

# os.system(ffmpegPath)