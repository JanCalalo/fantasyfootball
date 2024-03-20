
import matplotlib.pyplot as plt
import numpy as np
import nfl_data_py as nfl

team_desc = nfl.import_team_desc()

def logo_scatter_indiv(ax,x,y,s,team_abbr = None,team_id= None):

    if team_abbr is not None:


        team_logo_url = team_desc[team_desc['team_abbr'] == team_abbr]['team_logo_wikipedia'][0]

    elif team_id is not None:


        team_logo_url = team_desc[team_desc['team_id'] == team_id]['team_logo_wikipedia'][0]
    else:
        raise ValueError("No Team Identifier")

    im_ax =ax.inset_axes([x-s/2,y-s/2,s/2,s/2], transform=ax.transData)
    im_ax.imshow(plt.imread(team_logo_url))
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
        








