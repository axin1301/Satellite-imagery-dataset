import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

"""
OUTPUT_PATH = Path('./temp_output/walkability/daily_living_score')
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

poi = pd.read_csv('./temp_output/poi/poi.csv',dtype='str')

selected_naics = ['4451','44551','445110','44512','445120','71219','481','482','483','485']
poi['NAICSCode_3'] = poi['NAICSCode'].map(lambda x: x[:3])

poi = poi[poi['NAICSCode'].isin(selected_naics) | poi['NAICSCode_3'].isin(selected_naics)].drop(['NAICSCode_3'],axis=1)
poi['Count'] = pd.Series([1 for _ in range(poi.shape[0])])
poi = poi[['CityName','CityCode','Count']]
poi = poi.groupby(['CityName','CityCode']).sum().reset_index()
"""

area_lut = pd.read_csv('./Area_Lut_city.csv')
# STATEFP,PLACEFP,GEOID,NAME_SHP,NAME_process,ALAND,AWATER,AREA_CAL

#input_files = sorted([i for i in Path('./temp_output/osm_filter/pois/city_level').glob('*.geojson')])
input_files = glob.glob('../out_geojson_pois/*.geojson')

area_list = []
pois_num_list = []
pois_density_list = []
#city_code_list = []
city_name_list = []
year_list = []

for f in input_files:
    print(f)
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    if city_name in ['Anchorage municipality','Urban Honolulu CDP']:
        continue
    df = gpd.read_file(f, driver='GeoJSON')
    pois_num = df.shape[0]
    #city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    year = f.split('/')[-1].split('.')[0].split('_')[-1]
    area_lut_for_city = area_lut.loc[area_lut.NAME_process == city_name]

    area_list.append(area_lut_for_city['AREA_CAL'].iloc[0])
    pois_num_list.append(pois_num)
    pois_density_list.append(pois_num/area_lut_for_city['AREA_CAL'].iloc[0])
    city_name_list.append(city_name)
    year_list.append(int(str(20)+str(year)))

df = pd.DataFrame({'CityName':city_name_list, 'Year':year_list, 'PoiNum':pois_num_list, 'Area':area_list, 'PoiDensity':pois_density_list})
df = df.sort_values(by=['CityName','Year'],ascending=True)
df.to_csv('daily_living_score_city.csv',index=False)


    #poi['DailyLivingScore'] = poi['Count'] / poi['Area']
