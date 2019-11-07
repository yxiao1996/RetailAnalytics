from ra.MRCNNVizObserver import MRCNNVizObserver
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.MaskRCNNSubject import MaskRCNNSubject

IMG_DIR = "./data/imgs/cam4-2/"
MASK_DIR = "./data/masks/frames.h5"
MRCNN_ROOT = "./lib/mrcnn/"
#mrcnnSubject = FakeMaskRCNNSubject(MASK_DIR, IMG_DIR)
mrcnnSubject = MaskRCNNSubject(MRCNN_ROOT, IMG_DIR)
viz = MRCNNVizObserver()
mrcnnSubject.attach(viz)
mrcnnSubject.detectVideo()