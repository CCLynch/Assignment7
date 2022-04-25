'''
Plot rates of underserved and unserved by elegibility area
'''
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import PurePath

url = "../GeoJSON/raws/eligible-areas-2-226PEr9ZEyBEne5G8zrdRmw.geoJSON"
gdf = gpd.read_file(url)
fig, axs = plt.subplots(1,3, figsize=(16,8))
cmap = 'YlOrRd'

for i in range(len(fig.axes)):
    # turn off tick marks
    axs[i].tick_params(axis='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    # turn off borders
    axs[i].spines['top'].set_visible(False)
    axs[i].spines['right'].set_visible(False)
    axs[i].spines['bottom'].set_visible(False)
    axs[i].spines['left'].set_visible(False)

gdf.plot(ax=axs[0], column='%Underserved', cmap=cmap)
gdf.plot(ax=axs[1], column='%Unserved', cmap=cmap)
gdf.plot(ax=axs[2], column='%Eligible', cmap=cmap)

axs[0].set_title('Underserved', fontsize=20, pad=5)
axs[1].set_title('Unserved', fontsize=20, pad=5)
axs[2].set_title('Eligible', fontsize=20, pad=5)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=0,vmax=1))
sm.set_array([])
cbar = plt.colorbar(sm, ticks=np.linspace(0,1, 11), boundaries=np.arange(0,1.1,.1), ax=axs, shrink=.5)
cbar.ax.set_yticklabels(['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%'])

# save fig in various formats
for i in [100, 300, 600]:
        file_path = 'eligible_areas_' + str(i) + 'dpi.png'
        plt.savefig(PurePath('../img/eligible_areas/', file_path), dpi=i,bbox_inches='tight')
plt.savefig(PurePath('../img/eligible_areas/eligible_areas.svg'), transparent=True,bbox_inches='tight')

#plt.show()