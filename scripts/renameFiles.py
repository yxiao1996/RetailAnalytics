directory = "../data/imgs/cam2-2_square/"

import os

for filename in os.listdir(directory):
    imgId = (filename.split('.')[0]).split('_')[-1]
    newFilename = "frame" + ("%04d" % (int(imgId)-1)) + ".jpg"
    os.rename(directory+filename, directory+newFilename)