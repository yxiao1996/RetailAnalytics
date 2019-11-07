from ra.MRCNNVizObserver import MRCNNVizObserver
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject

IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"
MASK_DIR = "D:\\code_collection\\RetailAnalytics\\data\\masks\\frames.h5"

mrcnnSubject = FakeMaskRCNNSubject(MASK_DIR, IMG_DIR)
viz = MRCNNVizObserver()
mrcnnSubject.attach(viz)
mrcnnSubject.detectVideo()