import cv2
from ra.Observer import Observer

class VisualizationObserver(Observer):

    def __init__(self, vizType = "Tracking"):
        self.vizType = vizType

    def update(self, subject):
        objectBoundingBoxes = subject.objectBoundingBoxes
        objectIds = subject.objectIds
        image = subject.image

        # put bounding box and Id on image
        h, w, _ = image.shape
        thick = int((h + w) // 300)
        for (bbox, id_num) in zip(objectBoundingBoxes, objectIds):
            cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),
                                    (255,255,255), thick//3)
            cv2.putText(image, id_num, (int(bbox[0]), int(bbox[1]) - 12),0, 1e-3 * h, (255,255,255),thick//6)

        # display
        cv2.imshow(self.vizType, image)
        cv2.waitKey(1)