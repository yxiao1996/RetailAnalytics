import os
import cv2
import json
from ra.Subject import Subject

"""
A fake YOLO subject read bounding boxed from josn files and publish events to observers
"""
class FakeYOLOSubject(Subject):

    observers = []
    image = []
    detection = []

    def __init__(self, jsonDirectory, imgDirectory):
        self.jsonDirectory = jsonDirectory
        self.imgDirectory = imgDirectory

    def notify(self):
        print("FakeYOLOSubject: update people detection")
        for observer in self.observers:
            observer.update(self)

    def detectVideo(self):
        for jsonFile, imgFile in zip(os.listdir(self.jsonDirectory), os.listdir(self.imgDirectory)):
            if jsonFile.endswith(".json"):
                with open(self.jsonDirectory + jsonFile, 'r') as fileHandle:
                    self.detection = json.loads(fileHandle.read())
                self.image = cv2.imread(self.imgDirectory + imgFile) 
                self.notify()