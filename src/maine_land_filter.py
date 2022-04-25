'''
Maine County Shapes are given with water jurisdictions included, 
but we only want land for broadband maps.
This code removes water polygons from Maine_County Boundary_Polygons

*note*
Shapefile was downloaded from https://www.maine.gov/geolib/catalog.html,
https://services1.arcgis.com/RbMX0mRVOFNTdLzd/arcgis/rest/services/Maine_County_Boundary_Polygons/FeatureServer/0
then converted in mapshaper to 1% simplified GEOJSON file
'''

import geopandas as gpd
from pathlib import Path

# Mapshaper didn't record CRS correctly, set as 26919 then convery to 4326
raw_counties = gpd.read_file(Path("../GeoJSON/1%_Maine_County_Boundary_Polygons_Feature.geojson")).set_crs(26919,allow_override=True).to_crs(4326)

# filter out water polygons
land_counties = raw_counties[raw_counties['LAND'] == 'y']

# filter out empty geometries, from simplification in mapshaper then save to file
land_counties[land_counties['geometry'].notnull()].to_file(Path("../GeoJSON/1%_Maine_County_Land_Boundary_Polygons_Feature.geojson"), driver='GeoJSON')