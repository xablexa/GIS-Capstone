import pandas as pd
import geopandas
#import matplotlib.pyplot as plt
#from geodatasets import get_path

df = pd.read_csv('D:/Wikipedia/articles_wName_geo.csv', dtype={
    'gt_id':'int', 'gt_page_id':'int', 'gt_globe':'str', 'gt_primary':'int', 'gt_lat':'float',
    'gt_lon':'float', 'gt_dim':'int', 'gt_type':'str', 'gt_name':'str', 'gt_country':'str',
    'gt_region':'str', 'gt_lat_int':'str', 'gt_lon_int':'str'})

#print(df.head())
print(df.info())
#remove planets
df = df[df['gt_globe'] == "'earth'"] #removes about 8000 points
#print(gdf.info())
#remove single quotes from text entries and format all columns appropriately
df["gt_name"] = df["gt_name"].str.strip("'") #name
#type
#country
#regionn
print(df.head())
df.to_csv('articles_wName_geo_points.csv')
#convert to geopandas
gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.gt_lat, df.gt_lon), crs='EPSG:4326')

#group lines/polygons together?

gdf.to_file('D:/Wikipedia/articles_wName_geo_points.shp')
