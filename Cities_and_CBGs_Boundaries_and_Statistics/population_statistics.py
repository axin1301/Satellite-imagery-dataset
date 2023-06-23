import gdal
import pandas as pd
import numpy as np
import glob
import os
import math
gdal.AllRegister()
print("Run!")

city_list = []
year_list = []
WP_population = []

for year in range(2014,2021):
    f_list = glob.glob('cropped_popu/'+str(year)+'/*.tif')
    for f in f_list:
        city_name = f.split('/')[-1].split('.')[0]
        if f.split('/')[-1].split('.')[0] in ['Urban Honolulu CDP','Anchorage municipality']:
            continue
        pop_file = gdal.Open(f)
        pop_data = pop_file.ReadAsArray()
        pop_data[pop_data<0] = 0
        WP_population.append(np.sum(pop_data))
        city_list.append(city_name)
        year_list.append(year)

pd_dict = pd.DataFrame({'Name_process':city_list,'Year':year_list, 'WP_population':WP_population})
pd_dict.to_csv('population_statistics_city_level.csv', index=False)



"""
file_list = glob.glob('NTL_GINI/pop_clip_old/'+str(2016)+'/*.tif')
city_list = [x.split('/')[-1].split('.')[0] for x in file_list]
pop_array = np.zeros((len(city_list),5))

for city in city_list:
    row = int(city_list.index(city))
    for year in range(2016,2021):
        col = year - 2016
        pop_file = gdal.Open('NTL_GINI/pop_clip_old/'+str(year)+'/'+city+'.tif')
        pop_data = pop_file.ReadAsArray()
        pop_data[pop_data<0] = 0
        pop_array[row,col] = np.sum(pop_data)

col_names = [2016,2017,2018,2019,2020]
data_df = pd.DataFrame(pop_array, columns = col_names)
pd_dict = pd.DataFrame({'city':city_list})
pd_final = pd.concat([pd_dict, data_df], axis = 1)
pd_final.to_csv('population_statistics_old.csv', index=False)
"""        


"""
for year in [2016,2017,2018]:
    country_tif=gdal.Open('pop_USA_mainland_'+str(year)+'.tif')
    country = country_tif.ReadAsArray()
    print('country.shape', country.shape)

    tmpGeoTransform = country_tif.GetGeoTransform()

    csv_file_list = glob.glob('tilefile_multiple_zl_lnglat/*/*.csv')
    for f in csv_file_list:
        d = pd.read_csv(f)
        print(str(csv_file_list.index(f))+str('/')+str(len(csv_file_list)))
        zl = int(f.split('/')[1])

        if not os.path.exists('tile_popu/tilefile_multiple_zl_popu_'+str(year)+'/'+str(zl)):
            os.makedirs('tile_popu/tilefile_multiple_zl_popu_'+str(year)+'/'+str(zl))
    
        d['pop'] = 0.0

        for i in range(len(d)):
            y_init = int(math.floor((d.at[i,'top_left_lat'] -tmpGeoTransform[3])/tmpGeoTransform[5]))
            x_init = int(math.floor((d.at[i,'top_left_lng'] -tmpGeoTransform[0])/tmpGeoTransform[1]))
            x_end = int(math.ceil((d.at[i,'bottom_right_lng']-tmpGeoTransform[0])/tmpGeoTransform[1]))
            y_end = int(math.ceil((d.at[i,'bottom_right_lat']-tmpGeoTransform[3])/tmpGeoTransform[5]))

        #print(x_init,y_init,x_end,y_end)
            popu_tmp = np.array(country_tif.ReadAsArray(x_init,y_init,x_end-x_init,y_end-y_init))
            popu_tmp[popu_tmp<0] = 0
            d.at[i,'pop'] = np.sum(popu_tmp)

        d.to_csv('tile_popu/tilefile_multiple_zl_popu_'+str(year)+'/'+str(zl)+'/'+f.split('/')[-1], index=False)

"""
