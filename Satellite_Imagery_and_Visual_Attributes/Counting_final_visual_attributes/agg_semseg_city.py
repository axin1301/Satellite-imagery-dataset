import os
import glob
import pandas as pd

if not os.path.exists('semseg_results_city212223'):
    os.makedirs('semseg_results_city212223')

file_list = glob.glob('../ViT-Adapter-main-mine/segmentation/semseg_results_212223/*.csv')

df_final = pd.DataFrame({})

for f in file_list:
    df = pd.read_csv(f)
    #'New York city_2022_imgs_semseg'
    city = f.split('/')[-1].split('_')[0]
    year = f.split('/')[-1].split('_')[1]

    df.drop(['img_name'], axis = 1, inplace = True)
    df['city'] = city
    df_mean = df.groupby(['city']).mean().reset_index()
    df_mean['year'] = year
    df_mean.to_csv('semseg_results_city212223/semseg_'+city+'_'+str(year)+'.csv', index = False)

    df_final = pd.concat([df_final,df_mean])

#print(df.columns)
df_final.columns = ['City Name', 'Background', 'Building', 'Road', 'Water', 'Barren', 'Forest', 'Agricultural', 'Year']
df_final.sort_values(by=['City Name','Year'],axis=0,ascending=True,inplace=True)
df_final[['City Name','Year','Background', 'Building', 'Road', 'Water', 'Barren', 'Forest', 'Agricultural']].to_csv('final_semseg_concat_city.csv', index=False)
print(len(df_final))
