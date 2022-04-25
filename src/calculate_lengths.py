'''
Plot Heatmap of average speeds in different areas in Maine
'''

import geopandas as gpd

def line_measure(df):
    df['length']=df.to_crs('+proj=cea').length
    df['geometry']=df.to_crs('+proj=cea').centroid.to_crs(df.crs)
    return df

def main(): 
    df = gpd.read_file("..//GeoJSON//combined_tiers.geojson")
    len_df = line_measure(df)
    print(len_df)
    len_df.to_file('..//GeoJSON//length_centroid_combined_tiers.geojson', driver='GeoJSON')

if __name__ == "__main__":
    main()