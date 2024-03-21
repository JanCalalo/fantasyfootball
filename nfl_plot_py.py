
import matplotlib.pyplot as plt
import numpy as np
import nfl_data_py as nfl
from PIL import Image as pil_image
import requests
from io import BytesIO

team_desc = nfl.import_team_desc()
team_desc['loaded_logos'] = [[] for x in range(len(team_desc))]
for i in range(len(team_desc)):
    curr_im = team_desc.loc[i,'team_logo_espn']
    loaded_im = np.asarray(pil_image.open(BytesIO(requests.get(curr_im).content)))
    team_desc.loc[i,'loaded_logos'] = [loaded_im]


def logo_scatter_indiv(ax,x,y,s,team_abbr = None,team_id= None):

    if team_abbr is not None:


        img = team_desc[team_desc['team_abbr'] == team_abbr]['loaded_logos'][0]

    elif team_id is not None:


        img = team_desc[team_desc['team_id'] == team_id]['loaded_logos'][0]
    else:
        raise ValueError("No Team Identifier")


#    s_scale = ax.asp
    im_ax =ax.inset_axes([x-s/2,y-s/2,s,s], transform=ax.transData)#, bbox_to_anchor=[0.5, 0.5], loc='center')
    

    
    im_ax.imshow(img)

    im_ax.set_aspect('equal')
    return(ax)

def logo_scatter(ax,x,y,s,team_abbrs=None,team_ids=None):

    data_points = np.size(x)[0]

    if np.size(x)[0] != np.size(y)[0]:
        raise ValueError("Size Mismatch")
    elif np.size(x)[0] != np.size(y)[0]:
        raise ValueError("Size Mismatch")

    if np.size(s) == 1:
        s = np.ones(data_points)*s

    for i in range(data_points):
        if team_abbrs is not None:
           _ = logo_scatter_indiv(ax,x[i],y[i],s[i],team_abbr = team_abbrs[i])
        elif team_ids is not None:
           _ = logo_scatter_indiv(ax,x[i],y[i],s[i],team_id = team_ids[i])
        else:
            raise ValueError("No Team Identifier")
    
    return ax
        








