import geopandas as gpd
import random
#import pandas as pd

gdf = gpd.read_file("D:/ne_10m_populated_places/ne_10m_populated_places.shp")
'''for col in gdf.columns:
    print(col)'''
#remove columns that we don't need
#NAME 1, NAMEPAR 2, CAPIN, WORLDCITY, ADM0NAME, ADM0_A3, POP_MIN, POP_OTHER, RANK_MAX,
    #RANK_MIN, MEGANAME, LS_NAME

#add columns to keep
gdf["keep"] = 0

#select top 20 cities by population*
    #*if cities are too close to another city already selected, they will be skipped
cities_gdf = gpd.GeoDataFrame()

gdf = gdf.sort_values(by=["POP_MAX"], ascending=False)
#print(gdf.head())
print(gdf['NAME_EN'].loc[gdf.index[0]])

for i in range(len(gdf)):
    #print("i: {0}".format(i))
    #print("cities len: {0}".format(len(cities_gdf.index)))
    if len(cities_gdf.index) == 20:
        break
    elif i == 0:
        gdf.iloc[i, gdf.columns.get_loc("keep")] = 1
        cities_gdf = cities_gdf.append(gdf.iloc[i], ignore_index=True)
    else:
        p = 0
        for j in range(len(cities_gdf)):
            print("j: {0}".format(j))
            p1 = gdf.iloc[i]
            p2 = cities_gdf.iloc[j]
            dist = float(p1['geometry'].distance(p2['geometry']))
            if dist <= 3.5:
                p = 1
        if p == 0:
            gdf.iloc[i, gdf.columns.get_loc("keep")] = 1
            cities_gdf = cities_gdf.append(gdf.iloc[i], ignore_index=True)
        else:
            print("City too close, removing...")
print(cities_gdf)

#remove Scientific and Meteorological Stations
gdf = gdf[gdf['FEATURECLA'] != 'Scientific station']
gdf = gdf[gdf['FEATURECLA'] != 'Meteorological Station']
#gdf = gdf[gdf['FEATURECLA'] != 'Populated place']

#get random ones and check if they are too close
gdf["Rand_rank"] = float(0)

for i in gdf.index:
    gdf.at[i, "Rand_rank"] = random.random()
gdf = gdf.sort_values(by=["Rand_rank"], ascending=False)

for i in range(len(gdf)):
    #print("i: {0}".format(i))
    #print("cities len: {0}".format(len(cities_gdf.index)))
    if len(cities_gdf.index) == 60:
        break
    elif i == 0:
        gdf.iloc[i, gdf.columns.get_loc("keep")] = 1
        cities_gdf = cities_gdf.append(gdf.iloc[i], ignore_index=True)
    else:
        p = 0
        for j in range(len(cities_gdf)):
            print("j: {0}".format(j))
            p1 = gdf.iloc[i]
            p2 = cities_gdf.iloc[j]
            dist = float(p1['geometry'].distance(p2['geometry']))
            if dist <= 3.5:
                p = 1
        if p == 0:
            gdf.iloc[i, gdf.columns.get_loc("keep")] = 1
            cities_gdf = cities_gdf.append(gdf.iloc[i], ignore_index=True)
        else:
            print("City too close, removing...")
print(cities_gdf)

cities_gdf = gpd.GeoDataFrame(cities_gdf, geometry='geometry')
cities_gdf.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
cities_gdf.to_file("C:/Users/Axel/Desktop/GIS Master's Courses/Capstone/cities/cities.shp", driver='ESRI Shapefile')
