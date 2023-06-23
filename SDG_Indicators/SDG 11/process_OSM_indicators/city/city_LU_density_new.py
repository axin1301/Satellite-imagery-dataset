from PIL import Image
import numpy as np
import geopandas as gpd
import numpy as np
import pandas as pd
from pathlib import Path
import glob
import geopandas as gpd

#typ = 'driving'
area_lut = pd.read_csv('Area_Lut_cbg.csv')
all_city_list = list(pd.read_csv('../../process_post_osm/Area_Lut_city.csv')['NAME_process'])
#landuse_labels = ['grass', 'commercial', 'recreation_ground', 'churchyard', 'industrial', 'pond', 'reservoir', 'construction', 'basin', 'residential', 'railway', 'farmland', 'cemetery', 'quarry', 'retail', 'forest']
landuse_labels = ['commercial', 'industrial', 'construction', 'residential']
LABEL_NAMES = np.asarray(landuse_labels)

for typ in ['LU']:
    area_list = []
    building_num_list = []
    building_density_list = []
    year_list = []
    state_list = []
    cbg_list_all = []
    city_name_list_all = []
    segmentation_df = pd.DataFrame()
    for year in range(14,21):
        for c in all_city_list[20:]:
            if c == 'Anchorage municipality' or c == 'Urban Honolulu CDP':
                continue
            print(year, all_city_list.index(c))
            df = pd.read_csv(typ+'/'+c+'_cbg_'+typ+'_'+str(year)+'.csv')
            #print(df.columns)
            shapefile = gpd.read_file('../../out_geojson_'+typ+'/'+c+'_'+typ+'_'+str(year)+'.geojson', driver = 'geojson')
            #print(shapefile1.columns)
            cbg_list = list(set(list(df['CensusBlockGroup'])))
            for cbg in cbg_list:
                df_cbg = df[df['CensusBlockGroup'] == cbg]
                if len(df_cbg) == 0:
                    continue
                id_list = list(df_cbg['id'])
                shapefile_id_list = shapefile.loc[shapefile.id.isin(id_list)].copy()
                #print(shapefile_id_list)
                shapefile_id_list['geometry'] = shapefile_id_list.geometry.to_crs({'proj': 'cea'})
                shapefile_id_list['area'] = 0.0
                shapefile_id_list['area'] = shapefile_id_list['geometry'].area / 1000000
                #print(shapefile_id_list)
                df_final = shapefile_id_list.groupby(['landuse']).agg({'area':'sum'})
                #print(df_final)

                #for lu in landuse_labels:
                #    if lu in df_final.index:
                #        print(df_final.loc[lu,'area'])
                #    else:
                #        print(0)
				
                area_lut_for_city = area_lut.loc[area_lut.CensusBlockGroup == cbg]
                area_list.append(area_lut_for_city['area'].iloc[0])
                tmp_seg_results = {}
                tmp_seg_results['CensusBlockGroup'] = str(cbg)
                tmp_seg_results['Year'] = int(str(20)+str(year))
                for i in range(len(LABEL_NAMES)):
                    if LABEL_NAMES[i] in df_final.index:
                        #print(LABEL_NAMES[i])
                        tmp_seg_results[LABEL_NAMES[i]] = [float(df_final.loc[LABEL_NAMES[i],'area']/area_lut_for_city['area'].iloc[0])]
                    else:
                        tmp_seg_results[LABEL_NAMES[i]] = [0.0]
				
                state_list.append(area_lut_for_city['StateFIPS'].iloc[0])
                year_list.append(int(str(20)+str(year)))
                cbg_list_all.append(str(cbg))
                city_name_list_all.append(c)
                #print(tmp_seg_results)
                #print(pd.DataFrame(tmp_seg_results))
                segmentation_df = pd.concat([segmentation_df,pd.DataFrame(tmp_seg_results)])
                #print(segmentation_df)

    xxx = pd.DataFrame({'CityName':city_name_list_all,'CensusBlockGroup':cbg_list_all,'Year':year_list,'Area':area_list})
    df_seg_concat = xxx.merge(segmentation_df.reset_index(),on = ['CensusBlockGroup','Year'])
    df_seg_concat.to_csv('LU_density_cbg_new_1.csv',index=False)
