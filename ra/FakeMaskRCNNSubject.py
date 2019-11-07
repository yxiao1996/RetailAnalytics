import os
import cv2
import h5py
from ra.Subject import Subject

class FakeMaskRCNNSubject(Subject):

    observers = []
    imgae = []
    rois = []
    masks = []
    scores = []
    END = False

    ROIS = "rois"
    MASKS = "masks"
    SCORES = "scores"

    def __init__(self, h5Path, imgDirectory):
        # read h5py file 
        self.imgDirectory = imgDirectory
        self.h5File = h5py.File(h5Path, 'r')

    def notify(self):
        print("Fake Mask-RCNN Subject: update people detection")
        for observer in self.observers:
            observer.update(self)

    def detectVideo(self, maxNumFrame = 99):
        frameNames = list(self.h5File.keys())
        for i, imgFile in zip(range(0, len(frameNames)), os.listdir(self.imgDirectory)):
            detect = self.h5File.get(str(i))
            self.rois = [self.convertTLRBToLTWH(roi) for roi in detect.get(self.ROIS)]
            self.masks = detect.get(self.MASKS)
            self.scores = detect.get(self.SCORES)
            self.image = cv2.imread(self.imgDirectory + imgFile) 
            self.notify()
            if(maxNumFrame > 0):
                if(i >= maxNumFrame):
                    break
        
        self.END = True
        self.notify()

    def convertTLRBToLTWH(self, roi):
        top, left, bottom, right = roi
        return [left, top, right-left, bottom-top]