import geopandas as gpd
import glob
import os

if not os.path.exists('cbg_in_city_new'):
    os.mkdir('cbg_in_city_new')

if not os.path.exists('cbg_in_city_new_2020'):
    os.mkdir('cbg_in_city_new_2020')

#cbg = gpd.read_file('../prescribing/cbg.geojson') #2014 to 2019
cbg = gpd.read_file('../prescribing/cbg_2020.geojson') # 2020 to 2023
#print(len(cbg))
print(cbg.crs)
#print(data.columns)
#['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup', CensusBlockGroup', 'State', 'County', 'ClassCode', 'geometry']

#'StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'ClassCode', 'geometry','index_right', 'STATEFP', 'PLACEFP', 'PLACENS', 'GEOID', 'NAME','NAMELSAD', 'LSAD', 'CLASSFP', 'PCICBSA', 'PCINECTA', 'MTFCC','FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON'


shp_list = glob.glob('shape_scd_city/*.shp')
for shp in shp_list:
    city_name = shp.split('/')[-1].split('.')[0]
    print(city_name)
    city_tmp = gpd.read_file(shp)
    print(city_tmp.crs)
    city_tmp = city_tmp.to_crs(4326)
    cbg_with_city = gpd.sjoin(cbg,city_tmp,how='inner',op='intersects')
    #cbg_with_city = gpd.sjoin(cbg, city_tmp, how='inner', op = 'within')
    #cbg_with_city = gpd.sjoin(cbg,city_tmp.to_crs(4326),how='inner',op='intersects')
    #print(cbg_with_city.columns)
    #print(len(cbg_with_city))
    #cbg_with_city[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'ClassCode', 'STATEFP', 'PLACEFP', 'GEOID', 'NAME']].to_csv('cbg_in_city_new/' + city_name + '_sjoin_cbg.csv',index=False) #2014to2020

    cbg_with_city[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup', 'CensusBlockGroup', 'State', 'County', 'geometry']].to_file('cbg_in_city_new_2020/'+city_name +'_cbgs.geojson', driver='GeoJSON') #2020to2023 



#f_list = glob.glob('cbg_in_city/*.geojson')
f_list = glob.glob('cbg_in_city_new_2020/*.geojson')
for f in f_list:
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    print(city_name)
    #shp = 'tilefile_zl19_scd/'+city_name+'.shp'
    city_tmp = gpd.read_file(shp)
    city_tmp = city_tmp.to_crs(4326)
    cbg = gpd.read_file(f)
    cbg['drop'] = 1
    for i in range(len(cbg)):
        if cbg.at[i,'geometry'].intersection(city_tmp.at[0,'geometry']).area>=cbg.at[i,'geometry'].area*0.1:
            cbg.at[i,'drop'] = 0
    cbg_new = cbg[cbg['drop']==0].drop(['drop'], axis = 1)
    cbg_new.to_file('cbg_in_city_new_2020/'+city_name +'_cbgs.geojson', driver='GeoJSON')

