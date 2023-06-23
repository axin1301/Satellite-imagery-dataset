import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

shp_list = glob.glob('shape_scd/*.shp')
#'STATEFP', 'PLACEFP', 'PLACENS', 'GEOID', 'NAME', 'NAMELSAD', 'LSAD',
#       'CLASSFP', 'PCICBSA', 'PCINECTA', 'MTFCC', 'FUNCSTAT', 'ALAND',
#              'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry'
statefp_list = []
placefp_list =[]
GEOID_list = []
NAME_SHP_list = []
NAME_process_list = []
ALAND_list = []
AWATER_list = []
AREA_CAL_list = []

for shp in shp_list:
    d = gpd.read_file(shp)
    print(d.columns)
    city_name = shp.split('/')[-1].split('.')[0]
    print(d.crs)
    d['geometry'] = d.geometry.to_crs({'proj':'cea'})
    d_area = d.at[0,'geometry'].area
    #d_area = d.to_crs(4326).area#.to_crs(d.crs)
    #print(city_name, d.at[0,'ALAND']/1000000 +  d.at[0,'AWATER']/1000000)
    #print(d_area/1000000)
    
    statefp_list.append(d.at[0,'STATEFP'])
    placefp_list.append(d.at[0,'PLACEFP'])
    GEOID_list.append(d.at[0,'GEOID'])
    NAME_SHP_list.append(d.at[0,'NAME'])
    NAME_process_list.append(city_name)
    ALAND_list.append(d.at[0,'ALAND']/1000000)
    AWATER_list.append(d.at[0,'AWATER']/1000000)
    AREA_CAL_list.append(d_area/1000000)
    
area_lut_pd = pd.DataFrame({'STATEFP':statefp_list, 'PLACEFP':placefp_list, 'GEOID':GEOID_list, 'NAME_SHP':NAME_SHP_list, 'NAME_process':NAME_process_list,'ALAND':ALAND_list,'AWATER':AWATER_list,'AREA_CAL':AREA_CAL_list})
area_lut_pd.to_csv('Area_Lut_city.csv', index=False)
