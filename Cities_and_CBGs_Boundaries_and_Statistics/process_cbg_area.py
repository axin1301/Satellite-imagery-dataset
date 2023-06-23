import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

#shp_list = glob.glob('../../cbg_in_city_new/*.geojson')
#shp_list = glob.glob('../../../ACS/cbg_in_city_new/*.geojson')#2014to2019
shp_list = glob.glob('../../../ACS/cbg_in_city_new_2020/*.geojson') #2020to2023

df_final = pd.DataFrame()
cnt = 0
for shp in shp_list:
    d = gpd.read_file(shp,driver = 'geojson')
    print(d.columns)
    d2 = d#.iloc[:10,:]
    city_name = shp.split('/')[-1].split('.')[0]
    print(d.crs)
    d2['geometry'] = d2.geometry.to_crs({'proj': 'cea'})
    d2['area'] = 0.0
    for i in range(len(d2)):
        d2.at[i, 'area'] = d2.at[i, 'geometry'].area/1000000

    df_final = pd.concat([df_final,d2])
    cnt+=len(d)
print(df_final)
#df_final[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'area']].to_csv('Area_Lut_cbg19.csv', index = False)
df_final[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'area']].to_csv('Area_Lut_cbg20.csv', index = False)
print(len(df_final))
print(cnt)

