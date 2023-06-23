from scipy.ndimage import zoom
import glob
import geopandas as gpd
import pandas as pd
import numpy as np
import gdal

def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / sum_wealths
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)

#for year in range(2018,2019):
for year in range(2014,2021):
    pop_file=glob.glob('../WorldPop/cropped_popu/'+str(year)+'/*.tif')
    #print(len(pop_file))
    NTL_path = 'cropped_NTL/'+str(year)+'/'

    file_name_list=[]
    pop_value_list=[]
    pop_pixel_num=[]
    gini_list = []

    for file1 in pop_file:
        NTL_data = gdal.Open(NTL_path+ file1.split('/')[-1].split('.')[0]+ '.tif')
        NTL_data = NTL_data.ReadAsArray()
        #NTL_data[NTL_data < 1] = 0
        print(file1.split('/')[-1].split('.')[0])
    #print(NTL_data.shape)
        data = gdal.Open(file1)
        pop_data = data.ReadAsArray()
    #print(pop_data.shape)
        if np.sum(pop_data) == 0:
            continue
        pop_data[pop_data<1] = 0  
        pop_data_new = zoom(pop_data, (NTL_data.shape[0]*5 / pop_data.shape[0], NTL_data.shape[1]*5 / pop_data.shape[1]))
        #NTL_data[NTL_data<1] = 0
        # pop_valid_idx=np.where(pop_data>0)
        print(pop_data_new.shape)

        B = np.ones((5,5))
        pop_sum = np.ones((NTL_data.shape[0],NTL_data.shape[1]))
        for i in range(NTL_data.shape[0]):
            for j in range(NTL_data.shape[1]):
            #print((i+1)*5,(j+1)*5)
                pop_sum[i,j] = np.sum(pop_data_new[i*5:(i+1)*5,5*j:(j+1)*5]*B)
        
        pop_valid_idx = np.where(pop_sum >1)
        NTL_valid_idx = np.where(NTL_data[pop_valid_idx] > 0)
        #print(NTL_data[NTL_valid_idx]/pop_sum[NTL_valid_idx])
        gini_list.append(gini_coef(NTL_data[pop_valid_idx][NTL_valid_idx]/pop_sum[pop_valid_idx][NTL_valid_idx]))
        file_name_list.append(file1.split('/')[-1].split('.')[0])

    pd_file=pd.DataFrame({'city': file_name_list, 'Gini_index':gini_list})
    pd_file.to_csv('NTL_gini_city/NTL_gini_'+str(year)+'.csv', index=False)
