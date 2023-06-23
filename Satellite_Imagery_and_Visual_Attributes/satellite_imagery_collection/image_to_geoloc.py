import os
import math
import pandas as pd
import numpy as np
import glob

def num2deg1(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg#, lon_deg)

def num2deg2(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return  lon_deg

def concat_str(a,b):
    return str(a)+'_'+str(b)

f_list1 = glob.glob('tilefile_scd/*.csv')
f_list2 = glob.glob('tilefile_zl19_scd_2/*.csv')
f_list = f_list1 + f_list2

for f in f_list:
    f_img_list = pd.read_csv(f)
    print(f_img_list.columns)
    city_name = f.split('/')[-1].split('.')[0]
    #if not city_name in ['St Louis city','St Paul city','St Petersburg city']:
    #    continue
    print(city_name)
    if os.path.exists('tilefile_zl19_scd_geoloc/' + city_name + '.csv'):
        continue
    f_img_list['lng_tl'] = 0.0
    f_img_list['lat_tl'] = 0.0
    f_img_list['lng_br'] = 0.0
    f_img_list['lat_br'] = 0.0
    f_img_list['lng_c'] = 0.0
    f_img_list['lat_c'] = 0.0
    #for i in range(len(f_img_list)):
        #f_img_list.at[i, 'lat_tl'], f_img_list.at[i, 'lng_tl'] = num2deg(f_img_list.at[i, 'x_tile'], f_img_list.at[i, 'y_tile'], 18)
        #f_img_list.at[i, 'lat_br'], f_img_list.at[i, 'lng_br'] = num2deg(f_img_list.at[i, 'x_tile'] + 1, f_img_list.at[i, 'y_tile'] + 1, 18)
        #f_img_list.at[i, 'lng_c'] = (f_img_list.at[i, 'lng_tl'] + f_img_list.at[i, 'lng_br'])/2
        #f_img_list.at[i, 'lat_c'] = (f_img_list.at[i, 'lat_tl'] + f_img_list.at[i, 'lat_br'])/2
    f_img_list['lat_tl'] = f_img_list.apply(lambda x: num2deg1(x['x_tile'], x['y_tile'], 18), axis = 1)
    f_img_list['lng_tl'] = f_img_list.apply(lambda x: num2deg2(x['x_tile'], x['y_tile'], 18), axis = 1)
    f_img_list['lat_br'] = f_img_list.apply(lambda x: num2deg1(x['x_tile'] + 1, x['y_tile'] + 1, 18), axis = 1)
    f_img_list['lng_br'] = f_img_list.apply(lambda x: num2deg2(x['x_tile'] + 1, x['y_tile'] + 1, 18), axis = 1)
    f_img_list['lng_c'] = (f_img_list['lng_tl'] + f_img_list['lng_br'])/2
    f_img_list['lat_c'] = (f_img_list['lat_tl'] + f_img_list['lat_br'])/2
    f_img_list.to_csv('tilefile_zl19_scd_geoloc/' + city_name + '.csv', index=False)


f_list = glob.glob('tilefile_zl19_scd_geoloc/*.csv')
for f in f_list:
    f_img_list = pd.read_csv(f)
    print(f_img_list.columns)
    city_name = f.split('/')[-1].split('.')[0]
    #if not city_name in ['St Louis city','St Paul city','St Petersburg city']:
    #    continue
    print(city_name)
    f_img_list['img_name'] = 's'
    #for i in range(len(f_img_list)):
        #f_img_list.at[i, 'img_name'] = str(f_img_list.at[i, 'y_tile'])+'_'+str(f_img_list.at[i, 'x_tile'])
    f_img_list['img_name'] = f_img_list.apply(lambda x: concat_str(x['y_tile'], x['x_tile']), axis = 1)
    f_img_list.to_csv('tilefile_zl19_scd_geoloc/' + city_name + '.csv', index=False)

