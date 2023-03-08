import numpy as np
from .api import *

def Centering(dset_raw, threshold, inspect_range=3, double_count_range=5):
    threshold_min, threshold_max = threshold
    height, width = np.shape(dset_raw)
    inspect_range_distance = round((inspect_range-1)/2)

    dset = dset_raw
    dset = np.hstack(
        (dset, np.zeros((inspect_range_distance, height), dtype=np.uint16).T))
    dset = np.hstack(
        (np.zeros((inspect_range_distance, height), dtype=np.uint16).T, dset))
    dset = np.hstack(
        (dset.T, np.zeros((inspect_range_distance, width + inspect_range_distance*2), dtype=np.uint16).T))
    dset = np.hstack(
        (np.zeros((inspect_range_distance, width + inspect_range_distance*2), dtype=np.uint16).T, dset))
    dset = dset.T
    width, height = np.shape(dset)

    in_threshold = np.where((dset < threshold_min) | (dset > threshold_max), 0, 1)
    highest_dset = np.ones((width, height), dtype=np.uint16)
    # sum_int_dset = np.zeros((width, height))

    tmp_dset = dset.astype(np.int16)

    # inspect_range_distance ^2 の範囲で中心が高いものを探す
    distance = inspect_range_distance
    for i in range(-distance, distance+1):
        for j in range(-distance, distance+1):
            if i == 0 and j == 0:
                continue
            highest_dset = np.multiply(highest_dset, np.signbit(
                np.roll(tmp_dset, (i, j), axis=(0, 1)) - tmp_dset))
            # sum_int_dset += np.roll(dset, (i, j), axis=(0, 1))

    writeImage(highest_dset, "highest_dset_raw")
    highest_dset = np.multiply(highest_dset, in_threshold)

    def CenterOfGravity(array):
        ry, rx = array.shape
        tile_x = np.tile(np.arange(1, rx+1, 1, dtype=np.uint16), (ry, 1))
        tile_y = np.tile(np.arange(1, ry+1, 1, dtype=np.uint16), (rx, 1)).T
        array_sum = np.sum(array)
        cx = np.sum(array * tile_x) / array_sum - rx/2 - 1
        cy = np.sum(array * tile_y) / array_sum - rx/2 - 1
        return cy, cx, array_sum
    
    sum_highest_dset = np.copy(highest_dset)
    distance = (inspect_range_distance + double_count_range)
    for i in range(-distance, distance+1):
        for j in range(-distance, distance+1):
            if i == 0 and j == 0:
                continue
            sum_highest_dset += np.roll(highest_dset, (i, j), axis=(0, 1))
    
    writeImage(sum_highest_dset, "sum_highest_dset")
    # sum_highest_dset = np.multiply(highest_dset, sum_highest_dset)
    # doble_count_dset = np.where(sum_highest_dset > 1, 1, 0)
    # single_count_dset = np.where(sum_highest_dset == 1, 1, 0)
    single_count = np.where(np.multiply(highest_dset, sum_highest_dset) == 1)

    single_count_length = single_count[0].shape[0]
    single_count_list = []

    for i in range(single_count_length):
        center_y, center_x, intensity = CenterOfGravity(dset[
            single_count[0][i] - inspect_range_distance: single_count[0][i] + inspect_range_distance+1,
            single_count[1][i] - inspect_range_distance: single_count[1][i] + inspect_range_distance+1
        ])
        single_count_list.append([
            np.round(center_x + single_count[0][i], decimals=2),
            np.round(center_y + single_count[1][i], decimals=2),
            intensity.tolist()
        ])


    # for i in range(inspect_range_distance + double_count_range, width - inspect_range_distance * 2 - double_count_range * 2):
    #     for j in range(inspect_range_distance + double_count_range, height - inspect_range_distance * 2 - double_count_range * 2):
    #         if highest_dset[i, j] > 0:
    #             if highest_dset[i, j] == np.sum(highest_dset[i-inspect_range_distance + double_count_range:i+inspect_range_distance+1 + double_count_range, j-inspect_range_distance + double_count_range:j+inspect_range_distance+1 + double_count_range]):
    #                 single_count_dset[i, j] = sum_int_dset[i, j]
    #                 center_y, center_x = CenterOfGravity(dset[i - inspect_range_distance: i +
    #                                                         inspect_range_distance+1, j - inspect_range_distance: j +
    #                                                         inspect_range_distance+1])
    #                 single_count_list.append(
    #                     np.append([center_y + i - inspect_range_distance, center_x + j - inspect_range_distance], sum_int_dset[i, j]))
    #             else:
    #                 doble_count_dset[i, j] = sum_int_dset[i, j]

    # single_count_list = np.array(single_count_list)
    # single_count_list = np.round(single_count_list, decimals=2)

    highest_dset = highest_dset[inspect_range_distance:-inspect_range_distance, inspect_range_distance:-inspect_range_distance]
    sum_highest_dset = sum_highest_dset[inspect_range_distance:-inspect_range_distance, inspect_range_distance:-inspect_range_distance]
    # single_count_dset = single_count_dset[inspect_range_distance:-inspect_range_distance, inspect_range_distance:-inspect_range_distance]
    # doble_count_dset = doble_count_dset[inspect_range_distance:-inspect_range_distance, inspect_range_distance:-inspect_range_distance]


    # writeImage(dset_raw, "dset_raw")
    # writeImage(dset, "dset")
    # print(np.max(dset), "dset max")
    # print(threshold, "threshold range")
    # writeImage(in_threshold, "thres")
    # writeImage(highest_dset, "highest_dset")
    # writeImage(single_count_dset, "single_count_dset")
    # writeImage(doble_count_dset, "doble_count_dset")

    return sum_highest_dset, single_count_list
