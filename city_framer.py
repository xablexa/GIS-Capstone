import overpy
import json
import geopandas as gpd
import re

api = overpy.Overpass()

#import cities and make list
cities_gdf = gpd.read_file("C:/Users/Axel/Desktop/GIS Master's Courses/Capstone/cities/cities.shp", driver='ESRI Shapefile')
city_list = cities_gdf["NAME"].tolist()
city_en_list = cities_gdf["NAME_EN"].tolist()
#city_wiki_list = cities_gdf["WIKIDATAID"].tolist()
cities = list(map(list, zip(city_list, city_en_list)))
for i in range(len(cities)):
    cities[i][0] = re.sub(r'[^\w\s]', '', cities[i][0])
    cities[i][1] = re.sub(r'[^\w\s]', '', cities[i][1])

print(cities)
print(len(cities))
#city_list = ["Baltimore", "London", "Beijing", "Istanbul", "Cairo"]

for i in range(len(cities)):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    q = """[out:json][timeout:45];
        (
        rel['name:en'=""" + "'" + cities[i][0] + "'" + """]['type'='boundary'];
        rel['name:en'=""" + "'" + cities[i][1] + "'" + """]['type'='boundary'];
        rel['name'=""" + "'" + cities[i][0] + "'" + """][type=boundary];
        rel['name'=""" + "'" + cities[i][1] + "'" + """][type=boundary];
        );
        (._;>;);
        out skel qt;"""
    result = api.query(q)

    #print(result.from_json())
    print(result.relations)
    #print(result.ways)
    #print(result.nodes)

    for way in result.ways:
        # Extract coordinates
        coord_list = []
        for node in way.nodes:
            lon = float(node.lon)
            lat = float(node.lat)
            coord_list.append([lon, lat])

        # Create a GeoJSON feature for each node
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": coord_list
            }
        }
        geojson["features"].append(feature)

    filename = "C:/Users/Axel/Desktop/GIS Master's Courses/Capstone/cities/" + cities[i][1] + ".geojson"
    with open(filename, "w") as f:
        json.dump(geojson, f)

    print("GeoJSON file created successfully!")
    print()
    print()

print("Finished!")