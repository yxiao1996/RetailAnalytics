import os
from ra.DeepSortNode import DeepSortNode
from ra.FakeYOLOSubject import FakeYOLOSubject
from ra.VisualizationObserver import VisualizationObserver
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.MaskRCNNSubject import MaskRCNNSubject

os.environ['CUDA_VISIBLE_DEVICES'] = '0'

MRCNN_ROOT = "./lib/mrcnn/"
JSON_DIR = "D:\\code_collection\\RetailAnalytics\\data\\bb\\cam4-2\\"
IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"
ENCODER_DIR = "D:\\code_collection\\RetailAnalytics\\lib\\deep_sort\\deep_sort\\resources\\networks\\mars-small128.ckpt-68577"
#ENCODER_DIR = "D:\\code_collection\\RetailAnalytics\\data\\models\\Market1501\\cosine-softmax\\market1501.ckpt"
MASK_DIR = "D:\\code_collection\\RetailAnalytics\\data\\masks\\frames.h5"

confidenceThreshold = 0.0
#detectSubject = FakeYOLOSubject(JSON_DIR, IMG_DIR, confidenceThreshold)
#detectSubject = FakeMaskRCNNSubject(MASK_DIR, IMG_DIR)
detectSubject = MaskRCNNSubject(MRCNN_ROOT, IMG_DIR)

deepSortNode = DeepSortNode(ENCODER_DIR)
detectSubject.attach(deepSortNode)

vizNode = VisualizationObserver("Path", False)
deepSortNode.attach(vizNode)

detectSubject.detectVideo()