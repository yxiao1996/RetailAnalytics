from ra.NaivePeopleCountObserver import NaivePeopleCountObserver
from ra.FakeYOLOSubject import FakeYOLOSubject
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.MaskRCNNSubject import MaskRCNNSubject

WRITE = True
MRCNN_ROOT = "./lib/mrcnn/"
JSON_DIR = "./data/bb/cam4-2/"
IMG_DIR = "./data/imgs/cam4-2/"
MASK_DIR = "./data/masks/frames.h5"

#detectSubject = FakeMaskRCNNSubject(MASK_DIR, IMG_DIR)
#detectSubject = MaskRCNNSubject(MRCNN_ROOT, IMG_DIR)
detectSubject = FakeYOLOSubject(JSON_DIR, IMG_DIR)

countObserver = NaivePeopleCountObserver(WRITE)

detectSubject.attach(countObserver)
detectSubject.detectVideo()