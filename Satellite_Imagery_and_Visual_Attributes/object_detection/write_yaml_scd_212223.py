import pandas as pd
import os
import sys

#df = pd.read_csv('../New_folder1/zl19_images/statis_city.csv')
#df = pd.read_csv('../New_folder1/zl19_images/statis2.csv')
#df = pd.read_csv('obd_vakka_scd_single_2018.csv')
#df = pd.read_csv('obd_vakka_scd_single2_2018.csv')

city_list = ['Fort Wayne city','Fort Worth city','Fremont city','Fresno city','Garland city','Gilbert town','Glendale city','Greensboro city','Irvine city','Irving city','Jersey City city','Laredo city','Las Vegas city','Lexington-Fayette urban county','Lincoln city','Long Beach city','Louisville-Jefferson County metro government (balance)']
df = pd.DataFrame({'city':city_list})

for i in range(len(df)):
    dir_name = df.at[i,'city']
    for year in [2021,2022,2023]:
        #year = df.at[i,'year']
        dir_name_= dir_name.replace(' ','_')
        #if year != 2018: # for first time, run 2018
        #    continue
        if os.path.exists('obd_yaml_file_212223'+'/dataset_DOTA_' + str(year) + '_' + dir_name_ + '.yaml'):
            continue

        #with open('obd_yaml_file'+'/dataset_DOTA_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        #with open('obd_yaml_file_otheryear'+'/dataset_DOTA_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        with open('obd_yaml_file_212223'+'/dataset_DOTA_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        #with open('obd_vakka_scd_single_2018_yaml'+'/dataset_DOTA_' + str(year) + '_' + dir_name + '.yaml', "w") as variable_name:
        #with open('obd_vakka_scd_single2_2018_yaml'+'/dataset_DOTA_' + str(year) + '_' + dir_name + '.yaml', "w") as variable_name:
            variable_name.write('path: ../sci_data_2021/zl19_images/')
            variable_name.write('\n')
            variable_name.write('val: ' + str(year) + '/' + dir_name)
            variable_name.write('\n')
            variable_name.write('nc: 18')
            variable_name.write('\n')
            variable_name.write(
        'names: [\'plane\', \'ship\', \'storage-tank\', \'baseball-diamond\', \'tennis-court\',\'basketball-court\', \'ground-track-field\', \'harbor\', \'bridge\', \'large-vehicle\',    \'small-vehicle\', \'helicopter\', \'roundabout\', \'soccer-ball-field\',\'swimming-pool\', \'container-crane\', \'airport\', \'helipad\']')


        if os.path.exists('obd_yaml_file_212223'+'/dataset_xview_' + str(year) + '_' + dir_name_ + '.yaml'):
            continue
        #with open('obd_yaml_file'+ '/dataset_xview_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        #with open('obd_yaml_file_otheryear'+ '/dataset_xview_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        with open('obd_yaml_file_212223'+ '/dataset_xview_' + str(year) + '_' + dir_name_ + '.yaml', "w") as variable_name:
        #with open('obd_vakka_scd_single_2018_yaml'+ '/dataset_xview_' + str(year) + '_' + dir_name + '.yaml', "w") as variable_name:
        #with open('obd_vakka_scd_single2_2018_yaml'+ '/dataset_xview_' + str(year) + '_' + dir_name + '.yaml', "w") as variable_name:
            variable_name.write('path: ../sci_data_2021/zl19_images/')
            variable_name.write('\n')
            variable_name.write('val: ' + str(year) + '/' + dir_name)
            variable_name.write('\n')
            variable_name.write('nc: 11')
            variable_name.write('\n')
            variable_name.write(
        'names: [\'Fixed-wing aircraft\',\'Passenger Vehicle\',\'Building\',\'Truck\',\'Railway Vehicle\',\'Maritime Vessel\',\'Engineering Vehicle\',\'Helipad\',\'Vehicle Lot\',\'Construction Site\',\'Unknown\']')
