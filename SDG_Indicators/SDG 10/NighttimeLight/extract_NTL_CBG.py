import geopandas as gpd
import json
import glob
import os, shapefile, shutil
import gdal
from scipy.ndimage import zoom
import numpy as np
import pandas as pd
import rasterio as rio
from rasterio.mask import mask

def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / sum_wealths
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)

#extract-by-mask
#shpfile_list=glob.glob('shape_scd/*.shp')
#cbg_in_city_list = glob.glob('../ACS/cbg_in_city_new_2/*.geojson')
cbg_in_city_list = glob.glob('../ACS/cbg_in_city_new_2_2020/*.geojson')

#cbg_list = gpd.read_file(cbg_in_city_list[0])
#print(len(cbg_list))
#print(cbg_list.columns)
#cbg_list.to_crs(4326)

#with open(cbg_in_city_list[0]) as data_file:    
#    geoms= json.load(data_file)
#city_name = cbg_in_city_list[0].split('/')[-1].split('.')[0]
#print(len(geoms))
#print(list(geoms.keys()))
#print([list(geoms['features'])[0]])

for j in range(len(cbg_in_city_list)):
    with open(cbg_in_city_list[j]) as data_file:
        geoms= json.load(data_file)
    city_name = cbg_in_city_list[j].split('/')[-1].split('.')[0]
    print(city_name)

    for year in ['2020']:#[2014,2015,2016,2017,2018,2019]:#,2020]:
        print(year)
        #input_raster = 'NTL/VNL_v21_npp_'+str(year)+'_global_vcmslcfg_c202205302300.median_masked.dat.tif'
        input_raster = 'popu_worldpop/pop_USA_mainland_'+str(year)+'.tif'
    #input_raster=gdal.Open(input_raster)
        with rio.open(input_raster) as src:

    #folderPolyAimMap = 'NTL_GINI/NTL_clip/'+str(year)+'/'
    #folderPolyAimMap = 'NTL_GINI/pop_clip_old/'+str(year)+'/'
            #folderPolyAimMap = 'cropped_NTL_cbg/'+str(year)+'/'+city_name+'/'
            folderPolyAimMap = 'cropped_popu_cbg/'+str(year)+'/'+city_name+'/'
            if not os.path.exists(folderPolyAimMap):
                os.makedirs(folderPolyAimMap)
            for i in range(len(list(geoms['features']))):
                #print(i)
                out_image, out_transform = mask(src,[list(geoms['features'])[i]['geometry']], crop=True)
        #hh = gpd.read_file('shape_scd/Dallas city.shp')
#            out_image, out_transform = mask(src,hh.geometry, crop=True)
                out_meta = src.meta.copy()
                out_meta.update({"driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform})
            
                output_name =str(list(geoms['features'])[i]['properties']['CensusBlockGroup'])+'.tif'
                output_name = folderPolyAimMap+output_name

                with rio.open(output_name, 'w', **out_meta) as dst:
                    dst.write(out_image)

    # tif输入路径，打开文件
    # input_raster = r"D:/ArcGIS/pop_USA_mainland1.tif"

    #for shpfile in shpfile_list:
    #    print(shpfile)
    #    input_shape=shpfile
    #    r = shapefile.Reader(input_shape)
    #    output_name_tmp=shpfile.split('/')[-1]
    #    output_name = output_name_tmp.replace('shp','tif')
#    for i in range(3):#len(cbg_list)):
#        print(i)
        #r = cbg_list.iloc[[i]]#.at[i,'geometry']
        #output_name = cbg_list.at[i,'CensusBlockGroup']+'.tif'
        
        # 矢量文件路径，打开矢量文件
#        output_raster=folderPolyAimMap+output_name
        # 开始裁剪，一行代码，爽的飞起
#        ds = gdal.Warp(output_raster,input_raster,format = 'GTiff', outputBounds=r,dstNodata = -1)
