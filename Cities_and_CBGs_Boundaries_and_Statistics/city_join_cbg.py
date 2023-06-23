import geopandas as gpd
import glob

#cbg = gpd.read_file('cbg.geojson')
cbg = gpd.read_file('cbg_2020.geojson')
#print(len(cbg))
print(cbg.crs)
#print(data.columns)
#['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup', CensusBlockGroup', 'State', 'County', 'ClassCode', 'geometry']

#'StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'ClassCode', 'geometry','index_right', 'STATEFP', 'PLACEFP', 'PLACENS', 'GEOID', 'NAME','NAMELSAD', 'LSAD', 'CLASSFP', 'PCICBSA', 'PCINECTA', 'MTFCC','FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON'


shp_list = glob.glob('shape_scd/*.shp')
#shp_list = glob.glob('tilefile_zl19_scd_2/*.shp')
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
    #cbg_with_city[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup','CensusBlockGroup', 'State', 'County', 'ClassCode', 'STATEFP', 'PLACEFP', 'GEOID', 'NAME']].to_csv('cbg_in_city/' + city_name + '_sjoin_cbg.csv',index=False)

    cbg_with_city[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup', 'CensusBlockGroup', 'State', 'County', 'geometry']].to_file('cbg_in_city_new_2_2020/'+city_name +'_cbgs.geojson', driver='GeoJSON')  
    #cbg_with_city[['StateFIPS', 'CountyFIPS', 'TractCode', 'BlockGroup', 'CensusBlockGroup', 'State', 'County', 'ClassCode', 'geometry']].to_file('cbg_in_city_new_2_2020/'+city_name +'_cbgs.geojson', driver='GeoJSON')  



#f_list = glob.glob('cbg_in_city/*.geojson')
f_list = glob.glob('cbg_in_city_new_2_2020/*.geojson')
for f in f_list:
    city_name = f.split('/')[-1].split('.')[0].split('_')[0]
    print(city_name)
    shp = 'shape_scd/'+city_name+'.shp'
    #shp = 'tilefile_zl19_scd_2/'+city_name+'.shp'
    city_tmp = gpd.read_file(shp)
    city_tmp = city_tmp.to_crs(4326)
    cbg = gpd.read_file(f)
    cbg['drop'] = 1
    for i in range(len(cbg)):
        if cbg.at[i,'geometry'].intersection(city_tmp.at[0,'geometry']).area>=cbg.at[i,'geometry'].area*0.1:
            cbg.at[i,'drop'] = 0
    cbg_new = cbg[cbg['drop']==0].drop(['drop'], axis = 1)
    cbg_new.to_file('cbg_in_city_new_2_2020/'+city_name +'_cbgs.geojson', driver='GeoJSON')

