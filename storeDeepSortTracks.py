from ra.DeepSortNode import DeepSortNode
from ra.StoreTrackObserver import StoreTrackObserver
from ra.FakeYOLOSubject import FakeYOLOSubject
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.MaskRCNNSubject import MaskRCNNSubject

MRCNN_ROOT = "./lib/mrcnn/"
JSON_DIR = "./data/bb/cam4-2/"
IMG_DIR = "./data/imgs/cam4-2/"
ENCODER_DIR = "./lib/deep_sort/deep_sort/resources/networks/mars-small128.ckpt-68577"
APPLY_MASK = False
confidenceThreshold = 0.3

#detectSubject = FakeYOLOSubject(JSON_DIR, IMG_DIR, confidenceThreshold)
detectSubject = MaskRCNNSubject(MRCNN_ROOT, IMG_DIR)

deepSortNode = DeepSortNode(ENCODER_DIR, APPLY_MASK)
storeNode = StoreTrackObserver()
detectSubject.attach(deepSortNode)
deepSortNode.attach(storeNode)
detectSubject.detectVideo()