'''
test out gpd explore function
'''
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

def plot(lines, state, cities, basemap, cmap, lw, label, dpi):
    
    # dictionary of basemap tile servers
    tile_urls ={
        'mapnik':'http://a.tile.osm.org/{z}/{x}/{y}.png',
        'hot':'http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', 
        'arc_darkgray':'http://services.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', 
        'arc_oceanbase': 'http://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
        'arc_worldstreetmap': 'http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        'arc_imagery': 'http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'arc_physical': 'http://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',
        'arc_worldtopo': 'http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        'dark_nolabel': 'http://a.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png'
        }
    
    # plot broadband lines, color by tier
    ax = lines.plot('v_layer', figsize=(8,12), cmap=cmap, categorical=True, linewidth=lw, legend=True)
    # first basemap provides actual basemap
    cx.add_basemap(ax, source=tile_urls[basemap])
    
    # Some base maps don't include state border
    # add light state boundary on dark basemaps:
    if basemap in ['arc_darkgray', 'arc_imagery', 'dark_nolabel']:
        border_color = 'lightgray'
    # add dark boundary on light basemaps:
    else:
        border_color = '#00222B'
    state.plot(ax=ax, color=border_color, linewidth=2, linestyle='solid')
    
    # for fun, cities can be drawn on map as well
    if label == 'label':
        if cmap is 'viridis':
            cities_color = '#CC382B'
        elif cmap in ['bwr', 'coolwarm']:
            cities_color = 'blue'
        else:
            cities_color = 'r'
        cities.plot(ax=ax, edgecolors = cities_color, facecolors='none', markersize= 80, linewidth=2, zorder = 10)

    # turn off borders
    ax.tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # move legend to bottom right over labels
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.85,0.17))    
    leg.set_zorder(100)
    plt.tight_layout()
    
    # unique file name with parameters
    save_path = '..//img//tiers//' + basemap + '_' + cmap + '_' + label + '_' + str(lw) +  '_' + str(dpi) + 'dpi.png'
    plt.savefig(save_path, dpi=dpi)
    plt.close('all')

def param_test(lines, state, cities):
    # various parameters to try out
    basemaps = ['arc_worldstreetmap', 'dark_nolabel', 'arc_imagery']
    cmaps = ['viridis', 'bwr']
    lws = [1.5]
    labels = ['no_label', 'label']
    dpis = [72]

    params = [(basemap, cmap, lw, label, dpi) for basemap in basemaps for cmap in cmaps for lw in lws for label in labels for dpi in dpis]
    for p in params:
        plot(lines, state, cities, p[0], p[1], p[2], p[3], p[4])
        print('Plotted with params: ', p)
    print('    Testing Complete')

def main():
    # convert CRS to webmercator for using contextlilly basemaps
    lines = gpd.read_file('..//GeoJSON//1%_0001_combined_tiers.json').to_crs(3857)
    state = gpd.read_file('..//GeoJSON//statelines.json').to_crs(3857)    
    # set of 10 largest cities in Maine
    cities = gpd.read_file('..//GeoJSON//maine_cities.geojson').to_crs(3857)    
    print('File read complete')

    # to quickly try out different plotting parameters, use the function below
    param_test(lines, state, cities)
    
    # single plot
    #plot(lines, state, 'arc_oceanbase', 'coolwarm', lw=1, label='no_labels', dpi=72)

if __name__ == "__main__":
    main()
