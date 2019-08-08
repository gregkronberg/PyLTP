import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import functions
from collections import OrderedDict 
import itertools
import pdb
import copy
import inspect
import math

def _format_figures(fig, ax, figdf, tick_max=40):
    '''
    '''
    # get ylim and xlim across all figures
    #-------------------------------------
    xlim={}
    ylim={}
    xlims=[]
    ylims=[]
    # iterate over figures
    for figkey in ax:
        # get ticks
        yticks = ax[figkey].get_yticks()
        xticks = ax[figkey].get_xticks()
        # apply scaling to ticks
        #-------------------------------------
        if 'fig_yscale' in figdf:

            yscale = figdf.loc[figkey].fig_yscale.unique()[0]
            print 'yscale', yscale
            yticks = yscale*yticks
        if 'fig_xscale' in figdf:
            xscale = figdf.loc[figkey].fig_xscale.unique()[0]
            xticks = xscale*xticks
        ax[figkey].set_yticks(yticks)
        ax[figkey].set_xticks(xticks)
        # get updated lims
        xlim[figkey] = functions._to_1sigfig(ax[figkey].get_xlim())
        ylim[figkey] = functions._to_1sigfig(ax[figkey].get_ylim())
        # print ylim
        xlims.append(copy.copy(xlim[figkey]))
        ylims.append(copy.copy(ylim[figkey]))
    # find x and y lims across all figures in group
    xlim_all = [min([temp[0] for temp in xlims]), max([temp[1] for temp in xlims])]
    ylim_all = [min([temp[0] for temp in ylims]), max([temp[1] for temp in ylims])]

    # iterate over figures and update attributes
    #---------------------------------------------
    for figkey, axes in ax.iteritems():
        # get x and y lims
        ylim_current = list(ax[figkey].get_ylim())
        xlim_current = list(ax[figkey].get_xlim())
        # set ylim across all figures
        #----------------------------
        if all(figdf.fig_ylim_all):
            xlim_current = xlim_all
            ylim_current = ylim_all
        if 'fig_ymin' in figdf.keys():
            ylim_current[0] = figdf.loc[figkey].fig_ymin.unique()[0]
        if 'fig_xmin' in figdf.keys():
            xlim_current[0] = figdf.loc[figkey].fig_xmin.unique()[0]
        if 'fig_ymax' in figdf.keys():
            ylim_current[1] = figdf.loc[figkey].fig_ymax.unique()[0]
        if 'fig_xmax' in figdf.keys():
            xlim_current[1] = figdf.loc[figkey].fig_xmax.unique()[0]

        ax[figkey].set_ylim(ylim_current)
        ax[figkey].set_xlim(xlim_current)

        # set x and y ticks
        #------------------------------------------------------------------
        print 'setting ticks'
        # get current lims and ticks
        xlim[figkey] = copy.copy(list(ax[figkey].get_xlim()))
        ylim[figkey] = copy.copy(list(ax[figkey].get_ylim()))
        xticks = ax[figkey].get_xticks()
        yticks = ax[figkey].get_yticks()
        nyticks=5
        dyticks = float(abs(ylim[figkey][1]-ylim[figkey][0]))/nyticks
        nxticks=5
        dxticks = float(abs(xlim[figkey][1]-xlim[figkey][0]))/nxticks
        # print 'ylim', ylim[figkey]
        if 'fig_dyticks' in figdf:
            dyticks = figdf.loc[figkey].fig_dyticks.unique()[0]
            nyticks = len(np.arange(ylim[figkey][0], ylim[figkey][1], dyticks))
        elif 'fig_nyticks' in figdf:
            nyticks = figdf.loc[figkey].fig_nyticks.unique()[0]
            dyticks = float(abs(ylim[figkey][1]-ylim[figkey][0]))/nyticks
        # else:
        #     nyticks=5
        #     dyticks = float(abs(ylim[figkey][1]-ylim[figkey][0]))/nyticks

        if nyticks>tick_max:
            nyticks=tick_max
            dyticks = float(abs(ylim[figkey][1]-ylim[figkey][0]))/nyticks
        if 'fig_ytick_assert' in figdf:
            ytick_assert = figdf.loc[figkey].fig_ytick_assert.unique()[0]
        else:
            ytick_assert = ylim[figkey][0]
        print ylim[figkey]
        print ytick_assert
        yticks_new_1 = np.flip(np.arange(ytick_assert, ylim[figkey][0], -dyticks))
        print yticks_new_1
        yticks_new_2 = np.arange(ytick_assert, ylim[figkey][1], dyticks)
        yticks_new = np.append(yticks_new_1, yticks_new_2)

        if 'fig_dxticks' in figdf:
            dxticks = figdf.loc[figkey].fig_dxticks.unique()[0]
            nxticks = len(np.arange(xlim[figkey][0], xlim[figkey][1], dxticks))
        elif 'fig_nxticks' in figdf:
            nxticks = figdf.loc[figkey].fig_nxticks.unique()[0]
            dxticks = float(abs(xlim[figkey][1]-xlim[figkey][0]))/nxticks
        # else:
        #     nxticks=5
        #     dxticks = float(abs(xlim[figkey][1]-xlim[figkey][0]))/nxticks
        if nxticks>tick_max:
            nxticks=tick_max
            dxticks = float(abs(xlim[figkey][1]-xlim[figkey][0]))/nxticks
        if 'fig_xtick_assert' in figdf:
            xtick_assert = figdf.loc[figkey].fig_xtick_assert.unique()[0]
        else:
            xtick_assert = xlim[figkey][0]
            xtick_assert = functions._to_1sigfig(xtick_assert)
        xticks_new_1 = np.flip(np.arange(xtick_assert, xlim[figkey][0], -dxticks))
        xticks_new_2 = np.arange(xtick_assert, xlim[figkey][1], dxticks)
        xticks_new = np.append(xticks_new_1, xticks_new_2)

        if 'fig_ytick_round' in figdf:
            decimals = figdf.loc[figkey].fig_ytick_round.unique()[0]
            yticks_new = np.round(yticks_new, decimals=decimals)

        if 'fig_xtick_round' in figdf:
            decimals = figdf.loc[figkey].fig_xtick_round.unique()[0]
            xticks_new = np.round(xticks_new, decimals=decimals)

        print 'yticks_new',yticks_new
        print 'xticks_new',xticks_new
        ax[figkey].set_yticks(yticks_new)
        ax[figkey].set_xticks(xticks_new)

        # set tick decimal places
        #---------------------------------------------------------------
        if 'fig_xtick_decimals' in figdf:
            dec = figdf.loc[figkey].fig_xtick_decimals.unique()[0]
            ax[figkey].xaxis.set_major_formatter(FormatStrFormatter('%.{}f'.format(dec)))
        if 'fig_ytick_decimals' in figdf:
            dec = figdf.loc[figkey].fig_ytick_decimals.unique()[0]
            ax[figkey].yaxis.set_major_formatter(FormatStrFormatter('%.{}f'.format(dec)))




        #     yticks = np.arange(ylim[figkey][0], ylim[figkey][1], figdf.loc[figkey].fig_dyticks.unique()[0])
        # elif 'fig_nyticks' in figdf:
        #     dstep = float(abs(ylim[figkey][1]-ylim[figkey][0]))/figdf.loc[figkey].fig_nyticks.unique()[0]
        #     yticks = np.arange(ylim[figkey][0], ylim[figkey][1], dstep)

        # if 'fig_dxticks' in figdf:
        #     xticks = np.arange(xlim[figkey][0], xlim[figkey][1], figdf.loc[figkey].fig_dxticks.unique()[0])
        # elif 'fig_nxticks' in figdf:
        #     dstep = float(abs(xlim[figkey][1]-xlim[figkey][0]))/figdf.loc[figkey].fig_nxticks.unique()[0]
        #     xticks = np.arange(xlim[figkey][0], xlim[figkey][1], dstep)
        # print 'resetting ticks'
        # print xticks
        # # print len(yticks)
        # # print xticks
        # ax[figkey].set_yticks(yticks)
        # ax[figkey].set_xticks(xticks)

        

        # set ticklabel attributes
        #--------------------------
        print 'setting ticklabels'
        for temp in ax[figkey].get_xticklabels():
            temp.set_fontweight(figdf.loc[figkey].fig_xtick_fontweight.unique()[0])
            temp.set_fontsize(figdf.loc[figkey].fig_xtick_fontsize.unique()[0])
        for temp in ax[figkey].get_yticklabels():
            temp.set_fontweight(figdf.loc[figkey].fig_ytick_fontweight.unique()[0])
            temp.set_fontsize(figdf.loc[figkey].fig_ytick_fontsize.unique()[0])

        # turn off axes box
        #------------------
        if all(figdf.loc[figkey].fig_boxoff):
            ax[figkey].spines['right'].set_visible(False)
            ax[figkey].spines['top'].set_visible(False)

        if 'fig_axesoff' in figdf.keys() and all(figdf.loc[figkey].fig_axesoff):
            ax[figkey].set_axis_off()

        # set axes linewidth and tick position
        #----------------------
        ax[figkey].spines['left'].set_linewidth(figdf.loc[figkey].fig_axes_linewidth.unique()[0])
        ax[figkey].spines['bottom'].set_linewidth(figdf.loc[figkey].fig_axes_linewidth.unique()[0])
        ax[figkey].xaxis.set_ticks_position('bottom')
        ax[figkey].yaxis.set_ticks_position('left')

        # set axes labels
        #----------------

        # print 'fontsize',figdf['fig_xlabel_fonstize']
        # print 'fontsize',figdf.loc[figkey]['fig_xlabel_fonstize']
        # print 'fontsize',figdf.loc[figkey]['fig_xlabel_fonstize'].unique()[0]
        # print 'fontsize',figdf.loc[figkey].fig_xlabel_fontsize.unique()
        ax[figkey].set_xlabel(figdf.loc[figkey].fig_xlabel.unique()[0], fontsize=figdf.loc[figkey]['fig_xlabel_fontsize'].unique()[0], fontweight=figdf.loc[figkey].fig_xlabel_fontweight.unique()[0])
        ax[figkey].set_ylabel(figdf.loc[figkey].fig_ylabel.unique()[0], fontsize=figdf.loc[figkey]['fig_ylabel_fontsize'].unique()[0], fontweight=figdf.loc[figkey].fig_ylabel_fontweight.unique()[0])

        # set tight layout
        #-------------------
        if all(figdf.loc[figkey].fig_tight_layout):
            plt.figure(fig[figkey].number)
            plt.tight_layout()

    return fig, ax

def _default_figdf():
        '''
        '''
        all_dict={
        # hide the top and right axes boundaries
            'fig_dpi':350,
            'fig_boxoff':True,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[25],#'xx-large',#[25],
            'fig_ylabel_fontsize':[25],#'xx-large',#[25],
            'fig_xlabel_fontweight':[1000],#'extra bold',
            'fig_ylabel_fontweight':[1000],#'extra bold',
            'fig_xtick_fontsize':[20],#'large',#[15],
            'fig_ytick_fontsize':[20],#'large',#[15],
            'fig_xtick_fontweight':[1000], #'extra bold',#'light', #1000, #'heavy',
            'fig_ytick_fontweight':[1000],# 'extra bold',#'light', #1000,#'heavy',
            # figure tight layout
            'fig_tight_layout':True,
        }
        all_df = pd.DataFrame(all_dict, dtype='object')

        return all_df

