import numpy as np
import csv
import cv2
from .pyimagesearch_indexer import ImageDescriptor


class Searcher:
    def __init__(self, indexPath):
		# store our index path
        self.indexPath = indexPath
    def search(self, queryFeatures, limit = 10):
        # initialize our dictionary of results
        results = {}
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                features = [float(x) for x in row[1:]]
                d = self.chi2_distance(features, queryFeatures)
                print(d)

                results[row[0]] = d
            # close the reader
            f.close()
        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list)
        results = sorted([(v, k) for (k, v) in results.items()])

        return results[:limit]


    def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])
        return d


def search(queryLocation, indexPath, limit=10):
    iDesc = ImageDescriptor((8, 12, 3))
    queryImg = cv2.imread(queryLocation)
    features = iDesc.describe(queryImg)

    searcher = Searcher(indexPath)
    results = searcher.search(features, limit)

    names = []
    for (d, name) in results:
        names.append(name)

    return names

if __name__ == '__main__':
    search('test.jpg', 'indexing.csv', 1)