#from datetime import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import glob

#OUTPUT_PATH = Path('./output/environmental_determinants/built_environment/road_density')
#OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

#input_files = sorted([i for i in Path('./temp_output/osm_filter/pois/city_level').glob('*.geojson')])

typ = 'driving'
#input_files = glob.glob('../out_geojson_'+typ+'/*.geojson')
input_files = glob.glob('../out_geojson_2city/*'+typ+'*.geojson')
#area_lut = pd.read_csv('./Area_Lut_city.csv')
area_lut = pd.read_csv('./Area_Lut_city_2city.csv')
# STATEFP,PLACEFP,GEOID,NAME_SHP,NAME_process,ALAND,AWATER,AREA_CAL

# Driving Net
#input_files = sorted([i for i in Path('./temp_output/osm_filter/road_network/city_level').glob('*driving.geojson')])

area_list = []
road_length_list = []
road_density_list = []
year_list = []
city_name_list = []

for f in input_files:
    df = gpd.read_file(f, driver='GeoJSON')
    road_length = df['length'].dropna().sum()/1000
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    print(city_name)
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]

    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    road_length_list.append(road_length)
    road_density_list.append(road_length/area_lut_for_city['AREA_CAL'].iloc[0])
    city_name_list.append(area_lut_for_city['NAME_process'].iloc[0])
    year_list.append(year)

df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list,'RoadLength':road_length_list, 'Area':area_list, 'RoadDensity':road_density_list})
#df.to_csv(typ+'_road_density_city.csv',index=False)
df.to_csv(typ+'_road_density_city_2city.csv',index=False)
    #df.to_csv(OUTPUT_PATH.joinpath('driving_road_density_city.csv'),index=False)

typ = 'walking'
#input_files = glob.glob('../out_geojson_'+typ+'/*.geojson')
input_files = glob.glob('../out_geojson_2city/*'+typ+'*.geojson')
area_list = []
road_length_list = []
road_density_list = []
year_list = []
city_name_list = []

for f in input_files:
    df = gpd.read_file(f, driver='GeoJSON')
    road_length = df['length'].dropna().sum()/1000
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    print(city_name)
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]

    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    road_length_list.append(road_length)
    road_density_list.append(road_length/area_lut_for_city['AREA_CAL'].iloc[0])
    city_name_list.append(area_lut_for_city['NAME_process'].iloc[0])
    year_list.append(year)

df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list,'RoadLength':road_length_list, 'Area':area_list, 'RoadDensity':road_density_list})
#df.to_csv(typ+'_road_density_city.csv',index=False)
df.to_csv(typ+'_road_density_city_2city.csv',index=False)


typ = 'cycling'
#input_files = glob.glob('../out_geojson_'+typ+'/*.geojson')
input_files = glob.glob('../out_geojson_2city/*'+typ+'*.geojson')
area_list = []
road_length_list = []
road_density_list = []
year_list = []
city_name_list = []

for f in input_files:
    df = gpd.read_file(f, driver='GeoJSON')
    road_length = df['length'].dropna().sum()/1000
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    print(city_name)
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]

    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    road_length_list.append(road_length)
    road_density_list.append(road_length/area_lut_for_city['AREA_CAL'].iloc[0])
    city_name_list.append(area_lut_for_city['NAME_process'].iloc[0])
    year_list.append(year)

df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list,'RoadLength':road_length_list, 'Area':area_list, 'RoadDensity':road_density_list})
#df.to_csv(typ+'_road_density_city.csv',index=False)
df.to_csv(typ+'_road_density_city_2city.csv',index=False)