class BuildFigDF:
    '''
    '''
    def __init__(self):
        '''
        '''

        # set dpi for final png image
        #----------------------------
        self.dpi=350

        # colors for plots
        #-------------------
        self.black = (0,0,0)
        self.gray = (0.7,0.7, 0.7)
        self.red = (1,0,0)
        self.red_light = (1,0.7, 0.7)
        self.blue=(0,0,1)
        self.blue_light = (0.7, 0.7, 1)


    def _slopes_probe(self):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            #-------------------------------------------------
            'apical TBS only all 20 Vm':{
                # subgroup
                'apical TBS only all 20 Vm':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),

                ]
            },
            #-------------------------------------------------
            'apical TBS 1path 5 Vm':{
                # subgroup
                'apical TBS only 5 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            #---------------------------------------------------
            'apical TBS 1path 20 Vm':{
                # subgroup
                'apical TBS only 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                ]
            },

            # figure
            #-----------------------------------------------------
            'basal TBS 1path 20 Vm':{
                # subgroup
                'basal TBS 1path 20 Vm':[
                    # trace
                    ('TBS', 'None', 'basal', 'control', '0'),
                    ('TBS', 'None', 'basal', 'anodal', '20'),
                    ('TBS', 'None', 'basal', 'cathodal', '20'),
                ]
            },
            # figure
            #-----------------------------------------------------
            'apical TBS 1path ac 20 Vm':{
                # subgroup
                'apical TBS 1path ac 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'trough', '20'),
                    ('TBS', 'None', 'apical', 'peak', '20'),
                ]
            },

            # figure
            #------------------------------------------------
            'apical TBS 1path allfield':{
                # subgroup
                'apical TBS only 1path allfield':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },

            'strong unpaired':{
                # subgroup
                'strong unpaired':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('nostim', 'TBS', 'apical', 'control', '0'),
                    ('nostim', 'TBS', 'apical', 'anodal', '20'),

                ]
            },

            # figure
            #---------------------------------------------------
            'weak unpaired':{
                # subgroup
                'weak unpaired':[
                    # trace
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('nostim','weak5Hz', 'apical', 'control', '0'),
                    ('nostim','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },

            # figure
            #---------------------------------------------------
            'paired':{
                # subgroup
                'paired':[
                    # trace
                    ('weak5Hz','TBS', 'apical', 'control', '0'),
                    ('weak5Hz','TBS', 'apical', 'anodal', '20'),
                    ('TBS','weak5Hz', 'apical', 'control', '0'),
                    ('TBS','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },
        }
        # load default figure parameters and colors
        #------------------------------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        figdf['trace_markersize']=10
        # print figdf.fig_nyticks
        figdf['fig_nyticks']=5
        figdf['fig_nxticks']=10
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        figdf['fig_ylim_all']=True
        figdf['fig_xlim_all']=True
        figdf['fig_ymin']=0.8
        figdf['fig_xmin']=0.
        figdf['fig_ylabel']='Normalized fEPSP slope'
        figdf['fig_xlabel']='Time (min)'
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_style']='shade'
        figdf['trace_linewidth']=4


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']='temp'
        figdf['error_color']='temp'
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:
            if 'control' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'error_color']=gray
                else:
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'error_color']=black
            elif 'anodal' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'error_color']=red_light
                else:
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'error_color']=red
            elif 'cathodal' in key[2]:
                figdf.at[key, 'trace_color']=blue
                figdf.at[key, 'error_color']=blue
            elif 'trough' in key[2]:
                figdf.at[key, 'trace_color']=red
                figdf.at[key, 'error_color']=red
            elif 'peak' in key[2]:
                figdf.at[key, 'trace_color']=blue
                figdf.at[key, 'error_color']=blue
            if key[0]=='strong unpaired':
                if 'control' in key[2]:
                    if key[2][0]=='nostim':
                        figdf.at[key, 'trace_color']=gray
                        figdf.at[key, 'error_color']=gray
                if 'anodal' in key[2]:
                    if key[2][0]=='nostim':
                        figdf.at[key, 'trace_color']=red_light
                        figdf.at[key, 'error_color']=red_light


        return figdf
    
    def _induction_variables(self):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            #-------------------------------------------------
            'apical TBS only all 20 Vm':{
                # subgroup
                'apical TBS only all 20 Vm':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),

                ]
            },
            #-------------------------------------------------
            'apical TBS 1path 5 Vm':{
                # subgroup
                'apical TBS only 5 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            #---------------------------------------------------
            'apical TBS 1path 20 Vm':{
                # subgroup
                'apical TBS only 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                ]
            },

            # figure
            #-----------------------------------------------------
            'basal TBS 1path 20 Vm':{
                # subgroup
                'basal TBS 1path 20 Vm':[
                    # trace
                    ('TBS', 'None', 'basal', 'control', '0'),
                    ('TBS', 'None', 'basal', 'anodal', '20'),
                    ('TBS', 'None', 'basal', 'cathodal', '20'),
                ]
            },
            # figure
            #-----------------------------------------------------
            'apical TBS 1path ac 20 Vm':{
                # subgroup
                'apical TBS 1path ac 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'trough', '20'),
                    ('TBS', 'None', 'apical', 'peak', '20'),
                ]
            },

            # figure
            #------------------------------------------------
            'apical TBS 1path allfield':{
                # subgroup
                'apical TBS only 1path allfield':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },

            'strong unpaired':{
                # subgroup
                'strong unpaired':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('nostim', 'TBS', 'apical', 'control', '0'),
                    ('nostim', 'TBS', 'apical', 'anodal', '20'),

                ]
            },

            # figure
            #---------------------------------------------------
            'weak unpaired':{
                # subgroup
                'weak unpaired':[
                    # trace
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('nostim','weak5Hz', 'apical', 'control', '0'),
                    ('nostim','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },

            # figure
            #---------------------------------------------------
            'paired':{
                # subgroup
                'paired':[
                    # trace
                    # ('weak5Hz','TBS', 'apical', 'control', '0'),
                    # ('weak5Hz','TBS', 'apical', 'anodal', '20'),
                    ('TBS','weak5Hz', 'apical', 'control', '0'),
                    ('TBS','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },
        }
        # load default figure parameters and colors
        #------------------------------------------
        # load default figure parameters and colors
        #------------------------------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        figdf['trace_markersize']=10
        # print figdf.fig_nyticks
        figdf['fig_nyticks']=5
        figdf['fig_nxticks']=10
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        figdf['fig_ylim_all']=True
        figdf['fig_xlim_all']=True
        figdf['fig_ymin']=0.8
        figdf['fig_xmin']=0.
        figdf['fig_ylabel']='Norm. fEPSP slope'
        figdf['fig_xlabel']='Time (min)'
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_style']='shade'
        figdf['trace_linewidth']=4


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']='temp'
        figdf['error_color']='temp'
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:
            if 'control' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'error_color']=gray
                else:
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'error_color']=black
            elif 'anodal' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'error_color']=red_light
                else:
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'error_color']=red
            elif 'cathodal' in key[2]:
                figdf.at[key, 'trace_color']=blue
                figdf.at[key, 'error_color']=blue
            elif 'trough' in key[2]:
                figdf.at[key, 'trace_color']=red
                figdf.at[key, 'error_color']=red
            elif 'peak' in key[2]:
                figdf.at[key, 'trace_color']=blue
                figdf.at[key, 'error_color']=blue

        return figdf
    
    def _baseline_input_output(self):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            #-------------------------------------------------
            'apical TBS only all 20 Vm':{
                # subgroup
                'apical TBS only all 20 Vm':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),

                ]
            },
            #-------------------------------------------------
            'apical TBS 1path 5 Vm':{
                # subgroup
                'apical TBS only 5 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            #---------------------------------------------------
            'apical TBS 1path 20 Vm':{
                # subgroup
                'apical TBS only 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                ]
            },

            # figure
            #-----------------------------------------------------
            'basal TBS 1path 20 Vm':{
                # subgroup
                'basal TBS 1path 20 Vm':[
                    # trace
                    ('TBS', 'None', 'basal', 'control', '0'),
                    ('TBS', 'None', 'basal', 'anodal', '20'),
                    ('TBS', 'None', 'basal', 'cathodal', '20'),
                ]
            },
            # figure
            #-----------------------------------------------------
            'apical TBS 1path ac 20 Vm':{
                # subgroup
                'apical TBS 1path ac 20 Vm':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'trough', '20'),
                    ('TBS', 'None', 'apical', 'peak', '20'),
                ]
            },

            # figure
            #------------------------------------------------
            'apical TBS 1path allfield':{
                # subgroup
                'apical TBS only 1path allfield':[
                    # trace
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },

            'strong unpaired':{
                # subgroup
                'strong unpaired':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('nostim', 'TBS', 'apical', 'control', '0'),
                    ('nostim', 'TBS', 'apical', 'anodal', '20'),

                ]
            },

            # figure
            #---------------------------------------------------
            'weak unpaired':{
                # subgroup
                'weak unpaired':[
                    # trace
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('nostim','weak5Hz', 'apical', 'control', '0'),
                    ('nostim','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },

            # figure
            #---------------------------------------------------
            'paired':{
                # subgroup
                'paired':[
                    # trace
                    # ('weak5Hz','TBS', 'apical', 'control', '0'),
                    # ('weak5Hz','TBS', 'apical', 'anodal', '20'),
                    ('TBS','weak5Hz', 'apical', 'control', '0'),
                    ('TBS','weak5Hz', 'apical', 'anodal', '20'),
                ]
            },
        }
        # load default figure parameters and colors
        #------------------------------------------
        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        figdf['trace_markersize']=15
        # print figdf.fig_nyticks
        figdf['fig_nyticks']=5
        figdf['fig_nxticks']=10
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        figdf['fig_ylim_all']=True
        figdf['fig_xlim_all']=True
        figdf['fig_ymin']=0.8
        figdf['fig_xmin']=0.
        figdf['fig_ylabel']='Normalized fEPSP slope'
        figdf['fig_xlabel']='Time (min)'
        figdf['fig_dyticks']=.2
        figdf['fig_dxticks']=20
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_style']='shade'
        figdf['trace_linewidth']=4


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']='temp'
        figdf['error_color']='temp'
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:
            if 'control' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'error_color']=gray
                else:
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'error_color']=black
            elif 'anodal' in key[2]:
                if key[2][0]=='weak5Hz':
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'error_color']=red_light
                else:
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'error_color']=black
            elif 'cathodal' in key[2]:
                figdf.at[key, 'trace_color']=black
                figdf.at[key, 'error_color']=black
            elif 'trough' in key[2]:
                figdf.at[key, 'trace_color']=red
                figdf.at[key, 'error_color']=red
            elif 'peak' in key[2]:
                figdf.at[key, 'trace_color']=blue
                figdf.at[key, 'error_color']=blue

        return figdf

    def _build_figdf_from_dict(self, figdict):
        '''
        '''
        # build multiindex for trace parameters
        multi_list = []
        level_names = ['figure','subgroup', 'trace']
        for level_1_key, level_1 in figdict.iteritems():
            for level_2_key, level_2 in level_1.iteritems():
                for level_3_i, level_3_key in enumerate(level_2):
                    multi_list.append((level_1_key, level_2_key, level_3_key))
        multiindex = pd.MultiIndex.from_tuples(multi_list, names=level_names)
        # build dataframe
        figdf = pd.DataFrame(index=multiindex, dtype='object')

        return figdf

    def _var2var_corr_all(self):
        '''
        '''
        # conditions for each figure
        #----------------------------
        figdict = {
            'all':{
                # subgroup
                'all':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                    ('TBS', 'weak5Hz', 'apical', 'control', '0'),
                    ('TBS', 'weak5Hz', 'apical', 'anodal', '20'),
                    ('TBS', 'weak5Hz', 'apical', 'cathodal', '20'),
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('weak5Hz','nostim' ,'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'basal', 'control', '0'),
                    ('TBS', 'None', 'basal', 'anodal', '20'),
                    ('TBS', 'None', 'basal', 'cathodal', '20'),
                    ('weak5Hz', 'TBS', 'apical', 'control', '0'),
                    ('weak5Hz', 'TBS', 'apical', 'anodal', '20'),
                    ('weak5Hz', 'TBS', 'apical', 'cathodal', '20'),
                ]
            },

            'apical all':{
                # subgroup
                'apical all':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                    ('TBS', 'weak5Hz', 'apical', 'control', '0'),
                    ('TBS', 'weak5Hz', 'apical', 'anodal', '20'),
                    ('TBS', 'weak5Hz', 'apical', 'cathodal', '20'),
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('weak5Hz','nostim' ,'apical', 'cathodal', '20'),
                    ('weak5Hz', 'TBS', 'apical', 'control', '0'),
                    ('weak5Hz', 'TBS', 'apical', 'anodal', '20'),
                    ('weak5Hz', 'TBS', 'apical', 'cathodal', '20'),
                ]
            },
            # figure
            #-------------------------------------------------
            'apical TBS only all':{
                # subgroup
                'apical TBS only all':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            # figure
            #------------------------------------------------
            'apical TBS only 1path':{
                # subgroup
                'apical TBS only 1path':[
                    # trace
                    # ('TBS', 'nostim', 'apical', 'control', '0'),
                    ('TBS', 'None', 'apical', 'control', '0'),
                    # ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '20'),
                    ('TBS', 'None', 'apical', 'anodal', '5'),
                    # ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            # figure
            #-------------------------------------------------
            'apical TBS unpaired 2path':{
                # subgroup
                'apical TBS unpaired 2path':[
                    # trace
                    ('TBS', 'nostim', 'apical', 'control', '0'),
                    # ('TBS', 'None', 'apical', 'control', '0'),
                    ('TBS', 'nostim', 'apical', 'anodal', '20'),
                    # ('TBS', 'None', 'apical', 'anodal', '20'),
                    # ('TBS', 'None', 'apical', 'anodal', '5'),
                    ('TBS', 'nostim', 'apical', 'cathodal', '20'),
                    # ('TBS', 'None', 'apical', 'cathodal', '20'),
                    # ('TBS', 'None', 'apical', 'cathodal', '5'),
                ]
            },
            # figure
            #--------------------------------------------------
            'apical TBS paired':{
                # subgroup
                'apical TBS paired':[
                    # trace
                    ('TBS', 'weak5Hz', 'apical', 'control', '0'),
                    ('TBS', 'weak5Hz', 'apical', 'anodal', '20'),
                    ('TBS', 'weak5Hz', 'apical', 'cathodal', '20'),
                ]
            },
            # figure
            #---------------------------------------------------
            'apical weak paired':{
                # subgroup
                'apical weak paired':[
                    # trace
                    ('weak5Hz','TBS', 'apical', 'control', '0'),
                    ('weak5Hz','TBS', 'apical', 'anodal', '20'),
                    ('weak5Hz','TBS', 'apical', 'cathodal', '20'),
                ]
            },
            # figure
            #---------------------------------------------------
            'apical weak unpaired':{
                # subgroup
                'apical weak unpaired':[
                    # trace
                    ('weak5Hz','nostim', 'apical', 'control', '0'),
                    ('weak5Hz','nostim', 'apical', 'anodal', '20'),
                    ('weak5Hz','nostim' ,'apical', 'cathodal', '20'),
                ]
            },
            # figure
            #-----------------------------------------------------
            'basal TBS only':{
                # subgroup
                'basal TBS only':[
                    # trace
                    ('TBS', 'None', 'basal', 'control', '0'),
                    ('TBS', 'None', 'basal', 'anodal', '20'),
                    ('TBS', 'None', 'basal', 'cathodal', '20'),
                ]
            },
        }
        # print figdf
        default = Default()
        black = default.black
        gray = default.gray
        red=default.red
        red_light=default.red_light
        blue=default.blue
        blue_light=default.blue_light
        # create df for figure parameters
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace column as only index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default.all_df]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # apply to all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        figdf['trace_markersize']=10


        # individual trace parameters
        #----------------------------
        # get list of all trace names 
        trace_values = figdf.index.values
        figdf['trace_color']='temp'
        figdf['error_color']='temp'

        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        idx_keys = figdf.index.unique().values
        for key in idx_keys:
            if 'control' in key[2]:
                figdf.at[key, 'trace_color']=black
            elif 'anodal' in key[2]:
                figdf.at[key, 'trace_color']=red
            elif 'cathodal' in key[2]:
                figdf.at[key, 'trace_color']=blue

        return figdf
    
    def _induction_bar(self, path):
        '''
        '''
        if path=='1path':
            default = _default_figdf()
            black = self.black
            gray = self.gray
            red=self.red
            red_light=self.red_light
            blue=self.blue
            blue_light=self.blue_light
            # conditions for each figure
            #----------------------------
            figdict = {
                # # figure
                # 'apical 1 Vm dc':{
                #     # subgroup
                #     'apical 1 Vm dc':[
                #         # trace
                #         ('control', 'apical', '0'),
                #         ('anodal', 'apical', '1'),
                #         ('cathodal', 'apical', '1'),
                #     ]
                # },
                # 'apical 5 Vm dc':{
                #     # subgroup
                #     'apical 5 Vm dc':[
                #         # trace
                #         ('control', 'apical', '0'),
                #         ('anodal', 'apical', '5'),
                #         ('cathodal', 'apical', '5'),
                #     ]
                # },
                # 'apical 10 Vm dc':{
                #     # subgroup
                #     'apical 10 Vm dc':[
                #         # trace
                #         ('control', 'apical', '0'),
                #         ('anodal', 'apical', '10'),
                #         ('cathodal', 'apical', '10'),
                #     ]
                # },
                # 'apical 20 Vm dc':{
                #     # subgroup
                #     'apical 20 Vm dc':[
                #         # trace
                #         ('control', 'apical', '0'),
                #         ('anodal', 'apical', '20'),
                #         ('cathodal', 'apical', '20'),
                #     ]
                # },
                'apical 20 Vm ac':{
                    # subgroup
                    'apical 20 Vm ac':[
                        # trace
                        # ('control', 'apical', '0'),
                        # ('trough', 'apical', '20'),
                        # ('peak', 'apical', '20'),
                         # trace
                        ('TBS', 'None', 'apical', 'control', '0'),
                        ('TBS', 'None', 'apical', 'trough', '20'),
                        ('TBS', 'None', 'apical', 'peak', '20'),
                    ]
                },
                # 'basal 20 Vm dc':{
                #     # subgroup
                #     'basal 20 Vm dc':[
                #         # trace
                #         ('control', 'basal', '0'),
                #         ('anodal', 'basal', '20'),
                #         ('cathodal', 'basal', '20'),
                #     ]
                # },
                #---------------------------------------------------
                'apical TBS 1path 20 Vm':{
                    # subgroup
                    'apical TBS only 20 Vm':[
                        # trace
                        ('TBS', 'None', 'apical', 'control', '0'),
                        ('TBS', 'None', 'apical', 'anodal', '20'),
                        ('TBS', 'None', 'apical', 'cathodal', '20'),
                    ]
                },

                # figure
                #-----------------------------------------------------
                'basal TBS 1path 20 Vm':{
                    # subgroup
                    'basal TBS 1path 20 Vm':[
                        # trace
                        ('TBS', 'None', 'basal', 'control', '0'),
                        ('TBS', 'None', 'basal', 'anodal', '20'),
                        ('TBS', 'None', 'basal', 'cathodal', '20'),
                    ]
                },
            }

            # create df for figure parameters
            #---------------------------------
            figdf = functions._build_figure_params(figdict)
            # set trace column as only index
            figdf = figdf.reset_index().set_index('trace')
            # get default parameters
            figdf_default = pd.concat([default]*len(figdf))
            # set index of defaultdf to match figdf
            figdf_default.index=figdf.index
            # add default df to figdf
            figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

            # apply to all traces
            #---------------------
            # figure level parameters
            figdf['fig_topercent']=False
            figdf['fig_ylim_all']=False
            figdf['fig_xlim_all']=True
            figdf['fig_ymin']=1.
            figdf['fig_ymax']=1.61
            # figdf['fig_xmin']=0.
            figdf['fig_ylabel']='Norm. fEPSP slope'
            figdf['fig_xlabel']=''
            # figdf['fig_nyticks']=5
            # figdf['fig_nxticks']=10
            figdf['fig_dyticks']=.1
            # figdf['fig_dxticks']=20
            # trace level parameters
            figdf['error_alpha']=1
            figdf['error_style']='bar'
            figdf['trace_linewidth']=4
            figdf['fig_xtick_rotate']=0
            figdf['fig_barwidth']=1
            figdf['fig_barspacing']=1
            figdf['fig_groupspacing']=1
            figdf['sub_location']=1
            figdf['fig_ytick_decimals']=1

            # apply subgroup parameters
            #-------------------------------
            # reset to hierachichal
            # figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            # # set subgroup locations
            # figdf.loc[('weak_associative', 'control'), 'sub_location']=1
            # figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
            # figdf.loc[('specificity', 'control'), 'sub_location']=1
            # figdf.loc[('specificity', 'anodal'), 'sub_location']=4
            # # reset index to trace 
            # figdf = figdf.reset_index().set_index('trace')

            # individual trace parameters
            #----------------------------
            # get list of all trace names 
            trace_values = figdf.index.values
            # preallocate columns as 'object' dtype
            figdf['trace_color']='temp'
            figdf['trace_ecolor']='temp'
            # convert to hierarchical
            figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            idx_keys = figdf.index.unique().values
            for key in idx_keys:
                if 'control' in key[2]:
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']='control'

                elif 'anodal' in key[2]:
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=2
                    figdf.at[key, 'trace_label']='anodal'
                elif 'cathodal' in key[2]:
                    figdf.at[key, 'trace_color']=blue
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']='cathodal'
                elif 'trough' in key[2]:
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=2
                    figdf.at[key, 'trace_label']='peak'
                elif 'peak' in key[2]:
                    figdf.at[key, 'trace_color']=blue
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']='trough'

        elif path=='2path':
            # colors for plots
            #-------------------
            default = _default_figdf()
            black = self.black
            gray = self.gray
            red=self.red
            red_light=self.red_light
            blue=self.blue
            blue_light=self.blue_light

            # conditions for each figure
            #----------------------------
            figdict = {
                # figure
                'weak_associative':{
                    # subgroup
                    'control':[
                        # trace
                        ('control', 'weak5Hz', 'nostim'),
                        ('control', 'weak5Hz', 'TBS'),
                    ],
                    'anodal':[
                        # trace
                        ('anodal', 'weak5Hz', 'nostim'),
                        ('anodal', 'weak5Hz', 'TBS')
                    ]
                },
                'specificity':{
                    'control':[
                        ('control', 'TBS', 'nostim'),
                        ('control', 'nostim', 'TBS'),
                    ],
                    'anodal':[
                        ('anodal', 'TBS', 'nostim'),
                        ('anodal', 'nostim', 'TBS'),
                    ]
                },
                # figure
                'strong_associative':{
                    # subgroup
                    'control':[
                        # trace
                        ('control', 'TBS', 'weak5Hz'),
                        ('control', 'TBS', 'nostim'),
                    ],
                    'anodal':[
                        # trace
                        ('anodal', 'TBS', 'weak5Hz'),
                        ('anodal', 'TBS', 'nostim')
                    ]
                },
            }

            # create df for figure parameters
            #---------------------------------
            figdf = functions._build_figure_params(figdict)
            # set trace column as only index
            figdf = figdf.reset_index().set_index('trace')
            # get default parameters
            figdf_default = pd.concat([default]*len(figdf))
            # set index of defaultdf to match figdf
            figdf_default.index=figdf.index
            # add default df to figdf
            figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

            # apply to all traces
            #---------------------
            # figure level parameters
            figdf['fig_topercent']=False
            figdf['fig_ylim_all']=False
            figdf['fig_xlim_all']=True
            figdf['fig_ymax']=1.51
            figdf['fig_ymin']=1
            # figdf['fig_xmin']=0.
            # figdf['fig_ymax']=1.5
            figdf['fig_ylabel']='Norm. fEPSP slope'
            figdf['fig_xlabel']=''
            # figdf['fig_nyticks']=5
            # figdf['fig_nxticks']=10
            figdf['fig_dyticks']=.1
            # figdf['fig_dxticks']=20
            # trace level parameters
            figdf['error_alpha']=1
            figdf['error_style']='bar'
            figdf['trace_linewidth']=4
            figdf['fig_xtick_rotate']=0
            figdf['fig_barwidth']=1
            figdf['fig_barspacing']=1
            figdf['fig_groupspacing']=1
            figdf['fig_ytick_decimals']=1

            # apply subgroup parameters
            #-------------------------------
            # reset to hierachichal
            figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            # set subgroup locations
            figdf.loc[('weak_associative', 'control'), 'sub_location']=1
            figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
            figdf.loc[('strong_associative', 'control'), 'sub_location']=1
            figdf.loc[('strong_associative', 'anodal'), 'sub_location']=4
            figdf.loc[('specificity', 'control'), 'sub_location']=1
            figdf.loc[('specificity', 'anodal'), 'sub_location']=4

            figdf.loc[('weak_associative', 'control'), 'xticks_minor_loc']=1.5
            figdf.loc[('weak_associative', 'anodal'), 'xticks_minor_loc']=4.5
            figdf.loc[('strong_associative', 'control'), 'xticks_minor_loc']=1.5
            figdf.loc[('strong_associative', 'anodal'), 'xticks_minor_loc']=4.5
            figdf.loc[('specificity', 'control'), 'xticks_minor_loc']=1.5
            figdf.loc[('specificity', 'anodal'), 'xticks_minor_loc']=4.5
            # reset index to trace 
            figdf = figdf.reset_index().set_index('trace')

            # individual trace parameters
            #----------------------------
            # get list of all trace names 
            trace_values = figdf.index.values
            figdf['trace_color']='temp'
            figdf['trace_ecolor']='temp'

            figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            idx_keys = figdf.index.unique().values
            for key in idx_keys:
                #=======================================
                if key[2] == ('control','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                #=======================================
                elif key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'TBS'
                elif key[2] == ('control','nostim','TBS'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'Inactive'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'TBS'
                elif key[2] == ('anodal','nostim','TBS'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'Inactive'

                #=======================================
                elif key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'TBS'
                elif key[2] == ('control','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#TBS\n+5Hz'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'TBS'
                elif key[2] == ('anodal','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#TBS\n+5Hz'
        
        return figdf

    def _var2var_corr(self, path):
        '''
        '''
        if path=='1path':
            default = Default()
            black = default.black
            gray = default.gray
            red=default.red
            red_light=default.red_light
            blue=default.blue
            blue_light=default.blue_light
            # conditions for each figure
            #----------------------------
            figdict = {
                # figure
                'apical 1 Vm dc':{
                    # subgroup
                    'apical 1 Vm dc':[
                        # trace
                        ('control', 'apical', '0'),
                        ('anodal', 'apical', '1'),
                        ('cathodal', 'apical', '1'),
                    ]
                },
                'apical 5 Vm dc':{
                    # subgroup
                    'apical 5 Vm dc':[
                        # trace
                        ('control', 'apical', '0'),
                        ('anodal', 'apical', '5'),
                        ('cathodal', 'apical', '5'),
                    ]
                },
                'apical 10 Vm dc':{
                    # subgroup
                    'apical 10 Vm dc':[
                        # trace
                        ('control', 'apical', '0'),
                        ('anodal', 'apical', '10'),
                        ('cathodal', 'apical', '10'),
                    ]
                },
                'apical 20 Vm dc':{
                    # subgroup
                    'apical 20 Vm dc':[
                        # trace
                        ('control', 'apical', '0'),
                        ('anodal', 'apical', '20'),
                        ('cathodal', 'apical', '20'),
                    ]
                },
                'apical 20 Vm ac':{
                    # subgroup
                    'apical 20 Vm ac':[
                        # trace
                        ('control', 'apical', '0'),
                        ('trough', 'apical', '20'),
                        ('peak', 'apical', '20'),
                    ]
                },
                'basal 20 Vm dc':{
                    # subgroup
                    'basal 20 Vm dc':[
                        # trace
                        ('control', 'basal', '0'),
                        ('anodal', 'basal', '20'),
                        ('cathodal', 'basal', '20'),
                    ]
                },
            }
            # create df for figure parameters
            #---------------------------------
            figdf = functions._build_figure_params(figdict)
            # set trace column as only index
            figdf = figdf.reset_index().set_index('trace')
            # get default parameters
            figdf_default = pd.concat([default.corr_df]*len(figdf))
            # set index of defaultdf to match figdf
            figdf_default.index=figdf.index
            # add default df to figdf
            figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

            # apply to all traces
            #---------------------
            # figure level parameters
            figdf['fig_topercent']=False
            figdf['fig_ylim_all']=False
            figdf['fig_xlim_all']=False
            figdf['trace_markersize']=10

            # apply subgroup parameters
            #-------------------------------
            # # reset to hierachichal
            # figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            # # set subgroup locations
            # figdf.loc[('weak_associative', 'control'), 'sub_location']=1
            # figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
            # figdf.loc[('strong_associative', 'control'), 'sub_location']=1
            # figdf.loc[('strong_associative', 'anodal'), 'sub_location']=4
            # figdf.loc[('specificity', 'control'), 'sub_location']=1
            # figdf.loc[('specificity', 'anodal'), 'sub_location']=4
            # # reset index to trace 
            # figdf = figdf.reset_index().set_index('trace')

            # individual trace parameters
            #----------------------------
            # get list of all trace names 
            trace_values = figdf.index.values
            figdf['trace_color']='temp'
            figdf['error_color']='temp'

            figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            idx_keys = figdf.index.unique().values
            for key in idx_keys:
                if 'control' in key[2]:
                    figdf.at[key, 'trace_color']=black
                elif 'anodal' in key[2]:
                    figdf.at[key, 'trace_color']=red
                elif 'cathodal' in key[2]:
                    figdf.at[key, 'trace_color']=blue

        elif path=='2path':
            default = Default()
            # colors for plots
            #-------------------
            default = Default()
            black = default.black
            gray = default.gray
            red=default.red
            red_light=default.red_light
            blue=default.blue
            blue_light=default.blue_light

            # conditions for each figure
            #----------------------------
            figdict = {
                # figure
                'weak_associative':{
                    # subgroup
                    'weak_associative':[
                        # trace
                        ('control', 'weak5Hz', 'nostim'),
                        ('anodal', 'weak5Hz', 'nostim')
                        # ('control', 'weak5Hz', 'TBS'),
                    ],
                },
                'specificity':{
                    'specificity':[
                        ('control', 'TBS', 'nostim'),
                        ('anodal', 'TBS', 'nostim')
                        # ('control', 'nostim', 'TBS'),
                    ],
                },
                # figure
                'strong_associative':{
                    # subgroup
                    'strong associative':[
                        # trace
                        ('control', 'TBS', 'weak5Hz'),
                        ('anodal', 'TBS', 'weak5Hz')
                        # ('control', 'TBS', 'nostim'),
                    ],
                },
            }

            # create df for figure parameters
            #---------------------------------
            figdf = functions._build_figure_params(figdict)
            # set trace column as only index
            figdf = figdf.reset_index().set_index('trace')
            # get default parameters
            figdf_default = pd.concat([default.corr_df]*len(figdf))
            # set index of defaultdf to match figdf
            figdf_default.index=figdf.index
            # add default df to figdf
            figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

            # apply to all traces
            #---------------------
            # figure level parameters
            figdf['fig_topercent']=False
            figdf['fig_ylim_all']=False
            figdf['fig_xlim_all']=False
            figdf['trace_markersize']=10

            # apply subgroup parameters
            #-------------------------------
            # # reset to hierachichal
            # figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            # # set subgroup locations
            # figdf.loc[('weak_associative', 'control'), 'sub_location']=1
            # figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
            # figdf.loc[('strong_associative', 'control'), 'sub_location']=1
            # figdf.loc[('strong_associative', 'anodal'), 'sub_location']=4
            # figdf.loc[('specificity', 'control'), 'sub_location']=1
            # figdf.loc[('specificity', 'anodal'), 'sub_location']=4
            # # reset index to trace 
            # figdf = figdf.reset_index().set_index('trace')

            # individual trace parameters
            #----------------------------
            # get list of all trace names 
            trace_values = figdf.index.values
            figdf['trace_color']='temp'
            figdf['error_color']='temp'

            figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
            idx_keys = figdf.index.unique().values
            for key in idx_keys:
                if 'control' in key[2]:
                    figdf.at[key, 'trace_color']=black
                elif 'anodal' in key[2]:
                    figdf.at[key, 'trace_color']=red
                elif 'cathodal' in key[2]:
                    figdf.at[key, 'trace_color']=blue

        return figdf

    def _ltp_bar_2path(self,):
        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            'weak_associative':{
                # subgroup
                'Unpaired':[
                    # trace
                    ('control', 'weak5Hz', 'nostim'),
                    ('anodal', 'weak5Hz', 'nostim'),
                    
                ],
                'Paired':[
                    # trace
                    ('control', 'weak5Hz', 'TBS'),
                    ('anodal', 'weak5Hz', 'TBS')
                ]
            },
            'specificity':{
                'Inactive':[
                    
                    ('control', 'nostim', 'TBS'),
                    ('anodal', 'nostim', 'TBS'),
                ],
                'Strong':[
                    ('control', 'TBS', 'nostim'),
                    ('anodal', 'TBS', 'nostim'),
                ]
            },
            # figure
            'strong_associative':{
                # subgroup
                'Unpaired':[
                    # trace
                    
                    ('control', 'TBS', 'nostim'),
                    ('anodal', 'TBS', 'nostim')
                ],
                'Paired':[
                    # trace
                    ('control', 'TBS', 'weak5Hz'),
                    ('anodal', 'TBS', 'weak5Hz'),
                ]
            },
        }

        # create df for figure parameters
        #---------------------------------
        figdf = functions._build_figure_params(figdict)
        # set trace column as only index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # apply to all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=True
        figdf['fig_ymax']=1.51
        figdf['fig_ymin']=1
        # figdf['fig_xmin']=0.
        # figdf['fig_ymax']=1.5
        figdf['fig_ylabel']='Norm. fEPSP slope'
        figdf['fig_xlabel']=''
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        figdf['fig_dyticks']=.1
        # figdf['fig_dxticks']=20
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_style']='bar'
        figdf['trace_linewidth']=4
        figdf['fig_xtick_rotate']=0
        figdf['fig_barwidth']=1
        figdf['fig_barspacing']=1
        figdf['fig_groupspacing']=1
        figdf['fig_ytick_decimals']=1

        # apply subgroup parameters
        #-------------------------------
        # reset to hierachichal
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        # set subgroup locations
        figdf.loc[('weak_associative', 'Unpaired'), 'sub_location']=1
        figdf.loc[('weak_associative', 'Paired'), 'sub_location']=4
        figdf.loc[('specificity', 'Inactive'), 'sub_location']=1
        figdf.loc[('specificity', 'Strong'), 'sub_location']=4
        figdf.loc[('strong_associative', 'Unpaired'), 'sub_location']=1
        figdf.loc[('strong_associative', 'Paired'), 'sub_location']=4

        figdf.loc[('weak_associative', 'Unpaired'), 'xticks_minor_loc']=1.5
        figdf.loc[('weak_associative', 'Paired'), 'xticks_minor_loc']=4.5
        figdf.loc[('specificity', 'Inactive'), 'xticks_minor_loc']=1.5
        figdf.loc[('specificity', 'Strong'), 'xticks_minor_loc']=4.5
        figdf.loc[('strong_associative', 'Unpaired'), 'xticks_minor_loc']=1.5
        figdf.loc[('strong_associative', 'Paired'), 'xticks_minor_loc']=4.5
        # reset index to trace 
        figdf = figdf.reset_index().set_index('trace')

        # individual trace parameters
        #----------------------------
        # get list of all trace names 
        trace_values = figdf.index.values
        figdf['trace_color']='temp'
        figdf['trace_ecolor']='temp'

        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        idx_keys = figdf.index.unique().values
        for key in idx_keys:
            if key[0]=='weak_associative':
                if key[2] == ('control','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'

            elif key[0]=='strong_associative':
                if key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'

            elif key[0]=='specificity':
                if key[2] == ('control','nostim','TBS'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','nostim','TBS'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
    
        return figdf

    def _ltp_bar_2path_2(self,):
        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            'weak_associative':{
                # subgroup
                'Weak only':[
                    # trace
                    ('control', 'weak5Hz', 'nostim'),
                    ('anodal', 'weak5Hz', 'nostim'),
                    
                ],
                'Weak+strong':[
                    # trace
                    ('control', 'weak5Hz', 'TBS'),
                    ('anodal', 'weak5Hz', 'TBS')
                ]
            },
            'specificity':{
                'Inactive':[
                    
                    ('control', 'nostim', 'TBS'),
                    ('anodal', 'nostim', 'TBS'),
                ],
                'Strong':[
                    ('control', 'TBS', 'nostim'),
                    ('anodal', 'TBS', 'nostim'),
                ]
            },
            # figure
            'strong_associative':{
                # subgroup
                'Unpaired':[
                    # trace
                    
                    ('control', 'TBS', 'nostim'),
                    ('anodal', 'TBS', 'nostim')
                ],
                'Paired':[
                    # trace
                    ('control', 'TBS', 'weak5Hz'),
                    ('anodal', 'TBS', 'weak5Hz'),
                ]
            },
        }

        # create df for figure parameters
        #---------------------------------
        figdf = functions._build_figure_params(figdict)
        # set trace column as only index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # apply to all traces
        #---------------------
        # figure level parameters
        figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=True
        figdf['fig_ymax']=1.51
        figdf['fig_ymin']=1
        # figdf['fig_xmin']=0.
        # figdf['fig_ymax']=1.5
        figdf['fig_ylabel']='Norm. fEPSP slope'
        figdf['fig_xlabel']=''
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        figdf['fig_dyticks']=.1
        # figdf['fig_dxticks']=20
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_style']='bar'
        figdf['trace_linewidth']=4
        figdf['fig_xtick_rotate']=0
        figdf['fig_barwidth']=1
        figdf['fig_barspacing']=1
        figdf['fig_groupspacing']=1
        figdf['fig_ytick_decimals']=1

        # apply subgroup parameters
        #-------------------------------
        # reset to hierachichal
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        # set subgroup locations
        figdf.loc[('weak_associative', 'Weak only'), 'sub_location']=1
        figdf.loc[('weak_associative', 'Weak+strong'), 'sub_location']=4
        figdf.loc[('specificity', 'Inactive'), 'sub_location']=1
        figdf.loc[('specificity', 'Strong'), 'sub_location']=4
        figdf.loc[('strong_associative', 'Unpaired'), 'sub_location']=1
        figdf.loc[('strong_associative', 'Paired'), 'sub_location']=4

        figdf.loc[('weak_associative', 'Weak only'), 'xticks_minor_loc']=1.5
        figdf.loc[('weak_associative', 'Weak+strong'), 'xticks_minor_loc']=4.5
        figdf.loc[('specificity', 'Inactive'), 'xticks_minor_loc']=1.5
        figdf.loc[('specificity', 'Strong'), 'xticks_minor_loc']=4.5
        figdf.loc[('strong_associative', 'Unpaired'), 'xticks_minor_loc']=1.5
        figdf.loc[('strong_associative', 'Paired'), 'xticks_minor_loc']=4.5
        # reset index to trace 
        figdf = figdf.reset_index().set_index('trace')

        # individual trace parameters
        #----------------------------
        # get list of all trace names 
        trace_values = figdf.index.values
        figdf['trace_color']='temp'
        figdf['trace_ecolor']='temp'

        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        idx_keys = figdf.index.unique().values
        for key in idx_keys:
            if key[0]=='weak_associative':
                if key[2] == ('control','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','weak5Hz','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','weak5Hz','TBS'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'

            elif key[0]=='strong_associative':
                if key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','TBS','weak5Hz'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'

            elif key[0]=='specificity':
                if key[2] == ('control','nostim','TBS'):
                    figdf.at[key, 'trace_color']=gray
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('anodal','nostim','TBS'):
                    figdf.at[key, 'trace_color']=red_light
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#'5Hz'
                elif key[2] == ('control','TBS','nostim'):
                    figdf.at[key, 'trace_color']=black
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=0
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
                elif key[2] == ('anodal','TBS','nostim'):
                    figdf.at[key, 'trace_color']=red
                    figdf.at[key, 'trace_ecolor']=gray
                    figdf.at[key, 'trace_location']=1
                    figdf.at[key, 'trace_label']=''#5Hz\n+TBS'
    
        return figdf

    def _vtrace_1path_mean(self, ):
        '''
        '''
        # load default figure parameters and colors
        #------------------------------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # default = Default()
        # black = default.black
        # gray = default.gray
        # red=default.red
        # red_light=default.red_light
        # blue=default.blue
        # blue_light=default.blue_light
        # conditions for each figure
        #----------------------------
        figdict = {
            # figure
            'apical 20 Vm':{
                # subgroup
                'apical 20 Vm':[
                    # trace
                    ('TBS','None', 'apical', 'control''0'),
                    ('TBS','None','apical', 'anodal','20'),
                    ('TBS','None','apical','cathodal', '20'),
                ]
            },
            'basal 20 Vm':{
                # subgroup
                'basal 20 Vm':[
                    # trace
                    ('TBS','None', 'basal','control', '0'),
                    ('TBS','None','basal', 'anodal', '20'),
                    ('TBS','None','basal', 'cathodal', '20'),
                ]
            },
            'basal control only':{
                # subgroup
                'basal control only':[
                    # trace
                    ('TBS','None','basal','control',  '0',),
                ]
            },
            'apical control only':{
                # subgroup
                'apical control only':[
                    # trace
                    ('TBS','None','apical', 'control', '0',),
                ]
            },
        }

        # create df for figure parameters
        #---------------------------------
        figdf = functions._build_figure_params(figdict)
        # set trace column as only index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # apply to all traces
        #---------------------
        # figure level parameters
        figdf['fig_ylim_all']=True
        figdf['fig_xlim_all']=True
        figdf['fig_ymin']=-4
        # figdf['fig_xmin']=0.
        # figdf['fig_ylabel']='Normalized fEPSP slope'
        # figdf['fig_xlabel']='Time (min)'
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=20
        figdf['fig_average_bursts']=True
        # trace level parameters
        figdf['error_alpha']=1
        figdf['error_shade']=True
        figdf['error_style']='shade'
        figdf['trace_linewidth']=4

        # individual trace parameters
        #----------------------------
        # get list of all trace names 
        trace_values = figdf.index.values

        # preallocate columns as 'object' dtype
        figdf['trace_color']='temp'
        figdf['error_color']='temp'
        figdf['trace_label']='temp'

        # set trace column as only index
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all trace names 
        trace_values = figdf.index.values
        # iterate over individual traces
        for trace in trace_values:
            # print figdf.head
            # print trace
            # print figdf.index
            # create label for current trace
            figdf.at[(trace), 'trace_label']=trace[2][0]

            # set plot colors
            #----------------------------
            if 'control' in trace[2]:
                if trace[1]=='weak5Hz':
                    figdf.at[trace, 'trace_color']=gray
                    figdf.at[trace, 'error_color']=gray
                else:
                    # print figdf.at[trace, 'trace_color']
                    figdf.at[trace, 'trace_color']=black
                    figdf.at[trace, 'error_color']=black

            if 'anodal' in trace[2]:
                if trace[1]=='weak5Hz':
                    figdf.at[trace, 'trace_color']=red_light
                    figdf.at[trace, 'error_color']=red_light
                else:
                    figdf.at[trace, 'trace_color']=red
                    figdf.at[trace, 'error_color']=red

            if 'cathodal' in trace[2]:
                if trace[1]=='weak5Hz':
                    figdf.at[trace, 'trace_color']=blue_light
                    figdf.at[trace, 'error_color']=blue_light
                else:
                    figdf.at[trace, 'trace_color']=blue
                    figdf.at[trace, 'error_color']=blue

        return figdf

    def _dose_response_individual_points_mahima(self, ):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # conditions for each figure
        #----------------------------
        figdict = {
            'dose response':{
                # subgroup
                'dose response':[
                    # trace
                    ('cathodal',),
                    ('anodal', ),
                    ('control',),

                ]
            },
        }

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        # figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        # figdf['trace_markersize']=10
        # # print figdf.fig_nyticks
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=np.exp(10)
        # figdf['fig_dxticks']=5
        # figdf['fig_ylim_all']=True
        # figdf['fig_xlim_all']=True
        # figdf['fig_ymin']=1.2
        # figdf['fig_xmin']=-25.
        # figdf['fig_xmax']=26.
        figdf['fig_ylabel']='LTP'
        figdf['fig_xlabel']='Electric field (V/m)'
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=20
        # # trace level parameters
        # figdf['error_alpha']=1
        figdf['error_style']='bar'
        figdf['trace_marker']='o'
        figdf['trace_markersize']=10
        figdf['trace_linewidth']=0
        figdf['error_linewidth']=2

        # figdf.at[slice(None), 'trace_ecolor'] = gray
        figdf['fig_xscale_log']=False
        figdf['fig_barwidth']=0.8
        figdf['fig_data_style']='point'
        figdf['fig_xtick_decimals']=0
        figdf['fig_ytick_decimals']=2
        figdf['fig_set_xscale']='linear'


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']=None
        figdf['trace_ecolor']=None
        # figdf['fig_xticks']=None
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])

        # locations = [-20, -5, -1, 0, 1, 5, 20]
        # locations_log = []
        # for location in locations:
        #     if location<0:
        #         new_loc = -np.log(np.abs(location)+1)
        #     else:
        #         new_loc = np.log(np.abs(location)+1)
        #     locations_log.append(new_loc)



        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:

            # set trace location to field magnitude
            #------------------------------------
            # figdf.at[key, 'trace_location'] = locations.index(key[2][0])
            # figdf.at[key, 'trace_location'] = key[2][0]
            # figdf.at[key, 'trace_location'] = locations_log[locations.index(key[2][0])]
            # figdf.at[key, 'trace_location'] = np.log(key[2][0]+1)
            # figdf.at[key, 'trace_label'] = key[2][0]
            # figdf.at[key, 'fig_xticks'] = locations

            # set colors
            #------------------------------------
            print key[2][0]
            # cathodal
            if key[2][0]=='cathodal':
                figdf.at[key, 'trace_color']=blue
            # control
            if key[2][0]=='control':
                figdf.at[key, 'trace_color']=black
            # anodal
            if key[2][0]=='anodal':
                figdf.at[key, 'trace_color']=red

            figdf.at[key, 'trace_ecolor']=gray

        return figdf

    def _dose_response_individual_points_mahima_connect(self, ):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # conditions for each figure
        #----------------------------
        figdict = {
            'dose response':{
                # subgroup
                'dose response':[
                    # trace
                    ('cathodal',),
                    ('anodal', ),
                    ('control',),

                ]
            },
        }

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        # figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        # figdf['trace_markersize']=10
        # # print figdf.fig_nyticks
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=np.exp(10)
        # figdf['fig_dxticks']=5
        # figdf['fig_ylim_all']=True
        # figdf['fig_xlim_all']=True
        # figdf['fig_ymin']=1.2
        # figdf['fig_xmin']=-25.
        # figdf['fig_xmax']=26.
        figdf['fig_ylabel']='LTP'
        figdf['fig_xlabel']='Electric field (V/m)'
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=20
        # # trace level parameters
        # figdf['error_alpha']=1
        figdf['error_style']='bar'
        figdf['trace_marker']='o'
        figdf['trace_markersize']=10
        figdf['trace_linewidth']=0
        figdf['error_linewidth']=2

        # figdf.at[slice(None), 'trace_ecolor'] = gray
        figdf['fig_xscale_log']=False
        figdf['fig_barwidth']=0.8
        figdf['fig_data_style']='point'
        figdf['fig_xtick_decimals']=0
        figdf['fig_ytick_decimals']=2
        figdf['fig_set_xscale']='linear'


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']=None
        figdf['trace_ecolor']=None
        # figdf['fig_xticks']=None
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])

        # locations = [-20, -5, -1, 0, 1, 5, 20]
        # locations_log = []
        # for location in locations:
        #     if location<0:
        #         new_loc = -np.log(np.abs(location)+1)
        #     else:
        #         new_loc = np.log(np.abs(location)+1)
        #     locations_log.append(new_loc)



        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:

            # set trace location to field magnitude
            #------------------------------------
            # figdf.at[key, 'trace_location'] = locations.index(key[2][0])
            # figdf.at[key, 'trace_location'] = key[2][0]
            # figdf.at[key, 'trace_location'] = locations_log[locations.index(key[2][0])]
            # figdf.at[key, 'trace_location'] = np.log(key[2][0]+1)
            # figdf.at[key, 'trace_label'] = key[2][0]
            # figdf.at[key, 'fig_xticks'] = locations

            # set colors
            #------------------------------------
            print key[2][0]
            # cathodal
            if key[2][0]=='cathodal':
                figdf.at[key, 'trace_color']=blue
            # control
            if key[2][0]=='control':
                figdf.at[key, 'trace_color']=black
            # anodal
            if key[2][0]=='anodal':
                figdf.at[key, 'trace_color']=red

            figdf.at[key, 'trace_ecolor']=gray

        return figdf
    
    def _dose_response_ltp_final_mahima(self, ):
        '''
        '''
        # print progress to terminal
        #-----------------------------
        print 'building figdf:', inspect.stack()[0][3]

        # colors for plots
        #-------------------
        default = _default_figdf()
        black = self.black
        gray = self.gray
        red=self.red
        red_light=self.red_light
        blue=self.blue
        blue_light=self.blue_light

        # conditions for each figure
        #----------------------------
        figdict = {
            'dose response':{
                # subgroup
                'dose response':[
                    # trace
                    ('cathodal', ('-20', '-5')),
                    ('anodal', ('2.5', '5', '20')),
                    ('control', ('0')),

                ]
            },
        }

        # create figdf
        #---------------------------------
        figdf = self._build_figdf_from_dict(figdict)
        # set trace level as index
        figdf = figdf.reset_index().set_index('trace')
        # get default parameters
        figdf_default = pd.concat([default]*len(figdf))
        # set index of defaultdf to match figdf
        figdf_default.index=figdf.index
        # add default df to figdf
        figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

        # fig parameters for all traces
        #---------------------
        # figure level parameters
        # figdf['fig_topercent']=False
        figdf['fig_ylim_all']=False
        figdf['fig_xlim_all']=False
        # figdf['trace_markersize']=10
        # # print figdf.fig_nyticks
        # figdf['fig_nyticks']=5
        # figdf['fig_nxticks']=10
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=np.exp(10)
        # figdf['fig_dxticks']=5
        # figdf['fig_ylim_all']=True
        # figdf['fig_xlim_all']=True
        # figdf['fig_ymin']=1.2
        # figdf['fig_xmin']=-25.
        # figdf['fig_xmax']=26.
        figdf['fig_ylabel']='LTP'
        figdf['fig_xlabel']='Electric field (V/m)'
        # figdf['fig_dyticks']=.2
        # figdf['fig_dxticks']=20
        # # trace level parameters
        # figdf['error_alpha']=1
        figdf['error_style']='bar'
        figdf['trace_marker']='o'
        figdf['trace_markersize']=10
        figdf['trace_linewidth']=0
        figdf['error_linewidth']=2

        # figdf.at[slice(None), 'trace_ecolor'] = gray
        figdf['fig_xscale_log']=False
        figdf['fig_barwidth']=0.8
        figdf['fig_data_style']='point'
        figdf['fig_xtick_decimals']=0
        figdf['fig_ytick_decimals']=2
        figdf['fig_set_xscale']='linear'


        # individual trace parameters
        #----------------------------
        # preallocate columns as object type
        figdf['trace_color']=None
        figdf['trace_ecolor']=None
        # figdf['fig_xticks']=None
        # reset index
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])

        # locations = [-20, -5, -1, 0, 1, 5, 20]
        # locations_log = []
        # for location in locations:
        #     if location<0:
        #         new_loc = -np.log(np.abs(location)+1)
        #     else:
        #         new_loc = np.log(np.abs(location)+1)
        #     locations_log.append(new_loc)



        # get all figure, subgroup, trace combinations
        idx_keys = figdf.index.unique().values
        # iterate over combinations
        for key in idx_keys:

            # set trace location to field magnitude
            #------------------------------------
            # figdf.at[key, 'trace_location'] = locations.index(key[2][0])
            # figdf.at[key, 'trace_location'] = key[2][0]
            # figdf.at[key, 'trace_location'] = locations_log[locations.index(key[2][0])]
            # figdf.at[key, 'trace_location'] = np.log(key[2][0]+1)
            # figdf.at[key, 'trace_label'] = key[2][0]
            # figdf.at[key, 'fig_xticks'] = locations

            # set colors
            #------------------------------------
            print key[2][0]
            # cathodal
            if key[2][0]=='cathodal':
                figdf.at[key, 'trace_color']=blue
            # control
            if key[2][0]=='control':
                figdf.at[key, 'trace_color']=black
            # anodal
            if key[2][0]=='anodal':
                figdf.at[key, 'trace_color']=red

            figdf.at[key, 'trace_ecolor']=gray

        return figdf

class LoadNSortDF:
    '''
    '''
    def __init__(self):
        '''
        '''
        pass
    #########################################################################
    #########################################################################
    def _slopes_spikes_all(self, 
        paths=['1path', '2path'], 
        conditions=['induction_pattern_0_slopes',
        'induction_pattern_other_0_slopes', 
        'induction_location_0_slopes', 
        'field_polarity_0_slopes',
        'field_mag_0_slopes']):
        '''
        '''
        print 'loading and sorting group datafames:', inspect.stack()[0][3]

        # constraints to be applied to group data (only rows that meet the criteria are kept)
        #--------------------------------------------------------------
        constraints_spec = OrderedDict(
            [('remove', {
                ('TBS','weak5Hz'):['==',False],
                ('TBS','nostim'): ['==',False],
                ('weak5Hz', 'nostim'):['==',False],
                ('apical', 'None'):['==',False],#20181113
                ('basal', 'None'):['==', False],#20170405
                ('perforant', 'None'):['>=',False],
                }),
            ('baseline_percent_slopes', {
                ('TBS','weak5Hz'):['==',30], #30
                ('TBS','nostim'): ['==',30],#30
                ('weak5Hz', 'nostim'):['==',30]#30
                }),
            ('date_slopes', {
                ('TBS','weak5Hz'):['>=',20181113],#20181113
                ('TBS','nostim'): ['>=',20181210],#20181210
                ('weak5Hz', 'nostim'):['>',20180920],#20180920
                ('apical', 'None'):['>=',0],#20181113
                ('basal', 'None'):['>=', 20170405],#20170405
                ('perforant', 'None'):['>=',20170426],#20170426
                })]
            ) 
        # constraint applied to all conditions. this gets overwritten by specific constraints
        #-------------------------------
        constraints_all = OrderedDict([
            ('remove', ['==',False])
            ])

    
        group_directory = 'Variables/'
        df_sorted={}
        figdf={}
        df_all_temp=pd.DataFrame()
        # iterate over 1path and 2 path experiments
        #--------------------------------------------
        for path in paths:
            df_sorted[path]={}
            figdf[path]={}
            # 1path experiments
            #------------------------
            if path=='1path':
                # filenames
                filename_spikes = 'spikes_df_1path.pkl'
                filename_slopes = 'slopes_df_1path.pkl'
                filename_slopes_asif = 'slopes_df_asif.pkl'
                # load slopes and spikes data
                df_slopes = pd.read_pickle(group_directory+filename_slopes)
                df_slopes_asif = pd.read_pickle(group_directory+filename_slopes_asif)
                df_slopes = df_slopes.append(df_slopes_asif, ignore_index=True, )
                df_spikes = pd.read_pickle(group_directory+filename_spikes)
                # df_spikes = df_spikes.append(df_slopes_asif[['name','path']], ignore_index=True)
            # 2path
            #--------------------------
            elif path=='2path':
                # filenames
                filename_spikes = 'spikes_df.pkl'
                filename_slopes = 'slopes_df.pkl'
                # load slopes and spikes
                df_slopes = pd.read_pickle(group_directory+filename_slopes)
                df_spikes = pd.read_pickle(group_directory+filename_spikes)

            # merge slopes and spikes
            #---------------------------
            df_merged = pd.merge(df_slopes, df_spikes, on=['name','path'], how='left', suffixes=['_slopes','_spikes'])

            # append 1 path and 2path df's
            #-----------------------------
            df_all_temp = df_all_temp.append(copy.deepcopy(df_merged), ignore_index=True)

        # sort df (remove row based on contraints specified above)
        #----------------------------
        df_sorted = functions._sortdf(df=df_all_temp, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

        # recombine df_sorted into a single dataframe
        #------------------------------------------
        df_all=pd.DataFrame()
        for key, df in df_sorted.iteritems():
            df_all = df_all.append(df, ignore_index=True)

        # add mahima's data
        #------------------------------------------------------
        df_all_mahima = self._dose_response_mahima()
        df_all = df_all.append(df_all_mahima.reset_index(), ignore_index=True)

        # add greg as experimenter 
        #------------------------------------------------------------
        df_all.loc[df_all.experimenter.isna(), 'experimenter']='greg'

        # set multiindex levels to match specified conditions (keys for df_sorted and indices for df_all should match)
        #----------------------------------------------------
        df_all = df_all.reset_index().set_index(conditions)

        return df_sorted, df_all

    def _slopes_vtrace_all(self, 
        paths=['1path', '2path'], 
        conditions=['induction_pattern_0_slopes',
        'induction_pattern_other_0_slopes', 
        'induction_location_0_slopes', 
        'field_polarity_0_slopes',
        'field_mag_0_slopes'],
        filt=''):
        '''
        '''
        print 'loading and sorting group datafames:', inspect.stack()[0][3]

        # constraints to be applied to group data (only row that meet the criteria are kept)
        #--------------------------------------------------------------
        constraints_spec = OrderedDict(
            [('remove', {
                ('TBS','weak5Hz'):['==',False],
                ('TBS','nostim'): ['==',False],
                ('weak5Hz', 'nostim'):['==',False],
                ('apical', 'None'):['==',False],#20181113
                ('basal', 'None'):['==', False],#20170405
                ('perforant', 'None'):['>=',False],
                }),
            ('baseline_percent_slopes', {
                ('TBS','weak5Hz'):['==',30], #30
                ('TBS','nostim'): ['==',30],#30
                ('weak5Hz', 'nostim'):['==',30]#30
                }),
            ('date_slopes', {
                ('TBS','weak5Hz'):['>=',20181113],#20181113
                ('TBS','nostim'): ['>=',20181210],#20181210
                ('weak5Hz', 'nostim'):['>',20180920],#20180920
                ('apical', 'None'):['>=',0],#20181113
                ('basal', 'None'):['>=', 20170405],#20170405
                ('perforant', 'None'):['>=',20170426],#20170426
                })]
            ) 
        # constraint applied to all conditions. this gets overwritten by specific constraints
        #-------------------------------
        constraints_all = OrderedDict([
            ('remove', ['==',False])
            ])

    
        group_directory = 'Variables/'
        df_sorted={}
        figdf={}
        df_all_temp=pd.DataFrame()
        # iterate over 1path and 2 path experiments
        #--------------------------------------------
        for path in paths:
            df_sorted[path]={}
            figdf[path]={}
            # 1path experiments
            #------------------------
            if path=='1path':
                # filenames
                filename_vtrace = 'vtrace_df_1path_'+filt+'.pkl'
                filename_slopes = 'slopes_df_1path.pkl'
                filename_slopes_asif = 'slopes_df_asif.pkl'
                # load slopes and spikes data
                df_slopes = pd.read_pickle(group_directory+filename_slopes)
                df_slopes_asif = pd.read_pickle(group_directory+filename_slopes_asif)
                df_slopes = df_slopes.append(df_slopes_asif, ignore_index=True, )
                df_vtrace = pd.read_pickle(group_directory+filename_vtrace)
                # df_spikes = df_spikes.append(df_slopes_asif[['name','path']], ignore_index=True)
            # 2path
            #--------------------------
            elif path=='2path':
                # filenames
                filename_vtrace = 'vtrace_df_'+filt+'.pkl'
                filename_slopes = 'slopes_df.pkl'
                # load slopes and spikes
                df_slopes = pd.read_pickle(group_directory+filename_slopes)
                df_vtrace = pd.read_pickle(group_directory+filename_vtrace)

            # merge slopes and spikes
            #---------------------------
            df_merged = pd.merge(df_slopes, df_vtrace, on=['name','path'], how='left', suffixes=['_slopes','_vtrace'])

            # append 1 path and 2path df's
            #-----------------------------
            df_all_temp = df_all_temp.append(copy.deepcopy(df_merged), ignore_index=True)

        # sort df (remove row based on contraints specified above)
        #----------------------------
        df_sorted = functions._sortdf(df=df_all_temp, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

        # recombine df_sorted into a single dataframe
        #------------------------------------------
        df_all=pd.DataFrame()
        for key, df in df_sorted.iteritems():
            df_all = df_all.append(df, ignore_index=True)

        # set multiindex levels to match specified conditions (keys for df_sorted and indices for df_all should match)
        #----------------------------------------------------
        df_all = df_all.reset_index().set_index(conditions)

        return df_sorted, df_all

    def _dose_response_mahima(self, 
        paths=['1path'], 
        conditions=['induction_pattern_0_slopes',
        'induction_pattern_other_0_slopes', 
        'induction_location_0_slopes', 
        'field_polarity_0_slopes',
        'field_mag_0_slopes']):
        '''
        '''
        print 'loading and sorting group datafames:', inspect.stack()[0][3]

        # constraints to be applied to group data (only row that meet the criteria are kept)
        #--------------------------------------------------------------
        constraints_spec = OrderedDict(
            [('exp_fit_remove', {
                ('TBS','None'):['==',False],
                }),
            ('date_slopes', {
                ('TBS','weak5Hz'):['>=',0],#20181113
                })]
            ) 
        # constraint applied to all conditions. this gets overwritten by specific constraints
        #-------------------------------
        constraints_all = OrderedDict([
            ('exp_fit_remove', ['==',False])
            ])

        group_directory = 'Variables/'

        # filenames
        #------------------------------------------------
        filename_slopes_mahima = 'slopes_df_mahima.pkl'
        filename_spikes_mahima = 'spikes_df_mahima.pkl'
        # load slopes and spikes data
        #-------------------------------------------------
        df_slopes_mahima = pd.read_pickle(group_directory+filename_slopes_mahima)
        df_spikes_mahima = pd.read_pickle(group_directory+filename_spikes_mahima)


        # merge slopes and spikes
        #---------------------------
        df_merged = pd.merge(df_slopes_mahima, df_spikes_mahima, on=['name','path'], how='left', suffixes=['_slopes','_spikes'])

        

        df_all = df_merged[df_merged.reset_index().exp_fit_remove==False]

        # # sort df (remove rows based on contraints specified above)
        # #----------------------------
        # df_sorted = functions._sortdf(df=df_merged, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

        # # recombine df_sorted into a single dataframe
        # #------------------------------------------
        # df_all=pd.DataFrame()
        # for key, df in df_sorted.iteritems():
        #     df_all = df_all.append(df, ignore_index=True)

        print 'HERE:', df_all.reset_index().set_index('field_polarity_0_slopes').loc['control'].exp_fit_remove



        # set multiindex levels to match specified conditions (keys for df_sorted and indices for df_all should match)
        #----------------------------------------------------
        df_all = df_all.reset_index().set_index(conditions)

        return df_all

class Default:
    '''
    '''
    def __init__(self):
        '''
        '''
        # set dpi for final png image
        #----------------------------
        self.dpi=350

        # colors for plots
        #-------------------
        self.black = (0,0,0)
        self.gray = (0.7,0.7, 0.7)
        self.red = (1,0,0)
        self.red_light = (1,0.7, 0.7)
        self.blue=(0,0,1)
        self.blue_light = (0.7, 0.7, 1)

        self.all_dict={
        # hide the top and right axes boundaries
            'fig_dpi':350,
            'fig_boxoff':True,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[25],
            'fig_ylabel_fontsize':[25],
            'fig_xlabel_fontweight':'heavy',
            'fig_ylabel_fontweight':'heavy',
            'fig_xtick_fontsize':[15],
            'fig_ytick_fontsize':[15],
            'fig_xtick_fontweight':'heavy',
            'fig_ytick_fontweight':'heavy',
            # figure tight layout
            'fig_tight_layout':True,
        }
        self.all_df = pd.DataFrame(self.all_dict, dtype='object')

        self.strace_dict = {
            # hide the top and right axes boundaries
            'fig_dpi':350,
            'fig_boxoff':True,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[15],
            'fig_ylabel_fontsize':[15],
            'fig_xlabel_fontweight':'heavy',
            'fig_ylabel_fontweight':'heavy',
            'fig_xtick_fontsize':[15],
            'fig_ytick_fontsize':[15],
            'fig_xtick_fontweight':'heavy',
            'fig_ytick_fontweight':'heavy',
            # figure tight layout
            'fig_tight_layout':True,
            'fig_nyticks':5,
            'fig_nxticks':10,
            'fig_dyticks':.2,
            'fig_dxticks':20,
            'fig_ylim_all':True,
            'fig_xlim_all':True,
            'fig_ymin':0.8,
            'fig_xmin':0.,
            'fig_ylabel':'Normalized fEPSP slope',
            'fig_xlabel':'Time (min)',
            'fig_dyticks':.2,
            'fig_dxticks':20,
            # trace level parameters
            'error_alpha':1,
            'error_style':'shade',
            'trace_linewidth':4,
        }
        self.strace_df = pd.DataFrame(self.strace_dict, dtype='object')

        self.bar_dict = {
            # hide the top and right axes boundaries
            'fig_boxoff':True,
            'fig_dpi':350,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[15],
            'fig_ylabel_fontsize':[15],
            'fig_xlabel_fontweight':'heavy',
            'fig_ylabel_fontweight':'heavy',
            'fig_xtick_fontsize':[15],
            'fig_ytick_fontsize':[15],
            'fig_xtick_fontweight':'heavy',
            'fig_ytick_fontweight':'heavy',
            # figure tight layout
            'fig_tight_layout':True,
            # figure level parameters
            'fig_topercent':False,
            'fig_ylim_all':False,
            'fig_xlim_all':True,
            # 'fig_ymin':-10,
            # 'fig_xmin':0., 
            'fig_ylabel':'% LTP',
            'fig_xlabel':'',
            # 'fig_dyticks':10,
            # figdf['fig_dxticks':20
            # trace level parameters
            'error_alpha':1,
            'error_style':'bar',
            'trace_linewidth':4,
            'fig_xtick_rotate':0,
            'fig_barwidth':1,
            'fig_barspacing':1,
            'fig_groupspacing':1,
            'fig_label_pvalues':True
        }
        self.bar_df = pd.DataFrame(self.bar_dict, dtype='object')

        self.corr_dict = {
            # hide the top and right axes boundaries
            'fig_boxoff':True,
            'fig_dpi':350,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[15],
            'fig_ylabel_fontsize':[15],
            'fig_xlabel_fontweight':'heavy',
            'fig_ylabel_fontweight':'heavy',
            'fig_xtick_fontsize':[15],
            'fig_ytick_fontsize':[15],
            'fig_xtick_fontweight':'heavy',
            'fig_ytick_fontweight':'heavy',
            # figure tight layout
            'fig_tight_layout':True,
            # figure level parameters
            'fig_topercent':False,
            'fig_ylim_all':False,
            'fig_xlim_all':False,
            # 'fig_ymin':-10,
            # 'fig_xmin':0., 
            # 'fig_ylabel':'% LTP',
            # 'fig_xlabel':'',
            # 'fig_dyticks':10,
            # figdf['fig_dxticks':20
            # trace level parameters
            # 'error_alpha':1,
            # 'error_style':'bar',
            # 'trace_linewidth':4,
            # 'fig_xtick_rotate':0,
            # 'fig_barwidth':1,
            # 'fig_barspacing':1,
            # 'fig_groupspacing':1,
            # 'fig_label_pvalues':True
        }
        self.corr_df = pd.DataFrame(self.corr_dict, dtype='object')

        self.vtrace_dict = {
            # hide the top and right axes boundaries
            'fig_dpi':350,
            'fig_boxoff':True,
            'fig_average_bursts':True, 
            'fig_yscale':1000,
            'fig_xscale':0.1,
            # axes and tick labels
            'fig_axes_linewidth':[4],
            'fig_xlabel_fontsize':[15],
            'fig_ylabel_fontsize':[15],
            'fig_xlabel_fontweight':'heavy',
            'fig_ylabel_fontweight':'heavy',
            'fig_xtick_fontsize':[15],
            'fig_ytick_fontsize':[15],
            'fig_xtick_fontweight':'heavy',
            'fig_ytick_fontweight':'heavy',
            # figure tight layout
            'fig_tight_layout':True,
            # 'fig_nyticks':5,
            # 'fig_nxticks':10,
            # 'fig_dyticks':.2,
            # 'fig_dxticks':20,
            'fig_ylim_all':True,
            'fig_xlim_all':True,
            # 'fig_ymin':0.8,
            'fig_xmin':0.,
            'fig_ylabel':'Field potential (mV)',
            'fig_xlabel':'Time (ms)',
            # trace level parameters
            'error_alpha':1,
            'error_style':'shade',
            'trace_linewidth':4,

        }
        self.vtrace_df = pd.DataFrame(self.vtrace_dict, dtype='object')

#############################################################################
# sort group df's for plotting
#############################################################################
def _sortdf_allpaths_merged(df):
    '''
    '''
    ['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes']

    constraints_spec = OrderedDict(
        [
        ('baseline_percent_slopes', {
            ('TBS','weak5Hz'):['==',30], #30
            ('TBS','nostim'): ['==',30],#30
            ('weak5Hz', 'nostim'):['==',30]#30
            }),
        ('date_slopes', {
            ('TBS','weak5Hz'):['>=',0],#20181113
            ('TBS','nostim'): ['>=',0],#20181210
            ('weak5Hz', 'nostim'):['>',0],#20180920
            ('apical', 'None'):['>=',0],#20181113
            ('basal', 'None'):['>=', 20170405],#20170405
            ('perforant', 'None'):['>=',20170426],#20170426
            })]
        ) 
    # constraint applied to all conditions. this gets overwritten by specific constraints
    #-------------------------------
    constraints_all = OrderedDict([
        ('remove', ['==',False])
        ])

    # sort df based on conditions
    #----------------------------
    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_2path(df):
    '''
    '''
    # list conditions to sort data by
    #-------------------------------
    conditions = ['field_polarity_0','induction_pattern_0','induction_pattern_other_0']
    # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
    #------------------------------
    constraints_spec = OrderedDict(
        [('remove', {
            ('TBS','weak5Hz'):['==',False],
            ('TBS','nostim'): ['==',False],
            ('weak5Hz', 'nostim'):['==',False]
            }),
        ('baseline_percent', {
            ('TBS','weak5Hz'):['==',30], 
            ('TBS','nostim'): ['==',30],
            ('weak5Hz', 'nostim'):['==',30]
            }),
        ('date', {
            ('TBS','weak5Hz'):['>=',20181113],#20181113
            ('TBS','nostim'): ['>=',20181210],#20181210
            ('weak5Hz', 'nostim'):['>',20180920]#20180920
            })]
        ) 
    # constraint applied to all conditions. this gets overwritten by specific constraints
    #-------------------------------
    constraints_all = OrderedDict([
        ('remove', ['==',False])
        ])

    # sort df based on conditions
    #----------------------------
    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_2path_spikes(df):
    '''
    '''
    # list conditions to sort data by
    #-------------------------------
    conditions = ['field_polarity_0_slopes','induction_pattern_0_slopes','induction_pattern_other_0_slopes']
    # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
    #------------------------------
    constraints_spec = OrderedDict(
        [('remove', {
            ('TBS','weak5Hz'):['==',False],
            ('TBS','nostim'): ['==',False],
            ('weak5Hz', 'nostim'):['==',False]
            }),
        ('baseline_percent_slopes', {
            ('TBS','weak5Hz'):['!=',100], #30
            ('TBS','nostim'): ['!=',100],#30
            ('weak5Hz', 'nostim'):['!=',100]#30
            }),
        ('date_slopes', {
            ('TBS','weak5Hz'):['>=',0],#20181113
            ('TBS','nostim'): ['>=',0],#20181210
            ('weak5Hz', 'nostim'):['>',0]#20180920
            })]
        ) 
    # constraint applied to all conditions. this gets overwritten by specific constraints
    #-------------------------------
    constraints_all = OrderedDict([
        ('remove', ['==',False])
        ])

    # sort df based on conditions
    #----------------------------
    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_2path_vtrace(df):
    '''
    '''
    # list conditions to sort data by
    #-------------------------------
    conditions = ['field_polarity_0_slopes','induction_pattern_0_slopes','induction_pattern_other_0_slopes']
    # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
    #------------------------------
    constraints_spec = OrderedDict(
        [('remove', {
            ('TBS','weak5Hz'):['==',False],
            ('TBS','nostim'): ['==',False],
            ('weak5Hz', 'nostim'):['==',False]
            }),
        ('baseline_percent_slopes', {
            ('TBS','weak5Hz'):['==',30], 
            ('TBS','nostim'): ['==',30],
            ('weak5Hz', 'nostim'):['==',30]
            }),
        ('date_slopes', {
            ('TBS','weak5Hz'):['>=',20181113],#20181113
            ('TBS','nostim'): ['>=',20181210],#20181210
            ('weak5Hz', 'nostim'):['>',20180920]#20180920
            })]
        ) 
    # constraint applied to all conditions. this gets overwritten by specific constraints
    #-------------------------------
    constraints_all = OrderedDict([
        ('remove', ['==',False])
        ])

    # sort df based on conditions
    #----------------------------
    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_1path(df, 
    conditions=['field_polarity_0', 'induction_location_0', 'field_mag_0']):
    '''
    '''
    # list conditions to sort data by
    # conditions = ['field_polarity_0', 'induction_location_0', 'field_mag_0']
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

    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_1path_spikes(df, 
    conditions=['field_polarity_0_slopes', 'induction_location_0_slopes', 'field_mag_0_slopes']):
    '''
    '''
    # list conditions to sort data by
    # conditions = ['field_polarity_0', 'induction_location_0', 'field_mag_0']
    # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
    constraints_spec = OrderedDict(
        [
        ('date_slopes', {
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

    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

def _sortdf_1path_vtrace(df, 
    conditions=['field_polarity_0_slopes', 'induction_location_0_slopes', 'field_mag_0_slopes']):
    '''
    '''
    # list conditions to sort data by
    # conditions = ['field_polarity_0', 'induction_location_0', 'field_mag_0']
    # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
    constraints_spec = OrderedDict(
        [
        ('date_slopes', {
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

    df_sorted = functions._sortdf(df=df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

    return df_sorted

#############################################################################
# default figure parameters
#############################################################################


#############################################################################
# format figures
#############################################################################


#############################################################################
# setup figure df for specific plot types
#############################################################################
def _strace_ind_2path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_unpaired':{
            # subgroup
            'weak_unpaired':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
                ('control', 'nostim', 'weak5Hz'),
                ('anodal', 'weak5Hz', 'nostim'),
                ('anodal', 'nostim', 'weak5Hz')
            ]
        },
        'strong_unpaired':{
            'strong_unpaired':[
                ('control', 'TBS', 'nostim'),
                ('control', 'nostim', 'TBS'),
                ('anodal', 'TBS', 'nostim'),
                ('anodal', 'nostim', 'TBS')
            ]
        },
        'paired':{
            'paired':[
                # ('control', 'weak5Hz', 'TBS'),
                ('control', 'TBS', 'weak5Hz'),
                # ('anodal', 'weak5Hz', 'TBS'),
                ('anodal', 'TBS', 'weak5Hz')
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-.5
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='Normalized fEPSP slope'
    figdf['fig_xlabel']='Pulse number'
    figdf['fig_nyticks']=5
    figdf['fig_nxticks']=10
    figdf['fig_dyticks']=.2
    figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # iterate over individual traces
    for trace in trace_values:
        # create label for current trace
        figdf.at[trace, 'trace_label']=trace[1]

        # set plot colors
        #----------------------------
        if 'control' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                # print figdf.at[trace, 'trace_color']
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _strace_ind_1path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical 1 Vm dc':{
            # subgroup
            'apical 1 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '1'),
                ('cathodal', 'apical', '1'),
            ]
        },
        'apical 5 Vm dc':{
            # subgroup
            'apical 5 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '5'),
                ('cathodal', 'apical', '5'),
            ]
        },
        'apical 10 Vm dc':{
            # subgroup
            'apical 10 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '10'),
                ('cathodal', 'apical', '10'),
            ]
        },
        'apical 20 Vm dc':{
            # subgroup
            'apical 20 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '20'),
                ('cathodal', 'apical', '20'),
            ]
        },
        'apical 20 Vm ac':{
            # subgroup
            'apical 20 Vm ac':[
                # trace
                ('control', 'apical', '0'),
                ('trough', 'apical', '20'),
                ('peak', 'apical', '20'),
            ]
        },
        'basal 20 Vm dc':{
            # subgroup
            'basal 20 Vm dc':[
                # trace
                ('control', 'basal', '0'),
                ('anodal', 'basal', '20'),
                ('cathodal', 'basal', '20'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    # figdf['fig_ylim_all']=True
    # figdf['fig_xlim_all']=True
    # figdf['fig_ymin']=0.8
    # figdf['fig_xmin']=0.
    figdf['fig_ylabel']='Normalized fEPSP slope'
    figdf['fig_xlabel']='Time (min)'
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # convert to hierarchical
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    # print 'idx_keys:', idx_keys
    for key in idx_keys:
        if 'control' in key[2]:
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=black
        elif 'anodal' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=red
        elif 'cathodal' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=blue
        elif 'trough' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=red
        elif 'peak' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=blue

    return figdf

def _strace_2path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_unpaired':{
            # subgroup
            'weak_unpaired':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
                ('control', 'nostim', 'weak5Hz'),
                ('anodal', 'weak5Hz', 'nostim'),
                ('anodal', 'nostim', 'weak5Hz')
            ]
        },
        'strong_unpaired':{
            'strong_unpaired':[
                ('control', 'TBS', 'nostim'),
                ('control', 'nostim', 'TBS'),
                ('anodal', 'TBS', 'nostim'),
                ('anodal', 'nostim', 'TBS')
            ]
        },
        'paired':{
            'paired':[
                ('control', 'weak5Hz', 'TBS'),
                ('control', 'TBS', 'weak5Hz'),
                ('anodal', 'weak5Hz', 'TBS'),
                ('anodal', 'TBS', 'weak5Hz')
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=0.8
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='Normalized fEPSP slope'
    figdf['fig_xlabel']='Time (min)'
    figdf['fig_nyticks']=5
    figdf['fig_nxticks']=10
    figdf['fig_dyticks']=.2
    figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # iterate over individual traces
    for trace in trace_values:
        # create label for current trace
        figdf.at[trace, 'trace_label']=trace[1]

        # set plot colors
        #----------------------------
        if 'control' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                # print figdf.at[trace, 'trace_color']
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _strace_1path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical 1 Vm dc':{
            # subgroup
            'apical 1 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '1'),
                ('cathodal', 'apical', '1'),
            ]
        },
        'apical 5 Vm dc':{
            # subgroup
            'apical 5 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '5'),
                ('cathodal', 'apical', '5'),
            ]
        },
        'apical 10 Vm dc':{
            # subgroup
            'apical 10 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '10'),
                ('cathodal', 'apical', '10'),
            ]
        },
        'apical 20 Vm dc':{
            # subgroup
            'apical 20 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '20'),
                ('cathodal', 'apical', '20'),
            ]
        },
        'apical 20 Vm ac':{
            # subgroup
            'apical 20 Vm ac':[
                # trace
                ('control', 'apical', '0'),
                ('trough', 'apical', '20'),
                ('peak', 'apical', '20'),
            ]
        },
        'basal 20 Vm dc':{
            # subgroup
            'basal 20 Vm dc':[
                # trace
                ('control', 'basal', '0'),
                ('anodal', 'basal', '20'),
                ('cathodal', 'basal', '20'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=0.8
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='Normalized fEPSP slope'
    figdf['fig_xlabel']='Time (min)'
    figdf['fig_nyticks']=5
    figdf['fig_nxticks']=10
    figdf['fig_dyticks']=.2
    figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # convert to hierarchical
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    for key in idx_keys:
        if 'control' in key[2]:
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=black
        elif 'anodal' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=red
        elif 'cathodal' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=blue
        elif 'trough' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=red
        elif 'peak' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=blue

    return figdf

def _vtrace_2path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_unpaired':{
            # subgroup
            'weak_unpaired':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
                # ('control', 'nostim', 'weak5Hz'),
                ('anodal', 'weak5Hz', 'nostim'),
                # ('anodal', 'nostim', 'weak5Hz')
            ]
        },
        'strong_unpaired':{
            'strong_unpaired':[
                ('control', 'TBS', 'nostim'),
                # ('control', 'nostim', 'TBS'),
                ('anodal', 'TBS', 'nostim'),
                # ('anodal', 'nostim', 'TBS')
            ]
        },
        'paired':{
            'paired':[
                # ('control', 'weak5Hz', 'TBS'),
                ('control', 'TBS', 'weak5Hz'),
                # ('anodal', 'weak5Hz', 'TBS'),
                ('anodal', 'TBS', 'weak5Hz')
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.vtrace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-4
    # figdf['fig_xmin']=0.
    # figdf['fig_ylabel']='Normalized fEPSP slope'
    # figdf['fig_xlabel']='Time (min)'
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=20
    figdf['fig_average_bursts']=True
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # iterate over individual traces
    for trace in trace_values:
        # create label for current trace
        figdf.at[trace, 'trace_label']=trace[1]

        # set plot colors
        #----------------------------
        if 'control' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                # print figdf.at[trace, 'trace_color']
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _vtrace_1path_mean():
    '''
    '''
    # load default figure parameters and colors
    #------------------------------------------
    default = _default_figdf()
    black = self.black
    gray = self.gray
    red=self.red
    red_light=self.red_light
    blue=self.blue
    blue_light=self.blue_light

    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical 20 Vm':{
            # subgroup
            'apical 20 Vm':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '20'),
                ('cathodal', 'apical', '20'),
            ]
        },
        'basal 20 Vm':{
            # subgroup
            'basal 20 Vm':[
                # trace
                ('control', 'basal', '0'),
                ('anodal', 'basal', '20'),
                ('cathodal', 'basal', '20'),
            ]
        },
        'basal control only':{
            # subgroup
            'basal control only':[
                # trace
                ('control', 'basal', '0',),
            ]
        },
        'apical control only':{
            # subgroup
            'apical control only':[
                # trace
                ('control', 'apical', '0',),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.vtrace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-4
    # figdf['fig_xmin']=0.
    # figdf['fig_ylabel']='Normalized fEPSP slope'
    # figdf['fig_xlabel']='Time (min)'
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=20
    figdf['fig_average_bursts']=True
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values

    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    figdf['trace_label']='temp'

    # set trace column as only index
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all trace names 
    trace_values = figdf.index.values
    # iterate over individual traces
    for trace in trace_values:
        # print figdf.head
        # print trace
        # print figdf.index
        # create label for current trace
        figdf.at[(trace), 'trace_label']=trace[2][0]

        # set plot colors
        #----------------------------
        if 'control' in trace[2]:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                # print figdf.at[trace, 'trace_color']
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace[2]:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace[2]:
            if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _vtrace_probe_2path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_unpaired_control':{
            # subgroup
            'before':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
            ],
            'after':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
            ]
        },
        # figure
        'weak_unpaired_anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'weak5Hz', 'nostim'),
            ],
            'after':[
                # trace
                ('anodal', 'weak5Hz', 'nostim'),
            ]
        },
        'strong_unpaired_control':{
            # subgroup
            'before':[
                # trace
                ('control', 'TBS', 'nostim'),
            ],
            'after':[
                # trace
                ('control', 'TBS', 'nostim'),
            ]
        },
        # figure
        'strong_unpaired_anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'TBS', 'nostim'),
            ],
            'after':[
                # trace
                ('anodal', 'TBS', 'nostim'),
            ]
        },
        # figure
        'weak_paired_control':{
            # subgroup
            'before':[
                # trace
                ('control', 'weak5Hz', 'TBS'),
            ],
            'after':[
                # trace
                ('control', 'weak5Hz', 'TBS'),
            ]
        },
        # figure
        'weak_paired_anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'weak5Hz', 'TBS'),
            ],
            'after':[
                # trace
                ('anodal', 'weak5Hz', 'TBS'),
            ]
        },
        'strong_paired_control':{
            # subgroup
            'before':[
                # trace
                ('control', 'TBS', 'weak5Hz'),
            ],
            'after':[
                # trace
                ('control', 'TBS', 'weak5Hz'),
            ]
        },
        # figure
        'strong_unpaired_anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'TBS', 'weak5Hz'),
            ],
            'after':[
                # trace
                ('anodal', 'TBS', 'weak5Hz'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.vtrace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-4
    # figdf['fig_xmin']=0.
    # figdf['fig_ylabel']='Normalized fEPSP slope'
    # figdf['fig_xlabel']='Time (min)'
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=20
    figdf['fig_average_bursts']=True
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4

    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    figdf = figdf.reset_index().set_index(['subgroup'])
    # set subgroup locations
    figdf.loc['before', 'before_after']='before'
    figdf.loc['after', 'before_after']='after'

    # reset index to trace 
    figdf = figdf.reset_index().set_index(['trace', 'before_after'])

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    figdf['trace_label']=None
    # iterate over individual traces
    for trace in trace_values:
        # create label for current trace
        figdf.at[trace, 'trace_label']=str(trace)

        # set plot colors
        #----------------------------
        if 'control' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _vtrace_probe_1path_mean():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical control':{
            # subgroup
            'before':[
                # trace
                ('control', 'apical', '0'),
            ],
            # subgroup
            'after':[
                # trace
                ('control', 'apical', '0'),
            ]
        },
        'apical 20 Vm anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'apical', '20'),
            ],
            # subgroup
            'after':[
                # trace
                ('anodal', 'apical', '20'),
            ]
        },
        'apical 20 Vm cathodal':{
            # subgroup
            'before':[
                # trace
                ('cathodal', 'apical', '20'),
            ],
            # subgroup
            'after':[
                # trace
                ('cathodal', 'apical', '20'),
            ]
        },
        'apical 5 Vm anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'apical', '5'),
            ],
            # subgroup
            'after':[
                # trace
                ('anodal', 'apical', '5'),
            ]
        },
        'apical 5 Vm cathodal':{
            # subgroup
            'before':[
                # trace
                ('cathodal', 'apical', '5'),
            ],
            # subgroup
            'after':[
                # trace
                ('cathodal', 'apical', '5'),
            ]
        },
        'basal control':{
            # subgroup
            'before':[
                # trace
                ('control', 'basal', '0'),
            ],
            # subgroup
            'after':[
                # trace
                ('control', 'basal', '0'),
            ]
        },
        'basal 20 Vm anodal':{
            # subgroup
            'before':[
                # trace
                ('anodal', 'basal', '20'),
            ],
            # subgroup
            'after':[
                # trace
                ('anodal', 'basal', '20'),
            ]
        },
        'basal 20 Vm cathodal':{
            # subgroup
            'before':[
                # trace
                ('cathodal', 'basal', '20'),
            ],
            # subgroup
            'after':[
                # trace
                ('cathodal', 'basal', '20'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.vtrace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_ylim_all']=True
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-4
    # figdf['fig_xmin']=0.
    # figdf['fig_ylabel']='Normalized fEPSP slope'
    # figdf['fig_xlabel']='Time (min)'
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=20
    figdf['fig_average_bursts']=True
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_shade']=True
    figdf['error_style']='shade'
    figdf['trace_linewidth']=4


    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    figdf = figdf.reset_index().set_index(['subgroup'])
    # set subgroup locations
    figdf.loc['before', 'before_after']='before'
    figdf.loc['after', 'before_after']='after'

    # reset index to trace 
    figdf = figdf.reset_index().set_index(['trace', 'before_after'])

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'

    # pdb.set_trace()
    print trace_values
    figdf['trace_label']=None
    # iterate over individual traces
    for trace in trace_values:
        # print sorted(figdf.loc[[trace]].keys())
        # create label for current trace
        figdf.at[trace, 'trace_label']=str(trace)

        # set plot colors
        #----------------------------
        if 'control' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=gray
                figdf.at[trace, 'error_color']=gray
            else:
                # print figdf.at[trace, 'trace_color']
                figdf.at[trace, 'trace_color']=black
                figdf.at[trace, 'error_color']=black

        if 'anodal' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=red_light
                figdf.at[trace, 'error_color']=red_light
            else:
                figdf.at[trace, 'trace_color']=red
                figdf.at[trace, 'error_color']=red

        if 'cathodal' in trace[0]:
            if trace[1]=='before':
            # if trace[1]=='weak5Hz':
                figdf.at[trace, 'trace_color']=blue_light
                figdf.at[trace, 'error_color']=blue_light
            else:
                figdf.at[trace, 'trace_color']=blue
                figdf.at[trace, 'error_color']=blue

    return figdf

def _sbar_2path():
    '''
    '''
    default = Default()
    # colors for plots
    #-------------------
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light

    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_associative':{
            # subgroup
            'control':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
                ('control', 'weak5Hz', 'TBS'),
            ],
            'anodal':[
                # trace
                ('anodal', 'weak5Hz', 'nostim'),
                ('anodal', 'weak5Hz', 'TBS')
            ]
        },
        'specificity':{
            'control':[
                ('control', 'TBS', 'nostim'),
                ('control', 'nostim', 'TBS'),
            ],
            'anodal':[
                ('anodal', 'TBS', 'nostim'),
                ('anodal', 'nostim', 'TBS'),
            ]
        },
        # figure
        'strong_associative':{
            # subgroup
            'control':[
                # trace
                ('control', 'TBS', 'weak5Hz'),
                ('control', 'TBS', 'nostim'),
            ],
            'anodal':[
                # trace
                ('anodal', 'TBS', 'weak5Hz'),
                ('anodal', 'TBS', 'nostim')
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.bar_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_topercent']=True
    figdf['fig_ylim_all']=False
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-10
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='% LTP'
    figdf['fig_xlabel']=''
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    figdf['fig_dyticks']=10
    # figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_style']='bar'
    figdf['trace_linewidth']=4
    figdf['fig_xtick_rotate']=0
    figdf['fig_barwidth']=1
    figdf['fig_barspacing']=1
    figdf['fig_groupspacing']=1

    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    # set subgroup locations
    figdf.loc[('weak_associative', 'control'), 'sub_location']=1
    figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
    figdf.loc[('strong_associative', 'control'), 'sub_location']=1
    figdf.loc[('strong_associative', 'anodal'), 'sub_location']=4
    figdf.loc[('specificity', 'control'), 'sub_location']=1
    figdf.loc[('specificity', 'anodal'), 'sub_location']=4
    # reset index to trace 
    figdf = figdf.reset_index().set_index('trace')

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    figdf['trace_color']='temp'
    figdf['error_color']='temp'

    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    for key in idx_keys:
        #=======================================
        if key[2] == ('control','weak5Hz','nostim'):
            figdf.at[key, 'trace_color']=gray
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='5Hz'
        elif key[2] == ('control','weak5Hz','TBS'):
            figdf.at[key, 'trace_color']=gray
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='5Hz\n+TBS'
        elif key[2] == ('anodal','weak5Hz','nostim'):
            figdf.at[key, 'trace_color']=red_light
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='5Hz'
        elif key[2] == ('anodal','weak5Hz','TBS'):
            figdf.at[key, 'trace_color']=red_light
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='5Hz\n+TBS'
        #=======================================
        elif key[2] == ('control','TBS','nostim'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('control','nostim','TBS'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='Inactive'
        elif key[2] == ('anodal','TBS','nostim'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('anodal','nostim','TBS'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='Inactive'

        #=======================================
        elif key[2] == ('control','TBS','nostim'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('control','TBS','weak5Hz'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='TBS\n+5Hz'
        elif key[2] == ('anodal','TBS','nostim'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('anodal','TBS','weak5Hz'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='TBS\n+5Hz'


    return figdf

def _sbar_1path():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical 1 Vm dc':{
            # subgroup
            'apical 1 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '1'),
                ('cathodal', 'apical', '1'),
            ]
        },
        'apical 5 Vm dc':{
            # subgroup
            'apical 5 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '5'),
                ('cathodal', 'apical', '5'),
            ]
        },
        'apical 10 Vm dc':{
            # subgroup
            'apical 10 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '10'),
                ('cathodal', 'apical', '10'),
            ]
        },
        'apical 20 Vm dc':{
            # subgroup
            'apical 20 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '20'),
                ('cathodal', 'apical', '20'),
            ]
        },
        'apical 20 Vm ac':{
            # subgroup
            'apical 20 Vm ac':[
                # trace
                ('control', 'apical', '0'),
                ('trough', 'apical', '20'),
                ('peak', 'apical', '20'),
            ]
        },
        'basal 20 Vm dc':{
            # subgroup
            'basal 20 Vm dc':[
                # trace
                ('control', 'basal', '0'),
                ('anodal', 'basal', '20'),
                ('cathodal', 'basal', '20'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_topercent']=True
    figdf['fig_ylim_all']=False
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-10
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='% LTP'
    figdf['fig_xlabel']=''
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    figdf['fig_dyticks']=10
    # figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_style']='bar'
    figdf['trace_linewidth']=4
    figdf['fig_xtick_rotate']=0
    figdf['fig_barwidth']=1
    figdf['fig_barspacing']=1
    figdf['fig_groupspacing']=1
    figdf['sub_location']=1

    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    # figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    # # set subgroup locations
    # figdf.loc[('weak_associative', 'control'), 'sub_location']=1
    # figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
    # figdf.loc[('specificity', 'control'), 'sub_location']=1
    # figdf.loc[('specificity', 'anodal'), 'sub_location']=4
    # # reset index to trace 
    # figdf = figdf.reset_index().set_index('trace')

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # convert to hierarchical
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    for key in idx_keys:
        if 'control' in key[2]:
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='control'

        elif 'anodal' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='anodal'
        elif 'cathodal' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=2
            figdf.at[key, 'trace_label']='cathodal'
        elif 'trough' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='peak'
        elif 'peak' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=2
            figdf.at[key, 'trace_label']='trough'

    return figdf

def _var2var_corr_2path():
    '''
    '''
    default = Default()
    # colors for plots
    #-------------------
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light

    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'weak_associative':{
            # subgroup
            'control':[
                # trace
                ('control', 'weak5Hz', 'nostim'),
                # ('control', 'weak5Hz', 'TBS'),
            ],
            'anodal':[
                # trace
                ('anodal', 'weak5Hz', 'nostim'),
                # ('anodal', 'weak5Hz', 'TBS')
            ]
        },
        'specificity':{
            'control':[
                ('control', 'TBS', 'nostim'),
                # ('control', 'nostim', 'TBS'),
            ],
            'anodal':[
                ('anodal', 'TBS', 'nostim'),
                # ('anodal', 'nostim', 'TBS'),
            ]
        },
        # figure
        'strong_associative':{
            # subgroup
            'control':[
                # trace
                ('control', 'TBS', 'weak5Hz'),
                # ('control', 'TBS', 'nostim'),
            ],
            'anodal':[
                # trace
                ('anodal', 'TBS', 'weak5Hz'),
                # ('anodal', 'TBS', 'nostim')
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.bar_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_topercent']=True
    figdf['fig_ylim_all']=False
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-10
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='% LTP'
    figdf['fig_xlabel']=''
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    figdf['fig_dyticks']=10
    # figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_style']='bar'
    figdf['trace_linewidth']=4
    figdf['fig_xtick_rotate']=0
    figdf['fig_barwidth']=1
    figdf['fig_barspacing']=1
    figdf['fig_groupspacing']=1

    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    # set subgroup locations
    figdf.loc[('weak_associative', 'control'), 'sub_location']=1
    figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
    figdf.loc[('strong_associative', 'control'), 'sub_location']=1
    figdf.loc[('strong_associative', 'anodal'), 'sub_location']=4
    figdf.loc[('specificity', 'control'), 'sub_location']=1
    figdf.loc[('specificity', 'anodal'), 'sub_location']=4
    # reset index to trace 
    figdf = figdf.reset_index().set_index('trace')

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    figdf['trace_color']='temp'
    figdf['error_color']='temp'

    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    for key in idx_keys:
        #=======================================
        if key[2] == ('control','weak5Hz','nostim'):
            figdf.at[key, 'trace_color']=gray
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='5Hz'
        elif key[2] == ('control','weak5Hz','TBS'):
            figdf.at[key, 'trace_color']=gray
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='5Hz\n+TBS'
        elif key[2] == ('anodal','weak5Hz','nostim'):
            figdf.at[key, 'trace_color']=red_light
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='5Hz'
        elif key[2] == ('anodal','weak5Hz','TBS'):
            figdf.at[key, 'trace_color']=red_light
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='5Hz\n+TBS'
        #=======================================
        elif key[2] == ('control','TBS','nostim'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('control','nostim','TBS'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='Inactive'
        elif key[2] == ('anodal','TBS','nostim'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('anodal','nostim','TBS'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='Inactive'

        #=======================================
        elif key[2] == ('control','TBS','nostim'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('control','TBS','weak5Hz'):
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='TBS\n+5Hz'
        elif key[2] == ('anodal','TBS','nostim'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='TBS'
        elif key[2] == ('anodal','TBS','weak5Hz'):
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='TBS\n+5Hz'


    return figdf

def _var2var_corr_1path():
    '''
    '''
    default = Default()
    black = default.black
    gray = default.gray
    red=default.red
    red_light=default.red_light
    blue=default.blue
    blue_light=default.blue_light
    # conditions for each figure
    #----------------------------
    figdict = {
        # figure
        'apical 1 Vm dc':{
            # subgroup
            'apical 1 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '1'),
                ('cathodal', 'apical', '1'),
            ]
        },
        'apical 5 Vm dc':{
            # subgroup
            'apical 5 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '5'),
                ('cathodal', 'apical', '5'),
            ]
        },
        'apical 10 Vm dc':{
            # subgroup
            'apical 10 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '10'),
                ('cathodal', 'apical', '10'),
            ]
        },
        'apical 20 Vm dc':{
            # subgroup
            'apical 20 Vm dc':[
                # trace
                ('control', 'apical', '0'),
                ('anodal', 'apical', '20'),
                ('cathodal', 'apical', '20'),
            ]
        },
        'apical 20 Vm ac':{
            # subgroup
            'apical 20 Vm ac':[
                # trace
                ('control', 'apical', '0'),
                ('trough', 'apical', '20'),
                ('peak', 'apical', '20'),
            ]
        },
        'basal 20 Vm dc':{
            # subgroup
            'basal 20 Vm dc':[
                # trace
                ('control', 'basal', '0'),
                ('anodal', 'basal', '20'),
                ('cathodal', 'basal', '20'),
            ]
        },
    }

    # create df for figure parameters
    #---------------------------------
    figdf = functions._build_figure_params(figdict)
    # set trace column as only index
    figdf = figdf.reset_index().set_index('trace')
    # get default parameters
    figdf_default = pd.concat([default.strace_df]*len(figdf))
    # set index of defaultdf to match figdf
    figdf_default.index=figdf.index
    # add default df to figdf
    figdf = pd.concat([figdf, figdf_default], axis=1, ignore_index=False)

    # apply to all traces
    #---------------------
    # figure level parameters
    figdf['fig_topercent']=True
    figdf['fig_ylim_all']=False
    figdf['fig_xlim_all']=True
    figdf['fig_ymin']=-10
    figdf['fig_xmin']=0.
    figdf['fig_ylabel']='% LTP'
    figdf['fig_xlabel']=''
    # figdf['fig_nyticks']=5
    # figdf['fig_nxticks']=10
    figdf['fig_dyticks']=10
    # figdf['fig_dxticks']=20
    # trace level parameters
    figdf['error_alpha']=1
    figdf['error_style']='bar'
    figdf['trace_linewidth']=4
    figdf['fig_xtick_rotate']=0
    figdf['fig_barwidth']=1
    figdf['fig_barspacing']=1
    figdf['fig_groupspacing']=1
    figdf['sub_location']=1

    # apply subgroup parameters
    #-------------------------------
    # reset to hierachichal
    # figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    # # set subgroup locations
    # figdf.loc[('weak_associative', 'control'), 'sub_location']=1
    # figdf.loc[('weak_associative', 'anodal'), 'sub_location']=4
    # figdf.loc[('specificity', 'control'), 'sub_location']=1
    # figdf.loc[('specificity', 'anodal'), 'sub_location']=4
    # # reset index to trace 
    # figdf = figdf.reset_index().set_index('trace')

    # individual trace parameters
    #----------------------------
    # get list of all trace names 
    trace_values = figdf.index.values
    # preallocate columns as 'object' dtype
    figdf['trace_color']='temp'
    figdf['error_color']='temp'
    # convert to hierarchical
    figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
    idx_keys = figdf.index.unique().values
    for key in idx_keys:
        if 'control' in key[2]:
            figdf.at[key, 'trace_color']=black
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=0
            figdf.at[key, 'trace_label']='control'

        elif 'anodal' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='anodal'
        elif 'cathodal' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=2
            figdf.at[key, 'trace_label']='cathodal'
        elif 'trough' in key[2]:
            figdf.at[key, 'trace_color']=red
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=1
            figdf.at[key, 'trace_label']='peak'
        elif 'peak' in key[2]:
            figdf.at[key, 'trace_color']=blue
            figdf.at[key, 'error_color']=gray
            figdf.at[key, 'trace_location']=2
            figdf.at[key, 'trace_label']='trough'

    return figdf
