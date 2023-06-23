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
    f_list = glob.glob('../SDG_Indicators/SDG 10/WorldPop/cropped_popu_cbg/'+str(year)+'/*/*.tif')
    for f in f_list:
        city_name = f.split('/')[-1].split('.')[0]
        pop_file = gdal.Open(f)
        pop_data = pop_file.ReadAsArray()
        pop_data[pop_data<0] = 0
        WP_population.append(np.sum(pop_data))
        city_list.append(city_name)
        year_list.append(year)

pd_dict = pd.DataFrame({'Name_process':city_list,'Year':year_list, 'WP_population':WP_population})
pd_dict.to_csv('population_statistics_cbg_level.csv', index=False)
