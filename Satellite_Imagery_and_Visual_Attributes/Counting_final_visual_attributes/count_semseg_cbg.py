import pandas as pd
import numpy as np
import warnings
import os, re
import json
import sys
import glob
from multiprocessing import Pool
import os

def subtask(order,Npara,Nlp,city_list):
    order = int(order)
    #print('Npara',Npara)
    if order == Npara - 1:
        # print(len(lng_lat))
        lines = list(range(order * Nlp, len(city_list)))
        print('lines',lines)
        # print(lines)
    
    else:
        print(order)
        # print(order*Nlp,(order+1)*Nlp)
        lines = list(range(order * Nlp, (order + 1) * Nlp))
        print('lines', lines)
        # lines=list(range(5))
        #print('subtask_working')

    new_city_list = [city_list[x] for x in lines]
    print(len(new_city_list))
    c_list = []
    y_list = []
    #for year in range(2020,2021): 
    for year in range(2021,2024): 
        for city in new_city_list:
            print('year: ', year)
            print('city: ', city)

            if os.path.exists('semseg_results_cbg212223/semseg_'+city+'_'+str(year)+'.csv'):
                continue
            #if city == 'Houston city' and year == 2015:
            #    continue
            #if city == 'Seattle city' and year == 2020:
            #    continue
   
            imgs_in_cbg_path = '../tongji_image_feature/code/imgs_within_cbg_2020/imgs_within_cbgs_'+city+'.csv'
            #print(len(imgs_in_cbg_path))

                    #print()
            if not os.path.exists('../ViT-Adapter-main-mine/segmentation/semseg_results_212223/'+city+'_'+str(year)+'_imgs_semseg.csv'):
                continue

            df = pd.read_csv('../ViT-Adapter-main-mine/segmentation/semseg_results_212223/'+city+'_'+str(year)+'_imgs_semseg.csv')

            corr_pd = pd.read_csv(imgs_in_cbg_path)
            print(corr_pd.columns)
            seg_info_f = pd.merge(corr_pd,df, on = 'img_name')
            seg_info_f.drop(['img_name'], axis = 1, inplace = True)
            print('seg_info_f ',len(seg_info_f))
            seg_info_mean = seg_info_f.groupby(['CensusBlockGroup']).mean().reset_index()
            seg_info_mean['year'] = year
            seg_info_mean['city'] = city
            seg_info_mean.to_csv('semseg_results_cbg212223/semseg_'+city+'_'+str(year)+'.csv', index = False)

            #df_final.drop(['img_name'], axis = 1, inplace = True)
            #df_final['city'] = city
            #df_final_mean = df_final.groupby(['city']).mean().reset_index()
            #df_final_mean['year'] = year
            #df_final_mean.to_csv('semseg_results_city/semseg_'+city+'_'+str(year)+'.csv', index = False)
    #cy_df = pd.DataFrame({'city':c_list, 'year':y_list})
    #cy_df.to_csv('no_semseg_city_list.csv', index = False)

if __name__ == '__main__':
    global Npara
    Npara = 1 

    if not os.path.exists('semseg_results_cbg212223'):
        os.makedirs('semseg_results_cbg212223')


    cbg_list = glob.glob('../2021/cbg_in_city_new_2_2020/*.geojson')
    city_list = [x.split('/')[-1].split('_')[0] for x in cbg_list]
    print((city_list))
    #city_list = ['Phoenix city']


    Nlp = int(len(city_list) / Npara)
#    p = Pool()
    # print(Npara)
#    for i in range(Npara):
#        # print(i)
#        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,city_list,))
    subtask(str(0),Npara,Nlp,city_list)
#    p.close()
#    p.join()
    print('All subprocesses done.')

