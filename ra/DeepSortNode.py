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

    END = False

    def __init__(self, encoderPath, applyMask = False):
        self.metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.9, 100)
        self.tracker = Tracker(self.metric,max_iou_distance = 0.9, max_age = 50, n_init=3, _lambda = 0.3)
        self.encoder = generate_detections.create_box_encoder(encoderPath, applyMask = applyMask)
        self.applyMask = applyMask

    def update(self, subject):       
        if(subject.END):
            self.END = True
            self.notify()
            return

        # update tracker with detection from detector
        boundBoxes = subject.rois
        confidences = subject.scores
        
        if(self.applyMask):
            features = self.encoder(subject.image, np.array(boundBoxes), subject.masks)
        else:
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
