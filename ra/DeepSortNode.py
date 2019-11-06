import numpy as np
from ra.Observer import Observer
from ra.Subject import Subject
from deep_sort import generate_detections
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.tracker import Tracker
from deep_sort.deep_sort.detection import Detection

class DeepSortNode(Observer, Subject):

    objectBoundingBoxes = []
    objectIds = []
    image = []

    LABEL = "label"
    PERSON = "person"
    CONFIDENCE = "confidence"
    TOP_LEFT = "topleft"
    BOTTOM_RIGHT = "bottomright"
    END = False

    def __init__(self, encoderPath, confidenceThreshold = 0.6):
        self.metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.9, 100)
        self.tracker = Tracker(self.metric,max_iou_distance = 0.9, max_age = 50, n_init=3, _lambda = 0.3)
        self.encoder = generate_detections.create_box_encoder(encoderPath)
        self.confidenceThreshold = confidenceThreshold

    def update(self, subject):       
        if(subject.END):
            self.END = True
            self.notify()
            return

        # update tracker with detection from detector
        boundBoxes = []
        confidences = []
        for detectedObject in subject.detection:
            if(detectedObject[self.LABEL] == self.PERSON and detectedObject[self.CONFIDENCE] > self.confidenceThreshold):
                leftTopWidthHeight = self.convertTLBRToLTWH(detectedObject)
                boundBoxes.append(np.array(leftTopWidthHeight).astype(np.float64))
                confidences.append(detectedObject[self.CONFIDENCE])
        features = self.encoder(subject.image, np.array(boundBoxes))
        detections = [
                Detection(bbox, confidence, feature) for bbox, confidence, feature in
                zip(boundBoxes, confidences, features)]
        self.tracker.predict()
        self.tracker.update(detections)       

        # extract bounding boxes and Ids 
        self.image = subject.image
        self.objectBoundingBoxes = []
        self.objectIds = []
        tracks = self.tracker.tracks
        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            self.objectBoundingBoxes.append(track.to_tlbr())
            self.objectIds.append(str(track.track_id))
        
        # notify deep sort event listeners
        self.notify()

    def notify(self):
        print("DeepSortNode: update people tracking")
        for observer in self.observers:
            observer.update(self)


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