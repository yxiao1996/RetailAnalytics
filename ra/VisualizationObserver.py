import cv2
from ra.Observer import Observer

class VisualizationObserver(Observer):

    VIZ_BOUNDING_BOX = "BoundingBox"
    VIZ_PATH = "Path"

    peoplePath = {} # keep track of each person

    def __init__(self, vizType = "BoundingBox", SaveVideo = False):
        self.vizType = vizType
        self.SaveVideo = SaveVideo
        if self.SaveVideo:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.videoWriter = cv2.VideoWriter('output.mp4', fourcc, 10, (1280, 720))

    def update(self, subject):
        if(subject.END and self.SaveVideo):
            self.videoWriter.release()
            return

        objectBoundingBoxes = subject.objectBoundingBoxes
        objectIds = subject.objectIds
        image = subject.image

        if(self.vizType == self.VIZ_BOUNDING_BOX):
            # put bounding box and Id on image
            h, w, _ = image.shape
            thick = int((h + w) // 300)
            for (bbox, id_num) in zip(objectBoundingBoxes, objectIds):
                cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                                        (255,255,255), thick//3)
                cv2.putText(image, id_num, (int(bbox[0]), int(bbox[1]) - 12),0, 1e-3 * h, (255,255,255),thick//6)

        if(self.vizType == self.VIZ_PATH):
            self._prunePeoplePath(objectIds)
            self._addNewPointsToPeoplePath(objectBoundingBoxes, objectIds)
            image = self._drawPathOnImage(image)

        # display
        #cv2.imshow(self.vizType, image)
        #cv2.waitKey(1)
        if self.SaveVideo:
            self.videoWriter.write(image)

    def _prunePeoplePath(self, objectIds):
        pruneKeys = []
        for personId in self.peoplePath.keys():
            if(personId not in objectIds):
                pruneKeys.append(personId)
        for personId in pruneKeys:
            self.peoplePath.pop(personId)
    
    def _addNewPointsToPeoplePath(self, objectBoundingBoxes, objectIds):
        for (bbox, personId) in zip(objectBoundingBoxes, objectIds):
            footPoint = (int(abs(bbox[2]-bbox[0])/2+bbox[0]), int(bbox[3]))
            if(personId not in self.peoplePath.keys()):
                self.peoplePath[personId] = [footPoint]
            else:
                self.peoplePath[personId].append(footPoint)    
    
    def _drawPathOnImage(self, image):
        h, w, _ = image.shape
        thick = int((h + w) // 300)
        for personId, footPoints in self.peoplePath.items():
            for i in range(0, len(footPoints)-2):
                cv2.line(image, footPoints[i], footPoints[i+1], (0, 255, 0), thick//2)
            cv2.putText(image, personId, footPoints[-1], 0, 1e-3 * h, (0,0,255),thick//6)
        return image
