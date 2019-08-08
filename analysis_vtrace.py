import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
from scipy import stats
import preprocess as pre
import itertools
from collections import OrderedDict 
import functions
import figsetup
import plots
import pdb

# directory and filename
#------------------------
group_directory = 'Variables/'
figure_directory = 'Figures/'
dpi=350
lastburst_i=14

# load sorted data
#-----------------------------
loadnsortdf =  figsetup.LoadNSortDF()
buildfigdf = figsetup.BuildFigDF()
arrayfuncs = plots.ArrayFunctions()
# conditions to organize data
#------------------------------
conditions=['induction_pattern_0_slopes',
        'induction_pattern_other_0_slopes', 
        'induction_location_0_slopes', 
        'field_polarity_0_slopes',
        'field_mag_0_slopes']
# filters for voltage traces
#----------------------------
filters = [
        'data_filt_iir_high_5_sortby_burst',
        'data_filt_iir_band_5_50_sortby_burst',
        'data_filt_iir_high_300_hilbert_sortby_burst',
        ]
# load group data
#--------------------------------
def _load_variables(filters):
    for filt in filters:
        df_sorted[filt],df_all[filt] = loadnsortdf._slopes_vtrace_all(conditions=conditions, filt=filt)
        df_all[filt] = df_all[filt].reset_index()

    return df_sorted, df_all

# df_sorted, df_all = _load_variables(filters)

#############################################################################
# plot voltage traces during induction
#############################################################################
# mean with error shaded
#-----------------------
run_ind=False
if run_ind:
    paths=['1path', '2path']
    # filters applied to votage time series
    filters = [
        'data_filt_iir_high_5_sortby_burst',
        'data_filt_iir_band_5_50_sortby_burst',
        'data_filt_iir_high_300_sortby_burst',
        'data_filt_iir_high_300_hilbert_sortby_burst',
        ]
    # which burst to show inplot
    burstns = ['first', 'last', 'mean']
    # recording location
    locations = ['apical', 'basal', 'soma']
    # timing of recording, e.g. probe or induction
    timings = ['induction']

    # preallocate df's
    df_sorted={}
    figdf={}
    # iterate over conditions and plot vtrace during induction
    #----------------------------------------------------------------------------
    # 1 pathway or 2 pathway experiments
    for path in paths:
        df_sorted[path]={}
        figdf[path]={}
        # iterate over filters
        for filt in filters:
            # set filename to load data
            if path=='1path':
                filename = 'vtrace_df_1path_'+filt+'.pkl'
                filename_slopes = 'slopes_df_1path.pkl'
            elif path=='2path':
                filename = 'vtrace_df_'+filt+'.pkl'
                filename_slopes = 'slopes_df.pkl'
            # load and merge df's
            df_vtrace = pd.read_pickle(group_directory+filename)
            df_slopes = pd.read_pickle(group_directory+filename_slopes)
            df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
            
            # sort df's
            if path=='1path':
                df_sorted[path][filt] = figsetup._sortdf_1path_vtrace(df_merged) 
            elif path=='2path':
                df_sorted[path][filt] = figsetup._sortdf_2path_vtrace(df_merged) 
            
            # setup default figure parameters
            if path=='1path':
                figdf[path][filt] = figsetup._vtrace_1path_mean()
            if path=='2path':
                figdf[path][filt] = figsetup._vtrace_2path_mean()

            figdf[path][filt]['fig_xmin']=0
            figdf[path][filt]['fig_xmax']=40.
            figdf[path][filt]['fig_dxticks']=10.
            # figdf[path][filt]['fig_dyticks']=1.
            figdf[path][filt]['fig_xlim_all']=False
            figdf[path][filt]['fig_ylabel_fonstize']=25
            figdf[path][filt]['fig_xlabel_fonstize']=25


            # iterate over locations
            for location  in locations:
                # set ylimits based on location
                if location=='soma':
                    figdf[path][filt]['fig_ymin']=-1
                    figdf[path][filt]['fig_ymax']=1.5
                elif location=='apical' or location=='basal':
                    figdf[path][filt]['fig_ymin']=-3
                    figdf[path][filt]['fig_ymax']=.5
                # iterate over timings
                for timing in timings:
                    # set variable to be plotted from data df
                    variable = 'data'+'_'+timing+'_'+filt+'_'+location
                    # check that the variable exists in the current df
                    if variable in df_merged:
                        # iterate over burst number
                        for burstn in burstns:
                            figtype = 'vtrace'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
                            # update which burst to plot in figdf
                            if burstn=='first':
                                figdf[path][filt]['fig_burst_number']=0
                                figdf[path][filt]['fig_average_bursts']=False
                            elif burstn=='last':
                                figdf[path][filt]['fig_burst_number']=lastburst_i
                                figdf[path][filt]['fig_average_bursts']=False
                            elif burstn=='mean':
                                figdf[path][filt]['fig_average_bursts']=True

                            # plot
                            #-------------------------------------------------
                            print 'fontsize',figdf[path][filt]['fig_xlabel_fonstize']

                            figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted[path][filt], figdf=figdf[path][filt], variable=variable)
                            # save figures
                            #--------------------------------------------------
                            for fig_key, fig in figs_vtrace.iteritems():
                                fname = figure_directory+figtype+str(fig_key)+'.png'
                                fig.savefig(fname, format='png', dpi=dpi)

