

import os
import errno

import rasterio
import numpy as np

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


src_path = "/sciclone/aiddata10/REU/geo/raw/esa_landcover_v207/ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2015-v2.0.7.tif"
dst_dir_path = "/sciclone/aiddata10/REU/geo/data/rasters/esa_landcover_v207"

make_dir(dst_dir_path)


mapping = {
    0: [0],
    10: [10, 11, 12],
    20: [20],
    30: [30, 40],
    50: [50, 60, 61, 62, 70, 71, 72, 80, 81, 82, 90, 100, 160, 170],
    110: [110, 130],
    120: [120, 121, 122],
    140: [140, 150, 151, 152, 153],
    180: [180],
    190: [190],
    200: [200, 201, 202],
    210: [210],
    220: [220]
}


start_year = 1992

with rasterio.open(src_path) as src:

    profile = src.profile
    profile.update(count=1)

    # 24 years/bands
    for i in range(24):

        year = start_year + i
        band = i + 1

        print "Running year: {0} (band: {1})".format(year, band)

        array = src.read(band)

        for new_cat in mapping.keys():

            for old_cat in mapping[new_cat]:

                array = np.where(array == old_cat, new_cat, array)

        dst_path = "{0}/esa_lc_{1}.tif".format(dst_dir_path, year)
        make_dir(os.path.dirname(dst_path))

        with rasterio.open(dst_path, 'w', **profile) as dst:
            dst.write(array, 1)

