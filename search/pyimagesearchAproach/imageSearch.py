import cv2
import numpy as np

img = cv2.imread('./img/about.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img,(300, 300))

imgFlat = np.float32(img.reshape(img.shape[0] * img.shape[1],3))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
K=3

ret, labels, centers = cv2.kmeans(imgFlat, K, None, criteria, 10, flags)
centers = np.uint8(centers)

indexedImg = centers[[labels.flatten()]]
indexedImg = indexedImg.reshape((img.shape))


# showing
cv2.imshow("img", indexedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()