import numpy as np
import cv2
import imutils
from skimage.feature import greycomatrix, greycoprops
import glob

class ImageDescriptor:
    def __init__(self, bins = (8, 12, 3)):
        self.bins = bins
    
    def describe(self, image):
        # convert the image to the HSV color space and initialize
        # the features used to quantify the image
        imageNormal = cv2.resize(image, (300, 300))
        image = cv2.cvtColor(imageNormal, cv2.COLOR_BGR2HSV)
        imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        features = []


        # grab the dimensions and compute the center of the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        # divide the image into four rectangles/segments (top-left,

        # top-right, bottom-right, bottom-left)
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
        (0, cX, cY, h)]
        # construct an elliptical mask representing the center of the
        # image
        (axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
        ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)
        # loop over the segments
        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting
            # the elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # extract a color histogram from the image, then update the
            # feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)
        # extract a color histogram from the elliptical region and
        # update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        # return the feature vector

        # apply sift and get features
        sift = cv2.SIFT_create(30)
        try:
            keyPoints, descriptors = sift.detectAndCompute(imgGray, None)
            for desc in descriptors:
                features.extend(desc)
        except TypeError:
            # if image has no blobs i guess ?
            return None

        # implement texture and add to feature vector
        energyFeature = []
        contrastFeature = []
        step = 25
        size = imgGray.shape

        for i in range(0,size[0],step):
            for j in range(0,size[1],step):
                patch = imgGray[i:i+step,j:j+step]
                glcm = greycomatrix(patch, [1], [0], 256, symmetric=True, normed=True)
                energyFeature.append(greycoprops(glcm, 'energy')[0, 0])
                contrastFeature.append(greycoprops(glcm, 'contrast')[0, 0])

        features.extend(energyFeature)
        features.extend(contrastFeature)
        # features = cv2.normalize(features, features).flatten()
        # features = np.array(features)


        return features

    def histogram(self, image, mask):

		# extract a 3D color histogram from the masked region of the
		# image, using the supplied number of bins per channel
        hist = cv2.calcHist([image], [2], mask, [256], [0, 256])
		# normalize the histogram if we are using OpenCV 2.4
		# return the histogram
        return hist


if __name__ == "__main__":
    iDesc = ImageDescriptor()
    output = open('indexing.csv', "w")
    # use glob to grab the image paths and loop over them
    for imagePath in glob.glob("static/database/*.jpg"):
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)
        # describe the image
        print(f"Describing image: {imagePath}")
        features = iDesc.describe(image)
        if not features:
            continue
        # write the features to file
        features = [str(f) for f in features]
        output.write("database/%s,%s\n" % (imageID, ",".join(features)))
        # break
    # close the index file
    output.close()