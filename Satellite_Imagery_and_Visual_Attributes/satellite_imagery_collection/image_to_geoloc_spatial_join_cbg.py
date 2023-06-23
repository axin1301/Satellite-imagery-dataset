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

"""
boundary = gpd.read_file('boundary_msoa.geojson', driver = 'geojson') #[['MSOACode', 'MSOAName', 'CityCode', 'CityName']]
d = pd.read_csv('sat_features_mosa.csv')
boundary_tmp = boundary[~boundary['MSOAName'].isin(list(d['MSOAName']))]
print(len(boundary_tmp))
print(set(boundary_tmp['CityName']))
print(boundary_tmp[boundary_tmp['CityName']=='Birmingham'])
boundary = gpd.GeoDataFrame(boundary_tmp)
boundary.crs = 'EPSG:4326'
"""


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
    #if os.path.exists('imgs_within_cbg/imgs_within_cbgs_'+city_name+'.csv'):
    #    continue
    #else:
    #    print(city_name)

    #if os.path.exists('cbg_in_city_new/'+city_name+'_cbgs.geojson'):
    #    boundary = gpd.read_file('cbg_in_city_new/'+city_name+'_cbgs.geojson')
    #elif os.path.exists('cbg_in_city_new_2/'+city_name+'_cbgs.geojson'):
    #    boundary = gpd.read_file('cbg_in_city_new_2/'+city_name+'_cbgs.geojson')
    #else:
    #    continue
    boundary = gpd.read_file('cbg_in_city_new_2/'+city_name+'_cbgs.geojson')
    #imgs_all = pd.concat([imgs_all,f_img_list],axis = 0)
    imgs_all = f_img_list
    print(len(imgs_all))
    print(imgs_all.columns)

    points = gpd.GeoDataFrame(imgs_all, geometry=gpd.points_from_xy(imgs_all.lng_c, imgs_all.lat_c)) #指定经纬度坐标所在列
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

