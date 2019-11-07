import os
import cv2
import json
import numpy as np
from ra.Subject import Subject

"""
A fake YOLO subject read bounding boxed from josn files and publish events to observers
"""
class FakeYOLOSubject(Subject):

    observers = []
    image = []
    rois = []
    scores = []
    END = False

    LABEL = "label"
    PERSON = "person"
    CONFIDENCE = "confidence"
    TOP_LEFT = "topleft"
    BOTTOM_RIGHT = "bottomright"

    def __init__(self, jsonDirectory, imgDirectory, confidenceThreshold = 0.0):
        self.jsonDirectory = jsonDirectory
        self.imgDirectory = imgDirectory
        self.confidenceThreshold = confidenceThreshold

    def notify(self):
        print("FakeYOLOSubject: update people detection")
        for observer in self.observers:
            observer.update(self)

    def detectVideo(self, maxNumFrame = 0):
        frameId = 0
        self.scores = []
        self.rois = []
        for jsonFile, imgFile in zip(os.listdir(self.jsonDirectory), os.listdir(self.imgDirectory)):
            if jsonFile.endswith(".json"):
                with open(self.jsonDirectory + jsonFile, 'r') as fileHandle:
                    detection = json.loads(fileHandle.read())
                for detectedObject in detection:
                    if(detectedObject[self.LABEL] == self.PERSON and detectedObject[self.CONFIDENCE] > self.confidenceThreshold):
                        leftTopWidthHeight = self.convertTLBRToLTWH(detectedObject)
                        self.rois.append(np.array(leftTopWidthHeight).astype(np.float64))
                        self.scores.append(detectedObject[self.CONFIDENCE])
                self.image = cv2.imread(self.imgDirectory + imgFile) 
                self.notify()
                if(maxNumFrame > 0):
                    if(frameId >= maxNumFrame):
                        break
                    else:
                        frameId += 1
        self.END = True
        self.notify()

    def convertTLBRToLTWH(self, detectedObject):
        # convert YOLO detection to deep sort Detection data model
        topLeft = detectedObject[self.TOP_LEFT]
        bottomRight = detectedObject[self.BOTTOM_RIGHT]
        top = topLeft['y']
        left = topLeft['x']
        bottom = bottomRight['y']
        right = bottomRight['x']
        width = abs(right - left)
        height = abs(top - bottom)
        leftTopWidthHeight = [left, top, width, height]
        return leftTopWidthHeight