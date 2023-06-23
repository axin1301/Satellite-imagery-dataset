import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd


shp_list = glob.glob('shape_scd_city/*.shp')

df_final = pd.DataFrame()
cnt = 0
for shp in shp_list:
    d = gpd.read_file(shp)
    print(d.columns)
    d2 = d#.iloc[:10,:]
    city_name = shp.split('/')[-1].split('.')[0]
    print(d.crs)
    d2 = d2.to_crs(4326)
    d2['centroid'] = d2['geometry'].map(lambda x:x.centroid)
    df_final = pd.concat([df_final,d2])
    cnt+=len(d)
print(df_final)
df_final[['STATEFP', 'PLACEFP', 'GEOID', 'NAME','centroid']].to_csv('Centroid_city.csv', index = False)
print(len(df_final))
