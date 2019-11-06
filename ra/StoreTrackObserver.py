import json
from ra.Observer import Observer

class StoreTrackObserver(Observer):

    tracks = {}

    def __init__(self, savePath = ".\\", filename = "trakcs.json"):
        self.savePath = savePath
        self.filename = filename
        self.curTime = 0

    def update(self, subject):
        if(subject.END):
            with open(self.savePath + self.filename, 'w') as fp:
                json.dump(self.tracks, fp)
            return

        objectBoundingBoxes = subject.objectBoundingBoxes
        objectIds = subject.objectIds

        for (bbox, personId) in zip(objectBoundingBoxes, objectIds):
            footPoint = (int(abs(bbox[2]-bbox[0])/2+bbox[0]), int(bbox[3]))
            if(personId not in self.tracks.keys()):
                self.tracks[personId] = [(footPoint, self.curTime)]
            else:
                self.tracks[personId].append((footPoint, self.curTime))

        self.curTime += 1