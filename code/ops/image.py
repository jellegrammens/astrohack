import numpy as np
from skimage import measure
from scipy import ndimage


def isolate_galaxy(galaxy_image):

    contour = find_contour(galaxy_image)
    # Reshape the contour to make an actual image matrix
    contour_image = np.zeros((galaxy_image.shape[0], galaxy_image.shape[1]))
    for i in range(len(contour)):
        x = int(np.floor(contour[i][0]))
        y = int(np.floor(contour[i][1]))

        contour_image[x][y] = 1

    # Then fill in the contour with ones to make a contour filter.
    contour_image = ndimage.binary_fill_holes(contour_image)

    # Then convolve the contour filter with the original image
    # to get a picture of the galaxy alone
    theGalaxy = myconvolve(galaxy_image, contour_image)

    return theGalaxy


def myconvolve(image1, image2):
    new_image = image1[:]
    if image1.shape != image2.shape:
        print("No way Jose! Your images are not the same size.")
        return -1
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            new_image[i][j] = image1[i][j]*image2[i][j]
    return new_image


def contour_centroid(points):
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    centroid = (sum(x) / len(points), sum(y) / len(points))
    return centroid


def find_contour(pic):
    # Find contours ==> value to be optimised (by image)
    contours = measure.find_contours(pic, 0.1)
    # Calculate centroids of all contours
    centroid = []
    for i in range(len(contours)):
        centroid.append(contour_centroid(contours[i]))
    # Calculate distance between centroids and center of image
    ctr = (np.floor([pic.shape[1]/2, pic.shape[0]/2])).astype(int)
    dist = []
    for i in range(len(centroid)):
        dist.append(np.linalg.norm(np.floor(list(centroid[i]) - ctr)))
    # Minimal distance between centroid and center of image gives the target contour
    index_min = dist.index(min(dist))
    return contours[index_min]


