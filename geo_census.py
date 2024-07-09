import requests
import pandas as pd
import geopandas as gpd
from bokeh.io import output_notebook, show, curdoc
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LogColorMapper, ColorBar, HoverTool, Select, Dropdown
from bokeh.layouts import column
from bokeh.palettes import Blues256, Greens256, Reds256, Purples256, Oranges256, Greys256

# Load the shapefile
gdf = gpd.read_file(r"C:\Users\Tejas.Iyer\OneDrive - GDIT\Documents\tl_2022_us_state\tl_2022_us_state.shp")
print(gdf.head())

api_key = 'f0c4eb00eca42436fb48ac7c95e9b0c902c5eeb4'

# Pull data
def get_data(year):
    url = f'https://api.census.gov/data/{year}/acs/acs5/subject?'

    params = {
        'get': 'NAME,S0101_C01_001E,S0101_C01_002E,S0101_C01_003E,S0101_C01_004E,S0101_C01_005E,S0101_C01_006E,S0101_C01_007E,S0101_C01_008E,S0101_C01_009E,S0101_C01_010E,S0101_C01_011E,S0101_C01_012E,S0101_C01_013E,S0101_C01_014E,S0101_C01_015E,S0101_C01_016E,S0101_C01_017E,S0101_C01_018E,S0101_C01_019E',
        'for': 'state:*',
        'key': api_key
    }

    response = requests.get(url, params=params)
    
    data = response.json()
    
    return data

year = '2022'
json_data = get_data(year)

# Create Data frame
df = pd.DataFrame(json_data[1:], columns=json_data[0])

# Rename columns
df = df.rename(columns={
    'S0101_C01_001E': 'Total Population',
    'S0101_C01_002E': 'Under 5',
    'S0101_C01_003E': '5-9',
    'S0101_C01_004E': '10-14',
    'S0101_C01_005E': '15-19',
    'S0101_C01_006E': '20-24',
    'S0101_C01_007E': '25-29',
    'S0101_C01_008E': '30-34',
    'S0101_C01_009E': '35-39',
    'S0101_C01_010E': '40-44',
    'S0101_C01_011E': '45-49',
    'S0101_C01_012E': '50-54',
    'S0101_C01_013E': '55-59',
    'S0101_C01_014E': '60-64',
    'S0101_C01_015E': '65-69',
    'S0101_C01_016E': '70-74',
    'S0101_C01_017E': '75-79',
    'S0101_C01_018E': '80-84',
    'S0101_C01_019E': '85+',
    
})

print(df['Under 5'])

# Convert columns to numeric
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col])
    

# Calculate percentages
age_groups = df.columns[2:20]
for col in age_groups:
    df[f'{col}_pct'] = (df[col] / df['Total Population']) * 100
   
pct_cols = {col : f'{col}_pct' for col in age_groups}

# Exclude US territories not part of 50 states
excluded = ['HI','VI','MP','GU','AS','PR']

for x in excluded:
    gdf = gdf[gdf.STUSPS != x]

merged_gdf = gdf.merge(df, left_on='NAME', right_on='NAME')

output_notebook()

# List of palettes
palettes = [
    Blues256, Greens256, Reds256, Purples256, Oranges256, Greys256,
    Blues256, Greens256, Reds256, Purples256, Oranges256, Greys256,
    Blues256, Greens256, Reds256, Purples256, Oranges256, Greys256
]

# Color Mappers
color_mappers = {}

for i in range(len(palettes)):
    color_mappers[list(pct_cols.values())[i]] = LogColorMapper(palette=palettes[i])
    
# Convert Geo Dataframe to JSON format
geosource = GeoJSONDataSource(geojson=merged_gdf.to_json())

initial = 'Under 5_pct'

# Create the figure
p = figure(title=f'Age Demographics across the US States - {initial}',
           toolbar_location='right',
           tools='pan, wheel_zoom, box_zoom, reset',
           tooltips=[
               ('State', '@NAME'), 
               ('Percentage', f'@{{{initial}}} %')
            ],
           width = 1200,
           height = 800,
           x_range = (-200, -50),
           y_range = (20, 90))

p.title.align = 'center'

patches = p.patches('xs', 'ys', source=geosource, fill_color={'field': initial, 'transform' : color_mappers[initial]}, line_width=0.25, fill_alpha=1)

# Create a color bar at the bottom
color_bar = ColorBar(color_mapper=color_mappers[initial], label_standoff=8, width=500, height=20, location=(0, 0), orientation='horizontal')
p.add_layout(color_bar, 'below')

# Create a dropdown menu of the percentages
menu = [(age, age) for age in age_groups]
dropdown = Dropdown(label='Select Age Group', button_type='warning', menu=menu)

# Select widget
select = Select(title='Select Age Group', value=initial, options=list(pct_cols.keys()))

# Callback method when a dropdown option is selected
def update_plot(attr, old, new):
    print(f'Update Triggered: old={old}, new={new}')
    age_group = pct_cols[select.value]
    print(age_group)
    patches.glyph.fill_color = {'field': age_group, 'transform': color_mappers[age_group]}
    color_bar.color_mapper = color_mappers[age_group]
    p.title.text = f'Age Demographics across the US States - {age_group}'
    
    p.select_one(HoverTool).tooltips = [
        ('State', '@NAME'),
        ('Percentage', f'@{{{age_group}}} %')
    ]


select.on_change('value', update_plot)

layout = column(select, p)
curdoc().add_root(layout)
show(layout)
