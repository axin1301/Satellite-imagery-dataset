import glob
import pandas as pd

# final_obd_cbg_DOTA  final_obd_cbg_xview  final_obd_city_DOTA  final_obd_city_xview
file_list = glob.glob('../final_obd_cbg_DOTA/*.csv')
pd_dict = pd.DataFrame({})

for f in file_list:
    pd_data = pd.read_csv(f)
    pd_dict = pd.concat([pd_dict, pd_data])
pd_dict.to_csv('final_obd_cbg_DOTA_RL3.csv', index = False)


file_list = glob.glob('../final_obd_cbg_xview/*.csv')
pd_dict = pd.DataFrame({})

for f in file_list:
    pd_data = pd.read_csv(f)
    pd_dict = pd.concat([pd_dict, pd_data])
pd_dict.to_csv('final_obd_cbg_xview_RL3.csv', index = False)

file_list = glob.glob('../final_obd_city_DOTA/*.csv')
pd_dict = pd.DataFrame({})

for f in file_list:
    pd_data = pd.read_csv(f)
    pd_dict = pd.concat([pd_dict, pd_data])
pd_dict.to_csv('final_obd_city_DOTA_RL3.csv', index = False)

file_list = glob.glob('../final_obd_city_xview/*.csv')
pd_dict = pd.DataFrame({})

for f in file_list:
    pd_data = pd.read_csv(f)
    pd_dict = pd.concat([pd_dict, pd_data])
pd_dict.to_csv('final_obd_city_xview_RL3.csv', index = False)
