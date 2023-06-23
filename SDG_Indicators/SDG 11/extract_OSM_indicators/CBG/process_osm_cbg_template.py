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
import argparse

def subtask(order,Npara,Nlp,multi_shp_year,typ):
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
        city_name = shp_name.split('/')[-1].split('.')[0].split('_')[0]

        if os.path.exists(typ+str(20)+str(year)+'/'+city_name+'_cbg_'+typ+'_'+str(year)+'.csv'):
            continue

        #if not os.path.exists('../out_geojson'+str(20)+str(year)+'/out_geojson_'+typ+'/'+city_name+'_'+typ+'_'+str(year)+'.geojson'):
        #    continue

        shapefile = gpd.read_file(shp_name, driver = 'geojson') # cbg in shp
        #shapefile = gpd.read_file("city_shape/Michigan_bg_1162.shp")
        print(shp_name)
        #print(shapefile.columns)
        city_name = shp_name.split('/')[-1].split('.')[0].split('_')[0]
        #print(city_name)
        attribute_shp = gpd.read_file('../out_geojson'+str(20)+str(year)+'/out_geojson_'+typ+'/'+city_name+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')

        attr_within_cbg = gpd.sjoin(attribute_shp, shapefile,how = 'inner', op = 'intersects')
        attr_within_cbg.to_csv(typ+str(20)+str(year)+'/'+city_name+'_cbg_'+typ+'_'+str(year)+'.csv', index=False)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='姓名')
    parser.add_argument('--typ', type=str, help='city_name')
    parser.add_argument('--year', type=int, help='city_name')
    args = parser.parse_args()
    
    typ = args.typ #'buildings'
    yyy = args.year
    if not os.path.exists(typ):
        os.mkdir(typ)
    #shp_list = glob.glob('shape_scd/*.shp')
    #shp_list = glob.glob('../../../ACS/cbg_in_city_new_2/*.geojson')
    shp_list = glob.glob('../cbg_in_city_new_2_2020/*.geojson')

    multi_shp_year = []
    for shp_name in shp_list: 
        #for year in range(14,20):
        for year in range(yyy,yyy+1):
            multi_shp_year.append([shp_name,year])

    Npara = 10
    print(len(multi_shp_year))
    Nlp = (len(multi_shp_year)/Npara)
    p = Pool() 
    for i in range(Npara):
        # print(i)
        p.apply_async(func=subtask, args=(str(i),Npara,Nlp,multi_shp_year,typ,))
    p.close()
    p.join()
    print('All subprocesses done.')
