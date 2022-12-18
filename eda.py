import os
import glob
from collections import namedtuple

import numpy as np
import SimpleITK as sitk
import pandas as pd


def xyz2irc(coords_xyz, origin_xyz, vxSize_xyz, direction_a):
    origin_a = np.array(origin_xyz)
    vxSize_a = np.array(vxSize_xyz)
    coord_a = np.array(coords_xyz)
    
    cri_a = ((coord_a - origin_a) @ np.linalg.inv(direction_a)) / vxSize_a
    cri_a - np.round(cri_a)
    return (int(cri_a[2]), int(cri_a[1]), int(cri_a[0]))


NoduleInfo = namedtuple(
    'NoduleInfo',
    'seriesuid, nodule_loc, diameter_mm'
)

df = pd.read_csv('data/annotations.csv')
paths = glob.glob('data/subset*/*.mhd')

on_disk = {os.path.split(path)[1][:-4] for path in paths}

nodule_info_list = []

for _, row in df.iterrows():
    seriesuid = row['seriesuid']
    
    if seriesuid not in on_disk:
        continue

    nodule_loc = row['coordX'], row['coordY'], row['coordZ']
    diameter_mm = row['diameter_mm']
    nodule_info_list.append(NoduleInfo(seriesuid, nodule_loc, diameter_mm))
