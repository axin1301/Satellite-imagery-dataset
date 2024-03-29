import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import glob


area_lut = pd.read_csv('../../../../../Cities_and_CBGs_Boundaries_and_Statistics/Area_Lut_city.csv')
# STATEFP,PLACEFP,GEOID,NAME_SHP,NAME_process,ALAND,AWATER,AREA_CAL

#input_files = sorted([i for i in Path('./temp_output/osm_filter/building/city_level').glob('*.geojson')])
input_files = glob.glob('../../../extract_OSM_indicators/out_geojson2023/out_geojson_LU/*.geojson')
landuse_labels = ['commercial', 'industrial', 'construction', 'residential']
LABEL_NAMES = np.asarray(landuse_labels)

#area_list = []
#LU_num_list = []
#building_density_list = []
#city_code_list = []
#city_name_list = []
#year_list = []
area_list = []
building_num_list = []
building_density_list = []
year_list = []
state_list = []
cbg_list_all = []
city_name_list_all = []
segmentation_df = pd.DataFrame()

for f in input_files:
    print(input_files.index(f))
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    #df = gpd.read_file(f, driver='GeoJSON')
    #print(df.columns)
    #city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]
    #print(set(df['landuse']))
    shapefile = gpd.read_file(f, driver = 'geojson')
    shapefile['geometry'] = shapefile.geometry.to_crs({'proj': 'cea'})
    shapefile['area'] = 0.0
    for i in range(len(shapefile)):
        shapefile.at[i,'area'] = shapefile.at[i,'geometry'].area/1000000
    #shapefile['area'] = shapefile['geometry'].area / 1000000
    df_final = shapefile.groupby(['landuse']).agg({'area':'sum'})
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]
    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    tmp_seg_results = {}
    tmp_seg_results['City'] = city_name
    tmp_seg_results['Year'] = int(str(20)+str(year))
    print(year)
    for i in range(len(LABEL_NAMES)):
        if LABEL_NAMES[i] in df_final.index:
            tmp_seg_results[LABEL_NAMES[i]] = [float(df_final.loc[LABEL_NAMES[i],'area']/area_lut_for_city['AREA_CAL'].iloc[0])]
        else:
            tmp_seg_results[LABEL_NAMES[i]] = [0.0]
    #state_list.append(area_lut_for_city['StateFIPS'].iloc[0])
    #year_list.append(int(str(20)+str(year)))
    #city_name_list_all.append(c)
    segmentation_df = pd.concat([segmentation_df,pd.DataFrame(tmp_seg_results)])
segmentation_df.to_csv('LU_density_city'+str(20)+str(year)+'.csv', index = False)
