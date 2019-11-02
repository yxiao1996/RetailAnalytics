from ra.DeepSortNode import DeepSortNode
from ra.FakeYOLOSubject import FakeYOLOSubject

JSON_DIR = "D:\\code_collection\\RetailAnalytics\\data\\bb\\cam4-2\\"
IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"
ENCODER_DIR = "D:\\code_collection\\RetailAnalytics\\lib\\deep_sort\\deep_sort\\resources\\networks\\mars-small128.ckpt-68577"


deepSortNode = DeepSortNode(ENCODER_DIR)
yolov2Subject = FakeYOLOSubject(JSON_DIR, IMG_DIR)
yolov2Subject.attach(deepSortNode)
yolov2Subject.detectVideo()