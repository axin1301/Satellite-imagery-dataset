import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

#shp_list = glob.glob('../../cbg_in_city_new/*.geojson')
#shp_list = glob.glob('../../../ACS/cbg_in_city_new_2/*.geojson')
shp_list = glob.glob('../../../ACS/cbg_in_city_new_2_2020/*.geojson')

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
df_final[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'area']].to_csv('Area_Lut_cbg20.csv', index = False)
print(len(df_final))
print(cnt)

"""
OUTPUT_PATH = Path('./output/environmental_determinants/basic_statistics/area')
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

city_lut = pd.read_csv('./city_defination_and_LUTs/city_look_up_table.csv')
city_lut = city_lut[['CityName','CityCode']]
city_lut = city_lut.drop_duplicates()

area = pd.read_csv('./city_defination_and_LUTs/Major_Towns_and_Cities_(December_2015)_Boundaries_V2.csv')[['TCITY15CD','Shape__Area']]
area = city_lut.merge(area, left_on = 'CityCode', right_on = 'TCITY15CD',how='left')
area['Area'] = area['Shape__Area']
area = area[['CityName','CityCode','Area']]
area['Area'] /= 1000000
area = area.sort_values(['CityCode'], ascending=True)

area.to_csv(OUTPUT_PATH.joinpath('area_city.csv'),index=False)
"""
