# This folder presents the codes for aggregating the visual attributes extracted from satellite images with the object detection and semantic segmentation models.

The image names and corresponding CBG where they belong is calculated by by image_geoloc.py

The image tile numbers (names) for each CBG are stored in the folder "imgs_within_cbg" for the year 2014~2019 and "imgs_within_cbg_2020" for the year 2020~2023.

## For visual attributes from DOTA dataset:

cal_DOTA_cbg.py

cal_DOTA_city.py

## For visual attributes from xView dataset:

cal_xView_cbg.py

cal_xView_city.py

## For visual attributes from LoveDA dataset:

agg_semseg_cbg.py

add_semseg_city.py
