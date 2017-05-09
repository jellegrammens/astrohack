import numpy as np


def reshape_to_3d_array(arr):
    pic_list = np.array([[0, 0, arr[0][0]]])
    for i in range(1, arr.shape[0]):
        for j in range(1, arr.shape[1]):
            pic_list = np.append(pic_list, [[int(i), int(j), arr[i][j]]], axis=0)
    return pic_list


