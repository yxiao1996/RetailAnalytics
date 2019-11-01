from ra.Subject import Subject
from darkflow.net.build import TFNet

PROJ_ROOT = "../"
DARKFLOW_DIR = PROJ_ROOT + "lib/darkflow/"

class YOLOv2Subject(Subject):
    def __init__(self, FLAGS):
        self.observers = []
        self.yoloNet = TFNet(FLAGS)

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, result):
        print("YOLOv2Subject: update people detection")
        for observer in self.observers:
            observer.update(result)

    def detectImage(self, image):
        self.notify(self.yoloNet.return_predict(image))

    def detectVideo(self):
        self.yoloNet.camera(self)
