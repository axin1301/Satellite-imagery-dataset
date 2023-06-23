import os
from PIL import Image
import numpy as np
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

#typ = 'driving'
#area_lut = pd.read_csv('Area_Lut_cbg19.csv')
area_lut = pd.read_csv('../Area_Lut_cbg20.csv')
all_city_list = list(pd.read_csv('../Area_Lut_city.csv')['NAME_process'])
for typ in ['driving']:#, 'walking','cycling']:
    area_list = []
    road_length_list = []
    road_density_list = []
    year_list = []
    state_list = []
    cbg_list_all = []
    city_name_list_all = []
    #for year in range(14,20):
    for year in range(21,22):
        for c in all_city_list:
            #if c == 'Anchorage municipality' or c == 'Urban Honolulu CDP' or c == 'Santa Clarita city' or c == 'San Bernardino city':
            #    continue
            #if c not in ['Santa Clarita city','San Bernardino city']:
            #    continue
            print(year, all_city_list.index(c))
            if not os.path.exists('../out_geojson_cbg'+str(20)+str(year)+'/'+typ+str(20)+str(year)+'/'+c+'_cbg_'+typ+'_'+str(year)+'.csv'):
                continue
            df = pd.read_csv('../out_geojson_cbg'+str(20)+str(year)+'/'+typ+str(20)+str(year)+'/'+c+'_cbg_'+typ+'_'+str(year)+'.csv', low_memory=False)
            #df = pd.read_csv('sjoin_2city/'+c+'_cbg_'+typ+'_'+str(year)+'.csv', low_memory=False)
            #print(df.columns)
            #shapefile = gpd.read_file('../../out_geojson_'+typ+'/'+c+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')
            shapefile = gpd.read_file('../out_geojson'+str(20)+str(year)+'/out_geojson_'+typ+'/'+c+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')
            #print(shapefile1.columns)
            cbg_list = list(set(list(df['CensusBlockGroup'])))
            for cbg in cbg_list:
                #print(cbg)
                df_cbg = df[df['CensusBlockGroup'] == cbg]
                if len(df_cbg) == 0:
                    continue
                id_list = list(df_cbg['id'])
                shapefile_id_list = shapefile.loc[shapefile.id.isin(id_list)]
                #print(shapefile_id_list)
                road_length = shapefile_id_list['length'].dropna().sum()/1000
                #print(road_length)
                area_lut_for_city = area_lut.loc[area_lut.CensusBlockGroup == cbg]
                area_list.append(area_lut_for_city['area'].iloc[0])
                state_list.append(area_lut_for_city['StateFIPS'].iloc[0])
                road_length_list.append(road_length)
                road_density_list.append(road_length/area_lut_for_city['area'].iloc[0])
                year_list.append(str(20)+str(year))
                cbg_list_all.append(cbg)
                city_name_list_all.append(c)

    df = pd.DataFrame({'STATEFP': state_list, 'CityName':city_name_list_all,'CensusBlockGroup':cbg_list_all, 'Year':year_list,'RoadLength':road_length_list, 'Area':area_list, 'RoadDensity':road_density_list})
    #df.to_csv(typ+'_road_density_city1419_2city.csv',index=False)
    df.to_csv(typ+'_road_density_city'+str(20)+str(year)+'.csv',index=False)
