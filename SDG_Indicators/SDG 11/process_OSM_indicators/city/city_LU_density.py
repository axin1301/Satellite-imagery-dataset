import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import geopandas as gpd
import glob

#OUTPUT_PATH = Path('./output/environmental_determinants/built_environment/building_density')
#OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

area_lut = pd.read_csv('../Area_Lut_city.csv')
# STATEFP,PLACEFP,GEOID,NAME_SHP,NAME_process,ALAND,AWATER,AREA_CAL

#input_files = sorted([i for i in Path('./temp_output/osm_filter/building/city_level').glob('*.geojson')])
input_files = glob.glob('../out_geojson2023/out_geojson_LU/*.geojson')
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
    #if city_name == 'Anchorage municipality' or city_name == 'Urban Honolulu CDP':
    #    continue
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


"""
    df['geometry'] = df.geometry.to_crs({'proj':'cea'})
    for i in range(len(df)):
        d_area = df.at[i,'geometry'].area
        #print(d_area/1000000)
        print(area_lut_for_city['AREA_CAL'].iloc[0])
        df.at[i,'AREA_percentage'] = d_area/1000000/area_lut_for_city['AREA_CAL'].iloc[0]

df = df.groupby(['landuse']).agg({'AREA_percentage':'sum'}).reset_index()
df.to_csv('tmp_LU/'+city_name+'_'+year+'_LU.csv', index = True)
"""

"""
    building_num = df.shape[0]
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]

    #d['geometry'] = d.geometry.to_crs({'proj':'cea'})
    #d_area = d.at[0,'geometry'].area

    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    building_num_list.append(building_num)
    building_density_list.append(building_num/area_lut_for_city['AREA_CAL'].iloc[0])
    #city_code_list.append(city_code)
    city_name_list.append(city_name)
    year_list.append(int(str(20)+str(year)))

    df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list, 'BuildingNum':building_num_list, 'Area':area_list, 'BuildingDensity':building_density_list})
    df = df.sort_values(by=['CityName','Year'],ascending=True)
    df.to_csv('building_density_city.csv',index=False)
"""
