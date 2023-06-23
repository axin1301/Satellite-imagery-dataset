import pandas as pd
import numpy as np
import random
import shapefile
import glob
import shapely
import math
import os
from shapely.geometry import Polygon

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

# get the range of tiles that intersect with the bounding box of the polygon
def getTileRange(polygon, zoom):
    bnds = polygon.bounds
    xm = bnds[0]
    xmx = bnds[2]
    ym = bnds[1]
    ymx = bnds[3]
    bottomRight = (xmx, ym)
    starting = deg2num(ymx, xm, zoom)
    ending = deg2num(ym, xmx, zoom)  # this will be the tiles containing the ending
    x_range = (starting[0], ending[0])
    y_range = (starting[1], ending[1])
    return (x_range, y_range)

# to get the tile as a polygon object
def getTileASpolygon(z, y, x):
    nw = num2deg(x, y, z)
    se = num2deg(x + 1, y + 1, z)
    xm = nw[1]
    xmx = se[1]
    ym = se[0]
    ymx = nw[0]
    tile_bound = Polygon([(xm, ym), (xmx, ym), (xmx, ymx), (xm, ymx)])
    return tile_bound

# to tell if the tile intersects with the given polygon
def doesTileIntersects(z, y, x, polygon):
    if (z < 10):  # Zoom tolerance; Below these zoom levels, only check if tile intersects with bounding box of polygon
        return True
    else:
    # get the four corners
        tile = getTileASpolygon(x, y, z)
        return polygon.intersects(tile)

city_list = list(pd.read_csv('image_download/final_download_info_state_fips.csv')['city2'])[:100]
fips_list = list(pd.read_csv('image_download/final_download_info_state_fips.csv')['state_code'])[:100]
#city_list = [x+' city' for x in c_list]

#city_list = ['Anchorage municipality', 'Gilbert town','Indianapolis city (balance)','Boise City city','Nashville-Davidson metropolitan government (balance)','Omaha','Lexington-Fayette urban county']
#fips_list = [2,4,18,16,47,31,21]


shp_list = glob.glob('shpfile/*/*.shp')
#shp_list = ['shpfile/tl_2021_31_place/tl_2021_31_place.shp']
print(len(shp_list))

for shp in shp_list:
    print(shp.split('.')[0])
    sf=shapefile.Reader(shp.split('.')[0])
    cnt = 0

    l = len(sf)
    for c in range(l):
        shaperec = sf.record(c)
        #print(shaperec['NAMELSAD'])
        if shaperec['NAMELSAD'] in city_list:

            city_iidx = int(city_list.index(shaperec['NAMELSAD']))
            state_no = int(fips_list[city_iidx])
            if int(shaperec['STATEFP']) != state_no:
                continue

            stArea = Polygon(sf.shapes()[c].points)
            print(shaperec['NAMELSAD'])

#print(stArea.bounds)

            tileList = []

            for z in range(18,19):
                ranges = getTileRange(stArea, z)
                x_range = ranges[0]
                y_range = ranges[1]

                for y in range(y_range[0], y_range[1] + 1):
                    for x in range(x_range[0], x_range[1] + 1):
                        if (doesTileIntersects(x, y, z, stArea)):
                            tileList.append((z, y, x))
            tileCount = len(tileList)
            print('Total number of Tiles: ' + str(tileCount))
            print(tileList[:10])

            y_list = [x[1] for x in tileList]
            x_list = [x[2] for x in tileList]

            pd_dict = pd.DataFrame({'y_tile':y_list, 'x_list':x_list})
            pd_dict.to_csv('./tilefile_zl19_scd/'+shaperec['NAMELSAD']+'.csv', index = False)
            #print('one city done')
