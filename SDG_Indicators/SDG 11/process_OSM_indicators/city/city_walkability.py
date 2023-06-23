from datetime import datetime
import numpy as np
import pandas as pd
from pathlib import Path
import glob

OUTPUT_PATH = Path('./output/environmental_determinants/built_environment/walkability')
OUTPUT_PATH.mkdir(exist_ok=True, parents=True)

city_lut = pd.read_csv('./city_defination_and_LUTs/city_look_up_table.csv')
city_lut = city_lut[['CityName','CityCode']]


daily_living_score = pd.read_csv('./temp_output/walkability/daily_living_score/daily_living_score_city.csv')[['CityCode','DailyLivingScore']]
road_intersection_density = pd.read_csv('./temp_output/walkability/road_intersection_density/walking_road_density_city.csv')[['CityCode','RoadIntersectionDensity']]
pop_density = pd.read_csv('./output/environmental_determinants/basic_statistics/population/population_city.csv')[['CityCode','PopulationDensity']]

daily_living_score['DailyLivingScoreZ'] = (daily_living_score['DailyLivingScore'] - daily_living_score['DailyLivingScore'].mean()) / daily_living_score['DailyLivingScore'].std()
road_intersection_density['RoadIntersectionDensityZ'] = (road_intersection_density['RoadIntersectionDensity'] - road_intersection_density['RoadIntersectionDensity'].mean()) / road_intersection_density['RoadIntersectionDensity'].std()
pop_density['PopulationDensityZ'] = (pop_density['PopulationDensity'] - pop_density['PopulationDensity'].mean()) / pop_density['PopulationDensity'].std()

daily_living_score = daily_living_score.drop('DailyLivingScore', axis=1)
road_intersection_density = road_intersection_density.drop('RoadIntersectionDensity',axis=1)
pop_density = pop_density.drop('PopulationDensity',axis=1)

walkability = daily_living_score.merge(road_intersection_density, left_on='CityCode', right_on='CityCode')
walkability = walkability.merge(pop_density, left_on='CityCode', right_on='CityCode')
walkability['Walkability'] = (walkability['DailyLivingScoreZ'] + walkability['RoadIntersectionDensityZ'] + walkability['PopulationDensityZ']) / 3

walkability = city_lut.merge(walkability, left_on='CityCode', right_on='CityCode')

walkability = walkability.sort_values(['CityCode','CityCode'], ascending=True)
walkability.to_csv(OUTPUT_PATH.joinpath('walkability_city.csv'),index=False)
