import os
import geopandas as gpd
import pandas as pd
import numpy as np
import glob

#boundary = gpd.read_file('boundary_msoa.geojson')
#print(len(boundary))
#print(boundary.columns)
#print(len(list(set(list(boundary['MSOAName'])))))
#print((list(set(list(boundary['CityName'])))))


imgs_all = pd.DataFrame()
f_list = glob.glob('tilefile_zl19_scd_geoloc/*.csv')
for f in f_list:
    f_img_list = pd.read_csv(f)
    #print(len(f_img_list))
    f_img_list.drop_duplicates(subset = ['img_name'], keep = 'last', inplace = True)
    #print(len(f_img_list))
    #print(f_img_list.columns)
    city_name = f.split('/')[-1].split('.')[0]
    print(city_name)

    boundary = gpd.read_file('cbg_in_city_new/'+city_name+'_cbgs.geojson') # 2014-2019
    #imgs_all = pd.concat([imgs_all,f_img_list],axis = 0)
    imgs_all = f_img_list
    print(len(imgs_all))
    print(imgs_all.columns)

    points = gpd.GeoDataFrame(imgs_all, geometry=gpd.points_from_xy(imgs_all.lng_c, imgs_all.lat_c)) #longitude, latitude
    points.crs = 'EPSG:4326'
    points_with_boundary = gpd.sjoin(boundary,points,how="inner", op='contains')
    points_with_boundary[['CensusBlockGroup','State','County','y_tile','x_tile','lng_c','lat_c','img_name']].to_csv('imgs_within_cbg/imgs_within_cbgs_'+city_name+'.csv', index = False)
    print(points_with_boundary.columns)
    print(len(points_with_boundary))


"""
f_list = glob.glob('imgs_within_cbg/*.csv')
for f in f_list:
    df = pd.read_csv(f)
    df[['CensusBlockGroup','State','County','y_tile','x_list','lng_c','lat_c','img_name']].to_csv(f, index=False)
"""

