import os
from ra.DeepSortNode import DeepSortNode
from ra.FakeYOLOSubject import FakeYOLOSubject
from ra.VisualizationObserver import VisualizationObserver
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.MaskRCNNSubject import MaskRCNNSubject

#os.environ['CUDA_VISIBLE_DEVICES'] = '0'

MRCNN_ROOT = "./lib/mrcnn/"
JSON_DIR = "./data/bb/yolo2cam2-2squareNMS/"
IMG_DIR = "./data/imgs/cam2-2_square/"
ENCODER_DIR = "./lib/deep_sort/deep_sort/resources/networks/mars-small128.ckpt-68577"
MASK_DIR = "./data/masks/frames.h5"
RECORD = False
APPLY_MASK = False

confidenceThreshold = 0.0
detectSubject = FakeYOLOSubject(JSON_DIR, IMG_DIR, confidenceThreshold)
#detectSubject = FakeMaskRCNNSubject(MASK_DIR, IMG_DIR)
#detectSubject = MaskRCNNSubject(MRCNN_ROOT, IMG_DIR)

deepSortNode = DeepSortNode(ENCODER_DIR, APPLY_MASK)
detectSubject.attach(deepSortNode)

vizNode = VisualizationObserver("Path", RECORD)
deepSortNode.attach(vizNode)

detectSubject.detectVideo(1000)
