import os
import glob
import pandas as pd

file_list = glob.glob('semseg_results_cbg212223/*.csv')
print(len(file_list))
df_final = pd.DataFrame({})
for f in file_list:
    df = pd.read_csv(f)
    df_final = pd.concat([df_final,df])
#print(df.columns)
df_final.columns = ['CBG Code', 'y_tile', 'x_tile', 'lng_c', 'lat_c', 'Background','Building_percent', 'Road', 'Water', 'Barren', 'Forest', 'Agricultural', 'Year','City Name']
df_final.sort_values(by=['City Name','CBG Code','Year'],axis=0,ascending=True,inplace=True)
df_final[['City Name','CBG Code','Year','Background', 'Building_percent', 'Road', 'Water', 'Barren', 'Forest', 'Agricultural']].to_csv('final_semseg_concat_cbg.csv', index=False)
#print(len(df_final))