def _vtrace_apical(df_all, buildfigdf):
    '''
    '''
    # setup figdf
    #------------------------------------
    figdf = buildfigdf._vtrace_1path_mean()
    figdf['fig_ylabel']='Field potential (mV)'
    figdf['fig_xlabel']='Time (ms)'
    figdf['fig_yscale']=1000
    figdf['fig_xscale']=0.1
    figdf['fig_xmin']=0
    figdf['fig_xmax']=40.1
    figdf['fig_dxticks']=10.
    # figdf[path][filt]['fig_dyticks']=1.
    figdf['fig_xlim_all']=False
    figdf['fig_ylabel_fonstize']=40
    figdf['fig_xlabel_fonstize']=40
    figdf['trace_linewidth']=8
    figdf['error_style']='none'
    figdf['fig_ymin']=-3.5
    figdf['fig_ymax']=.5
    figdf['fig_dyticks']=1.
    figdf['fig_ytick_assert']=0
    figdf['fig_xtick_decimals']=0
    figdf['fig_ytick_decimals']=0
    # specify voltage trace to plot
    #---------------------------------
    filt = 'data_filt_iir_high_5_sortby_burst'
    location = 'apical'
    timing='induction'
    burstn='mean'
    variable = 'data'+'_'+timing+'_'+filt+'_'+location   
    figtype = 'vtrace_example'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
    # array functions
    #---------------------
    array_funcs = [
    # np.abs, 
    # arrayfuncs._slice,
    arrayfuncs._mean, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to,
    # arrayfuncs._set_to,
    ]
    # array function keyword args
    #---------------------
    array_func_kws = [
    # {},
    # {'islice':slice(-1,None),'axis':2},
    {'axis':2} 
    # {'islice':slice(20), 'axis':1}, 
    # {'islice':slice(80,120), 'axis':1}, 
    # {'islice':slice(180,220), 'axis':1}, 
    # {'islice':slice(280,320), 'axis':1},
    # {'islice':slice(380,420), 'axis':1},
    ]
    # set df indices
    #-------------------
    df_all=df_all.reset_index()
    df_all = df_all.set_index(conditions)
    # plot
    #------------------
    figs, axes = plots.PlotFuncs()._trace_mean(df=df_all, figdf=figdf, variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # reset index
    #-------------------------
    df_all=df_all.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

filt='data_filt_iir_high_5_sortby_burst'
# _vtrace_apical(df_all=df_all[filt], buildfigdf=buildfigdf)

def _dendritic_integration(df_all, buildfigdf):
    '''
    '''
    # setup figdf
    #------------------------------------
    figdf = buildfigdf._vtrace_1path_mean()
    figdf['fig_ylabel']='Field potential (mV)'
    figdf['fig_xlabel']='Time (ms)'
    figdf['fig_yscale']=1000
    figdf['fig_xscale']=0.1
    figdf['fig_xmin']=0
    figdf['fig_xmax']=40.1
    figdf['fig_dxticks']=10.
    # figdf[path][filt]['fig_dyticks']=1.
    figdf['fig_xlim_all']=False
    figdf['fig_ylabel_fonstize']=40
    figdf['fig_xlabel_fonstize']=40
    figdf['trace_linewidth']=8
    figdf['error_style']='none'
    figdf['fig_ymin']=-3.5
    figdf['fig_ymax']=.5
    figdf['fig_dyticks']=1.
    figdf['fig_ytick_assert']=0
    figdf['fig_xtick_decimals']=0
    figdf['fig_ytick_decimals']=0
    # specify voltage trace to plot
    #---------------------------------
    filt = 'data_filt_iir_band_5_50_sortby_burst'
    location = 'apical'
    timing='induction'
    burstn='mean'
    variable = 'data'+'_'+timing+'_'+filt+'_'+location   
    figtype = 'vtrace_example'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
    # array functions
    #---------------------
    array_funcs = [
    # np.abs, 
    # arrayfuncs._slice,
    arrayfuncs._mean, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to,
    # arrayfuncs._set_to,
    ]
    # array function keyword args
    #---------------------
    array_func_kws = [
    # {},
    # {'islice':slice(-1,None),'axis':2},
    {'axis':2} 
    # {'islice':slice(20), 'axis':1}, 
    # {'islice':slice(80,120), 'axis':1}, 
    # {'islice':slice(180,220), 'axis':1}, 
    # {'islice':slice(280,320), 'axis':1},
    # {'islice':slice(380,420), 'axis':1},
    ]
    # set df indices
    #-------------------
    # df_all=df_all.reset_index()
    df_all = df_all.set_index(conditions)
    # plot
    #------------------
    figs, axes = plots.PlotFuncs()._trace_mean(df=df_all, figdf=figdf, variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # reset index
    #-------------------------
    df_all=df_all.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

filt='data_filt_iir_band_5_50_sortby_burst'
_dendritic_integration(df_all=df_all[filt], buildfigdf=buildfigdf)

def _vtrace_soma(df_all, buildfigdf):
    '''
    '''
    # setup figdf
    #------------------------------------
    figdf = buildfigdf._vtrace_1path_mean()
    figdf['fig_ylabel']='Field potential (mV)'
    figdf['fig_xlabel']='Time (ms)'
    figdf['fig_yscale']=1000
    figdf['fig_xscale']=0.1
    figdf['fig_xmin']=0
    figdf['fig_xmax']=40.1
    figdf['fig_dxticks']=10.
    # figdf[path][filt]['fig_dyticks']=1.
    figdf['fig_xlim_all']=False
    figdf['fig_ylabel_fonstize']=40
    figdf['fig_xlabel_fonstize']=40
    figdf['trace_linewidth']=8
    figdf['error_style']='none'
    figdf['fig_ymin']=-.5
    figdf['fig_ymax']=1.5
    figdf['fig_dyticks']=.5
    figdf['fig_xtick_decimals']=0
    # specify voltage trace to plot
    #---------------------------------
    filt = 'data_filt_iir_high_5_sortby_burst'
    location = 'soma'
    timing='induction'
    burstn='mean'
    variable = 'data'+'_'+timing+'_'+filt+'_'+location   
    figtype = 'vtrace_example'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
    # array functions
    #---------------------
    array_funcs = [
    # np.abs, 
    # arrayfuncs._slice,
    arrayfuncs._mean, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to, 
    # arrayfuncs._set_to,
    # arrayfuncs._set_to,
    ]
    # array function keyword args
    #---------------------
    array_func_kws = [
    # {},
    # {'islice':slice(-1,None),'axis':2},
    {'axis':2} 
    # {'islice':slice(20), 'axis':1}, 
    # {'islice':slice(80,120), 'axis':1}, 
    # {'islice':slice(180,220), 'axis':1}, 
    # {'islice':slice(280,320), 'axis':1},
    # {'islice':slice(380,420), 'axis':1},
    ]
    # set df indices
    #-------------------
    df_all=df_all.reset_index()
    df_all = df_all.set_index(conditions)
    # plot
    #------------------
    figs, axes = plots.PlotFuncs()._trace_mean(df=df_all, figdf=figdf, variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # reset index
    #-------------------------
    df_all=df_all.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

filt='data_filt_iir_high_5_sortby_burst'
# _vtrace_soma(df_all=df_all[filt], buildfigdf=buildfigdf)

def _somatic_activity(df_all, buildfigdf):
    '''
    '''
    # setup figdf
    #------------------------------------
    figdf = buildfigdf._vtrace_1path_mean()
    figdf['fig_ylabel']='Field potential (mV)'
    figdf['fig_xlabel']='Time (ms)'
    figdf['fig_yscale']=1000
    figdf['fig_xscale']=0.1
    figdf['fig_xmin']=0
    figdf['fig_xmax']=40.1
    figdf['fig_dxticks']=10.
    # figdf[path][filt]['fig_dyticks']=1.
    figdf['fig_xlim_all']=False
    figdf['fig_ylabel_fonstize']=40
    figdf['fig_xlabel_fonstize']=40
    figdf['trace_linewidth']=8
    figdf['error_style']='none'
    figdf['fig_ymin']=0
    figdf['fig_ymax']=0.51
    figdf['fig_dyticks']=.1
    figdf['fig_xtick_decimals']=0
    figdf['fig_ytick_decimals']=1
    # specify voltage trace to plot
    #---------------------------------
    filt = 'data_filt_iir_high_300_hilbert_sortby_burst'
    location = 'soma'
    timing='induction'
    burstn='mean'
    variable = 'data'+'_'+timing+'_'+filt+'_'+location   
    figtype = 'vtrace_example'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
    # array functions
    #---------------------
    array_funcs = [
    np.abs, 
    # arrayfuncs._slice,
    arrayfuncs._mean, 
    arrayfuncs._set_to, 
    arrayfuncs._set_to, 
    arrayfuncs._set_to, 
    arrayfuncs._set_to,
    arrayfuncs._set_to,
    ]
    # array function keyword args
    #---------------------
    array_func_kws = [
    {},
    # {'islice':slice(-1,None),'axis':2},
    {'axis':2},  
    {'islice':slice(20), 'axis':1}, 
    {'islice':slice(80,120), 'axis':1}, 
    {'islice':slice(180,220), 'axis':1}, 
    {'islice':slice(280,320), 'axis':1},
    {'islice':slice(380,420), 'axis':1},
    ]
    # set df indices
    #-------------------
    df_all=df_all.reset_index()
    df_all = df_all.set_index(conditions)
    # plot
    #------------------
    figs, axes = plots.PlotFuncs()._trace_mean(df=df_all, figdf=figdf, variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # reset index
    #-------------------------
    df_all=df_all.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

filt='data_filt_iir_high_300_hilbert_sortby_burst'
# _somatic_activity(df_all=df_all[filt], buildfigdf=buildfigdf)

# example traces of raw and filtered soma/dendrite
#--------------------------------------------------
run_ind=False
if run_ind:
    figdf={}
    df_sorted={}
    path='1path'
    locations = ['apical', 'basal', 'soma']
    timing='induction'
    burstn='mean'
    # iterate over filters
    for filt in df_all.keys():
        # df_sorted[filt],df_all[filt] = loadnsortdf._slopes_vtrace_all(conditions=conditions, filt=filt)


        # filename = 'vtrace_df_1path_'+filt+'.pkl'
        # filename_slopes = 'slopes_df_1path.pkl'
        # # load and merge df's
        # df_vtrace = pd.read_pickle(group_directory+filename)
        # df_slopes = pd.read_pickle(group_directory+filename_slopes)
        # df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
        # # sort df's
        # df_sorted[filt] = figsetup._sortdf_1path_vtrace(df_merged) 
        # setup default figure parameters
        figdf[filt] = buildfigdf._vtrace_1path_mean()

        figdf[filt]['fig_ylabel']='Field potential (mV)'
        figdf[filt]['fig_xlabel']='Time (ms)'
        figdf[filt]['fig_yscale']=1000
        figdf[filt]['fig_xscale']=0.1
        figdf[filt]['fig_xmin']=0
        figdf[filt]['fig_xmax']=40.
        figdf[filt]['fig_dxticks']=10.
        # figdf[path][filt]['fig_dyticks']=1.
        figdf[filt]['fig_xlim_all']=False
        figdf[filt]['fig_ylabel_fonstize']=40
        figdf[filt]['fig_xlabel_fonstize']=40
        figdf[filt]['trace_linewidth']=8
        figdf[filt]['error_style']='none'

        # iterate over locations
        for location  in locations:
            # set ylimits based on location
            if location=='soma':
                figdf[filt]['fig_ymin']=-.5
                figdf[filt]['fig_ymax']=1.5
                figdf[filt]['fig_dyticks']=.5
            elif location=='apical' or location=='basal':
                figdf[filt]['fig_ymin']=-3.5
                figdf[filt]['fig_ymax']=.5
                figdf[filt]['fig_dyticks']=1.
                figdf[filt]['fig_ytick_assert']=0


            # set variable to be plotted from data df
            variable = 'data'+'_'+timing+'_'+filt+'_'+location
            # check that the variable exists in the current df
            if variable in df_all[filt]:
                figtype = 'vtrace_noerror'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
                # update which burst to plot in figdf
                figdf[filt]['fig_average_bursts']=True

                # plot
                #-------------------------------------------------
                array_funcs = [np.abs, arrayfuncs._slice, arrayfuncs._set_to, arrayfuncs._set_to]
                array_func_kws = [{},{'islice':slice(-1,None),'axis':2}, {'islice':slice(20), 'axis':1}, {'islice':slice(80,120), 'axis':1}]
                df_all[filt] = df_all[filt].set_index(conditions)
                figs_vtrace, axes_vtrace = plots.PlotFuncs()._trace_mean(df=df_all[filt], figdf=figdf[filt], variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
                df_all[filt]=df_all[filt].reset_index()
                # save figures
                #--------------------------------------------------
                # for fig_key, fig in figs_vtrace.iteritems():
                #     fname = figure_directory+figtype+str(fig_key)+'.png'
                #     fig.savefig(fname, format='png', dpi=dpi)

# mean with no error
#-----------------------
run_ind=False
if run_ind:
    paths=['1path', '2path']
    # filters applied to votage time series
    filters = [
        'data_filt_iir_high_5_sortby_burst',
        'data_filt_iir_band_5_50_sortby_burst',
        'data_filt_iir_high_300_sortby_burst',
        'data_filt_iir_high_300_hilbert_sortby_burst',
        ]
    # which burst to show inplot
    burstns = ['first', 'last', 'mean']
    # recording location
    locations = ['apical', 'basal', 'soma']
    # timing of recording, e.g. probe or induction
    timings = ['induction']

    # preallocate df's
    df_sorted={}
    figdf={}
    # iterate over conditions and plot vtrace during induction
    #----------------------------------------------------------------------------
    # 1 pathway or 2 pathway experiments
    for path in paths:
        df_sorted[path]={}
        figdf[path]={}
        # iterate over filters
        for filt in filters:
            # set filename to load data
            if path=='1path':
                filename = 'vtrace_df_1path_'+filt+'.pkl'
                filename_slopes = 'slopes_df_1path.pkl'
            elif path=='2path':
                filename = 'vtrace_df_'+filt+'.pkl'
                filename_slopes = 'slopes_df.pkl'
            # load and merge df's
            df_vtrace = pd.read_pickle(group_directory+filename)
            df_slopes = pd.read_pickle(group_directory+filename_slopes)
            df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
            
            # sort df's
            if path=='1path':
                df_sorted[path][filt] = figsetup._sortdf_1path_vtrace(df_merged) 
            elif path=='2path':
                df_sorted[path][filt] = figsetup._sortdf_2path_vtrace(df_merged) 
            
            # setup default figure parameters
            if path=='1path':
                figdf[path][filt] = figsetup._vtrace_1path_mean()
            if path=='2path':
                figdf[path][filt] = figsetup._vtrace_2path_mean()

            figdf[path][filt]['fig_xmin']=0
            figdf[path][filt]['fig_xmax']=40.
            figdf[path][filt]['fig_dxticks']=10.
            # figdf[path][filt]['fig_dyticks']=1.
            figdf[path][filt]['fig_xlim_all']=False
            figdf[path][filt]['fig_ylabel_fonstize']=25
            figdf[path][filt]['fig_xlabel_fonstize']=25


            # iterate over locations
            for location  in locations:
                # set ylimits based on location
                if location=='soma':
                    figdf[path][filt]['fig_ymin']=-1
                    figdf[path][filt]['fig_ymax']=1.5
                elif location=='apical' or location=='basal':
                    figdf[path][filt]['fig_ymin']=-3
                    figdf[path][filt]['fig_ymax']=.5
                # iterate over timings
                for timing in timings:
                    # set variable to be plotted from data df
                    variable = 'data'+'_'+timing+'_'+filt+'_'+location
                    # check that the variable exists in the current df
                    if variable in df_merged:
                        # iterate over burst number
                        for burstn in burstns:
                            figtype = 'vtrace_noerror'+'_'+timing+'_'+path+'_'+filt+'_'+burstn+'_'+location+'_'
                            # update which burst to plot in figdf
                            if burstn=='first':
                                figdf[path][filt]['fig_burst_number']=0
                                figdf[path][filt]['fig_average_bursts']=False
                            elif burstn=='last':
                                figdf[path][filt]['fig_burst_number']=lastburst_i
                                figdf[path][filt]['fig_average_bursts']=False
                            elif burstn=='mean':
                                figdf[path][filt]['fig_average_bursts']=True

                            # plot
                            #-------------------------------------------------
                            print 'fontsize',figdf[path][filt]['fig_xlabel_fonstize']
                            figdf[path][filt]['error_style']='none'
                            figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted[path][filt], figdf=figdf[path][filt], variable=variable)
                            # save figures
                            #--------------------------------------------------
                            for fig_key, fig in figs_vtrace.iteritems():
                                fname = figure_directory+figtype+str(fig_key)+'.png'
                                fig.savefig(fname, format='png', dpi=dpi)

#############################################################################
# plot probe voltage traces before and after induction
#############################################################################
# conditions to iterate over
#----------------------------------------------------------------------------
run_probe=False
if run_probe:
    array_funcs = [plots.ArrayFunctions()._slice_mean, plots.ArrayFunctions()._slice_mean]
    kw_pre = {'islice':slice(0,20), 'axis':2}
    kw_post = {'islice':slice(20,None), 'axis':2}
    array_func_kws = [kw_pre, kw_post]

    # one and 2 pathway experiments
    paths=['1path', '2path']
    # filters applied to votage time series
    filters = [
        'data_filt_iir_high_5_sortby_pulse',
        # 'data_filt_iir_band_5_50_sortby_pulse',
        # 'data_filt_iir_high_300_sortby_pulse',
        # 'data_filt_iir_high_300_hilbert_sortby_pulse',
        ]
    # which burst to show inplot
    burstns = ['first', 'last', 'mean']
    # recording location
    locations = ['apical', 'basal', 'soma']
    # timing of recording, e.g. probe or induction
    timings = ['probe']

    # preallocate df's
    df_sorted={}
    figdf={}
    # iterate over conditions and plot vtrace during induction
    #----------------------------------------------------------------------------
    # 1 pathway or 2 pathway experiments
    for path in paths:
        df_sorted[path]={}
        figdf[path]={}
        # iterate over filters
        for filt in filters:
            # set filename to load data
            if path=='1path':
                filename = 'vtrace_df_1path_'+filt+'.pkl'
                filename_slopes = 'slopes_df_1path.pkl'
            elif path=='2path':
                filename = 'vtrace_df_'+filt+'.pkl'
                filename_slopes = 'slopes_df.pkl'
            # load and merge df's
            df_vtrace = pd.read_pickle(group_directory+filename)
            df_slopes = pd.read_pickle(group_directory+filename_slopes)
            df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
            
            # sort df's
            if path=='1path':
                df_sorted[path][filt] = figsetup._sortdf_1path_vtrace(df_merged) 
            elif path=='2path':
                df_sorted[path][filt] = figsetup._sortdf_2path_vtrace(df_merged) 
            
            # setup default figure parameters
            if path=='1path':
                figdf[path][filt] = figsetup._vtrace_probe_1path_mean()
            if path=='2path':
                figdf[path][filt] = figsetup._vtrace_probe_2path_mean()

            figdf[path][filt]['fig_xmin']=0
            figdf[path][filt]['fig_xmax']=20
            figdf[path][filt]['fig_xlim_all']=False
            figdf[path][filt]['fig_axesoff']=True
            figdf[path][filt]['fig_scalebars']=True


            # iterate over locations
            for location  in locations:
                # set ylimits based on location
                if location=='soma':
                    figdf[path][filt]['fig_ymin']=-2
                    figdf[path][filt]['fig_ymax']=3.
                elif location=='apical' or location=='basal':
                    figdf[path][filt]['fig_ymin']=-6
                    figdf[path][filt]['fig_ymax']=2.
                # iterate over timings
                for timing in timings:
                    # set variable to be plotted from data df
                    variable = 'data'+'_'+timing+'_'+filt+'_'+location+'_data_aligned_0'

                    # check that the variable exists in the current df
                    if variable in df_merged:
                        figtype = 'vtrace_beforeafter'+'_'+timing+'_'+path+'_'+filt+'_'+location+'_'
                        variables =  [variable, variable]

                        # plot
                        #-------------------------------------------------
                        figs_vtrace, axes_vtrace = plots._vtrace_probe_mean(df_sorted=df_sorted[path][filt], figdf=figdf[path][filt], variables=variables, array_funcs=array_funcs, array_func_kws=array_func_kws)
                        # save figures
                        #--------------------------------------------------
                        for fig_key, fig in figs_vtrace.iteritems():
                            fname = figure_directory+figtype+str(fig_key)+'.png'
                            fig.savefig(fname, format='png', dpi=dpi)


#############################################################################
# one pathway experiments
#############################################################################
#============================================================================
# setup df for 5 Hz highpass
#============================================================================
# filenames for slope and vtrace data
#-------------------------------------
# filename_1path = 'vtrace_df_1path.pkl'
# filename_1path ='vtrace_df_1path_data_filt_iir_high_5_sortby_burst.pkl'
# filename_slopes_1path = 'slopes_df_1path.pkl'
# # load group dataframes, merge slopes and vtrace
# #-----------------------------------------------
# df_vtrace_1path=pd.read_pickle(group_directory+filename_1path)
# df_slopes_1path = pd.read_pickle(group_directory+filename_slopes_1path)
# df_merged_1path = pd.merge(df_vtrace_1path, df_slopes_1path, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])


# # list conditions to sort data by
# #--------------------------------
# conditions_1path = ['field_polarity_0_vtrace', 'induction_location_0_vtrace', 'field_mag_0_vtrace']

# # constraints to apply to keep/reject data {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
# #-------------------------------------------------------------------
# constraints_spec_1path = OrderedDict(
#     [
#     ('date_vtrace', {
#         ('apical', ):['>=',0],#20181113
#         ('basal', ):['>=', 20170405],
#         ('perforant', ):['>=',20170426]
#         }),
#     ('remove', {
#         ('apical'):['==',False], 
#         ('basal'): ['==',False],
#         ('peforant'):['==',False]
#         }),
#     ]) 
# # constraint applied to all conditions. this gets overwritten by specific constraints
# #------------------------------------
# constraints_all_1path = OrderedDict([
#     # ('remove', ['==',False])
#     ])
# # sorted data
# #----------------
# df_sorted_1path = functions._sortdf(df=df_merged_1path, conditions=conditions_1path, constraints_all=constraints_all_1path, constraints_spec=constraints_spec_1path)
# #=====================================================================
# # setup df for 300 Hz highpass data
# #=====================================================================
# # filename_1path = 'vtrace_df_1path.pkl'
# filename_1path ='vtrace_df_1path_data_filt_iir_band_300_1000_sortby_burst.pkl'
# filename_slopes_1path = 'slopes_df_1path.pkl'
# # load group dataframes, merge slopes and vtrace
# #-----------------------------------------------
# df_vtrace_1path=pd.read_pickle(group_directory+filename_1path)
# df_slopes_1path = pd.read_pickle(group_directory+filename_slopes_1path)
# df_merged_1path = pd.merge(df_vtrace_1path, df_slopes_1path, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
# # list conditions to sort data by
# #--------------------------------
# conditions_1path = ['field_polarity_0_vtrace', 'induction_location_0_vtrace', 'field_mag_0_vtrace']
# # constraints to apply to keep/reject data {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
# #-------------------------------------------------------------------
# constraints_spec_1path = OrderedDict(
#     [
#     ('date_vtrace', {
#         ('apical', ):['>=',0],#20181113
#         ('basal', ):['>=', 20170405],
#         ('perforant', ):['>=',20170426]
#         }),
#     ('remove', {
#         ('apical'):['==',False], 
#         ('basal'): ['==',False],
#         ('peforant'):['==',False]
#         }),
#     ]) 
# # constraint applied to all conditions. this gets overwritten by specific constraints
# #------------------------------------
# constraints_all_1path = OrderedDict([
#     # ('remove', ['==',False])
#     ])
# # sorted data
# #----------------
# df_sorted_1path_high = functions._sortdf(df=df_merged_1path, conditions=conditions_1path, constraints_all=constraints_all_1path, constraints_spec=constraints_spec_1path)

# #============================================================================
# # voltage trace during induction apical one pathway
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_1path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_apical_1path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_apical_1path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_apical_1path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # voltage trace during induction basal one pathway
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_1path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_basal_1path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_basal'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_basal_1path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_basal'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_basal_1path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_5_sortby_burst_basal'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # voltage trace plots during induction soma one pathway
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_1path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_soma_1path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_1path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_1path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_1path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)


#############################################################################
# two pathway experiments
#############################################################################
#============================================================================
# setup df for 5 Hz highpass
#============================================================================
# # filename = 'vtrace_df.pkl'
# filename = 'vtrace_df_data_filt_iir_high_5_sortby_burst.pkl'
# filename_slopes = 'slopes_df.pkl'
# # filename_asif = 'slopes_df_asif.pkl'
# # load group data class object
# df_vtrace=pd.read_pickle(group_directory+filename)
# df_slopes = pd.read_pickle(group_directory+filename_slopes)
# # df_asif = pd.read_pickle(group_directory+filename_asif)
# df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
# # df_all = df_all.append(df_asif, ignore_index=True, )
# # list conditions to sort data by
# # print sorted(df_merged.keys())
# conditions = ['field_polarity_0_slopes','induction_pattern_0_slopes','induction_pattern_other_0_slopes']
# # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
# constraints_spec = OrderedDict(
#     [('remove', {
#         ('TBS','weak5Hz'):['==',False],
#         ('TBS','nostim'): ['==',False],
#         ('weak5Hz', 'nostim'):['==',False]
#         }),
#     ('baseline_percent_slopes', {
#         ('TBS','weak5Hz'):['==',30], 
#         ('TBS','nostim'): ['==',30],
#         ('weak5Hz', 'nostim'):['==',30]
#         }),
#     ('date_slopes', {
#         ('TBS','weak5Hz'):['>=',20181113],#20181113
#         ('TBS','nostim'): ['>=',20181210],#20181210
#         ('weak5Hz', 'nostim'):['>',20180920]#20180920
#         })]
#     ) 
# # constraint applied to all conditions. this gets overwritten by specific constraints
# constraints_all = OrderedDict([
#     ('remove', ['==',False])
#     ])

# df_sorted_2path = functions._sortdf(df=df_merged, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)
# #============================================================================
# # setup df for 300 Hz highpass
# #============================================================================
# filename = 'vtrace_df_data_filt_iir_high_300_hilbert_sortby_pulse.pkl'
# filename_slopes = 'slopes_df.pkl'
# # filename_asif = 'slopes_df_asif.pkl'
# # load group data class object
# df_vtrace=pd.read_pickle(group_directory+filename)
# # pdb.set_trace()
# # print df_vtrace.data_induction_data_filt_iir_band_300_1000_hilbert_sortby_burst_soma[:10]
# df_slopes = pd.read_pickle(group_directory+filename_slopes)
# # df_asif = pd.read_pickle(group_directory+filename_asif)
# df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])

# # pdb.set_trace()
# # print df_merged.data_induction_data_filt_iir_band_300_1000_hilbert_sortby_burst_soma[:10]

# # df_all = df_all.append(df_asif, ignore_index=True, )
# # list conditions to sort data by
# # print sorted(df_merged.keys())
# conditions = ['field_polarity_0_slopes','induction_pattern_0_slopes','induction_pattern_other_0_slopes']
# # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
# constraints_spec = OrderedDict(
#     [('remove', {
#         ('TBS','weak5Hz'):['==',False],
#         ('TBS','nostim'): ['==',False],
#         ('weak5Hz', 'nostim'):['==',False]
#         }),
#     ('baseline_percent_slopes', {
#         ('TBS','weak5Hz'):['==',30], 
#         ('TBS','nostim'): ['==',30],
#         ('weak5Hz', 'nostim'):['==',30]
#         }),
#     ('date_slopes', {
#         ('TBS','weak5Hz'):['>=',20181113],#20181113
#         ('TBS','nostim'): ['>=',20181210],#20181210
#         ('weak5Hz', 'nostim'):['>',20180920]#20180920
#         })]
#     ) 
# # constraint applied to all conditions. this gets overwritten by specific constraints
# constraints_all = OrderedDict([
#     ('remove', ['==',False])
#     ])

# df_sorted_2path_high = functions._sortdf(df=df_merged, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

# #============================================================================
# # setup df for 5-50 Hz bandpass
# #============================================================================
# filename = 'vtrace_df_data_filt_iir_band_5_50_sortby_burst.pkl'
# filename_slopes = 'slopes_df.pkl'
# # filename_asif = 'slopes_df_asif.pkl'
# # load group data class object
# df_vtrace=pd.read_pickle(group_directory+filename)
# df_slopes = pd.read_pickle(group_directory+filename_slopes)
# # df_asif = pd.read_pickle(group_directory+filename_asif)
# df_merged = pd.merge(df_vtrace, df_slopes, on=['name','path'], how='left', suffixes=['_vtrace','_slopes'])
# # df_all = df_all.append(df_asif, ignore_index=True, )
# # list conditions to sort data by
# # print sorted(df_merged.keys())
# conditions = ['field_polarity_0_slopes','induction_pattern_0_slopes','induction_pattern_other_0_slopes']
# # {constraint column}{(condition values from conditions list)}[constraint logical, constraint value]
# constraints_spec = OrderedDict(
#     [('remove', {
#         ('TBS','weak5Hz'):['==',False],
#         ('TBS','nostim'): ['==',False],
#         ('weak5Hz', 'nostim'):['==',False]
#         }),
#     ('baseline_percent_slopes', {
#         ('TBS','weak5Hz'):['==',30], 
#         ('TBS','nostim'): ['==',30],
#         ('weak5Hz', 'nostim'):['==',30]
#         }),
#     ('date_slopes', {
#         ('TBS','weak5Hz'):['>=',20181113],#20181113
#         ('TBS','nostim'): ['>=',20181210],#20181210
#         ('weak5Hz', 'nostim'):['>',20180920]#20180920
#         })]
#     ) 
# # constraint applied to all conditions. this gets overwritten by specific constraints
# constraints_all = OrderedDict([
#     ('remove', ['==',False])
#     ])

# df_sorted_2path_band_5_50 = functions._sortdf(df=df_merged, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

# #============================================================================
# # voltage trace during induction apical two pathway
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_2path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_apical_2path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_apical_2path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_apical_2path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_5_sortby_burst_apical'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # voltage trace during induction apical two pathway bandpass 5-50Hz
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_2path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_band_5_50_apical_2path_burst_mean_'
# variable = 'data_induction_data_filt_iir_band_5_50_sortby_burst_apical'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_band_5_50, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_band_5_50_apical_2path_burst_first_'
# variable = 'data_induction_data_filt_iir_band_5_50_sortby_burst_apical'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_band_5_50, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_band_5_50_apical_2path_burst_last_'
# variable=  'data_induction_data_filt_iir_band_5_50_sortby_burst_apical'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_band_5_50, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # voltage trace during induction soma two pathway
# #============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_2path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_soma_2path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_2path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_2path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_5_sortby_burst_soma'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)


#============================================================================
# voltage trace during induction soma two pathway high frequency
#============================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_vtrace = figsetup._vtrace_2path_mean()

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_mean_'
# variable = 'data_induction_data_filt_iir_band_300_1000_sortby_burst_soma'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_first_'
# variable = 'data_induction_data_filt_iir_band_300_1000_sortby_burst_soma'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_last_'
# variable=  'data_induction_data_filt_iir_band_300_1000_sortby_burst_soma'
# figdf_vtrace['fig_burst_number']=lastburst_i
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

#============================================================================
# voltage trace during induction soma two pathway high frequency
#============================================================================
# setup df of figure parameters
#------------------------------   
# figdf_vtrace = figsetup._vtrace_2path_mean()
# figdf_vtrace['fig_abs']=False
# figdf_vtrace['fig_imag']=False

# # average over bursts
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_mean_'
# variable = 'data_induction_data_filt_iir_high_300_hilbert_sortby_pulse_soma'
# figdf_vtrace['fig_average_bursts']=True
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # first burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_first_'
# variable = 'data_induction_data_filt_iir_high_300_hilbert_sortby_pulse_soma'
# figdf_vtrace.drop('fig_average_bursts',axis=1, inplace=True)
# figdf_vtrace['fig_burst_number']=0
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# # last burst
# #-------------------------------------
# figtype = 'vtrace_ind_soma_high_2path_burst_last_'
# variable=  'data_induction_data_filt_iir_high_300_hilbert_sortby_pulse_soma'
# figdf_vtrace['fig_burst_number']=lastburst_i-3
# figs_vtrace, axes_vtrace = plots._vtrace_induction_mean(df_sorted=df_sorted_2path_high, figdf=figdf_vtrace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_vtrace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

