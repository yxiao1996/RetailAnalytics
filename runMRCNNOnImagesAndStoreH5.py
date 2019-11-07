import os
import sys
import cv2
import h5py
import json
import numpy as np
from mrcnn import utils
import mrcnn.model as modellib

MRCNN_ROOT = "./lib/mrcnn/"
# Import COCO config
sys.path.append(os.path.join(MRCNN_ROOT, "samples/coco/"))
import coco

# Directory to save logs and trained model
MODEL_DIR = os.path.join(MRCNN_ROOT, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(MRCNN_ROOT, "mask_rcnn_coco.h5")

IMAGE_DIR = "./data/imgs/cam4-2/"
imageNames = os.listdir(IMAGE_DIR)

class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.05
    DETECTION_MAX_INSTANCES = 200

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

maxNumFrame = 10000
frameId = 0
h5File = h5py.File('./data/masks/frames.h5', 'w')
for imgName in imageNames:
    image = cv2.imread(os.path.join(IMAGE_DIR, "frame%04d.jpg"%frameId))
    detections = model.detect([image])[0]
    peopleDetect = {}
    detectClasses = detections['class_ids']
    peopleDetect["rois"] = detections["rois"][detectClasses == 1]
    peopleDetect["masks"] = detections["masks"][:, :, detectClasses == 1]
    peopleDetect["scores"] = detections["scores"][detectClasses == 1]
    #with open('./data/masks/frame%04d'%frameId+'.npy', 'w') as f:
        # json.dump(peopleDetect, f)
    #np.save('./data/masks/frame%04d'%frameId+'.npy', peopleDetect)
    frameGroup = h5File.create_group(str(frameId))
    frameGroup.create_dataset("rois", data=peopleDetect["rois"], compression="gzip", compression_opts=9)
    frameGroup.create_dataset("masks", data=peopleDetect["masks"], compression="gzip", compression_opts=9)
    frameGroup.create_dataset("scores", data=peopleDetect["scores"], compression="gzip", compression_opts=9)
    if(frameId > maxNumFrame):
        break
    else:
        frameId += 1
    print(frameId)
h5File.close()
