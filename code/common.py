import numpy as np
from scipy.signal import argrelextrema

from ops.image import isolate_galaxy


class Galaxy(object):

    def __init__(self):
        self.ssid = None
        self.matrix = None
        self.threed = None
        self.center = None
        self.sphericity = None
        self.isolated_matrix = None
        self.flux = None
        self.volatility = None

    def calculate_center(self):
        xcenter = int(np.floor(self.matrix.shape[0] / 2.))
        ycenter = int(np.floor(self.matrix.shape[1] / 2.))
        intensity = self.matrix[xcenter][ycenter]
        self.center = [xcenter, ycenter, intensity]

    def calculate_sphericity(self):
        """
        This part defines planar flow, works on array of 3 by N points representing [x, y, pixel_value]
        :param center: [x_center, y_center]
        :return: float between 0 & 1 where higher is more spherical
        """
        assert self.center
        I = [[0., 0.], [0., 0.]]
        total_intensity = 0.
        for point in self.threed:
            total_intensity = total_intensity + point[2]
            deltax = abs(point[0] - self.center[0])
            deltay = abs(point[1] - self.center[1])
            I[0][0] = I[0][0] + point[2] * float(deltax) * (deltax)
            I[1][1] = I[1][1] + point[2] * float(deltay) * (deltay)
            I[1][0] = I[1][0] + point[2] * float(deltax) * (deltay)
        I[0][1] = I[1][0]
        I = I / total_intensity
        determinant = I[0][0] * I[1][1] - I[1][0] * I[0][1]
        trace = I[0][0] + I[1][1]
        self.sphericity = 4.0 / 0.6 * determinant / (trace * trace)  # Threw in a 1/0.6 in order to get values from 0 to 1

    def isolate(self):
        self.isolated_matrix = isolate_galaxy(self.matrix)
        # also add total light intensity at this point, which is just sum of all pixels left
        self.flux = np.sum(self.isolated_matrix)

    def find_local_maxima(self):

        def cross_sections(matrix, ctr):
            horizontal = matrix[ctr[0]]
            vertical = matrix[:, ctr[1]]
            slash = [matrix[i][i] for i in range(matrix.shape[0])]
            backslash = [matrix[matrix.shape[0] - i - 1][i] for i in range(matrix.shape[0])]
            return [horizontal, vertical, slash, backslash]

        hor1, ver1, sl1, bl1 = cross_sections(self.isolated_matrix, self.center)
        scope = 40  # This is how many points to take from the center.
        slices = [hor1, ver1, sl1, bl1]
        max_n_maxima = 0
        for slice in slices:
            center = np.floor(len(slice) / 2)
            func = np.array(slice[int(center - scope):int(center + scope)])
            func = np.convolve(func, [1, 1, 1])
            maxInd = argrelextrema(func, np.greater)
            if len(maxInd[0]) > max_n_maxima:
                max_n_maxima = len(maxInd[0])
        self.volatility = max_n_maxima
