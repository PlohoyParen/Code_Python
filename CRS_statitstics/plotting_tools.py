import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

## this function controls the size on bars on the graphs 
def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value
        # we change the bar width
        patch.set_width(new_value)
        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

## creates proper labels
def getLabels(xticklabels):
    """ takes fig.get_xticklabels() """
    labels =[]
    for x in xticklabels:
        x = str(x).replace(" 00:00:00","").replace("Text(0, 0, '", "").replace("T00:00:00.000000000')", "")
        labels.append(x)
    return labels

def plot_crs_stats(fsw_df):
    pal = sns.color_palette("Set2")
    ## plot scores vs years
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(25,10))
    fig_scores = sns.barplot(x = 'Date of invitation', y = 'Scores', hue = 'Year',
                             data = fsw_df, ax=ax1, palette = pal)
    ## settings for axis labels
    fig_scores.set_xticklabels(getLabels(fig_scores.get_xticklabels()), fontsize=8, rotation=90)
    fig_scores.set(ylim = (420, 480))
    change_width(ax1, 0.85)
    
    ## plot number of invitations vs years
    fig_invites = sns.barplot(x = 'Date of invitation', y = 'Number of invitations (Top #)', 
                               hue = 'Year', data = fsw_df, ax=ax2, palette = pal)
    ## settings for axis labels 
    fig_invites.set_xticklabels(getLabels(fig_invites.get_xticklabels()), fontsize=8, rotation=90)
    fig_invites.set(ylim = (2600, 4100))
    change_width(ax2, 0.85)
    fig.savefig('CRS_statistics.png')