# Geo Census Data Project

This project fetches the ACS (American Community Survey) API in Python to collect and analyze demographic data, focusing on the age distribution across different states in the US. Includes visualizations such as stacked bar plots and chloropeth graphs. 

## Features

### census_api.ipynb
- Fetches age related data from ACS API from 2022
- Transforms JSON data into a dataframe using **Pandas**
- Utilizes **matplotlib** to create a stacked bar plot

### geo_census.py
-  Employs **geopandas** for handling geospatial data regarding the United States
-  Uses **bokeh** for creating an interactive chloropeth graph with dropdown menu

### json_vars.py
- Provides functionality to filter and manage large JSON data sets from the ACS API
- Work with smaller subsets of data more efficiently


## Prerequisites

- Python 3.x
- An active ACS API key

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Census_Data.git
    ```

2. **Navigate to Project Directory**
    ```sh
    cd Census_Data
    ```
3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run Jupyter Notebook:**
    ```sh
    jupyter notebook census_api.ipynb
    ```
5. **Run the geo_census script**
    ```sh
    bokeh serve --show geo_census.py
    ```

