import pandas as pd
import numpy as np
import warnings
import os, re
import json
import sys
import glob
from multiprocessing import Pool

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
        lines = list(range(order * Nlp, (order + 1) * Nlp))
        print('lines', lines)
        #print('subtask_working')
    
    new_city_list = [city_list[x] for x in lines]
    #print(len(new_city_list))
    print(new_city_list)
    for city in (new_city_list):
        city_ = city.replace(' ','_')
#    if 1:
        for year in range(2021,2024):
        #for year in range(2017,2019):
        #for year in range(2020, 2021):
        #object_detection_list = glob.glob(new_folder_list[i]+'/labels/*.txt')
            #if not city == 'Fort Wayne city':
            #    continue
            # if not city == 'Indianapolis city (balance)':
            #     continue
            if os.path.exists('../final_obd_cbg_DOTA/DOTA_'+city_+'_'+str(year)+'.csv'):
                continue
            print(city, year)
			
            Dir = '../../yolov5-master/runs/val/'

            label_flg = 0

            for nnn in range(7,0,-1):
                if os.path.exists(Dir+'city_year212223/dataset_DOTA_'+str(year)+'_'+city+str(nnn)):
                    label_dir = Dir+'city_year212223/dataset_DOTA_'+str(year)+'_'+city+str(nnn)
                    label_flg = 1
                    break

            if label_flg != 1:
                label_dir = Dir+'city_year212223/dataset_DOTA_'+str(year)+'_'+city_

            label_file_list = glob.glob(label_dir+'/labels/*.txt')
            if len(label_file_list) == 0:
                continue
            print(label_dir)
            imgs_in_cbg_path = 'imgs_within_cbg_2020/imgs_within_cbgs_'+city+'.csv'
            corr_pd = pd.read_csv(imgs_in_cbg_path)
            zl15_list = list(set(corr_pd['CensusBlockGroup']))
            print('len: ',len(zl15_list))
            object_cnt = np.zeros((len(zl15_list),18))
        
            for j in zl15_list:
                img_list = list(corr_pd[corr_pd['CensusBlockGroup'] == j]['img_name'])
                print('len:  ', len(zl15_list) ,len(img_list))
                idx = int(zl15_list.index(j))
            #print(idx)
                for im_name in img_list:
                    if not os.path.exists(label_dir+'/labels/'+im_name + '.txt'):
                        continue
                    data_np = np.loadtxt(label_dir+'/labels/'+im_name + '.txt').reshape(-1,6)
                    for k in range(data_np.shape[0]):
                        object_cnt[idx,int(data_np[k,0])] += 1
                    continue

                print(int(zl15_list.index(j)))
            # continue

                #print(obd_list[0][:obd_list[0].find('/labels')] )
                #data_path = obd_list[0][:obd_list[0].find('/labels')] +'/labels/'+im_name + '.txt'
                #print(data_path)
                #print(data_path)
                #if not os.path.exists(data_path):
                #    continue
                #data_np = np.loadtxt(data_path).reshape(-1,6)
                #print(data_np.shape)
                #if data_np.shape[0]>0:
                #for k in range(data_np.shape[0]):
                    #print(k)
                    #print(data_np[k,0])
                    #print(data_np[k,-1])
                        #if int(data_np[k,0]) == 10:
                        #    continue
                #    object_cnt[idx,int(data_np[k,0])] += 1
                #object_cnt[idx,int(data_np[k,0])+18] += data_np[k,-1]
            #print(object_cnt)
                #print('1 iterrrrr done.')
        #print(object_cnt)
        #np.savetxt('overall_object_cbg/'+i.split('/')[-1].split('.')[0]+'.txt',object_cnt, fmt = '%.5f')
            #pd_dict1 = pd.DataFrame({'cbg_list': zl15_list})
            pd_dict1 = pd.DataFrame({'cbg_list': zl15_list})
            pd_dict2 = pd.DataFrame(object_cnt.astype(int))
            DOTA_cols = ['plane', 'ship', 'storage-tank', 'baseball-diamond', 'tennis-court','basketball-court', 'ground-track-field', 'harbor', 'bridge', 'large-vehicle','small-vehicle', 'helicopter', 'roundabout', 'soccer-ball-field','swimming-pool', 'container-crane', 'airport', 'helipad']
        #col_names = DOTA_cols + [x+'_conf' for x in DOTA_cols]
            pd_dict2.columns = DOTA_cols#names
            print(len(pd_dict2))
            pd_dict2['city'] =city
            pd_dict2['year'] =year
            pd_dict = pd.concat([pd_dict1,pd_dict2],axis = 1)
            print(len(pd_dict))
            pd_dict.to_csv('../final_obd_cbg_DOTA/DOTA_'+city+'_'+str(year)+'.csv', index = False)
        #print(str(cnt)+' done')

if __name__ == '__main__':
    global Npara
    Npara = 10

    cbg_list = glob.glob('imgs_within_cbg_2020/*.csv')
    #cbg_list = glob.glob('../../2021/cbg_in_city_new_2_2020/*.geojson')
    city_list = [x.split('/')[-1].split('_')[-1].split('.')[0] for x in cbg_list]
    #print((city_list))
    #subtask(0,1,1,city_list)
    #for i in range(len(city_list)):
        #city = city_DOTA.at[i,'c_all']
        #city_for_obd = city.replace(' ','_')
        #year = city_DOTA.at[i, 'year']
        #subtask(0,1,1,city_list)
        #if os.path.exists('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd+str(3)):
        #    final_folder_list.append('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd+str(3))
        #elif os.path.exists('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd+str(2)):
        #    final_folder_list.append('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd+str(2))
        #elif os.path.exists('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd):
        #    final_folder_list.append('../../../../image_download/yolov5-master/runs/val/city/dataset_DOTA_'+str(year)+'_'+city_for_obd)

        #imgs_in_cbg_path = '../../../imgs_within_cbg/imgs_within_cbgs_'+city+'.csv'
        ####CensusBlockGroup,State,County,y_tile,x_tile,lng_c,lat_c,img_name

    Nlp = int(len(city_list) / Npara)
    p = Pool()
#    # print(Npara)
    for i in range(Npara):
        # print(i)
        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,city_list,))
#    subtask(str(0),Npara,Nlp,city_list)
    p.close()
    p.join()
    print('All subprocesses done.')

