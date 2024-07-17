import arcpy
import os
rootPath = r'D:\OpenStreetMap\All_Shapefiles'
arcpy.env.workspace = rootPath
arcpy.env.overwriteOutput = True
#fc = arcpy.ListFeatureClasses()
#print(fc)

sfiles = os.listdir(rootPath)
print(sfiles)

sfiles2 = []

for item in sfiles:
    if "zip" in item:
        print('removing...')
    else:
        sfiles2.append(item)
print(sfiles2)
print(len(sfiles2))

polys = ["gis_osm_buildings_a_free_1.shp", "gis_osm_landuse_a_free_1.shp",
         "gis_osm_natural_a_free_1.shp", "gis_osm_places_a_free_1.shp",
         "gis_osm_pofw_a_free_1.shp", "gis_osm_pois_a_free_1.shp",
         "gis_osm_traffic_a_free_1.shp", "gis_osm_transport_a_free_1.shp",
         "gis_osm_water_a_free_1.shp"]
lines = ["gis_osm_railways_free_1.shp", "gis_osm_roads_free_1.shp",
         "gis_osm_waterways_free_1.shp"]
pts = ["gis_osm_natural_free_1.shp", "gis_osm_places_free_1.shp",
       "gis_osm_pofw_free_1.shp", "gis_osm_pois_free_1.shp",
       "gis_osm_traffic_free_1.shp", "gis_osm_transport_free_1.shp"]

outFolder = os.path.join(rootPath, "temp_zip")


for item in sfiles2:
    print("Starting: {0}".format(item))

    polys2 = []
    lines2 = []
    pts2 = []

    for shp in polys:
        p = os.path.join(rootPath, item, shp)
        polys2.append(p)
    for shp in lines:
        p = os.path.join(rootPath, item, shp)
        lines2.append(p)
    for shp in pts:
        p = os.path.join(rootPath, item, shp)
        pts2.append(p)

    all_city_frame = "C:/Users/Axel/Documents/ArcGIS/Projects/Capstone_city_selector/Capstone_city_selector.gdb/all_city_frames"
    polys3 = []
    lines3 = []
    pts3 = []
    counter = 0
    for shp in polys2:
        outi = str(polys[counter][:-4] + "clipped.shp")
        outFile = os.path.join(outFolder, outi)
        arcpy.analysis.Clip(shp, all_city_frame, outFile)
        polys3.append(outFile)
        counter += 1
    print("polys clipped.")
    counter = 0
    for shp in lines2:
        outi = str(lines[counter][:-4] + "clipped.shp")
        outFile = os.path.join(outFolder, outi)
        arcpy.analysis.Clip(shp, all_city_frame, outFile)
        lines3.append(outFile)
        counter += 1
    print("lines clipped.")
    counter = 0
    for shp in pts2:
        outi = str(pts[counter][:-4] + "clipped.shp")
        outFile = os.path.join(outFolder, outi)
        arcpy.analysis.Clip(shp, all_city_frame, outFile)
        pts3.append(outFile)
        counter += 1
    print("points clipped.")


    poly_out = os.path.join(outFolder, "polyFile.shp")
    arcpy.management.Merge(polys3, poly_out)
    print("Merge complete!")
    poly_pts = os.path.join(outFolder, "poly_pts.shp")
    arcpy.management.FeatureToPoint(poly_out, poly_pts, "CENTROID")
    print("Polygons to Point complete!")

    line_out = os.path.join(outFolder, "lineFile.shp")
    arcpy.management.Merge(lines3, line_out)
    print("Merge complete!")
    line_pts = os.path.join(outFolder, "line_pts.shp")
    arcpy.management.FeatureToPoint(line_out, line_pts, "CENTROID")
    print("Lines to Point complete!")

    pts3.append([os.path.join(outFolder, "poly_pts.shp"), os.path.join(outFolder, "line_pts.shp")])
    outName = item[:-4] + "all_pts.shp"
    all_pts = os.path.join(outFolder, outName)
    arcpy.management.Merge(pts3, all_pts)
    print("Merge complete!")
    #all_city_frame = "C:/Users/Axel/Documents/ArcGIS/Projects/Capstone_city_selector/Capstone_city_selector.gdb/all_city_frames"
    #all_pts_clipped = os.path.join(outFolder, str(item[:-16]), "_osm_pts.shp")
    #arcpy.analysis.Clip(all_pts, all_city_frame, all_pts_clipped)
    #print("Points merged and clipped!")

    temp_files = ["temp_zip/polyFile.shp", "temp_zip/poly_pts.shp",
                  "temp_zip/lineFile.shp", "temp_zip/line_pts.shp"]
    temp_files = temp_files + polys3 + lines3 + pts3
    arcpy.management.Delete(temp_files)
    print("Temp files removed.")
    print()


osm_pts_split = os.listdir(outFolder)
osm_all_pts = os.path.join(rootPath, "all_osm_pts.shp")
arcpy.management.Merge(osm_pts_split, osm_all_pts)