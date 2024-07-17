# GIS-Capstone
Code for VOLUNTEERED GEOGRAPHIC INFORMATION: A GEOSPATIAL COMPARISON OF WIKIPEDIA AND OPENSTREETMAP CONTRIBUTION TRENDS GLOBALLY by Axel Bax

This repository contains 5 Python scripts:
1) city_selector.py
2) sql_regex.py
3) csv_to_geo.py
4) city_framer.py
5) shapefile_trimmer.py

and 2 Overpass turbo API scripts:
1) pulling relation from specific ID
2) searching for relations by name



city_selector.py:
  This script selects 60 case study cities. The first 20 are selected by population and the remaining 40 are random. Cities that are too close to a city already added to the list are removed.

sql_regex.py:
  This script parses information from the SQL file provided by Wikipedia into a CSV with location coordinates and names. Additional packages could be used to process it, but the Wikimedia package failed to unpack it into a CSV file.

csv_to_geo.py:
  This script is optional and can be replicated by loading the CSV table into ArcGIS as XY table, then exporting to a feature layer. It converts a CSV with lat/lon coordinates to a point shapefile.

city_framer.py
  This script takes the list of cities and searches for the appropriate OSM object using the Overpass QL, then saves the GeoJSON output of that result. However, the Overpass QL does not always behave the same way in Overpass turbo (web browser version) and in Python.
Most cities ended up being manually queried by ID in Overpass turbo to avoid any errors. More experimenting with this code needs to be done to eliminate idiosychracies. Results will also vary by name and language of the OSM object. It is recommended to instead identify
objects by hand in OSM and search for that ID to get the GeoJSON file to get the best results.

shapefile_trimmer.py
  This script iterates through Geofabrik shapefile exports that are all in one folder and returns a single shapefile that contains the point version of every feature only within the chosen city boundaries. This requires the arcpy package to work appropriately. Note: Mali and Somalia returned errors, but it is unclear why. All processes can be completed in ArcGIS following the process outlined in the paper.



Overpass turbo 1):
**NOTE: make sure that the city is contained in the bounding box. type is frequently 'boundary' but can be 'multipolygon' as below. Rarely, city boundaries are ways instead of relations. Just change 'rel' to 'way'.

[out:json][timeout:25];
// gather results
(
  rel(11489822)[type=multipolygon]({{bbox}});
);
(._;>;);
// print results
out geom;

Overpass turbo 2):
**NOTE: some cities return multiple results; these tend to get merged into the same layer, creating multi-part polygons that are incorrect. Double check print statements to see if any cities return multiple IDs, and cip them as necessary.

[out:json][timeout:45];
        (
        rel['name:en'=""" + "'" + cities[i][0] + "'" + """]['type'='boundary'];
        rel['name:en'=""" + "'" + cities[i][1] + "'" + """]['type'='boundary'];
        rel['name'=""" + "'" + cities[i][0] + "'" + """][type=boundary];
        rel['name'=""" + "'" + cities[i][1] + "'" + """][type=boundary];
        );
        (._;>;);
        out skel qt;
