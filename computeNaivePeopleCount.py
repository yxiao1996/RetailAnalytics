from ra.NaivePeopleCountObserver import NaivePeopleCountObserver
from ra.FakeYOLOSubject import FakeYOLOSubject

JSON_DIR = "D:\\code_collection\\RetailAnalytics\\data\\bb\\cam4-2\\"
IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"

countObserver = NaivePeopleCountObserver()
yolov2Subject = FakeYOLOSubject(JSON_DIR, IMG_DIR)
yolov2Subject.attach(countObserver)
yolov2Subject.detectVideo()