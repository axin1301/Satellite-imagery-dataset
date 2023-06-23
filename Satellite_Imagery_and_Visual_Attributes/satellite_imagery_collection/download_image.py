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

def subtask(order,Npara,Nlp,csv_file_list,token):
    order = int(order)
    if order == Npara - 1:
        lines = list(range(order * Nlp, len(csv_file_list)))
        print(lines)
    else:
        #print(order)
        lines = list(range(order * Nlp, (order + 1) * Nlp))
        print(lines)
    print(str(order) + '  subtask_working')

    base_url = 'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/48376/'  #2021 #########important number
    
    new_lines = [csv_file_list[x] for x in lines]
    print(new_lines)
    for csv_file in new_lines:
        city = csv_file.split('/')[-1].split('.')[0]
        #if city[0] not in ['F','G','H','I','J','L']:
        #    continue

        Dir = 'zl19_images/'+str(year)+'/'+city
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        print(csv_file)
        print(city)

        csv_file_data = pd.read_csv(csv_file)
        for i in range(len(csv_file_data)):

            msk = np.zeros((256*2, 256*2,3))
    
            y_tile = int(csv_file_data.at[i,'y_tile'])
            x_tile = int(csv_file_data.at[i,'x_tile'])
            print(y_tile, x_tile)
           
            if os.path.exists(Dir+'/'+str(y_tile)+'_'+str(x_tile)+'.png'):
                continue

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
                sleep(2)
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


def main(csv_file_list):
    p = Pool()
    # print(Npara)
    for i in range(Npara):
        # print(i)
        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,csv_file_list,token,))
    p.close()
    p.join()
    print('All subprocesses done.')
    # lng_lat.to_csv('sat2region.csv')


if __name__ == '__main__':
    global Npara
    Npara = 4
    global year
    year = 2021     #########important
    time_start = time.time()
    global token
    token = "AAPKa7a4264aebcd4ecc96154431a9b5689e0koHP6jXg1hMciQYnJOT-F2JWPFQPKUW-gfYPNXj3iMj3yQJBvuso1rQCyIJ6USM"
    #global token
    #token = 'AAPK868a38acc94c49c6b5fe93ec72d782848w26DEckXxsIoRYE1oI_rnk57Q3YYwSCh9xYvKNT5cmcS2N5v5RHyL-TZrX1jVDA'
    
    csv_file_list = glob.glob('tilefile_scd/*.csv')#[:20]
    print(len(csv_file_list))
    
    # city_tmp_list = ['Henderson city','Houston city','Indianapolis city (balance)','Los Angeles city']
    # csv_file_list = ['tilefile_scd/'+x+'.csv' for x in city_tmp_list]


    global Nlp
    Nlp = int(len(csv_file_list) / Npara)

    main(csv_file_list)

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
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/44710/'  #2022
#     'https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/46399/'  #2023


# ]



