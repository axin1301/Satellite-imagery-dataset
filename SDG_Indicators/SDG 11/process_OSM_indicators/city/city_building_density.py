import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import glob

area_lut = pd.read_csv('../../../../../Cities_and_CBGs_Boundaries_and_Statistics/Area_Lut_city.csv')

# STATEFP,PLACEFP,GEOID,NAME_SHP,NAME_process,ALAND,AWATER,AREA_CAL


input_files = glob.glob('../../../extract_OSM_indicators/out_geojson2021/out_geojson_buildings/*.geojson')


area_list = []
building_num_list = []
building_density_list = []
#city_code_list = []
city_name_list = []
year_list = []

for f in input_files:
    #print(f)

    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    year = f.split('/')[-1].split('.')[0].split('_')[-1]

    print(f)
    df = gpd.read_file(f, driver='GeoJSON')
    building_num = df.shape[0]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]
    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    building_num_list.append(building_num)
    building_density_list.append(building_num/area_lut_for_city['AREA_CAL'].iloc[0])
    #city_code_list.append(city_code)
    city_name_list.append(city_name)
    year_list.append(int(str(20)+str(year)))

df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list, 'BuildingNum':building_num_list, 'Area':area_list, 'BuildingDensity':building_density_list})
df = df.sort_values(by=['CityName','Year'],ascending=True)
df.to_csv('building_density_city2021.csv',index=False)
print(len(df))
