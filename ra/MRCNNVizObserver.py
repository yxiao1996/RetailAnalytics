import cv2
import numpy as np
from mrcnn.visualize import random_colors, apply_mask
from ra.Observer import Observer

class MRCNNVizObserver(Observer):

    def update(self, subject):
        image = subject.image
        masks = subject.masks
        rois = subject.rois
        colors = random_colors(masks.shape[2])
        for i in range(0, masks.shape[2]):
            mask = masks[:, :, i]
            image = apply_mask(image, mask, colors[i])
        # display
        cv2.imshow("Mask RCNN", image)
        cv2.waitKey(1)