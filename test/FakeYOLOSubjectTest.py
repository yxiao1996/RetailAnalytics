from ra.Observer import Observer
from ra.FakeYOLOSubject import FakeYOLOSubject

JSON_DIR = "D:\\code_collection\\RetailAnalytics\\data\\bb\\cam4-2\\"
IMG_DIR = "D:\\code_collection\\RetailAnalytics\\data\\imgs\\cam4-2\\"

class FakeObserver(Observer):

    def update(self, result):
        print("FakeObserver: receive result " + str(result))

fakeYOLO = FakeYOLOSubject(JSON_DIR, IMG_DIR)
fakeObserver = FakeObserver()

fakeYOLO.attach(fakeObserver)

fakeYOLO.detectVideo()