# -*- coding: utf-8 -*-
#from shapely.geometry import Polygon
#import scipy.io as scio
import pandas as pd
import glob
import csv
import cv2 as cv
#import shutil
#from shapely.geometry import Point
import numpy as np
import random
import os
#from PIL import Image
from multiprocessing import Pool
import os
import urllib.request
import random
from time import sleep
import argparse
import ast
import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import glob

def subtask(order,Npara,Nlp,full_pd,token):
    order = int(order)
    if order == Npara - 1:
        lines = list(range(order * Nlp, len(f_list)))
        #print(lines)
    else:
        #print(order)
        lines = list(range(order * Nlp, (order + 1) * Nlp))
        #print(lines)
    print(str(order) + '  subtask_working')

    base_url = 'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/14765/'
    
    new_lines = full_pd.iloc[lines,:]
    new_lines.reset_index(inplace=True)
    print(len(new_lines))
    cities = list(set(list(new_lines['city'])))
    print(len(cities))
    for city in cities:
        Dir = 'zl19_images/'+str(year)+'/'+city
        if not os.path.exists(Dir):
            os.makedirs(Dir)

    msk = np.zeros((256*2, 256*2,3))
    for i in range(len(new_lines)):
        y_tile = int(new_lines.at[i,'y_tile'])
        x_tile = int(new_lines.at[i,'x_tile'])
            #print(y_tile, x_tile)
            
            #if str(y_tile)+'_'+str(x_tile) in download_list:
            #    continue;
        filename1 = Dir + '/' + str(y_tile*2) + '_' + str(x_tile*2) + '.png'
        filename2 = Dir + '/' + str(y_tile*2+1) + '_' + str(x_tile*2) + '.png'
        filename3 = Dir + '/' + str(y_tile*2) + '_' + str(x_tile*2+1) + '.png'
        filename4 = Dir + '/' + str(y_tile*2+1) + '_' + str(x_tile*2+1) + '.png'

        url1 = base_url + str(19) + '/' + str(y_tile*2) + '/' + str(x_tile*2)   +'?token='+token
        url2 = base_url + str(19) + '/' + str(y_tile*2+1) + '/' + str(x_tile*2)   +'?token='+token
        url3 = base_url + str(19) + '/' + str(y_tile*2) + '/' + str(x_tile*2+1)   +'?token='+token
        url4 = base_url + str(19) + '/' + str(y_tile*2+1) + '/' + str(x_tile*2+1)   +'?token='+token
            #print('url',url4)

        try:
            urllib.request.urlretrieve(url1,filename1)
            urllib.request.urlretrieve(url2,filename2)
            urllib.request.urlretrieve(url3,filename3)
            urllib.request.urlretrieve(url4,filename4)
        except:
            sleep(1)
            urllib.request.urlretrieve(url1,filename1)
            urllib.request.urlretrieve(url2,filename2)
            urllib.request.urlretrieve(url3,filename3)
            urllib.request.urlretrieve(url4,filename4)
        im1 = cv.imread(filename1)
        im2 = cv.imread(filename2)
        im3 = cv.imread(filename3)
        im4 = cv.imread(filename4)
        msk[:256,:256,:] = im1
        msk[256:,:256,:] = im2
        msk[:256,256:,:] = im3
        msk[256:,256:,:] = im4
        cv.imwrite(Dir+'/'+str(y_tile)+'_'+str(x_tile)+'.png', msk)
            #print('good')
        os.remove(filename1)
            #print('remove_op done1')
        os.remove(filename2)
            #print('remove_op done2')
        os.remove(filename3)
            #print('remove_op done3')
        os.remove(filename4)
            #print('remove_op done4')


def main():
    p = Pool()
    # print(Npara)
    for i in range(Npara):
        # print(i)
        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,full_pd,token,))
    p.close()
    p.join()
    print('All subprocesses done.')
    # lng_lat.to_csv('sat2region.csv')


if __name__ == '__main__':
    global Npara
    Npara = 100
    global year
    year = 2017
    time_start = time.time()
    # token = "AAPKa7a4264aebcd4ecc96154431a9b5689e0koHP6jXg1hMciQYnJOT-F2JWPFQPKUW-gfYPNXj3iMj3yQJBvuso1rQCyIJ6USM"
    global token
    token = 'AAPK868a38acc94c49c6b5fe93ec72d782848w26DEckXxsIoRYE1oI_rnk57Q3YYwSCh9xYvKNT5cmcS2N5v5RHyL-TZrX1jVDA'
    undone_file = pd.read_csv('undone_file/statis_2017_undone.csv')
    city_list = list(undone_file[undone_file['LikeOld']==1]['city'])
    city = city_list[0]
    global full_pd
    full_pd = pd.read_csv('../../tilefile_scd/'+city+'.csv')
    full_pd['city'] = city
    for city in city_list[1:]:
        if city == 'Anchorage municipality':
            continue
        df = pd.read_csv('../../tilefile_scd/'+city+'.csv')
        df['city'] = city
        full_pd = pd.concat([full_pd, df])

    print(len(full_pd))
    ######### new_down
    downloaded_file = []
    for city in city_list:
        downloaded_file = downloaded_file +  glob.glob('zl19_images/'+str(year)+'/'+city+'/*.png')
    print(len(downloaded_file))
    ######### old_down
    """
    undone_file.fillna(0, inplace=True)
    city_list2 = list(undone_file[undone_file['LikeOld']==1]['dir_name'])
    for city in city_list2:
        #print(city)
        if not os.path.exists('../zl19_images/'+str(year)+'/'+str(city)):
            continue 
        downloaded_file = downloaded_file +  glob.glob('../zl19_images/'+str(year)+'/'+city+'/*.png')
    print(len(downloaded_file))
    """
    downloaded_list = [x.split('/')[-1].split('.')[0] for x in downloaded_file]
    print(downloaded_list[:10])
    dd_y = [int(x.split('_')[0]) for x in downloaded_list]
    dd_x = [int(x.split('_')[1]) for x in downloaded_list]
    dd_dict = pd.DataFrame({'y_tile':dd_y, 'x_tile':dd_x})
    print(len(dd_dict))
    down_oldtime = pd.read_csv('down_oldtime/'+str(year)+'.csv')
    full_pd = pd.concat([full_pd, dd_dict, down_oldtime])
    full_pd.drop_duplicates(subset = ['y_tile','x_tile'], keep = False, inplace = True)
    full_pd.reset_index(drop=True)
    #print(full_pd.head(5))
    #print(full_pd.tail(5))
    print(len(full_pd))

    global Nlp
    Nlp = int(len(full_pd) / Npara)

    main()

    time_end = time.time()
    print('cost_time', time_end - time_start, 's')



# base_url = "https://tiledbasemaps.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/"
# base_urls=[
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/31144/', #14nian 6yue11
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/11952/',  #15nian 6 yue
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/11509/'],  #2016.6
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/14765/',   # 2017.6.14
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/8249/',   #2018.6.6
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/645/',      #2019.6.26
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/11135/']    #2020.6.10
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/48376/'     #2021.6.9


# ]



