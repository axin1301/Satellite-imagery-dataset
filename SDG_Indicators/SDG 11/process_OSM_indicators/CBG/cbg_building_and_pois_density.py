from PIL import Image
import numpy as np
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

#typ = 'driving'
area_lut = pd.read_csv('../../../../../Cities_and_CBGs_Boundaries_and_Statistics/Area_Lut_cbg20.csv')
all_city_list = list(pd.read_csv('../../../../../Cities_and_CBGs_Boundaries_and_Statistics/Area_Lut_city.csv')['NAME_process'])

for typ in ['buildings']:
    area_list = []
    building_num_list = []
    building_density_list = []
    year_list = []
    state_list = []
    cbg_list_all = []
    city_name_list_all = []
    #for year in range(14,21):
    for year in range(20,21):
        for c in all_city_list:
            print(year, all_city_list.index(c))
            df = pd.read_csv(typ+'/'+c+'_cbg_'+typ+'_'+str(year)+'.csv', low_memory=False)
            #print(df.columns)
            shapefile = gpd.read_file('../../../extract_OSM_indicators/CBG/out_geojson_'+typ+'/'+c+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')
            #print(shapefile1.columns)
            cbg_list = list(set(list(df['CensusBlockGroup'])))
            for cbg in cbg_list:
                df_cbg = df[df['CensusBlockGroup'] == cbg]
                if len(df_cbg) == 0:
                    continue
                id_list = list(df_cbg['id'])
                shapefile_id_list = shapefile.loc[shapefile.id.isin(id_list)]
                #print(shapefile_id_list)
                building_num = shapefile_id_list.shape[0]

                building_num_list.append(building_num)
                area_lut_for_city = area_lut.loc[area_lut.CensusBlockGroup == cbg]
                area_list.append(area_lut_for_city['area'].iloc[0])
                state_list.append(area_lut_for_city['StateFIPS'].iloc[0])
                building_density_list.append(building_num/area_lut_for_city['area'].iloc[0])
                year_list.append(str(20)+str(year))
                cbg_list_all.append(cbg)
                city_name_list_all.append(c)

    df = pd.DataFrame({'state': state_list,'CityName':city_name_list_all,'CensusBlockGroup':cbg_list_all, 'Year':year_list,'BuildingNum':building_num_list, 'Area':area_list, 'BuildingDensity':building_density_list})
    df.to_csv(typ + '_density_cbg20.csv',index=False)

for typ in ['pois']:
    area_list = []
    building_num_list = []
    building_density_list = []
    year_list = []
    state_list = []
    cbg_list_all = []
    city_name_list_all = []
    #for year in range(14,21):
    for year in range(20,21):
        for c in all_city_list:
            print(year, all_city_list.index(c))
            df = pd.read_csv(typ+'/'+c+'_cbg_'+typ+'_'+str(year)+'.csv')
            #print(df.columns)
            shapefile = gpd.read_file('../../../extract_OSM_indicators/CBG/out_geojson_'+typ+'/'+c+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')
            #print(shapefile1.columns)
            cbg_list = list(set(list(df['CensusBlockGroup'])))
            for cbg in cbg_list:
                df_cbg = df[df['CensusBlockGroup'] == cbg]
                if len(df_cbg) == 0:
                    continue
                id_list = list(df_cbg['id'])
                shapefile_id_list = shapefile.loc[shapefile.id.isin(id_list)]
                #print(shapefile_id_list)
                building_num = shapefile_id_list.shape[0]

                building_num_list.append(building_num)
                area_lut_for_city = area_lut.loc[area_lut.CensusBlockGroup == cbg]
                area_list.append(area_lut_for_city['area'].iloc[0])
                state_list.append(area_lut_for_city['StateFIPS'].iloc[0])
                building_density_list.append(building_num/area_lut_for_city['area'].iloc[0])
                year_list.append(str(20)+str(year))
                cbg_list_all.append(cbg)
                city_name_list_all.append(c)

    df = pd.DataFrame({'state': state_list,'CityName':city_name_list_all,'CensusBlockGroup':cbg_list_all, 'Year':year_list,'POINum':building_num_list, 'Area':area_list, 'POIDensity':building_density_list})
    df.to_csv(typ + '_density_cbg20.csv',index=False)
