'''
Create plots from the points of all unserved and underserved customers
The first implementation was a point map, but it struggles to represent dense areas
the second implementation is a geoplot kdeplot in heatmap()
'''
import geopandas as gpd
import geoplot as gplt
import matplotlib.pyplot as plt
from pathlib import PurePath
import contextily as cx


# draw a kde plot based on points_path
# plot ontop of basemap if webmap=true
# basemap_path is used to clip boudaries
def heatmap(points_path, basemap_path, save_name, bw=0.5, webmap=True):
    # get geoJSON files
    points = gpd.read_file(points_path)
    basemap = gpd.read_file(basemap_path)
    
    if webmap:
        # webmap is the openstreetmap basemap, but the kde plot still gets clipped inside Maine county shapes
        ax = gplt.webmap(basemap, projection=gplt.crs.WebMercator())
        gplt.kdeplot(points['geometry'], ax=ax,clip=basemap, shade=True, cmap='rocket_r', projection=gplt.crs.AlbersEqualArea(), zorder=0, bw_adjust =bw, alpha=0.6)
    else:
        # polyplot is the basemap of Maine counties, with the kde plot clipped inside  Maine borders
        ax = gplt.polyplot(basemap, projection=gplt.crs.AlbersEqualArea(), zorder=1)
        gplt.kdeplot(points['geometry'], ax=ax,clip=basemap, shade=True, cmap='rocket_r', projection=gplt.crs.AlbersEqualArea(), zorder=0, bw_adjust =bw)

    # save various versions of plot in img folder
    for i in [100, 300, 600]:
        file_path = save_name + '_' + str(i) + 'dpi.png'
        plt.savefig(PurePath(file_path), dpi=i,bbox_inches='tight')
    file_path = save_name + '.svg'
    plt.savefig(PurePath(file_path), transparent=True,bbox_inches='tight')

def points_map(unserved, underserved, save_name):
    # get geoJSON files
    unserved = gpd.read_file(unserved).to_crs(3857)
    underserved = gpd.read_file(underserved).to_crs(3857)

    fig, ax = plt.subplots(figsize=(8,12))
    
    ax.set_aspect('equal')
    unserved.plot(ax=ax, marker='*', color='maroon', markersize=0.1)
    underserved.plot(ax=ax, marker='*', color='orange', markersize=0.05)
    
    ax.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    # turn off borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # add openstreetmap basemap
    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)

     # save various versions of plot in img folder
    for i in [100, 300, 600]:
        file_path = save_name + '_' + str(i) + 'dpi.png'
        plt.savefig(PurePath(file_path), dpi=i,bbox_inches='tight')


def main():
    unserved = '../GeoJSON/raws/unserved-subscriber-loactions-2-22v-2H_5_QzFwpIqXW3pGCn.geojson'
    underserved = '../GeoJSON/raws/underserved-subscriber-locations-2-2285o-RU1eSwhXVY0oL0t9_.geojson'
    basemap = '../GeoJSON/1%_Maine_County_Land_Boundary_Polygons_Feature.geojson'
    print('File read complete')

    heatmap(unserved, basemap, '../img/heatmap/unserved', bw = 0.4)
    #heatmap(underserved, basemap,'../img/heatmap/underserved', bw = 0.5)
    #points_map(unserved,underserved, '../img/heatmap/pointplot/subscriber_locations')

if __name__ == "__main__":
    main()