from darkflow.defaults import argHandler #Import the default arguments
from darkflow.net.build import TFNet
import cv2

PROJ_ROOT = "../"
DARKFLOW_DIR = PROJ_ROOT + "lib/darkflow/"


FLAGS = argHandler()
FLAGS.setDefaults()
FLAGS.model = DARKFLOW_DIR + "cfg/yolov2.cfg"
FLAGS.load = DARKFLOW_DIR + "bin/yolov2.weights"
FLAGS.labels = DARKFLOW_DIR + "cfg/coco.names"
FLAGS.threshold = 0.1

yoloNet = TFNet(FLAGS)

imageTest = cv2.imread(DARKFLOW_DIR + "./sample_img/sample_dog.jpg")

testResult = yoloNet.return_predict(imageTest)

print(testResult)