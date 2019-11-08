import json
from ra.Observer import Observer
from ra.FakeYOLOSubject import FakeYOLOSubject
from ra.FakeMaskRCNNSubject import FakeMaskRCNNSubject
from ra.DeepSortNode import DeepSortNode

class NaivePeopleCountObserver(Observer):
    
    END = False
    WRITE = False

    DETECT_SUBJECT = (FakeYOLOSubject, FakeMaskRCNNSubject)
    TRACK_SUBJECT = (DeepSortNode)

    def __init__(self, WRITE = False):
        self.WRITE = WRITE
        if(WRITE):
            self.countBuffer = []

    def update(self, subject):
        if(subject.END and self.WRITE):
            with open('peopleCount.json', 'w') as f:
                json.dump(self.countBuffer, f)
            self.END = True

        # count the number of people in subject
        if(isinstance(subject, self.DETECT_SUBJECT)):
            peopleCount = len(subject.rois)
        elif(isinstance(subject, self.TRACK_SUBJECT)):
            peopleCount = len(subject.objectIds)
        else:
            raise Exception("People Count Observer: Unidentified subject.")

        if(self.WRITE):
            self.countBuffer.append(str(peopleCount))
        print("Naive People Count: " + str(peopleCount))