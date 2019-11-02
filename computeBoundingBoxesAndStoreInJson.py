from darkflow.defaults import argHandler 
from ra.NaivePeopleCountObserver import NaivePeopleCountObserver
from ra.YOLOv2Subject import YOLOv2Subject
import cv2

PROJ_ROOT = "./"
DARKFLOW_DIR = PROJ_ROOT + "lib/darkflow/"
imageTest = cv2.imread(DARKFLOW_DIR + "./sample_img/sample_person.jpg")

FLAGS = argHandler()
FLAGS.setDefaults()
FLAGS.imgdir = PROJ_ROOT + "data/bb/"
FLAGS.demo = PROJ_ROOT + "videos/cam4-2.mkv"
FLAGS.model = DARKFLOW_DIR + "cfg/yolov2.cfg"
FLAGS.load = DARKFLOW_DIR + "bin/yolov2.weights"
FLAGS.labels = DARKFLOW_DIR + "cfg/coco.names"
FLAGS.threshold = 0.1
FLAGS.json = True
FLAGS.save = True
print(FLAGS)

countObserver = NaivePeopleCountObserver()
yolov2Subject = YOLOv2Subject(FLAGS)
yolov2Subject.attach(countObserver)
yolov2Subject.detectVideo()