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

cbg_in_city_list = glob.glob('../../../prescribing/cbg_in_city_new/*.geojson')
#cbg_in_city_list = glob.glob('../../../prescribing/cbg_in_city_new_2020/*.geojson')
city_name_list = [x.split('/')[-1].split('.')[0] for x in cbg_in_city_list]

for year in range(2014,2020):
#for year in range(2020,2021):
    file_name_list=[]
    pop_value_list=[]
    pop_pixel_num=[]
    gini_list = []
    city_name_csv = []

    #for city in ['Denver city_cbgs']:#city_name_list:
    for city in city_name_list:
        print(city)
        pop_file=glob.glob('../WorldPop/cropped_popu_cbg/'+str(year)+'/'+city+'/*.tif')
        #print(len(pop_file))
        NTL_path = 'cropped_NTL_cbg/'+str(year)+'/'+city+'/'

        #file_name_list=[]
        #pop_value_list=[]
        #pop_pixel_num=[]
        #gini_list = []
        #city_name_csv = []

        #for file1 in ['cropped_popu_cbg/'+str(2020)+'/'+'Denver city_cbgs'+'/080310027052.tif']:#pop_file:080310041093 080310027052
        for file1 in pop_file: #
            NTL_data = gdal.Open(NTL_path+ file1.split('/')[-1].split('.')[0]+ '.tif')
            NTL_data = NTL_data.ReadAsArray()
            #print(file1.split('/')[-1].split('.')[0])
            #print(NTL_data.shape)
            data = gdal.Open(file1)
            pop_data = data.ReadAsArray()
            #print(pop_data)
            #NTL_valid_idx = np.where(NTL_data > 0)
            #print(len(NTL_valid_idx[0]))
            #pop_valid_idx = np.where(pop_data >=1)
            #print(len(pop_valid_idx[0]))
            if np.sum(pop_data) == 0:
                pop_pixel_num.append(np.sum(pop_data))
                gini_list.append(0)
                file_name_list.append(file1.split('/')[-1].split('.')[0])
                city_name_csv.append(city)
                continue
            pop_data[pop_data<1] = 0
            pop_data_new = zoom(pop_data, (NTL_data.shape[0]*5 / pop_data.shape[0], NTL_data.shape[1]*5 / pop_data.shape[1]))
        #NTL_data[NTL_data<1] = 0
        # pop_valid_idx=np.where(pop_data>0)
            #print(pop_data_new.shape)

            B = np.ones((5,5))
            pop_sum = np.ones((NTL_data.shape[0],NTL_data.shape[1]))
            for i in range(NTL_data.shape[0]):
                for j in range(NTL_data.shape[1]):
            #print((i+1)*5,(j+1)*5)
                    pop_sum[i,j] = np.sum(pop_data_new[i*5:(i+1)*5,5*j:(j+1)*5]*B)

            #NTL_valid_idx = np.where(NTL_data > 1)
            #print(NTL_data[NTL_valid_idx]/pop_sum[NTL_valid_idx])
            #pop_pixel_num.append(np.sum(pop_data))
            #gini_list.append(gini_coef(NTL_data[NTL_valid_idx]/pop_sum[NTL_valid_idx]))
            pop_valid_idx = np.where(pop_sum >=1)
            #print(len(pop_valid_idx[0]))
            #print(NTL_data[pop_valid_idx])
            if len(pop_valid_idx[0])<=1:
                pop_pixel_num.append(np.sum(pop_data))
                gini_list.append(0)
            else:
                NTL_valid_idx = np.where(NTL_data[pop_valid_idx] > 0)
                #print(len(NTL_valid_idx[0]))
                if len(NTL_valid_idx[0])<=1:
                    pop_pixel_num.append(np.sum(pop_data))
                    gini_list.append(0)
                else:
                    pop_pixel_num.append(np.sum(pop_data))
            #print(NTL_data[NTL_valid_idx]/pop_sum[NTL_valid_idx])
                    gini_list.append(gini_coef(NTL_data[pop_valid_idx][NTL_valid_idx]/pop_sum[pop_valid_idx][NTL_valid_idx]))
                    #print(gini_coef(NTL_data[pop_valid_idx][NTL_valid_idx]/pop_sum[pop_valid_idx][NTL_valid_idx]))
            file_name_list.append(file1.split('/')[-1].split('.')[0])
            city_name_csv.append(city)


    pd_file=pd.DataFrame({'city':city_name_csv, 'cbg_name': file_name_list, 'Gini_index':gini_list,'popu_num':pop_pixel_num})
    pd_file.to_csv('NTL_gini_cbg/NTL_gini_'+str(year)+'.csv', index=False)
