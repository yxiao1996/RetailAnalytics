import os
import cv2
import sys
import numpy as np
from mrcnn import utils
import mrcnn.model as modellib
from ra.Subject import Subject

class MaskRCNNSubject(Subject):

    observers = []
    image = []
    rois = []
    masks = []
    scores = []
    END = False

    ROIS = "rois"
    MASKS = "masks"
    SCORES = "scores"

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

    def __init__(self, MASK_RCNN_ROOT, IMG_DIR):
        self.MASK_RCNN_ROOT = MASK_RCNN_ROOT
        self.MODEL_DIR = os.path.join(MASK_RCNN_ROOT, "logs")
        self.COCO_MODEL_PATH = os.path.join(MASK_RCNN_ROOT, "mask_rcnn_coco.h5")
        self.IMG_DIR = IMG_DIR

    def notify(self):
        print("Mask-RCNN Subject: update people detection")
        for observer in self.observers:
            observer.update(self)

    def detectVideo(self, maxNumFrame = 0):
        sys.path.append(os.path.join(self.MASK_RCNN_ROOT, "samples/coco/"))
        import coco
        imageNames = os.listdir(self.IMG_DIR)

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
        model = modellib.MaskRCNN(mode="inference", model_dir=self.MODEL_DIR, config=config)

        # Load weights trained on MS-COCO
        model.load_weights(self.COCO_MODEL_PATH, by_name=True)

        frameId = 0
        for imgName in imageNames:
            self.image = cv2.imread(os.path.join(self.IMG_DIR, "frame%04d.jpg"%frameId))
            detections = model.detect([self.image])[0]
            detectClasses = detections['class_ids']
            self.rois = [self.convertTLRBToLTWH(roi) for roi in detections["rois"][detectClasses == 1]]
            self.masks = detections["masks"][:, :, detectClasses == 1]
            self.scores = detections["scores"][detectClasses == 1]
            self.notify()
            if(maxNumFrame > 0):
                if(frameId > maxNumFrame):
                    break
            frameId += 1
            print("frame Id: " + str(frameId))
        self.END = True
        self.notify()

    def convertTLRBToLTWH(self, roi):
        top, left, bottom, right = roi
        return [left, top, right-left, bottom-top]