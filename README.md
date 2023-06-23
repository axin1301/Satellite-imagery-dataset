# A Satellite Imagery Dataset for Long-Term Sustainable Development in the U.S. Cities

## Introduction

This repo is the code for generating the dataset discribed in "A Satellite Imagery Dataset for Long-Term Sustainable Development in United States Cities".

## Folder Structure
```none
├── Dataset
│   ├── Cities_and_CBGs_Boundaries_and_Statistics (cities/CBGs basic geographical statistics)
│   ├── Satellite_Imagery_and_Visual_Attributes
│   │   ├── satellite_imagery_collection (directory to store satellite image and indices)
│   │   ├── Segmentation (segmentation code for satellite images, fork from https://github.com/czczup/ViT-Adapter and make changes)
│   │   │   ├── detection (not used in our work)
│   │   │   ├── segmentation
│   │   │   │   ├── process_semseg.py (entry code to process satellite image semantic segmentation)
│   │   ├── Object_Detection (object detection code for satellite images, Yolov5 (fork from https://github.com/ultralytics/yolov5 and make changes))
│   │   │   ├── process_imagery_xview.py (entry code to process satellite images with the model trained on xView)
│   │   │   ├── process_imagery_DOTAv2.py (entry code to process satellite images with the model trained on DOTAv2)
│   │   ├── Counting_final_visual_attributes (calculating final visual attributes for each city and CBG)
│   ├── SDG_Indicators
│   │   ├── SDG 1 (No poverty)
│   │   │   ├── Population_Above/Below_Poverty
│   │   │   ├── Population_with_a_ratio_of_Income_to_Poverty_Level
│   │   │   ├── Median Household Income
│   │   ├── SDG 3 (Good health and well-being)
│   │   │   ├── Population_with_no_Health_Insurance_for_Different_Age_Groups
│   │   ├── SDG 4 (Quality education)
│   │   │   ├── Population_with_Different_Education_Status
│   │   ├── SDG 10 (Reduced inequalities)
│   │   │   ├── ACS Income Gini data
│   │   │   ├── Nighttime_Light_Data
│   │   │   │   ├── Light Gini
│   │   │   ├── Population_Data
│   │   ├── SDG 11 (Sustainable cities and communities)
│   │   │   ├── extract_OSM_indicators
│   │   │   ├── process_OSM_indicators
│   │   │   ├── Residential_Segregation
│   ├── prescribing (collection of prescribing data)
│   │   ├── OSM_PBF (OSM data from Geofabrik)
│   │   ├── US_CBG_Geojson (CBG boundary file and ACS data at the CBG level)
│   │   ├── US_SHAPEFILE_city (US city boundary shapefile)
│   │   ├── NTL (nighttime light data from EOG)
│   │   ├── WorldPop_popu (population data from WorldPopulation)
│   ├── output (directory to store the final output dataset)
```

## System Requirement

### Example System Information
Operating System: Ubuntu 18.04.5 LTS
CPU: AMD Ryzen Threadripper 2990WX 32-Core Processor
Memory: 128G DDR4 Memory

### Installation Guide
Typically, a morden computer with fast internet can complete the installation within 10 mins.

1. Download Anaconda according to [Official Website](https://www.anaconda.com/products/distribution), which can be done by the fillowing command (newer version of anaconda should also works)
``` bash
wget -c https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
```
2. Install Anaconda through the commandline guide. Permit conda init when asked.
``` bash
./Anaconda3-2022.10-Linux-x86_64.sh
```
3. Quit current terminal window and open a new one. You should able to see (base) before your command line. 

4. Use the following command to install pre-configured environment through the provided `.yml` file (you should go to the directory of this project before performing the command). Note: for the segmentation code in `Land_Cover_Semantic_Segmentation` and `Object_Detection`, please refer to the corresponding official repo [ViT-Adapter](https://github.com/czczup/ViT-Adapter), [GeoSeg](https://github.com/WangLibo1995/GeoSeg), and [Yolov5](https://github.com/ultralytics/yolov5) to check detailed installation guide.
``` bash
conda env create -f ./anaconda_env_satellite_dataset.yml
```

5. Finally, activate the installed environment. Now you can run the example code through the following chapter.
``` bash
conda activate Satellite_Dataset
```

(Optional) If you need to exit the environment for other project, use the following command.

``` bash
conda deactivate 
```

(Optional) Command for creating our environment without the .yml file.

``` bash
conda create -n Satellite_Dataset python==3.8
pip install numpy ipython pandas matplotlib seaborn datetime pathlib shapely geopandas pyrosm h5netcdf haversine requests urllib3 tqdm scipy scikit-learn
```

## Running the code

1. Run the codes in Cities_and_CBGs_Boundaries_and_Statistics to generate the necessary boundary files for city/CBG as well as the CBG-city lookup table.

2. Collect the prescribing data manually to prepare the original dataset for processing.

3. Collect and process the satellite imagery dataset in Satellite_Imagery_and_Visual_Attributes.

4. Collect and process the ACS/NTL/WorldPop/ACS datasets in SDG_Indicators. 
