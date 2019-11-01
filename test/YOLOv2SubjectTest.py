from darkflow.defaults import argHandler 
from ra.Observer import Observer
from ra.YOLOv2Subject import YOLOv2Subject
import cv2

PROJ_ROOT = "../"
DARKFLOW_DIR = PROJ_ROOT + "lib/darkflow/"
imageTest = cv2.imread(DARKFLOW_DIR + "./sample_img/sample_dog.jpg")

FLAGS = argHandler()
FLAGS.setDefaults()
FLAGS.model = DARKFLOW_DIR + "cfg/yolov2.cfg"
FLAGS.load = DARKFLOW_DIR + "bin/yolov2.weights"
FLAGS.labels = DARKFLOW_DIR + "cfg/coco.names"
FLAGS.threshold = 0.1

class FakeObserver(Observer):

    def update(self, result):
        print("FakeObserver: receive result " + str(result))

fakeObserver = FakeObserver()
yolov2Subject = YOLOv2Subject(FLAGS)
yolov2Subject.attach(fakeObserver)
yolov2Subject.detectImage(imageTest)