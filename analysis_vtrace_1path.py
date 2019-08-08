import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
from scipy import stats
import preprocess as pre
import itertools
from collections import OrderedDict 
import functions

# directory and filename
group_directory = 'Variables/'
figure_directory = 'Figures/'
filename = 'vtrace_df_1path.pkl'
filename_slopes = 'slopes_df_1path.pkl'
# filename_asif = 'slopes_df_asif.pkl'
# load group data class object
df_vtrace=pd.read_pickle(group_directory+filename)
df_slopes = pd.read_pickle(group_directory+filename_slopes)
# df_asif = pd.read_pickle(group_directory+filename_asif)
df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
# df_all = df_all.append(df_asif, ignore_index=True, )
# list conditions to sort data by
conditions = ['field_polarity_0_vtrace', 'induction_location_0_vtrace', 'field_mag_0_vtrace']
# {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
constraints_spec = OrderedDict(
    [
    ('date_vtrace', {
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

df_sorted = functions._sortdf(df=df_merged, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

# print df_sorted.keys()
# figures = [('anodal','cathodal','control', 'apical', '0','20'), ('anodal','cathodal','control', 'basal','0','20'),]
figures = [('anodal','apical', '0','20'), ('cathodal','apical', '0','20'), ('control','apical', '0','20'),]
titles=OrderedDict(zip(figures,
    ['strong only', 'strong + weak', 'weak only']
    ))


# FIXME change colors for before after
colors = {'anodal':(1, .5,0.5), 'control':(0.5,.5,.5), 'cathodal':(0.5,0.5,1)}
colors_post = {'anodal':(1,0,0), 'control':(0,0,0), 'cathodal':(0,0,1)}
markers = {'apical':'o', 'basal':'o', '20':'x'}

red = (1,0,0)
black = (0,0,0)
red_light = (1,0.7, 0.7)
gray = (0.7,0.7, 0.7)
blue_light = (0.7,0.7, 1)
blue = (0,0, 1)

figure_params_burst = {
    'params':{
        # 'ylim_all':True,
        'xlim_all':True,
        # 'ylim':[0.9,2.6],
        'ylabel':'Field potential (mV)',
        'xlabel':'Time (ms)',
        'average_across_bursts':True,
        'burst_number':2,
        'induction_number':0,
        'yscale':1000.,
        'xscale':1000./10000.,

    },
    # figure name
    #_____________
    'Apical 20 Vm':{
        'params':{
            'rotation':0,
        },
        # subgroup of traces
        #____________________
        'Apical 20 Vm':{
            'params':{
                'plot_individual_trace':[],
                'plot_mean':True

            },
            # individual traces
            #__________________
            ('control', 'apical', '0'): {
                # trace parameters
                'color':black,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':gray,
                    'alpha':1,

                }
            },
            # individual traces
            #___________________
            ('anodal', 'apical', '20'): {
                # trace parameters
                'color':red,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':red,
                    'alpha':1,
                }
            },

            ('cathodal', 'apical', '20'): {
                # trace parameters
                'color':blue,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':blue,
                    'alpha':1,

                }
            },
        },
    },

    'Basal 20 Vm':{
        'params':{
        'rotation':0,

        },
        # subgroup of traces
        #____________________
        'Basal 20 Vm':{
            'params':{
                'plot_individual_trace':[],
                'plot_mean':True

            },
            # individual traces
            #__________________
            ('control', 'basal', '0'): {
                # trace parameters
                'color':black,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':black,
                    'alpha':1,

                }
            },
            # individual traces
            #___________________
            ('anodal', 'basal', '20'): {
                # trace parameters
                'color':red,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':red,
                    'alpha':1,

                }
            },
            ('cathodal', 'basal', '20'): {
                # trace parameters
                'color':blue,
                'label': '5Hz',
                'location':1,
                'shade_error':True,
                'linewidth':4,
                # error bar parameters
                #______________________
                'e_params':{
                    'color':blue,
                    'alpha':1,

                }
            },
        },
    },   
}

# vtrace_figs, vtrace_axes = functions._plot_vtrace(df_sorted=df_sorted, figures=figures, variable='data_aligned_0', colors=colors, markers=markers, titles=titles, mean=True, figures_any=True, conditions=conditions, shade_error=True, colors_post=colors_post)



# for fig_key, fig in burst_figs.iteritems():
#     fname = figure_directory+str(fig_key)+'.png'
#     fig.savefig(fname, format='png')


# burst_figs, burst_axes = functions._plot_induction_bursts(df_sorted=df_sorted, figure_params=figure_params_burst, variable='data_induction_data_filt_iir_high_5_sortby_burst_apical')

# for fig_key, fig in burst_figs.iteritems():
#     fname = figure_directory+'_induction_burst_trace_soma_'+str(fig_key)+'_1path.png'
#     fig.savefig(fname, format='png')

# burst_figs, burst_axes = functions._plot_induction_bursts(df_sorted=df_sorted, figure_params=figure_params_burst, variable='data_induction_data_filt_iir_high_5_sortby_burst_soma')

# for fig_key, fig in burst_figs.iteritems():
#     fname = figure_directory+'_induction_burst_trace_apical_'+str(fig_key)+'_1path.png'
#     fig.savefig(fname, format='png')

burst_figs, burst_axes = functions._plot_induction_bursts(df_sorted=df_sorted, figure_params=figure_params_burst, variable='data_induction_data_filt_iir_high_1000_sortby_burst_soma')

for fig_key, fig in burst_figs.iteritems():
    fname = figure_directory+'_induction_burst_trace_apical_'+str(fig_key)+'_1path.png'
    fig.savefig(fname, format='png')



