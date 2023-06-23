import matplotlib.pyplot as plt
from pyrosm import OSM
from pyrosm import get_data
import pandas as pd
import geopandas as gpd
import glob
from multiprocessing import Pool
import os
import time
import glob

def subtask(order,Npara,Nlp,shp_list,city_state_lut,state_osm_lut,multi_shp_year,typ):
    order = int(order)
    #print(order)
    Nlp = int(Nlp)
    if order == Npara - 1:
        #print(order, Nlp, len(multi_shp_year))
        lines = list(range(order * Nlp, len(multi_shp_year)))
        #print(lines)
    else:
        #print(order, Nlp, len(multi_shp_year))
        lines = list(range(order * Nlp, (order + 1) * Nlp))
        #print(lines)
    print(str(order) + '  subtask_working')

    new_lines = [multi_shp_year[x] for x in lines]
    #print(new_lines)
    print(len(new_lines))
    for k in (new_lines):
        shp_name = k[0]
        year = k[1]
        shapefile = gpd.read_file(shp_name)
        #shapefile = gpd.read_file("city_shape/Michigan_bg_1162.shp")
        print(shp_name)
        #print(shapefile.columns)
        city_name = shp_name.split('/')[-1].split('.')[0]
        print(city_name)
        state_name = list(city_state_lut.loc[city_state_lut['city_y']==city_name]['state'])[0]
        print(state_name)
        state_osm_name = list(state_osm_lut.loc[state_osm_lut['state1']==state_name]['state2'])[0]
        print(state_osm_name)

        #osm = OSM('us_osm_pbf/'+state_osm_name+'-' +str(year) + '0101.osm.pbf', bounding_box=shapefile.iloc[0,:]['geometry'])
        osm = OSM('us_osm_pbf2021/'+state_osm_name+'-' +str(year) + '0101.osm.pbf', bounding_box=shapefile.iloc[0,:]['geometry'])
        #drive_net = osm.get_network(network_type="walking")
        #drive_net = osm.get_network(network_type="driving")
        #drive_net = osm.get_network(network_type=typ)
        drive_net = osm.get_buildings()
        #drive_net.to_file('out_geojson_'+typ+'/' +city_name + '_'+typ+'_'+str(year)+'.geojson', driver='GeoJSON')
        #drive_net.to_file('out_geojson_2city/' +city_name + '_'+typ+'_'+str(year)+'.geojson', driver='GeoJSON') #14~20
        drive_net.to_file('out_geojson2021/out_geojson_'+typ+'/' +city_name + '_'+typ+'_'+str(year)+'.geojson', driver='GeoJSON')
        #drive_net.plot()
        #plt.show()
        #plt.savefig('out_png/Detroit_city_walking_'+str(year)+'.png')
        #plt.savefig('out_png/Detroit_city_driving_'+str(year)+'.png')
        #plt.savefig('out_png/Detroit_city_cycling'+str(year)+'.png')

if __name__ == '__main__':
    
    typ = 'buildings'
    #shp_list = glob.glob('shape_scd/*.shp')
    #shp_list = glob.glob('shape_scd_2/*.shp')
    shp_list = glob.glob('shape_scd/*.shp') + glob.glob('shape_scd_2/*.shp')
    city_state_lut = pd.read_csv('shape_summary_merge.csv')
    state_osm_lut = pd.read_csv('state4osm.csv')

    multi_shp_year = []
    for shp_name in shp_list: 
        #for year in range(14,21):
        for year in range(21,22):
            city_name = shp_name.split('/')[-1].split('.')[0]
            print(city_name)
            state_name = list(city_state_lut.loc[city_state_lut['city_y']==city_name]['state'])[0]
            #print(state_name)
            state_osm_name = list(state_osm_lut.loc[state_osm_lut['state1']==state_name]['state2'])[0]
            #if not os.path.exists('out_geojson_'+typ+'/' +city_name + '_'+typ+'_'+str(year)+'.geojson'):
            if not os.path.exists('out_geojson2021/out_geojson_'+typ+'/' +city_name + '_'+typ+'_'+str(year)+'.geojson'):
                multi_shp_year.append([shp_name,year])

    Npara = 10
    print(len(multi_shp_year))
    Nlp = (len(multi_shp_year)/Npara)
    p = Pool() 
    for i in range(Npara):
        # print(i)
        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,shp_list,city_state_lut,state_osm_lut,multi_shp_year,typ,))
    p.close()
    p.join()
    print('All subprocesses done.')
