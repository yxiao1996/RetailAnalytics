from ra.DeepSortNode import DeepSortNode
from ra.StoreTrackObserver import StoreTrackObserver
from ra.FakeYOLOSubject import FakeYOLOSubject

JSON_DIR = "D:\\code_collection\\RetailAnalytics\\data\\bb\\cam4-2\\"
IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"
ENCODER_DIR = "D:\\code_collection\\RetailAnalytics\\lib\\deep_sort\\deep_sort\\resources\\networks\\mars-small128.ckpt-68577"

confidenceThreshold = 0.0
yolov2Subject = FakeYOLOSubject(JSON_DIR, IMG_DIR)
deepSortNode = DeepSortNode(ENCODER_DIR, confidenceThreshold)
storeNode = StoreTrackObserver()
yolov2Subject.attach(deepSortNode)
deepSortNode.attach(storeNode)
yolov2Subject.detectVideo(100)