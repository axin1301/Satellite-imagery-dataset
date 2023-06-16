# A Satellite Imagery Dataset for Long-Term Sustainable Development in US Cities

## Introduction

This repo is the code for generating the dataset discribed in "A Satellite Imagery Dataset for Long-Term Sustainable Development in US Cities".

## Folder Structure
```none
├── Dataset
│   ├── Cities_and_CBGs_Boundaries_and_Statistics (cities/CBGs basic geographical statistics)
│   ├── Satellite_Imagery_and_Visual_Attributes
│   │   ├── Satellite_Imagery (directory to store satellite image and indices)
│   │   ├── Land_Cover_Semantic_Segmentation (segmentation code for satellite images)
│   │   │   ├── ViT-Adapter-main-mine (fork from https://github.com/czczup/ViT-Adapter and make changes)
│   │   │   │   ├── detection (not used in our proj)
│   │   │   │   ├── segmentation
│   │   │   │   │   ├── process_semseg.py (entry code to process satellite image semantic segmentation)
│   │   ├── Object_Detection (object detection code for satellite images)
│   │   │   ├── Yolov5 (fork from https://github.com/ultralytics/yolov5 and make changes)
│   │   │   │   ├── xView
│   │   │   │   │   ├── process_imagery_xview.py (entry code to process satellite images with the model trained on xView)
│   │   │   │   ├── DOTAv2
│   │   │   │   │   ├── process_imagery_DOTAv2.py (entry code to process satellite images with the model trained on DOTAv2)
│   ├── SDG_Indicators
│   │   ├── SDG 1 data (No poverty)
│   │   │   ├── ACS data
│   │   │   │   ├── Population_Above/Below_Poverty
│   │   │   │   ├── Population_with_a_ratio_of_Income_to_Poverty_Level
│   │   ├── SDG 3 data (Good health and well-being)
│   │   │   ├── ACS data
│   │   │   │   ├── Population_with_no_Health_Insurance_for_Different_Age_Groups
│   │   ├── SDG 4 data (Quality education)
│   │   │   ├── ACS data
│   │   │   │   ├── Population_with_Different_Education_Status
│   │   ├── SDG 10 data (Reduced inequalities)
│   │   │   ├── ACS data
│   │   │   │   ├── Income Gini
│   │   │   ├── Nighttime_Light_Data, Population_Data
│   │   │   │   ├── Light Gini
│   │   ├── SDG 11 data (Sustainable cities and communities)
│   │   │   ├── OSM data
│   ├── prescribing (code and results for collection prescribing data)
│   │   ├── get_data.py (download prescribing data)
│   │   ├── original_data (directory for save the prescribing data files)
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
