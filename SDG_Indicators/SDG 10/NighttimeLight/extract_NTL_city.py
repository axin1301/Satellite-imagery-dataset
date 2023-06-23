import json
import glob
import os, shapefile, shutil
import gdal
from scipy.ndimage import zoom
import numpy as np
import pandas as pd

def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / sum_wealths
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)

"""
pop_root_dir= 'NTL_GINI/pop_clip'
NTL_root_dir= 'NTL_GINI/NTL_clip'
for year in range(2016,2021):
    
    gini_list = []
    city_list = []

    pop_file = glob.glob(pop_root_dir + '/' + str(year) + '/*.tif')
    for f in pop_file:
        NTL_f = f.replace('pop','NTL')
        NTL_d = gdal.Open(NTL_f)
        NTL_data = NTL_d.ReadAsArray()
        print(NTL_data.shape)

        pop_d = gdal.Open(f)
        pop_data = pop_d.ReadAsArray()
        print(pop_data.shape)
        pop_data[pop_data<=1] = 0
        pop_data_new = zoom(pop_data, (NTL_data.shape[0]*5 / pop_data.shape[0], NTL_data.shape[1]*5 / pop_data.shape[1]))
        print(pop_data_new.shape)

        B = np.ones((5,5))
        pop_sum = np.ones((NTL_data.shape[0],NTL_data.shape[1]))
        print(pop_sum.shape)
        for i in range(NTL_data.shape[0]):
            for j in range(NTL_data.shape[1]):
                pop_sum[i,j] = np.sum(pop_data_new[i*5:(i+1)*5,5*j:(j+1)*5]*B)
        NTL_valid_idx = np.where(NTL_data > 1) #0
        print(NTL_valid_idx)
        pop_valid_idx = np.where(pop_sum[NTL_valid_idx]>1)
        print(pop_valid_idx)
        gini_list.append(gini_coef(NTL_data[NTL_valid_idx][pop_valid_idx]/pop_sum[NTL_valid_idx][pop_valid_idx]))
        city_list.append(f.split('/')[-1].split('.tif')[0])

    pd_dict = pd.DataFrame({'city':city_list, 'gini_NTL': gini_list})
    pd_dict.to_csv('NTL_GINI/NTL_gini_year_1/NTL_gini_'+str(year)+'.csv', index = False)
"""


#extract-by-mask
#shpfile_list=glob.glob('city_shape_supp/*.shp') #done
#shpfile_list=glob.glob('city_shape_old/*.shp')
#shpfile_list=glob.glob('shape_scd/*.shp')
shpfile_list=glob.glob('shape_scd_2/*.shp')

for year in [2014,2015,2016,2017,2018,2019,2020]:
    input_raster = 'NTL/VNL_v21_npp_'+str(year)+'_global_vcmslcfg_c202205302300.median_masked.dat.tif'
    #input_raster = 'popu_worldpop/pop_USA_mainland_'+str(year)+'.tif'
    input_raster=gdal.Open(input_raster)

    #folderPolyAimMap = 'NTL_GINI/NTL_clip/'+str(year)+'/'
    #folderPolyAimMap = 'NTL_GINI/pop_clip_old/'+str(year)+'/'
    folderPolyAimMap = 'cropped_NTL/'+str(year)+'/'
    #folderPolyAimMap = 'cropped_popu/'+str(year)+'/'
    if not os.path.exists(folderPolyAimMap):
        os.makedirs(folderPolyAimMap)
    # tif输入路径，打开文件
    # input_raster = r"D:/ArcGIS/pop_USA_mainland1.tif"

    for shpfile in shpfile_list:
        print(shpfile)
        input_shape=shpfile
        r = shapefile.Reader(input_shape)
        output_name_tmp=shpfile.split('/')[-1]
        output_name = output_name_tmp.replace('shp','tif')
        # 矢量文件路径，打开矢量文件
        output_raster=folderPolyAimMap+output_name
        #if not os.path.exists(output_raster):
        #    continue
        # 开始裁剪，一行代码，爽的飞起
        ds = gdal.Warp(output_raster,input_raster,format = 'GTiff', outputBounds=r.bbox,cutlineDSName = input_shape,dstNodata = -1)

