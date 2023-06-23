import pandas as pd
import os, shapefile, shutil
import shapely
import glob

#c_list = list(pd.read_csv('cities_without_shp.csv')['city'])
#city_list = [x+' city' for x in c_list]
#state_no = list(pd.read_csv('cities_without_shp.csv')['state_code'])

city_list = ['Santa Clarita city','San Bernardino city'] #city name and state name
state_no = [6,6]


print(len(city_list))

list1 = []
list2 = []
shp_list = glob.glob('../prescribing/US_SHAPEFILE_city/*/*.shp')
for shp in shp_list:
    #print(shp.split('.shp')[0])
    #sf=shapefile.Reader(shp.split('.shp')[0])
    #print(shp[:-4])
    sf=shapefile.Reader(shp[:-4])
    for shaperec in sf.iterShapeRecords():
        if shaperec.record['NAMELSAD'] in city_list:
            city_idx = int(city_list.index(shaperec.record['NAMELSAD']))
            if int(shaperec.record['STATEFP']) != int(state_no[city_idx]):
                continue

            print(shaperec.record['NAMELSAD'])
            if shaperec.record['NAMELSAD'] == 'St. Paul city':
                cname = 'St Paul city'
            elif shaperec.record['NAMELSAD'] == 'St. Louis city':
                cname = 'St Louis city'
            elif shaperec.record['NAMELSAD'] == 'St. Petersburg city':
                cname = 'St Petersburg city'
            elif shaperec.record['NAMELSAD'] == 'Louisville/Jefferson County metro government (balance)':
                cname = 'Louisville-Jefferson County metro government (balance)'
            else:
                cname = shaperec.record['NAMELSAD']

#St. Louis city.prj       St. Paul city.prj        St. Petersburg city
            #list1.append(shaperec.record['NAMELSAD'])
            print(shaperec.record['STATEFP'])

            #list2.append(shaperec.record['STATEFP'])
             
#pd_dict = pd.DataFrame({'city':list1, 'STATEFP':list2})
#pd_dict.to_csv('100_large_city_state.csv', index=False)
            #w = shapefile.Writer('city_shape_supp/'+shaperec.record['NAMELSAD'])
            #w = shapefile.Writer('shape_scd/'+shaperec.record['NAMELSAD'])
            w = shapefile.Writer('shape_scd_city/'+cname)
            #w = shapefile.Writer('tilefile_zl19_scd/'+cname)
            w.fields = sf.fields
            w.record(*shaperec.record)
            w.shape(shaperec.shape)
            w.close()
            #prj_file = shp.split('.')[0]+'.prj'
            prj_ori = shp.replace('.shp','.prj')
            #print(prj_ori)
            prj_file = 'shape_scd_city/'+cname+'.prj'
            #prj_file = 'tilefile_zl19_scd/'+cname+'.prj'
            #print(prj_file)

            if os.path.exists(prj_ori):
                shutil.copy(prj_ori, prj_file)

