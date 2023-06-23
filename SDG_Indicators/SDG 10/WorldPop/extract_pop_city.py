import json
import glob
import os, shapefile, shutil
import gdal
from scipy.ndimage import zoom
import numpy as np
import pandas as pd


#extract-by-mask
shpfile_list=glob.glob('shape_scd_city/*.shp')

for year in [2014,2015,2016,2017,2018,2019,2020]:
    input_raster = 'NTL/VNL_v21_npp_'+str(year)+'_global_vcmslcfg_c202205302300.median_masked.dat.tif'
    #input_raster = 'popu_worldpop/pop_USA_mainland_'+str(year)+'.tif'
    input_raster=gdal.Open(input_raster)

    #folderPolyAimMap = 'cropped_NTL/'+str(year)+'/'
    folderPolyAimMap = 'cropped_popu/'+str(year)+'/'
    if not os.path.exists(folderPolyAimMap):
        os.makedirs(folderPolyAimMap)
    # tif
    # input_raster = r"D:/ArcGIS/pop_USA_mainland1.tif"

    for shpfile in shpfile_list:
        print(shpfile)
        input_shape=shpfile
        r = shapefile.Reader(input_shape)
        output_name_tmp=shpfile.split('/')[-1]
        output_name = output_name_tmp.replace('shp','tif')
        # open vector data
        output_raster=folderPolyAimMap+output_name
        #if not os.path.exists(output_raster):
        #    continue
        # 
        ds = gdal.Warp(output_raster,input_raster,format = 'GTiff', outputBounds=r.bbox,cutlineDSName = input_shape,dstNodata = -1)

