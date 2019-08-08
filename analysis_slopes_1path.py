import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
from scipy import stats
import preprocess as pre
import itertools
from collections import OrderedDict 
import functions

# merge analysis of 1 path and 2 path data
# clean up code and add comments
# create figures that compare model and experiment
# plot baseline average trace for each condition
# plot hilbert transform trace to see if it reflects population spike
# update vargen vtrace to automatically process different filtered variables an locations
# analyze area under bursts without renormalizing each pulse


# directory and filename
group_directory = 'Variables/'
figure_directory='Figures/'
filename = 'slopes_df_1path.pkl'
filename_asif = 'slopes_df_asif.pkl'
# load group data class object
df_all=pd.read_pickle(group_directory+filename)
df_asif = pd.read_pickle(group_directory+filename_asif)

df_all = df_all.append(df_asif, ignore_index=True, )
# list conditions to sort data by
conditions = ['field_polarity_0', 'induction_location_0', 'field_mag_0']
# {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
constraints_spec = OrderedDict(
    [
    ('date', {
        ('apical', ):['>=',0],#20181113
        ('basal', ):['>=', 20170405],
        ('perforant', ):['>=',20170426]
        }),
    ('remove', {
        ('apical'):['==',False], 
        ('basal'): ['==',False],
        ('peforant'):['==',False]
        }),
    ]) 

# print constraints_spec.keys()
# constraint applied to all conditions. this gets overwritten by specific constraints
constraints_all = OrderedDict([
    # ('remove', ['==',False])
    ])


df_sorted = functions._sortdf(df=df_all, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

# FIXME use mutliindex dtaframe for passing figure parameters
# print df_sorted.keys()
figures = [('anodal','cathodal','control', 'apical', '0','1'),('anodal','cathodal','control', 'apical', '0','5'),('anodal','cathodal','control', 'apical', '0','20'), ('anodal','cathodal','control', 'basal','0','20'),('trough','peak','control', 'apical','0','20')]
titles=OrderedDict(zip(figures,
    ['strong only', 'strong + weak', 'weak only']
    ))
colors = {'anodal':(1,0,0), 'control':'k', 'cathodal':(0,0,1), 'peak':(0,0,1),'trough':(1,0,0)}
markers = {'apical':'o', 'basal':'o', '20':'x'}

common_ylim=False

# FIXME, function that takes arbitrary parameters, checks if they are attributes of the corresponding figure and sets that attribute accordingly e.g...
# loop over parameters in dict
# check if dict key is attribute of axes
# if attribute set attribute to val
# figs, axes = functions._plot_timeseries(df_sorted=df_sorted, figures=figures, variable='slopes_norm_aligned_0', colors=colors, markers=markers, titles=titles, mean=True, figures_any=True, conditions=conditions, shade_error=False, common_ylim=common_ylim, show_stats=False)

# figs_ind, axes_ind = functions._plot_timeseries(df_sorted=df_sorted, figures=figures, variable='slopes_ind_norm', colors=colors, markers=markers, titles=titles, mean=True, figures_any=True, conditions=conditions, shade_error=False, common_ylim=common_ylim, ylim=[0, 1.3], xlim=[-1,60])

# for fig_key, fig in figs.iteritems():
#     fname = figure_directory+'slopes_1path_'+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=350)

# for fig_key, fig in figs_ind.iteritems():
#     fname = figure_directory+'slopes_1path_ind_'+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=350)

# dose response
#=====================================================================================
red = (1,0,0)
black = (0,0,0)
red_light = (1,0.7, 0.7)
gray = (0.7,0.7, 0.7)
blue = (0,0,1)
figure_params = {
    'params':{
        'ylim_all':True,
        'markersize':15,

    },
    # figure name
    'mean':{
        'params':{
        'rotation':0

        },
        # subgroup of traces
        'control':{
            'params':{

            },
            # individual traces
            ('control', 'apical', '0'): {
                # trace parameters
                'color':black,
                'label': '0',
                'location':0,
            },
        },

        'anodal':{
            'params':{

            },
            # individual traces
            ('anodal', 'apical', '1'): {
                # trace parameters
                'color':red,
                'label':'1',
                'location':1,

            },
            
            ('anodal', 'apical', '5'):{
                'color':red,
                'label':'5',
                'location':5,
            },
            ('anodal', 'apical', '10'):{
                'color':red,
                'label':'10',
                'location':10,
            },
            ('anodal', 'apical', '20'):{
                'color':red,
                'label':'20',
                'location':20,
            },
        },
        'cathodal':{
            'params':{

            },
            
            ('cathodal', 'apical', '5'):{
                'color':blue,
                'label':'5',
                'location':-5,
            },
            ('cathodal', 'apical', '10'):{
                'color':blue,
                'label':'10',
                'location':-10,
            },
            ('cathodal', 'apical', '20'):{
                'color':blue,
                'label':'20',
                'location':-20,
            },
        },
    },
}


print 'fig_params:',figure_params.keys()
bar_figs, bar_axes = functions._plot_dose_response_all(df_sorted=df_sorted, figure_params=figure_params, variable='ltp_final')

print 'fig_params:',figure_params.keys()
bar_figs, bar_axes = functions._plot_dose_response_mean(df_sorted=df_sorted, figure_params=figure_params, variable='ltp_final')