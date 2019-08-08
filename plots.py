import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import functions
import figsetup
import itertools
from sklearn.cross_decomposition import CCA
import copy
import pdb
import math
import inspect
from matplotlib import cm as colormap
from functions import _2array, _to_1sigfig

def _plot_io(df, figdf, variables, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
    '''FIXME add docs
    '''
    print 'plotting:', inspect.stack()[0][3]
    fig={}
    ax={}
    xlim={}
    ylim={}
    # iteratively apply functions for creating new column to dataframe
    #----------------------------------------------------------------
    if len(df_funcs)>0:
        for df_func_i, df_func in enuemrate(df_funcs):
            df = df_func(df, axis=1, **df_func_kws[df_func_i])
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        # create figure, passing params as **kwargs
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # iterate over traces
            for tracekey in traces:
                # get params from figdf
                params = figdf.loc[(figkey,subkey, tracekey)]
                # get sub df from df 
                if tracekey in list(df.index.values) and variables[0] in df and variables[1] in df:
                    # print variable, 'found in', tracekey
                    # get corresponding series
                    trace_series = df.loc[tracekey][variables]
                    # remove nans from trace series
                    na = trace_series.isna()
                    trace_series = trace_series[~na]

                    for row_i, row in trace_series.iterrows():
                        ax[figkey].plot(row[variables[0]], row[variables[1]], '.', color=params.trace_color)

                    plt.title(figkey)

    plt.show(block=False)

    return fig, ax

def _hist(df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
    '''FIXME add docs
    '''
    print 'plotting:', inspect.stack()[0][3]
    fig={}
    ax={}
    xlim={}
    ylim={}
    # iteratively apply functions for creating new column to dataframe
    #----------------------------------------------------------------
    if len(df_funcs)>0:
        for df_func_i, df_func in enuemrate(df_funcs):
            df = df_func(df, axis=1, **df_func_kws[df_func_i])
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        # create figure, passing params as **kwargs
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # iterate over traces
            for tracekey in traces:
                # get params from figdf
                params = figdf.loc[(figkey,subkey, tracekey)]
                # get sub df from df 
                if tracekey in list(df.index.values) and variable in df:
                    print variable, 'found in', tracekey
                    # get corresponding series
                    trace_series = df.loc[tracekey][variable]
                    # remove nans from trace series
                    na = trace_series.isna()
                    trace_series = trace_series[~na]

                    # convert to array
                    data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1)#*1000
                    print 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])

                    print 'data array shape:', data_array.shape
                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                        if len(data_array.shape)!=1:
                            data_array = data_array.flatten()

                        weights=np.ones_like(data_array)/float(len(data_array))
                        # bins = 100
                        # bins='auto'
                        data_range = [min(data_array), max(data_array)]
                        # print data_range
                        # bins =int(np.floor(len(data_array)/4))
                        # bins = np.arange(0, data_range[1], .01)
                        bins = np.arange(0, 4, .01)
                        # print data_array
                        ax[figkey].hist(data_array, color=params.trace_color, bins=bins, cumulative=True, histtype='step', weights=weights, orientation='vertical')
                        ax[figkey].invert_xaxis()
                        plt.title(figkey)
                        # if len(data_array.shape)==1:
                        #     # mean across slices
                        #     data_mean = data_array
                        #     #std across slices
                        #     data_std = 0
                        #     # sem across slices
                        #     data_sem = 0
                        # # get stats across first dimension
                        # else:
                        #     # mean across slices
                        #     data_mean = np.mean(data_array, axis=0)
                        #     #std across slices
                        #     data_std = np.std(data_array, axis=0)
                        #     # sem across slices
                        #     data_sem = stats.sem(data_array, axis=0)

                        # # time vector
                        # t = np.arange(len(data_mean))#

    #                     assert 'error_style' in figdf, 'specify error style'
    #                     # line plot with shaded error
    #                     #-----------------------------------
    #                     if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
    #                         ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
    #                         # print params.error_color
    #                         plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.error_color, alpha=params.error_alpha)
    #                     # error bar plot
    #                     #--------------------------------------
    #                     elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
    #                         ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
    #                             marker=params.trace_marker,  
    #                             markersize=params.markersize, 
    #                             elinewidth=params.error_linewidth, 
    #                             linewidth=params.trace_linewidth, 
    #                             markerfacecolor=params.trace_color, 
    #                             ecolor=params.error_color)

    # fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf,)

    plt.show(block=False)

    return fig, ax

def _trace_mean(df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
    '''FIXME add docs
    '''
    print 'plotting:', inspect.stack()[0][3]
    fig={}
    ax={}
    xlim={}
    ylim={}
    # iteratively apply functions for creating new column to dataframe
    #----------------------------------------------------------------
    if len(df_funcs)>0:
        for df_func_i, df_func in enuemrate(df_funcs):
            df = df_func(df, axis=1, **df_func_kws[df_func_i])
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        # create figure, passing params as **kwargs
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # iterate over traces
            for tracekey in traces:
                # get params from figdf
                params = figdf.loc[(figkey,subkey, tracekey)]
                # get sub df from df 
                if tracekey in list(df.index.values) and variable in df:
                    print variable, 'found in', tracekey
                    # get corresponding series
                    trace_series = df.loc[tracekey][variable]
                    # convert to array
                    data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1)#*1000
                    print 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])
                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                        if len(data_array.shape)==1:
                            # mean across slices
                            data_mean = data_array
                            #std across slices
                            data_std = 0
                            # sem across slices
                            data_sem = 0
                        # get stats across first dimension
                        else:
                            # mean across slices
                            data_mean = np.mean(data_array, axis=0)
                            #std across slices
                            data_std = np.std(data_array, axis=0)
                            # sem across slices
                            data_sem = stats.sem(data_array, axis=0)

                        # time vector
                        t = np.arange(len(data_mean))#

                        assert 'error_style' in figdf, 'specify error style'
                        # line plot with shaded error
                        #-----------------------------------
                        if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                            ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
                            # print params.error_color
                            plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.error_color, alpha=params.error_alpha)
                        # error bar plot
                        #--------------------------------------
                        elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                            ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
                                marker=params.trace_marker,  
                                markersize=params.markersize, 
                                elinewidth=params.error_linewidth, 
                                linewidth=params.trace_linewidth, 
                                markerfacecolor=params.trace_color, 
                                ecolor=params.error_color)

    fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf,)

    plt.show(block=False)

    return fig, ax

def _vtrace_probe_mean(df_sorted, figdf, variables, array_funcs, array_func_kws, **kwargs):
    '''FIXME add docs
    '''
    # FIXME add kwargs to alter figure details
    # create figure groupings (all conditions that will go on the same figure)
    fig={}
    ax={}
    xlim={}
    ylim={}
    kw_pre = {'islice':slice(0,20), 'axis':2}
    kw_post = {'islice':slice(20,None), 'axis':2}
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values


    # pdb.set_trace()
    # print sorted(figdf.keys())
    # iterate over figures
    for figkey in figures:
        # create figure, passing params as **kwargs
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        # get which induction number to plot
        if 'fig_induction_number' in figdf.loc[figkey]:
            induction_number = figdf.loc[figkey].fig_induction_number.unique(
                )[0]
        else: 
            induction_number=0
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # iterate over traces
            for tracekey in traces:
                params = figdf.loc[(figkey,subkey, tracekey)]
                # check that the tracekey exists in df
                if tracekey in df_sorted:
                    # iterate over variables
                    for variable_i, variable in enumerate(variables):
                        # get corresponding data manipulation
                        array_func=array_funcs[variable_i]
                        array_func_kw=array_func_kws[variable_i]
                        # check that variable exists
                        if variable in df_sorted[tracekey]:
                            # get series from df sorted
                            trace_series = df_sorted[tracekey][variable]
                            # convert to array
                            data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1, list_index=induction_number)
                            # apply array function
                            # data_array = array_func(data_array, **array_func_kw)

                            # scale y values
                            if 'fig_yscale' in figdf.loc[figkey]:
                                yscale = figdf.loc[figkey].fig_yscale.unique()[0]
                                data_array=data_array*yscale

                            # if there is more than 1 slice for the given conditions
                            if data_array.shape[0]!=0:
                                # pdb.set_trace()
                                # print 'before_after' in figdf.loc[figkey]
                                if 'before_after' in figdf.loc[figkey]:
                                    print params.before_after
                                    if params.before_after=='before':
                                        print 'before'
                                        data_array = ArrayFunctions()._slice_mean(data_array, **kw_pre)
                                    elif params.before_after=='after':
                                        print 'after'
                                        data_array = ArrayFunctions()._slice_mean(data_array, **kw_post)

                                # apply array function
                                # data_array = array_func(data_array, **array_func_kw)
                                assert len(data_array.shape)<=2,'dimsensions of data >2, unclear which dimension to average'

                                if len(data_array.shape)==1:
                                    # mean across slices
                                    data_mean = data_array
                                    #std across slices
                                    data_std = 0
                                    # sem across slices
                                    data_sem = 0
                                else:
                                    # get stats
                                    # mean across slices
                                    data_mean = np.mean(data_array, axis=0)
                                    #std across slices
                                    data_std = np.std(data_array, axis=0)
                                    # sem across slices
                                    data_sem = stats.sem(data_array, axis=0)

                                t = np.arange(len(data_mean))#
                                # scale x values
                                if 'fig_xscale' in figdf.loc[figkey]:
                                    xscale = figdf.loc[figkey].fig_xscale.unique()[0]
                                    t=t*xscale

                                if 'fig_scalebars' in figdf.loc[figkey] and figdf.loc[figkey].fig_scalebars.unique()[0]:
                                    functions._plot_scalebar(axes=ax[figkey], yscale=1, xscale=2, origin=(15,-2.8), width=4)
                                # line plot with shaded error
                                if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                                    ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
                                    # print t.shape, data_mean.shape, data_sem.shape
                                    plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.error_color, alpha=params.error_alpha)
                                # error bar plot
                                elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                                    ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
                                        marker=params.trace_marker,  
                                        markersize=params.markersize, 
                                        elinewidth=params.error_linewidth, 
                                        linewidth=params.trace_linewidth, 
                                        markerfacecolor=params.trace_color, 
                                        ecolor=params.error_color)
        # get x and y limits based data
        xlim[figkey] = ax[figkey].get_xlim()
        ylim[figkey] = ax[figkey].get_ylim()

    fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, xlim=xlim, ylim=ylim)

    plt.show(block=False)

    return fig, ax

def _vtrace_induction_mean(df_sorted, figdf, variable, **kwargs):
    '''FIXME add docs
    '''
    # FIXME add kwargs to alter figure details
    # create figure groupings (all conditions that will go on the same figure)
    fig={}
    ax={}
    xlim={}
    ylim={}
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])

    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        # create figure, passing params as **kwargs
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        # get which induction number to plot
        if 'fig_induction_number' in figdf.loc[figkey]:
            induction_number = figdf.loc[figkey].fig_induction_number.unique(
                )[0]
        else: 
            induction_number=0
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # iterate over traces
            for tracekey in traces:
                params = figdf.loc[(figkey,subkey, tracekey)]
                # print 'variable:', variable
                # get series from df sorted
                trace_series = df_sorted[tracekey][variable]
                # convert to array
                data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1, list_index=induction_number)#*1000


                # if there is more than 1 slice for the given conditions
                if data_array.shape[0]!=0:
                    # data array is 3d, slices x samples x bursts, and must be reduced to 2d for plotting 
                    if len(data_array.shape)>2:
                        # pdb.set_trace()
                        print tracekey, data_array.shape
                        # average over bursts
                        if 'fig_average_bursts' in figdf.loc[figkey] and all(figdf.loc[figkey].fig_average_bursts):
                            data_array = np.mean(data_array, axis=2).squeeze()
                        # show a specific burst or range of bursts
                        elif 'fig_burst_number' in figdf.loc[figkey]:
                            burst_number = figdf.loc[figkey].fig_burst_number.unique()[0]
                            data_array= data_array[:,:,burst_number].squeeze()
                            if len(data_array.shape)>2:
                                data_array.reshape(data_array.shape[0], -1, order='F')

                    # scale y values
                    if 'fig_yscale' in figdf.loc[figkey]:
                        yscale = figdf.loc[figkey].fig_yscale.unique()[0]
                        data_array=data_array*yscale

                    if 'fig_abs' in figdf.loc[figkey]and all(figdf.loc[figkey].fig_abs):
                        data_array=np.abs(data_array)

                    elif 'fig_imag' in figdf.loc[figkey]and all(figdf.loc[figkey].fig_imag):
                        data_array=np.imag(data_array)

                    if len(data_array.shape)==1:
                        # mean across slices
                        data_mean = data_array
                        #std across slices
                        data_std = 0
                        # sem across slices
                        data_sem = 0
                    else:
                        # get stats
                        # mean across slices
                        data_mean = np.mean(data_array, axis=0)
                        #std across slices
                        data_std = np.std(data_array, axis=0)
                        # sem across slices
                        data_sem = stats.sem(data_array, axis=0)
                    # # get stats
                    # # mean across slices
                    # data_mean = np.mean(data_array, axis=0)
                    # #std across slices
                    # data_std = np.std(data_array, axis=0)
                    # # sem across slices
                    # data_sem = stats.sem(data_array, axis=0)
                    # time vector
                    t = np.arange(len(data_mean))#
                    # scale x values
                    if 'fig_xscale' in figdf.loc[figkey]:
                        xscale = figdf.loc[figkey].fig_xscale.unique()[0]
                        t=t*xscale
                    # line plot with shaded error
                    if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                        ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
                        # print t.shape, data_mean.shape, data_sem.shape
                        plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.error_color, alpha=params.error_alpha)
                    # error bar plot
                    elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                        ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
                            marker=params.trace_marker,  
                            markersize=params.markersize, 
                            elinewidth=params.error_linewidth, 
                            linewidth=params.trace_linewidth, 
                            markerfacecolor=params.trace_color, 
                            ecolor=params.error_color)

                    # line plot with shaded error
                    elif figdf.loc[(figkey,subkey,tracekey)].error_style=='none':
                        print 'line_width', params.trace_linewidth
                        ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
        # get x and y limits based data
        # xlim[figkey] = ax[figkey].get_xlim()
        # ylim[figkey] = ax[figkey].get_ylim()
    
    fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, )

    plt.show(block=False)

    return fig, ax

def _bar(df_sorted, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], group_space=1, bar_width=1, bar_spacing=1):
    '''
    '''
    fig={}
    ax={}
    n_subgroups={}
    n_traces={}
    xlim={}
    ylim={}
    data={}
    heights={}
    locations={}
    y_errors={}
    tracelist={}
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # get pairwise comparisons between traces
    ttests  = Stats()._pairwise_ttests(df_sorted, variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # iterate over figures
    for figkey in figures:
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        locations[figkey] = []
        tracelist[figkey]=[]
        heights[figkey]=[]
        y_errors[figkey]=[]
        colors=[]
        xticks=[]
        xticklabels=[]
        cnt=bar_spacing
        # iterate over subgroups of traces
        for subkey in subgroups:
            traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
            # FIXME distribute subgroup padrameters to each trace in the subgroup, with priority to trace parameters
            cnt+=group_space
            # iterate over traces
            for tracekey in traces:
                param = figdf.loc[(figkey,subkey, tracekey)]
                if tracekey in df_sorted:

                    # iteratively apply functions for creating new column to dataframe
                    if len(df_funcs)>0:
                        for df_func_i, df_func in enuemrate(df_funcs):
                            df_sorted[tracekey] = df_func(df_sorted[tracekey], axis=1, **df_func_kws[df_func_i])

                    # get series from df sorted
                    trace_series = df_sorted[tracekey][variable]
                    # convert to array
                    data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1)#*1000
                    data[tracekey]=data_array

                    # iteratively apply functions to resulting data array
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])

                    # change data units to percent
                    if all(figdf.loc[figkey].fig_topercent):
                        print 'converting to percent'
                        data_array = 100.*(data_array-1)

                    # get stats
                    if type(data_array)==np.ndarray and len(data_array.shape)==1:
                        # pdb.set_trace()
                        # print figkey
                        # print data_array
                        # mean across slices
                        data_mean = np.mean(data_array, axis=0)
 
                        #std across slices
                        data_std = np.std(data_array, axis=0)
                        # sem across slices
                        data_sem = stats.sem(data_array, axis=0)
                        # add plot location
                        # print figkey, subkey, tracekey, param.sub_location, param.trace_location
                        plot_location = param.sub_location+param.trace_location
                        tracelist[figkey].append(tracekey)
                        locations[figkey].append(plot_location)
                        xticks.append(plot_location)
                        xticklabels.append(param.trace_label)
                        colors.append(param.trace_color)
                        heights[figkey].append(data_mean)
                        y_errors[figkey].append(data_sem)
                        print tracekey, data_mean.shape
                        plt.errorbar(locations[figkey][-1], data_mean, data_sem, color=param.error_color)
        
        # if len(heights[figkey])>0:
        barcontainer = ax[figkey].bar(locations[figkey], heights[figkey], width=param.fig_barwidth, tick_label=xticklabels)

        # get x and y lims
        xlim[figkey] = ax[figkey].get_xlim()
        ylim[figkey] = ax[figkey].get_ylim()
    
        # set bar color
        for bar_i, bar in enumerate(barcontainer):
            bar.set_color(colors[bar_i])

    # fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, )

    
    for figkey in ax:
        if 'fig_label_pvalues' in figdf and all(figdf.loc[figkey].fig_label_pvalues):
            _label_pvalues(ax=ax[figkey], ttests=ttests, traces=tracelist[figkey], x_locations=locations[figkey], y_means=heights[figkey], y_errors=y_errors[figkey])
        # get x and y lims
        xlim[figkey] = ax[figkey].get_xlim()
        ylim[figkey] = ax[figkey].get_ylim()

    # ylim may change after add significance markers, so reformat
    # fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, )


    # stats
    # get pairwise combinations of traces
    # combos = itertools.combinations(data.keys(), 2)
    # ttests = {}
    # for combo in combos:
    #     ttests[combo] = stats.ttest_ind(data[combo[0]], data[combo[1]])


    plt.show(block=False)

    return fig, ax

def _var2var_corr(df_sorted, figdf, variables, df_funcs=[], df_func_kws=[],array_funcs_x=[],array_func_kws_x=[],array_funcs_y=[],array_func_kws_y=[], group_space=1, bar_width=1, bar_spacing=1):
    '''
    '''
    fig={}
    ax={}
    n_subgroups={}
    n_traces={}
    xlim={}
    ylim={}
    data={}         
    data_x_subgroup={}
    data_y_subgroup={}
    colors={}
    markersizes={}
    regressions={}
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        data_x_subgroup[figkey]={}
        data_y_subgroup[figkey]={}
        colors[figkey]={}
        markersizes[figkey]={}
        regressions[figkey]={}
        # iterate over subgroups of traces
        for subkey in subgroups:
            # pdb.set_trace()
            # print figkey
            # print subkey
            # print (figkey,subkey)
            # print figdf.loc[(figkey, subkey, slice(None),)].index.get_level_values('trace').values
            traces = figdf.loc[(figkey, subkey, slice(None),)].index.get_level_values('trace').unique().values
            

            # FIXME distribute subgroup padrameters to each trace in the subgroup, with priority to trace parameters
            data_x_subgroup[figkey][subkey]=np.array([])
            data_y_subgroup[figkey][subkey]=np.array([])
            colors[figkey][subkey]=[]
            markersizes[figkey][subkey]=[]
            # iterate over traces
            for tracekey in traces:
                # print tracekey
                # print sorted(df_sorted.keys())
                param = figdf.loc[(figkey,subkey, tracekey)]
                if tracekey in df_sorted:
                    # apply df funcs
                    # print tracekey
                    for i, df_func in enumerate(df_funcs):
                        # print tracekey, i, df_func
                        df_sorted[tracekey] = df_func(df=df_sorted[tracekey], **df_func_kws[i])

                    if variables[0] in df_sorted[tracekey] and variables[0] in df_sorted[tracekey]:
                        # get series from df sorted
                        trace_series_x = df_sorted[tracekey][variables[0]]
                        # get series from df sorted
                        trace_series_y = df_sorted[tracekey][variables[1]]

                        # check for missing values and remove rows
                        nax = ~trace_series_x.isna()
                        nay = ~trace_series_y.isna()
                        
                        trace_series_x = trace_series_x[nax&nay]
                        trace_series_y = trace_series_y[nax&nay]

                        # convert to array
                        data_array_x = functions._2array(trace_series_x, remove_nans=True, remove_nans_axis=1)
                        # convert to array
                        data_array_y = functions._2array(trace_series_y, remove_nans=True, remove_nans_axis=1)

                        # apply array functions
                        for i, array_func in enumerate(array_funcs_x):
                            data_array_x = array_func(data_array_x, **array_func_kws_x[i])
                        for i, array_func in enumerate(array_funcs_y):
                            data_array_y = array_func(data_array_y, **array_func_kws_y[i])

                        if type(data_array_x)==np.ndarray and len(data_array_x.shape)==1 and data_array_x.shape[0]>0 and type(data_array_y)==np.ndarray and len(data_array_y.shape)==1 and data_array_y.shape[0]>0:

                            data_x_subgroup[figkey][subkey] = np.append(data_x_subgroup[figkey][subkey], data_array_x)
                            data_y_subgroup[figkey][subkey] = np.append(data_y_subgroup[figkey][subkey], data_array_y)
                            colors[figkey][subkey].append([param.trace_color]*len(data_array_y))
                            markersizes[figkey][subkey].append([param.trace_markersize]*len(data_array_y))

                            # if data_array_x.shape[0]>0 and  data_array_x.shape[0]>0:
                            ax[figkey].plot(data_array_x, data_array_y, marker='.',linestyle='None', color=param.trace_color, markersize=param.trace_markersize)
            # pdb.set_trace()
            print data_x_subgroup[figkey][subkey]
            print data_y_subgroup[figkey][subkey]
            if type(data_y_subgroup[figkey][subkey])==np.ndarray and type(data_x_subgroup[figkey][subkey])==np.ndarray and  data_y_subgroup[figkey][subkey].shape[0]>0 and data_x_subgroup[figkey][subkey].shape[0]>0:

                regressions[figkey][subkey] = stats.linregress(x=data_x_subgroup[figkey][subkey], y=data_y_subgroup[figkey][subkey])


        # get x and y lims
        xlim[figkey] = ax[figkey].get_xlim()
        ylim[figkey] = ax[figkey].get_ylim()

    # pdb.set_trace()
    for figkey in regressions:
        x = np.arange(xlim[figkey][0], xlim[figkey][1], (xlim[figkey][1]-xlim[figkey][0])/3.)
        y = np.arange(ylim[figkey][0], ylim[figkey][1], (ylim[figkey][1]-ylim[figkey][0])/3.)
        for subkey in regressions[figkey]:
            print subkey
            y_fit = regressions[figkey][subkey][0]*x + regressions[figkey][subkey][1]

            ax[figkey].plot(x, y_fit) 
            r = regressions[figkey][subkey][2]
            p = regressions[figkey][subkey][3]
            p = round(p, -int(math.floor(math.log10(abs(p)))))
            corrcoef_str = 'r={} \n p={}'.format(r, p)
            if 'fig_show_corrcoef' in figdf and all(figdf.loc[figkey].fig_show_corrcoef):
                ax[figkey].annotate(corrcoef_str, xy=(0.8,0.9), xycoords='axes fraction')



    fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, )


    # sta/stats.ttest_ind(data[combo[0]], data[combo[1]])


    plt.show(block=False)

    return fig, ax,

def _cca(df_sorted, figdf, x_variables, y_variables, df_funcs=[], df_func_kws=[],array_funcs_x=[],array_func_kws_x=[],array_funcs_y=[],array_func_kws_y=[], group_space=1, bar_width=1, bar_spacing=1):
    '''
    '''
    fig={}
    ax={}
    n_subgroups={}
    n_traces={}
    xlim={}
    ylim={}
    data={}         
    data_x_subgroup={}
    data_y_subgroup={}
    colors={}
    markersizes={}
    regressions={}
    # set figdf to hierarchical index (figure, subgroup, trace)
    figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
    # get list of all figure names
    figures = figdf.index.get_level_values('figure').unique().values
    # iterate over figures
    for figkey in figures:
        fig[figkey], ax[figkey] = plt.subplots()
        # get subgroups list
        subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
        data_x_subgroup[figkey]={}
        data_y_subgroup[figkey]={}
        colors[figkey]={}
        markersizes[figkey]={}
        regressions[figkey]={}
        # iterate over subgroups of traces
        for subkey in subgroups:
            # pdb.set_trace()
            # print figkey
            # print subkey
            # print (figkey,subkey)
            # print figdf.loc[(figkey, subkey, slice(None),)].index.get_level_values('trace').values
            traces = figdf.loc[(figkey, subkey, slice(None),)].index.get_level_values('trace').unique().values
            

            # FIXME distribute subgroup padrameters to each trace in the subgroup, with priority to trace parameters
            data_x_subgroup[figkey][subkey]=np.array([])
            data_y_subgroup[figkey][subkey]=np.array([])
            colors[figkey][subkey]=[]
            markersizes[figkey][subkey]=[]
            # iterate over traces
            for tracekey in traces:
                # print tracekey
                # print sorted(df_sorted.keys())
                param = figdf.loc[(figkey,subkey, tracekey)]
                if tracekey in df_sorted:
                    # apply df funcs
                    print tracekey
                    for i, df_func in enumerate(df_funcs):
                        # print tracekey, i, df_func
                        df_sorted[tracekey] = df_func(df=df_sorted[tracekey], **df_func_kws[i])

                    # for 

                    # if variables[0] in df_sorted[tracekey] and variables[0] in df_sorted[tracekey]:
                        # get series from df sorted
                    trace_series_x = df_sorted[tracekey][x_variables]
                    # get series from df sorted
                    trace_series_y = df_sorted[tracekey][y_variables]

                    # print trace_series_y
                    # print trace_series_x


                    # check for missing values and remove rows
                    nax = ~trace_series_x.isna().any(axis=1)
                    nay = ~trace_series_y.isna().any(axis=1)
                    
                    trace_series_x = trace_series_x[nax&nay]
                    trace_series_y = trace_series_y[nax&nay]

                    data_array_x = np.zeros(trace_series_x.shape)
                    for i, x_var in enumerate(x_variables):
                        data_array_x[:, i] = functions._2array(trace_series_x[x_var], remove_nans=True, remove_nans_axis=1)

                    data_array_y = np.zeros(trace_series_y.shape)
                    for i, y_var in enumerate(y_variables):
                        data_array_y[:, i] = functions._2array(trace_series_y[y_var], remove_nans=True, remove_nans_axis=1)
                    # pdb.set_trace()
                    # print data_array_x.shape
                    # print data_array_y.shape
                    # # convert to array
                    #----------------------
                    # data_array_x = functions._2array(trace_series_x, remove_nans=True, remove_nans_axis=1)
                    # # convert to array
                    # data_array_y = functions._2array(trace_series_y, remove_nans=True, remove_nans_axis=1)

                    # apply array functions
                    #--------------------------
                    # for i, array_func in enumerate(array_funcs_x):
                    #     data_array_x = array_func(data_array_x, **array_func_kws_x[i])
                    # for i, array_func in enumerate(array_funcs_y):
                    #     data_array_y = array_func(data_array_y, **array_func_kws_y[i])

                    if type(data_array_x)==np.ndarray and data_array_x.shape[0]>0 and type(data_array_y)==np.ndarray and data_array_y.shape[0]>0:

                        if data_x_subgroup[figkey][subkey].size==0:
                            data_x_subgroup[figkey][subkey]=data_array_x
                        else:
                            data_x_subgroup[figkey][subkey] = np.append(data_x_subgroup[figkey][subkey], data_array_x, axis=0)
                        if data_y_subgroup[figkey][subkey].size==0:
                            data_y_subgroup[figkey][subkey]=data_array_y
                        else:
                            data_y_subgroup[figkey][subkey] = np.append(data_y_subgroup[figkey][subkey], data_array_y, axis=0)
                        colors[figkey][subkey]+=[param.trace_color]*(data_array_y.shape[0])
                        markersizes[figkey][subkey]+=[param.trace_markersize]*data_array_y.shape[0]

                        # if data_array_x.shape[0]>0 and  data_array_x.shape[0]>0:
                        # ax[figkey].plot(data_array_x, data_array_y, marker='.',linestyle='None', color=param.trace_color, markersize=param.trace_markersize)
            # pdb.set_trace()

            # perform cca and plot result
            #-------------------------------------------------------------
            # pdb.set_trace()
            # print data_y_subgroup[figkey][subkey].shape
            # print data_x_subgroup[figkey][subkey].shape
            if type(data_y_subgroup[figkey][subkey])==np.ndarray and type(data_x_subgroup[figkey][subkey])==np.ndarray and  data_y_subgroup[figkey][subkey].shape[0]>0 and data_x_subgroup[figkey][subkey].shape[0]>0:
                x = data_x_subgroup[figkey][subkey]
                y = data_y_subgroup[figkey][subkey]
                # print x
                # print y
                cca = CCA(n_components=1)
                cca.fit(x,y)
                x_c, y_c = cca.transform(x,y)
                ax[figkey].scatter(x_c, y_c, s=markersizes[figkey][subkey], c=colors[figkey][subkey])
                w1 = functions._to_1sigfig(cca.x_weights_[0,0])
                w2 = functions._to_1sigfig(cca.x_weights_[1,0])
                weight_str = 'w_spike={} \n w_epsp={}'.format(w1, w2)
                ax[figkey].annotate(weight_str, xy=(0.7,0.), xycoords='axes fraction')
                print x_c.shape
                print y_c.shape
                regressions[figkey][subkey] = stats.linregress(x=x_c.squeeze(), y=y_c.squeeze())

        xlim[figkey] = ax[figkey].get_xlim()
        ylim[figkey] = ax[figkey].get_ylim()
    # plot regression line
    #------------------------------------------
    for figkey in regressions:
        x = np.arange(xlim[figkey][0], xlim[figkey][1], (xlim[figkey][1]-xlim[figkey][0])/3.)
        y = np.arange(ylim[figkey][0], ylim[figkey][1], (ylim[figkey][1]-ylim[figkey][0])/3.)
        for subkey in regressions[figkey]:
            print subkey
            y_fit = regressions[figkey][subkey][0]*x + regressions[figkey][subkey][1]

            ax[figkey].plot(x, y_fit) 
            r = regressions[figkey][subkey][2]
            p = regressions[figkey][subkey][3]
            r = functions._to_1sigfig(r)
            p = round(p, -int(math.floor(math.log10(abs(p)))))
            corrcoef_str = 'r={} \n p={}'.format(r, p)
            if 'fig_show_corrcoef' in figdf and all(figdf.loc[figkey].fig_show_corrcoef):
                ax[figkey].annotate(corrcoef_str, xy=(0.7,0.9), xycoords='axes fraction')



    fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, )


    # sta/stats.ttest_ind(data[combo[0]], data[combo[1]])


    plt.show(block=False)

    return fig, ax,

def _label_pvalues(ax, ttests, traces, x_locations, y_means, y_errors, show_sig=True, y_scale=0.05):
    '''
    '''
    def _label_diff(ax, text,x,y_mean, y_error, level, max_height, y_scale=0.05,):
        '''
        '''
        # get ylim
        ylim = ax.get_ylim()
        # set y value to for line to max bar height
        y=max_height
        # x and y values for the line
        xy =[[x[0], y], [x[1], y]]
        # transform to axes coordinates
        ax0 = ax.transLimits.transform(xy)
        x_ax = ax0[:,0]
        y_ax = ax0[:,1]
        x_text = min(x_ax[0], x_ax[1]) + float(abs(x_ax[0]-x_ax[1]))/2.
        # step up y value based on level
        y =  y_ax+y_scale*level
        # set new location for y text
        y_text=y[0]

        # draw lines and text
        props = {'connectionstyle':'arc','arrowstyle':'-',
                     'shrinkA':0,'shrinkB':0,'linewidth':2}
        ax.annotate(text, xy=(x_text,y_text), zorder=10, xycoords='axes fraction')
        ax.annotate('', xy=(x_ax[0],y[0]), xytext=(x_ax[1],y[1]), arrowprops=props, xycoords='axes fraction')

    if len(traces)>0:
        # all combinations of traces
        trace_combos = [temp for temp in itertools.combinations(traces, 2)]
        # combinations of x locations
        x_combos =  [temp for temp in itertools.combinations(x_locations, 2)]
        y_mean_combos = [temp for temp in itertools.combinations(y_means, 2)]
        y_error_combos = [temp for temp in itertools.combinations(y_errors, 2)]
        heights = [temp + y_errors[i] for i, temp in enumerate(y_means)]
        max_height = max(heights)
        # if only drawing lines between significant, need to reset levels
        if show_sig:
            # get indices of significant trace pairs
            sig_i = [i for i, trace_combo in enumerate(trace_combos) for key in ttests if key[0] in trace_combo and key[1] in trace_combo if ttests[key].pvalue <=0.05 ]
            # reset all indices based on significant values
            trace_combos = [trace_combos[i] for i in sig_i]
            x_combos = [x_combos[i] for i in sig_i]
            y_mean_combos = [y_mean_combos[i] for i in sig_i]
            y_error_combos = [y_error_combos[i] for i in sig_i]
        # get new levels
        levels = np.argsort([abs(temp[0] - temp[1]) for temp in x_combos])+1
        # reset ylim based on max plot height
        ylim = ax.get_ylim()
        level_stepsize = y_scale*(ylim[1]-ylim[0])
        level_peak = max_height+len(levels)*level_stepsize
        ax.set_ylim([ylim[0], level_peak+level_stepsize])
        # iterate over trace combinations
        for i, trace_combo in enumerate(trace_combos):
            # get correspnding key in ttests dictionary
            key = [temp for temp in ttests if temp[0] in trace_combo and temp[1] in trace_combo][0]
            # pair of x locations
            x = x_combos[i]
            # pair of y means
            y_mean = y_mean_combos[i]
            # pair of y errors
            y_error=y_error_combos[i]
            # level of relationship bar
            level = levels[i]
            # p values
            p = ttests[key].pvalue
            # round to first sigifg
            p = round(p, -int(math.floor(math.log10(abs(p)))))
            # if only showing significant pairings
            if show_sig:
                if p<=0.05: 
                    text='*'
                    _label_diff(ax=ax, text=text, x=x, y_mean=y_mean, y_error=y_error, level=level, max_height=max_height, y_scale=y_scale)
                else:
                    continue
            else:
                text = 'p='+str(p)
                _label_diff(ax=ax, text=text, x=x, y_mean=y_mean, y_error=y_error, level=level, max_height=max_height, y_scale=y_scale)

#############################################################################
# plotting functions
#############################################################################
class PlotFuncs:
    ''' each plot function should have coresponding function to generate figdf in BuildFigDF
    '''
    def __init__(self):
        '''
        '''
        pass

    def _draw_lines(self, fig, ax, figdf):
        '''
        '''
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # iterate over figures
        for figkey in figures:
            if 'fig_hlines' in figdf:
                yvals = figdf.loc[figkey].fig_hlines.unique()[0]
                xlims = ax[figkey].get_xlim()
                ax[figkey].hlines(yvals, xlims[0], xlims[1])
            if 'fig_vlines' in figdf:
                xvals = figdf.loc[figkey].fig_vlines.unique()[0]
                ylims = ax[figkey].get_ylim()
                ax[figkey].vlines(xvals, ylims[0], ylims[1])
        return fig, ax

    def _dose_response(self, df, figdf, variable, **kwargs):
        '''
        '''
        print 'plotting:', inspect.stack()[0][3]
        # preallocate fig and ax objects
        fig={}
        ax={}
        locations={}
        heights={}
        y_errors={}
        # figdf = figdf.reset_index()
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        print figdf.index.names
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        df = df.set_index(['field', 'path_1_syn_num'])
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            locations[figkey] = []
            heights[figkey]=[]
            y_errors[figkey]=[]
            colors=[]
            ecolors=[]
            xticks=[]
            xticklabels=[]
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    params = figdf.loc[(figkey,subkey, tracekey)]

                    try:
                        # get corresponding series
                        trace_series = df.loc[tracekey, slice(None)][variable]
                    except:
                        print tracekey, 'not in df index'
                        continue

                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    # check that data is correct  shape
                    if type(data_array)==np.ndarray and len(data_array.shape)==1:
                        # print data_array
                        # mean across cells
                        data_mean = np.mean(data_array, axis=0)
                        #std across cells
                        data_std = np.std(data_array, axis=0)
                        # sem across cells
                        data_sem = stats.sem(data_array, axis=0)
                        # check if trace location has been set manually
                        # if 'trace_location' in params:
                        plot_location = params.trace_location
                        locations[figkey].append(plot_location)
                        xticks.append(plot_location)
                        if 'trace_label' in params:
                            xticklabels.append(params.trace_label)
                        else:
                            xticklabels.append(plot_location)

                        colors.append(params.trace_color)
                        ecolors.append(params.trace_ecolor)
                        heights[figkey].append(data_mean)
                        y_errors[figkey].append(data_sem)
                        plt.errorbar(locations[figkey][-1], data_mean, data_sem, ecolor=params.trace_ecolor, elinewidth=2)
                        if 'fig_data_style' in figdf and figdf.fig_data_style.unique()[0]=='point':
                            ax[figkey].plot(locations[figkey][-1], heights[figkey][-1], color=colors[-1], linestyle='None', markersize=30, marker='.')
            if 'fig_barwidth' in figdf:
                width=figdf.fig_barwidth.unique()[0]
            else:
                width=1

            # if 'fig_data_style' in figdf and figdf.fig_data_style.unique()[0]=='point':
            #     ax[figkey].plot(locations[figkey], heights[figkey], linestyle='None', markersize=30, marker='.')

            # barcontainer = ax[figkey].bar(locations[figkey], heights[figkey], width=width, tick_label=xticklabels)
            # ax[figkey].set_xscale('symlog')
            # print xticks
            # ax[figkey].set_xticks(xticks)
            # ax[figkey].set_xticklabels(xticks)


            # set bar color
            # for bar_i, bar in enumerate(barcontainer):
            #     bar.set_color(colors[bar_i])

        # fig, ax = _format_figures(fig=fig, ax=ax, figdf=figdf)

        # fig, ax = FormatFig()._set_fontsizes(figures=fig, axes=ax, figdf=figdf)
        # fig, ax = FormatFig()._set_yticks(figures=fig, axes=ax, figdf=figdf)
        # fig, ax = FormatFig()._scale_ticklabels(figures=fig, axes=ax, figdf=figdf)
        # fig, ax = FormatFig()._set_ticklabel_decimals(figures=fig, axes=ax, figdf=figdf)

        fig, ax = FormatFig()._standard_figformat(figures=fig, axes=ax, figdf=figdf)

        plt.show(block=False)

        # fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, xlim=xlim, ylim=ylim)

        # for figkey in ax:
        # if 'fig_label_pvalues' in figdf and all(figdf.loc[figkey].fig_label_pvalues):
        #     _label_pvalues(ax=ax[figkey], ttests=ttests, traces=tracelist[figkey], x_locations=locations[figkey], y_means=heights[figkey], y_errors=y_errors[figkey])
        # # get x and y lims
        # xlim[figkey] = ax[figkey].get_xlim()
        # ylim[figkey] = ax[figkey].get_ylim()

        # # ylim may change after add significance markers, so reformat
        # fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, xlim=xlim, ylim=ylim)

        return fig, ax

    def _trace_mean(self, df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
        '''FIXME add docs
        '''
        if 'dt' in kwargs:
            dt=kwargs['dt']
        else:
            dt=1
        # report progress
        print 'plotting:', inspect.stack()[0][3]
        # preallocate figures and axes
        fig={}
        ax={}
        # iteratively apply functions for creating new column to dataframe
        #----------------------------------------------------------------
        if len(df_funcs)>0:
            for df_func_i, df_func in enuemrate(df_funcs):
                df = df_func(df, axis=1, **df_func_kws[df_func_i])
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    #-----------------------
                    params = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][variable]
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue
                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    print tracekey, variable
                    print 'data array shape:', data_array.shape

                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                        # iteratively apply array functions
                        #-----------------------------------
                        if len(array_funcs)>0:
                            for array_func_i, array_func in enumerate(array_funcs):
                                data_array=array_func(data_array, **array_func_kws[array_func_i])
                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:

                        # if array is 1d, convert to 2d
                        if len(data_array.shape)==1:
                            data_array = data_array.reshape((1,-1))
                        # mean across slices
                        data_mean = np.mean(data_array, axis=0)
                        print 'mean',data_mean.shape
                        #std across slices
                        data_std = np.std(data_array, axis=0)
                        # sem across slices
                        data_sem = stats.sem(data_array, axis=0)
                        # time vector
                        t = np.arange(0, len(data_mean)*dt, dt)

                        assert 'error_style' in figdf, 'specify error style'
                        print figdf.loc[(figkey,subkey,tracekey)].error_style
                        # line plot with shaded error
                        #-----------------------------------
                        if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                            print 'plotting'
                            ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
                            # print params.error_color
                            plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.trace_ecolor, alpha=params.trace_ealpha)
                        # error bar plot
                        #--------------------------------------
                        elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                            ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
                                marker=params.trace_marker,  
                                markersize=params.markersize, 
                                elinewidth=params.error_linewidth, 
                                linewidth=params.trace_linewidth, 
                                markerfacecolor=params.trace_color, 
                                ecolor=params.trace_ecolor)

                        else:
                            ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
        # format figure
        #----------------
        fig, ax = FormatFig()._standard_figformat(figures=fig, axes=ax, figdf=figdf)

        # fig, ax = _format_figures(fig=fig, ax=ax, figdf=figdf,)

        plt.show(block=False)

        return fig, ax

    def _var2var_mean(self, df, figdf, x_variable, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
        '''FIXME add docs
        '''
        if 'dt' in kwargs:
            dt=kwargs['dt']
        else:
            dt=1
        # report progress
        print 'plotting:', inspect.stack()[0][3]
        # preallocate figures and axes
        fig={}
        ax={}
        # iteratively apply functions for creating new column to dataframe
        #----------------------------------------------------------------
        if len(df_funcs)>0:
            for df_func_i, df_func in enuemrate(df_funcs):
                df = df_func(df, axis=1, **df_func_kws[df_func_i])
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    #-----------------------
                    params = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][[x_variable, variable]]
                    except:
                        print tracekey,'or', variable, 'or', x_variable, 'not in df index'
                        continue

                    # group data by x_variable
                    #-------------------------------------------------
                    trace_series = trace_series.set_index(x_variable)

                    # iterate over x_variable values
                    #------------------------------------------------
                    x_vals = np.sort(trace_series.index.unique().values)
                    y_vals = np.full_like(x_vals, np.nan, dtype=np.double)
                    e_vals = np.full_like(x_vals, np.nan, dtype=np.double)
                    for i, x_val in enumerate(x_vals):
                        print trace_series.loc[x_val, variable]
                        # get corresponding y data and convert to array
                        #----------------------------------------------
                        data_array = _2array(trace_series.loc[x_val, variable], remove_nans=True, remove_nans_axis=1)
                        print 'data array shape:', data_array.shape
                        # iteratively apply array functions
                        #-----------------------------------
                        if len(array_funcs)>0:
                            for array_func_i, array_func in enumerate(array_funcs):
                                data_array=array_func(data_array, **array_func_kws[array_func_i])
                        # make sure array is the correct shape
                        #--------------------------------------
                        if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                            assert len(data_array.shape)==1, 'data array must be 1d'
                            # mean across slices
                            data_mean = np.mean(data_array, axis=0)
                            #std across slices
                            data_std = np.std(data_array, axis=0)
                            # sem across slices
                            data_sem = stats.sem(data_array, axis=0)
                            # update y values and errors for plot
                            y_vals[i]=data_mean
                            e_vals[i]=data_sem

                    print 'x',x_vals
                    print 'y',y_vals
                    print 'e',e_vals
                    # line plot with shaded error
                    #-----------------------------------
                    if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                        ax[figkey].plot(x_vals, y_vals ,color=params.trace_color, linewidth=params.trace_linewidth)
                        # print params.error_color
                        plt.fill_between(x_vals, y_vals-e_vals, y_vals+e_vals, color=params.trace_ecolor, alpha=params.trace_ealpha)
                    # error bar plot
                    #--------------------------------------
                    elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                        ax[figkey].plot(x_vals, y_vals, 
                            color=params.trace_color, 
                            marker=params.trace_marker,  
                            markersize=params.trace_markersize,  
                            linewidth=params.trace_linewidth, 
                            markerfacecolor=params.trace_color)
                        ax[figkey].errorbar(x_vals, y_vals, yerr=e_vals, color=params.trace_color, 
                            marker=params.trace_marker,  
                            markersize=params.trace_markersize, 
                            elinewidth=params.error_linewidth, 
                            linewidth=params.trace_linewidth, 
                            markerfacecolor=params.trace_color, 
                            ecolor=params.trace_ecolor)

        # fig, ax = _format_figures(fig=fig, ax=ax, figdf=figdf,)
        # plt.axhline(y=1, color='black', linestyle='--', linewidth=4)
        # figure formatting
        #--------------------
        fig, ax = FormatFig()._set_fontsizes(figures=fig, axes=ax, figdf=figdf)
        fig, ax = FormatFig()._set_yticks(figures=fig, axes=ax, figdf=figdf)
        fig, ax = FormatFig()._scale_ticklabels(figures=fig, axes=ax, figdf=figdf)
        # plt.show(block=False)

        return fig, ax

    def _trace_individual(self, df, figdf, variable, index=0, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
        '''FIXME add docs
        '''
        # set dt
        #---------
        if 'dt' in kwargs:
            dt=kwargs['dt']
        else:
            dt=1
        # report progress
        #------------------
        print 'plotting:', inspect.stack()[0][3]
        # preallocate figures and axes
        fig={}
        ax={}
        # iteratively apply functions for creating new column to dataframe
        #----------------------------------------------------------------
        if len(df_funcs)>0:
            for df_func_i, df_func in enuemrate(df_funcs):
                df = df_func(df, axis=1, **df_func_kws[df_func_i])
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    #-----------------------
                    params = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][variable]
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue
                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    print 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])
                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                        # if array is 1d, convert to 2d
                        if len(data_array.shape)==1:
                            data_array = data_array.reshape((1,-1))
                        # mean across slices
                        data_mean = np.mean(data_array, axis=0)
                        #std across slices
                        data_std = np.std(data_array, axis=0)
                        # sem across slices
                        data_sem = stats.sem(data_array, axis=0)
                        # time vector
                        t = np.arange(0, len(data_mean)*dt, dt)

                        assert 'error_style' in figdf, 'specify error style'
                        # line plot with shaded error
                        #-----------------------------------
                        if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
                            ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
                            # print params.error_color
                            plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.trace_ecolor, alpha=params.trace_ealpha)
                        # error bar plot
                        #--------------------------------------
                        elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
                            ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
                                marker=params.trace_marker,  
                                markersize=params.markersize, 
                                elinewidth=params.error_linewidth, 
                                linewidth=params.trace_linewidth, 
                                markerfacecolor=params.trace_color, 
                                ecolor=params.trace_ecolor)

        fig, ax = _format_figures(fig=fig, ax=ax, figdf=figdf,)

        plt.show(block=False)

        return fig, ax

    def _hist(self, df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[],**kwargs):
        '''FIXME add docs
        '''
        print 'plotting:', inspect.stack()[0][3]
        fig={}
        ax={}
        xlim={}
        ylim={}
        # iteratively apply functions for creating new column to dataframe
        #----------------------------------------------------------------
        if len(df_funcs)>0:
            for df_func_i, df_func in enuemrate(df_funcs):
                df = df_func(df, axis=1, **df_func_kws[df_func_i])
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    params = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][variable]
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue
                    # remove nans from trace series
                    na = trace_series.isna()
                    trace_series = trace_series[~na]

                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    print 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])

                    print 'data array shape:', data_array.shape
                    # make sure array is the correct shape
                    if type(data_array)==np.ndarray and data_array.shape[0]!=0:
                        if len(data_array.shape)!=1:
                            data_array = data_array.flatten()

                        weights=np.ones_like(data_array)/float(len(data_array))
                        # bins = 100
                        # bins='auto'
                        data_range = [min(data_array), max(data_array)]
                        # print data_range
                        # bins =int(np.floor(len(data_array)/4))
                        # bins = np.arange(0, data_range[1], .01)
                        bins = np.arange(0, 4, .01)
                        # bins='auto'
                        # print data_array
                        ax[figkey].hist(data_array, color=params.trace_color, bins=bins, cumulative=False, histtype='step', weights=weights, orientation='vertical', linewidth=params.trace_linewidth)
                        # ax[figkey].invert_xaxis()
                        # plt.title(figkey)

        # fig, ax = FormatFig()._set_fontsizes(figures=fig, axes=ax, figdf=figdf)
        # fig, ax = FormatFig()._set_yticks(figures=fig, axes=ax, figdf=figdf)
        # fig, ax = FormatFig()._scale_ticklabels(figures=fig, axes=ax, figdf=figdf)
        fig, ax = FormatFig()._standard_figformat(figures=fig, axes=ax, figdf=figdf)

        plt.show(block=False)

        return fig, ax

    def _shapeplot(self, df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], df_sorted=[], cmap=colormap.PiYG, **kwargs):
        '''
        '''
        print 'plotting:', inspect.stack()[0][3]
        fig={}
        ax={}
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        df = df.reset_index().set_index('field')
        # iterate over figures
        for figkey in figures:
            # create figure, passing params as **kwargs
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # iterate over subgroups of traces
            for subkey in subgroups:
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # iterate over traces
                for tracekey in traces:
                    # get params from figdf
                    params = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        data=df.loc[tracekey,slice(None)][variable].values
                        morpho=df.loc[tracekey, slice(None)]['morpho'].values
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue

                    patches, colors = ShapePlot().basic(morpho=morpho, data=data, axes=ax[figkey], width_scale=3, colormap=cmap)

                    # plot collection
                    ax[figkey].add_collection(patches)
                    # show colorbar
                    plt.colorbar(patches)
                    # autoscale axes
                    ax[figkey].autoscale()
                    ax[figkey].set_aspect(1.)
                    plt.axis('off')
        plt.show(block=False)

        return fig, ax

    def _bar(self, df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], group_space=1, bar_width=1, bar_spacing=1, **kwargs):
        '''
        '''
        # preallocate variables to be passed to barplot
        #-----------------------------------------------
        fig={}
        ax={}
        n_subgroups={}
        n_traces={}
        xlim={}
        ylim={}
        data={}
        heights={}
        locations={}
        y_errors={}
        tracelist={}
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # get pairwise comparisons between traces
        # ttests  = Stats()._pairwise_ttests(df_sorted, variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
        # iterate over figures
        #--------------------
        for figkey in figures:
            # create figure objects
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # preallocate
            #---------------
            locations[figkey] = []
            tracelist[figkey]=[]
            heights[figkey]=[]
            y_errors[figkey]=[]
            colors=[]
            xticks=[]
            xticklabels=[]

            cnt=bar_spacing
            # iterate over subgroups of traces
            #---------------------------------
            for subkey in subgroups:
                # get traces
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # count subgroups
                cnt+=group_space
                # iterate over traces
                #---------------------
                for tracekey in traces:
                    # trace parameters
                    param = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][variable]
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue
                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    if len(data_array.shape)==0 or data_array.shape[0]==0:
                        continue
                    print tracekey, 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])
                            print array_func.__name__, data_array.shape
                    print 'data array shape:', data_array.shape
                    print tracekey, data_array
                    # make sure array is the correct shape (1 dimensional with at least one entry in first dimension)
                    #-------------------------------------------
                    if not (type(data_array)==np.ndarray and len(data_array.shape)==1 and data_array.shape[0]!=0):
                        continue
                    # pdb.set_trace()
                    # print figkey
                    # print data_array
                    # mean across slices
                    data_mean = np.mean(data_array, axis=0)
                    #std across slices
                    data_std = np.std(data_array, axis=0)
                    # sem across slices
                    data_sem = stats.sem(data_array, axis=0)
                    # add plot location
                    # print figkey, subkey, tracekey, param.sub_location, param.trace_location
                    print data_mean
                    plot_location = param.sub_location+param.trace_location
                    tracelist[figkey].append(tracekey)
                    locations[figkey].append(plot_location)
                    xticks.append(plot_location)
                    xticklabels.append(param.trace_label)
                    colors.append(param.trace_color)
                    heights[figkey].append(data_mean)
                    y_errors[figkey].append(data_sem)
                    print tracekey, data_mean.shape
                    plt.errorbar(locations[figkey][-1], data_mean, data_sem, color=param.trace_ecolor)


                    # plot individual data points
                    #-------------------------------------------
                    # binsize = float(param.fig_barwidth)/len(data_array)
                    # x_temp = np.linspace(plot_location-float(param.fig_barwidth)/2.,plot_location+float(param.fig_barwidth)/2., len(data_array))
                    # print x_temp
                    # plt.plot(x_temp, data_array, color=param.trace_color, marker='o', linestyle='None')
            
            # if len(heights[figkey])>0:
            barcontainer = ax[figkey].bar(locations[figkey], heights[figkey], width=param.fig_barwidth, tick_label=xticklabels)

            # get x and y lims
            xlim[figkey] = ax[figkey].get_xlim()
            ylim[figkey] = ax[figkey].get_ylim()
        
            # set bar color
            for bar_i, bar in enumerate(barcontainer):
                bar.set_color(colors[bar_i])
                # bar.set_edgecolor(colors[bar_i])

        # format figure
        #----------------
        fig, ax = FormatFig()._standard_figformat(figures=fig, axes=ax, figdf=figdf, xticks=False, xscale=False, xticks_minor=True)

        plt.show(block=False)

        return fig, ax

    def _bar_with_points(self, df, figdf, variable, array_funcs=[], array_func_kws=[], df_funcs=[], df_func_kws=[], group_space=1, bar_width=1, bar_spacing=1, **kwargs):
        '''
        '''
        # preallocate variables to be passed to barplot
        #-----------------------------------------------
        fig={}
        ax={}
        n_subgroups={}
        n_traces={}
        xlim={}
        ylim={}
        data={}
        heights={}
        locations={}
        y_errors={}
        tracelist={}
        # set figdf to hierarchical index (figure, subgroup, trace)
        figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
        # get list of all figure names
        figures = figdf.index.get_level_values('figure').unique().values
        # get pairwise comparisons between traces
        # ttests  = Stats()._pairwise_ttests(df_sorted, variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
        # iterate over figures
        #--------------------
        for figkey in figures:
            # create figure objects
            fig[figkey], ax[figkey] = plt.subplots()
            # get subgroups list
            subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
            # preallocate
            #---------------
            locations[figkey] = []
            tracelist[figkey]=[]
            heights[figkey]=[]
            y_errors[figkey]=[]
            colors=[]
            xticks=[]
            xticklabels=[]

            cnt=bar_spacing
            # iterate over subgroups of traces
            #---------------------------------
            for subkey in subgroups:
                # get traces
                traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
                # count subgroups
                cnt+=group_space
                # iterate over traces
                #---------------------
                for tracekey in traces:
                    # trace parameters
                    param = figdf.loc[(figkey,subkey, tracekey)]
                    # get corresponding series and convert to array
                    #----------------------------------------------
                    # if available, get series, otherwise next iter
                    try:
                        trace_series=df.loc[tracekey,slice(None)][variable]
                    except:
                        print tracekey,'or', variable, 'not in df index'
                        continue
                    # convert to array
                    data_array = _2array(trace_series, remove_nans=True, remove_nans_axis=1)
                    if len(data_array.shape)==0 or data_array.shape[0]==0:
                        continue
                    print tracekey, 'data array shape:', data_array.shape
                    # iteratively apply array functions
                    #-----------------------------------
                    if len(array_funcs)>0:
                        for array_func_i, array_func in enumerate(array_funcs):
                            data_array=array_func(data_array, **array_func_kws[array_func_i])
                            print array_func.__name__, data_array.shape
                    print 'data array shape:', data_array.shape
                    print tracekey, data_array
                    # make sure array is the correct shape (1 dimensional with at least one entry in first dimension)
                    #-------------------------------------------
                    if not (type(data_array)==np.ndarray and len(data_array.shape)==1 and data_array.shape[0]!=0):
                        continue
                    # pdb.set_trace()
                    # print figkey
                    # print data_array
                    # mean across slices
                    data_mean = np.mean(data_array, axis=0)
                    #std across slices
                    data_std = np.std(data_array, axis=0)
                    # sem across slices
                    data_sem = stats.sem(data_array, axis=0)
                    # add plot location
                    # print figkey, subkey, tracekey, param.sub_location, param.trace_location
                    print data_mean
                    plot_location = param.sub_location+param.trace_location
                    tracelist[figkey].append(tracekey)
                    locations[figkey].append(plot_location)
                    xticks.append(plot_location)
                    xticklabels.append(param.trace_label)
                    colors.append(param.trace_color)
                    heights[figkey].append(data_mean)
                    y_errors[figkey].append(data_sem)
                    print tracekey, data_mean.shape
                    plt.errorbar(locations[figkey][-1], data_mean, data_sem, color=param.trace_ecolor)


                    # plot individual data points
                    #-------------------------------------------
                    binsize = float(param.fig_barwidth)/len(data_array)
                    x_temp = np.linspace(plot_location-float(param.fig_barwidth)/2.,plot_location+float(param.fig_barwidth)/2., len(data_array))
                    print x_temp
                    plt.plot(x_temp, data_array, color=param.trace_color, marker='o', linestyle='None')
            
            # if len(heights[figkey])>0:
            barcontainer = ax[figkey].bar(locations[figkey], heights[figkey], width=param.fig_barwidth, tick_label=xticklabels)

            # get x and y lims
            xlim[figkey] = ax[figkey].get_xlim()
            ylim[figkey] = ax[figkey].get_ylim()
        
            # set bar color
            for bar_i, bar in enumerate(barcontainer):
                bar.set_color((0,0,0,0))
                bar.set_edgecolor(colors[bar_i])

        # format figure
        #----------------
        fig, ax = FormatFig()._standard_figformat(figures=fig, axes=ax, figdf=figdf, xticks=False, xscale=False, xticks_minor=True)

        plt.show(block=False)

        return fig, ax
#############################################################################
# figure formatting
#############################################################################
class FormatFig:
    '''
    '''
    def __init__(self, ):
        '''
        '''
        pass

    def _standard_figformat(self, figures, axes, figdf, tight=True, xticks=True, yticks=True, xscale=True, yscale=True, xticks_minor=False, **kwargs):
        '''
        '''
        
        # set yticks
        #--------------
        if yticks:
            figures, axes = FormatFig()._set_yticks(figures=figures, axes=axes, figdf=figdf)
        # set xticks
        #--------------
        if xticks:
            figures, axes = FormatFig()._set_xticks(figures=figures, axes=axes, figdf=figdf)
        # set xticks
        #--------------
        if xticks_minor:
            figures, axes = FormatFig()._set_xticks_minor(figures=figures, axes=axes, figdf=figdf)
        # scale yticklabels
        #-------------------
        if yscale:
            figures, axes = FormatFig()._scale_yticklabels(figures=figures, axes=axes, figdf=figdf)
        # scale xticklabels
        #-------------------
        if xscale:
            figures, axes = FormatFig()._scale_xticklabels(figures=figures, axes=axes, figdf=figdf)
        # set yticklabel decimals
        #-----------------------
        figures, axes = FormatFig()._set_yticklabel_decimals(figures=figures, axes=axes, figdf=figdf)
        # set xticklabel decimals
        #-----------------------
        figures, axes = FormatFig()._set_xticklabel_decimals(figures=figures, axes=axes, figdf=figdf)

        # set fontsizes
        #---------------
        figures, axes = FormatFig()._set_fontsizes(figures=figures, axes=axes, figdf=figdf)
        # set tight layout
        #-----------------
        if tight:
            for figkey in figures:
                figures[figkey].tight_layout()
            # plt.tight_layout()

        return figures, axes

    def _set_xticks(self, figures, axes, figdf, tick_max=10,**kwargs):
        '''
        '''

        print 'setting ticks'
        # get xlim across all figures
        #-------------------------------------
        xlim={}
        xlims=[]
        # iterate over figures
        for axkey, ax in axes.iteritems():
            
            # get ticks
            xticks = ax.get_xticks()
            print 'xTICKS',xticks
            # get updated lims (1  significant figure)
            xlim[axkey] = _to_1sigfig(ax.get_xlim())
            xlims.append(copy.copy(xlim[axkey]))
        # find x lims across all figures in group
        xlim_all = [min([temp[0] for temp in xlims]), max([temp[1] for temp in xlims])]

        # iterate over figures
        #--------------------------------------
        for axkey, ax in axes.iteritems():
            # # check if axes are numeric
            # #-----------------------------------------------------------
            # # get current ticklabels
            # xticklabels = [tick.get_text() for tick in ax.get_xticklabels()]
            # while '' in xticklabels:
            #     xticklabels.remove('')
            # print xticklabels
            # # check if tick labels are numeric
            # for label in xticklabels:
            #     try:
            #         label_float = type(float(label))==float
            #     except ValueError:
            #         label_float=False
            # # if ticklabels are numeric, scale them, otherwise leave them alone
            # if not label_float:
            #     continue
            # get ticks and limits
            #----------------------
            xticks = ax.get_xticks()
            # get scale factors
            #--------------------
            if 'fig_xscale' in figdf:
                xscale = figdf.loc[axkey].fig_xscale.values[0]
            else:
                xscale=1
            # get x lims
            xlim_current = list(ax.get_xlim())
            print 'xlim_current', xlim_current

            # set xlim across all figures
            #----------------------------
            if all(figdf.fig_xlim_all):
                xlim_current = xlim_all
            if 'fig_xmin' in figdf.keys():
                xlim_current[0] = figdf.loc[axkey].fig_xmin.unique()[0]/xscale
            if 'fig_xmax' in figdf.keys():
                xlim_current[1] = figdf.loc[axkey].fig_xmax.unique()[0]/xscale
            ax.set_xlim(xlim_current)

            # set x ticks
            #------------------------------------------------------------
            print 'setting ticks'
            # get current lims and ticks
            xlim[axkey] = copy.copy(list(ax.get_xlim()))
            print 'xlim', xlim[axkey]
            xticks = np.array(ax.get_xticks())
            xlim_scaled = np.array(xlim[axkey])

            # get number of ticks and tick spacing
            #------------------------------------------------
            # default nxticks and dxticks
            nxticks=5.
            dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
            # specifx dxticks
            if 'fig_dxticks' in figdf:
                dxticks = figdf.loc[axkey].fig_dxticks.unique()[0]/xscale
                nxticks = len(np.arange(xlim_scaled[0], xlim_scaled[1], dxticks))
            # specify nxticks
            elif 'fig_nxticks' in figdf:
                nxticks = figdf.loc[axkey].fig_nxticks.unique()[0]
                dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
            # make sure that there isn't a crazy number of ticks
            #-----------------------------------------------------
            if nxticks>tick_max:
                nxticks=tick_max
                dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks

            # assert a specific tick value
            #------------------------------
            if 'fig_xtick_assert' in figdf:
                xtick_assert = figdf.loc[axkey].fig_xtick_assert.unique()[0]/xscale
            else:
                xtick_assert = xlim_scaled[0]
            # crete new ticks
            #--------------------
            xticks_new_1 = np.flip(np.arange(xtick_assert, xlim_scaled[0], -dxticks))
            # print xticks_new_1
            xticks_new_2 = np.arange(xtick_assert, xlim_scaled[1], dxticks)
            xticks_new = np.append(xticks_new_1, xticks_new_2)
            print 'xticks new',xticks_new_1, xticks_new_2
            print 'xticks new',xtick_assert, xlim_scaled, dxticks, xscale

            # roud tick decimals
            #-------------------------
            if 'fig_xtick_round' in figdf:
                decimals = figdf.loc[axkey].fig_xtick_round.unique()[0]
                xticks_new = np.round(xticks_new, decimals=decimals)
            if 'fig_xticks' in figdf:
                xticks_new = figdf.fig_xticks.values[0]
            print 'xticks_new',xticks_new/xscale
            ax.set_xticks(xticks_new)
            ax.set_xticklabels(xticks_new)

        return figures, axes

    def _set_xticks_minor(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'setting xticks minor'
        # iterate over figures
        figdf = figdf.reset_index().set_index(['figure', 'subgroup', 'trace'])
        for axkey, ax in axes.iteritems():
            subgroups = figdf.loc[axkey].index.get_level_values('subgroup').unique().values
            xticks_minor=[]
            xticklabels_minor=[]
            if 'xticks_minor_loc' in figdf:
                for subgroup in subgroups:
                    subgroup_loc = figdf.loc[(axkey, subgroup)]['xticks_minor_loc'].unique()[0]
                    xticks_minor.append(subgroup_loc)
                    xticklabels_minor.append(subgroup)

            ax.set_xticks(xticks_minor, minor=True)
            ax.set_xticklabels(xticklabels_minor, minor=True, )

        return figures, axes

    
    def _set_yticks(self, figures, axes, figdf, tick_max=10,**kwargs):
        '''
        '''
        print 'setting ticks'
        # get ylim across all figures
        #-------------------------------------
        ylim={}
        ylims=[]
        # iterate over figures
        for axkey, ax in axes.iteritems():
            # get ticks
            yticks = ax.get_yticks()
            print 'YTICKS',yticks
            # get updated lims (1  significant figure)
            ylim[axkey] = _to_1sigfig(ax.get_ylim())
            # ylim[axkey] = ax.get_ylim()
            ylims.append(copy.copy(ylim[axkey]))
        # find x and y lims across all figures in group
        ylim_all = [min([temp[0] for temp in ylims]), max([temp[1] for temp in ylims])]

        # iterate over figures
        #--------------------------------------
        for axkey, ax in axes.iteritems():
            # draw figure to create ticklabels
            #----------------------------------
            # figures[axkey].canvas.draw()
            # # check that ticklabels are numeric
            # #----------------------------------------
            # # get current ticklabels
            # yticklabels = [tick.get_text() for tick in ax.get_yticklabels()]
            # while '' in yticklabels:
            #     yticklabels.remove('')
            # print yticklabels
            # # check if tick labels are numeric
            # for label in yticklabels:
            #     try:
            #         label_float = type(float(label))==float
            #     except ValueError:
            #         label_float=False
            # # if ticklabels are numeric, scale them, otherwise leave them alone
            # if not label_float:
            #     print 'yticks not numeric'
            #     continue

            # get ticks and limits
            #----------------------
            yticks = ax.get_yticks()
            # get scale factors
            #--------------------
            if 'fig_yscale' in figdf:
                yscale = figdf.loc[axkey].fig_yscale.values[0]
            else:
                yscale=1
            # get y lims
            ylim_current = list(ax.get_ylim())
            print 'ylim_current', ylim_current

            # set ylim across all figures
            #----------------------------
            if all(figdf.fig_ylim_all):
                ylim_current = ylim_all
            if 'fig_ymin' in figdf.keys():
                ylim_current[0] = figdf.loc[axkey].fig_ymin.unique()[0]/yscale
            if 'fig_ymax' in figdf.keys():
                ylim_current[1] = figdf.loc[axkey].fig_ymax.unique()[0]/yscale
            ax.set_ylim(ylim_current)

            # set y ticks
            #------------------------------------------------------------
            print 'setting ticks'
            # get current lims and ticks
            ylim[axkey] = copy.copy(list(ax.get_ylim()))
            print 'ylim', ylim[axkey]
            yticks = yscale*np.array(ax.get_yticks())
            ylim_scaled = yscale*np.array(ylim[axkey])

            # get number of ticks and tick spacing
            #------------------------------------------------
            # default nyticks and dyticks
            nyticks=5.
            dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
            # specify dyticks
            if 'fig_dyticks' in figdf:
                dyticks = figdf.loc[axkey].fig_dyticks.unique()[0]
                nyticks = len(np.arange(ylim_scaled[0], ylim_scaled[1], dyticks))
            # specify nyticks
            elif 'fig_nyticks' in figdf:
                nyticks = figdf.loc[axkey].fig_nyticks.unique()[0]
                dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
            # make sure that there isn't a crazy number of ticks
            #-----------------------------------------------------
            if nyticks>tick_max:
                nyticks=tick_max
                dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks

            # assert a specific tick value
            #------------------------------
            if 'fig_ytick_assert' in figdf:
                ytick_assert = figdf.loc[axkey].fig_ytick_assert.unique()[0]
            else:
                ytick_assert = ylim_scaled[0]
            # crete new ticks
            #--------------------
            yticks_new_1 = np.flip(np.arange(ytick_assert, ylim_scaled[0], -dyticks))
            # print yticks_new_1
            yticks_new_2 = np.arange(ytick_assert, ylim_scaled[1], dyticks)
            yticks_new = np.append(yticks_new_1, yticks_new_2)
            print 'yticks new',yticks_new_1, yticks_new_2
            print 'yticks new',ytick_assert, ylim_scaled, dyticks, yscale

            # roud tick decimals
            #-------------------------
            if 'fig_ytick_round' in figdf:
                decimals = figdf.loc[axkey].fig_ytick_round.unique()[0]
                yticks_new = np.round(yticks_new, decimals=decimals)
            if 'fig_yticks' in figdf:
                yticks_new = figdf.fig_yticks.values[0]
            print 'yticks_new',yticks_new
            ax.set_yticks(yticks_new/yscale)
            ax.set_yticklabels(yticks_new/yscale)

        return figures, axes

    def _set_yticklabel_decimals(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'setting tick decimals'
        for axkey, ax in axes.iteritems():
            # get ticks
            #----------------------
            yticks = ax.get_yticks()
            # apply scale factor
            #-------------------------
            if 'fig_yscale' in figdf:
                print 'yscale factor found'
                yscale = figdf.loc[axkey].fig_yscale.values[0]
            else:
                yscale=1
            # apply scaling factor
            yticks = yscale*yticks
            # set tick decimal places
            #---------------------------------------------------------------
            if 'fig_ytick_decimals' in figdf:
                # get decimal places
                dec = figdf.loc[axkey].fig_ytick_decimals.unique()[0]
                # get ticklabels
                yticklabels = ['%.{}f'.format(dec) % float(tick) for tick in yticks]
                print 'yticklabels',yticklabels
                # set ticklabels
                ax.set_yticklabels(yticklabels)
        return figures, axes
    
    def _set_xticklabel_decimals(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'setting tick decimals'
        for axkey, ax in axes.iteritems():
            # get ticks
            #-----------------------
            xticks = ax.get_xticks()
            # scale factor
            #-------------------------
            if 'fig_xscale' in figdf:
                print 'xscale factor found'
                xscale = figdf.loc[axkey].fig_xscale.values[0]
            else:
                xscale=1
            # apply scaling factor
            xticks = xscale*xticks
            # set tick decimal places
            #---------------------------------------------------------------
            if 'fig_xtick_decimals' in figdf:
                # get decimal places
                dec = figdf.loc[axkey].fig_xtick_decimals.unique()[0]
                # get ticklabels
                xticklabels = ['%.{}f'.format(dec) % float(tick) for tick in xticks]
                print 'xticklabels',xticklabels
                # set ticklabels
                ax.set_xticklabels(xticklabels)
        return figures, axes

    def _scale_yticklabels(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'scaling yticks'
        for axkey, ax in axes.iteritems():
            # get ticks
            yticks = ax.get_yticks()
            #--------------------------------------
            # yticks
            #-------------------------------------
            if 'fig_yscale' in figdf:
                print 'yscale factor found'
                yscale = figdf.loc[axkey].fig_yscale.values[0]
            else:
                yscale=1
            # apply scaling factor
            yticks = yscale*yticks
            # # get current ticklabels
            # yticklabels = [tick.get_text() for tick in ax.get_yticklabels()]
            # print yticklabels
            # # check if tick labels are numeric
            # for label in yticklabels:
            #     try:
            #         label_float = type(float(label))==float
            #     except ValueError:
            #         label_float=False
            # if ticklabels are numeric, scale them, otherwise leave them alone
            # if label_float:
            # update tick decimal places
            #-----------------------------
            # if 'fig_ytick_decimals' in figdf:
            #     # get decimal places
            #     dec = figdf.loc[axkey].fig_ytick_decimals.unique()[0]
            #     # get ticklabels with adjusted decimals
            #     yticklabels = ['%.{}f'.format(dec) % tick for tick in yticks]
            # else:
            #     yticklabels=yticks
            # set ticklabels
            yticklabels=yticks
            ax.set_yticklabels(yticklabels)
        return figures, axes

    def _scale_xticklabels(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'scaling xticks'
        for axkey, ax in axes.iteritems():
            # get ticks
            xticks = ax.get_xticks()
            print xticks
            # xticklabels = list(ax.get_xticklabels())
            #--------------------------------------
            # yticks
            #-------------------------------------
            if 'fig_xscale' in figdf:
                print 'xscale factor found'
                xscale = figdf.loc[axkey].fig_xscale.values[0]
            else:
                xscale=1
            # apply scaling factor
            xticks = xscale*xticks
            print xticks
            # # get current ticklabels
            # yticklabels = [tick.get_text() for tick in ax.get_yticklabels()]
            # print yticklabels
            # # check if tick labels are numeric
            # for label in yticklabels:
            #     try:
            #         label_float = type(float(label))==float
            #     except ValueError:
            #         label_float=False
            # if ticklabels are numeric, scale them, otherwise leave them alone
            # if label_float:
            # update tick decimal places
            #-----------------------------
            # if 'fig_xtick_decimals' in figdf:
            #     # get decimal places
            #     dec = figdf.loc[axkey].fig_xtick_decimals.unique()[0]
            #     # get ticklabels with adjusted decimals
            #     xticklabels = ['%.{}f'.format(dec) % tick for tick in xticks]
            # else:
            #     xticklabels=xticks
            # set ticklabels
            xticklabels=xticks
            ax.set_xticklabels(xticklabels)
        return figures, axes

    def _set_fontsizes(self, figures, axes, figdf, **kwargs):
        '''
        '''
        print 'setting axes properties'
        # iterate through figures
        for axkey, ax in axes.iteritems():
            # set ticklabel fontweight and size
            #-----------------------------------
            print 'setting ticklabels'
            # ytick labels
            for label in ax.get_xticklabels():
                # fontweight
                label.set_fontweight(figdf.loc[axkey].fig_xtick_fontweight.values[0])
                # fonstize
                label.set_fontsize(figdf.loc[axkey].fig_xtick_fontsize.values[0])
            # ytick labels
            for label in ax.get_yticklabels():
                # fontweight
                label.set_fontweight(figdf.loc[axkey].fig_ytick_fontweight.values[0])
                # fontsize
                label.set_fontsize(figdf.loc[axkey].fig_ytick_fontsize.values[0])
            for label in ax.get_xticklabels(which='minor'):
                print 'minor label', label
                label.set_fontweight(figdf.loc[axkey].fig_xtick_fontweight.values[0])
                label.set_fontsize(figdf.loc[axkey].fig_xtick_fontsize.values[0])
                # print 'minor label', label.fontweight

            # ax.tick_params(axis='x', which='minor', labelsize=figdf.loc[axkey].fig_ytick_fontsize.values[0], fontweight='bold')

            # turn off axes box
            #-----------------------------------
            # turn off top and right axes lines
            if all(figdf.loc[axkey].fig_boxoff):
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
            # turn off all axes lines
            if 'fig_axesoff' in figdf.keys() and all(figdf.loc[axkey].fig_axesoff):
                ax.set_axis_off()

            # set axes linewidth and tick position
            #--------------------------------------
            ax.spines['left'].set_linewidth(figdf.loc[axkey].fig_axes_linewidth.unique()[0])
            ax.spines['bottom'].set_linewidth(figdf.loc[axkey].fig_axes_linewidth.unique()[0])
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')

            # set axes labels
            #----------------
            if 'fig_xlabel' in figdf:
                ax.set_xlabel(figdf.loc[axkey].fig_xlabel.values[0], fontsize=figdf.loc[axkey]['fig_xlabel_fontsize'].values[0], fontweight=figdf.loc[axkey].fig_xlabel_fontweight.values[0])
            if 'fig_ylabel' in figdf:
                ax.set_ylabel(figdf.loc[axkey].fig_ylabel.values[0], fontsize=figdf.loc[axkey]['fig_ylabel_fontsize'].values[0], fontweight=figdf.loc[axkey].fig_ylabel_fontweight.values[0])

            # set tight layout
            #-------------------
            if all(figdf.loc[axkey].fig_tight_layout):
                plt.figure(figures[axkey].number)
                plt.tight_layout()

        return figures, axes

#############################################################################
#
#############################################################################
class ArrayFunctions:
    '''
    '''
    def _reject_outliers(self, array, std_tol=2, axis=0, **kwargs):
        '''
        '''
        # if 'std_tol' in kwargs:
        #     std_tol=kwargs['std_tol']
        # array_mean = np.mean(array, axis=axis)
        # array_std = np.std(array, axis=axis)
        # array_diff = array-array_mean

        array_new = array[abs(array- np.mean(data, axis=axis)) < m * np.std(array, axis=axis)]
        return array_new

    def _last(self, array, **kwargs):
        '''
        '''
        last = array[:,-1]

        return last

    def _first(self, array, **kwargs):
        '''
        '''
        first = array[:,0]
        return first

    def _slice_mean(self, array, islice, axis=2, **kwargs):
        '''
        '''
        # assert 'axis' in kwargs, 'please specificy axis to operate on'
        # assert '' in kwargs, 'please specificy axis to operate on'
        # axis = kwargs['axis']
        slicer = [slice(None)]*len(array.shape)
        # pdb.set_trace()
        # print slicer
        # print islice
        # print array.shape
        if axis<len(array.shape) and array.shape[axis]>0:
            slicer[axis]=islice
            # print slicer
            # print array[slicer]
            array_new = np.mean(array[slicer], axis=axis)
        else:
            array_new = array
        # array_new = np.mean(array[slicer], axis=axis)
        # else:
        #     array_new=array
        # print array_new.shape
        return array_new

    def _slice(self, array, islice, axis=1, **kwargs):
        '''
        '''
        # assert 'axis' in kwargs, 'please specificy axis to operate on'
        # assert '' in kwargs, 'please specificy axis to operate on'
        # axis = kwargs['axis']
        print 'slicing array',islice
        print array.shape
        slicer = [slice(None)]*len(array.shape)
        # pdb.set_trace()
        # print slicer
        # print islice
        # print array.shape
        if axis<len(array.shape) and array.shape[axis]>0:
            slicer[axis]=islice
            array_new =  copy.copy(array[slicer]).squeeze()
        else:
            array_new=array
        # print slicer
        # print array[slicer]
        # array_new =  copy.copy(array[slicer])
        # array_new = np.mean(array[slicer], axis=axis)
        print array_new.shape
        return array_new

    def _set_to(self, array, islice, axis=1, set_val=0., **kwargs):
        '''
        '''
        print 'setting array indices',islice, 'to',set_val
        print array.shape
        slicer = [slice(None)]*len(array.shape)
        array_new=copy.copy(array)
        if axis<len(array.shape) and array.shape[axis]>0:
            slicer[axis]=islice
            array_new[slicer]=set_val
            # array_new =  copy.copy(array[slicer]).squeeze()
        else:
            print 'slice dimensions do not match array dimensions'
        
        return array_new

    def _mean(self, array, axis=2, **kwargs):
        '''
        '''
        mean = np.mean(array, axis=axis)
        return mean

    def _adapt(self, array, **kwargs):
        '''
        '''
        adapt = array[:,-1]/array[:,0]
        return adapt

    def _nth(self, array, **kwargs):
        '''
        '''
        nth = array[:,kwargs['n']]
        return nth

    def _every_nth(self, array, **kwargs):
        '''
        '''
        pulses = kwargs['pulses']
        pulse_i = kwargs['pulse_i']
        mask = range(pulse_i, array.shape[1], pulses)
        every_nth = array[:,mask]
        return every_nth

class FrameFunctions:
    '''
    '''
    def _normalize_column(self, df, colnorm=[], colnames=[], colkeys=[], colkeys_exclude=[], other_path=False):
        '''
        '''
        # update columns to be normalized
        colnames=copy.copy(colnames)
        if len(colkeys)>0:
            columns = row.index.values
            for col in columns:
                if all([colkey in col for colkey in colkeys]) and not any([temp in col for temp in colkeys_exclude]):
                    
                    colnames.append(col)
        # get list of columns to be normalized
        def _norm(row, colnorm=colnorm, colnames=colnames, colkeys=colkeys, colkeys_exclude=colkeys_exclude, other_path=other_path):
            ''' normalize data in colnames columns based on data in colnorm column
            '''
            col_add = '_norm_'+colnorm
            norm = row[colnorm]
            # print colnorm
            # print colnames
            for col in colnames:
                new_data =np.array(row[col])/np.array(norm)
                get_inf = np.isinf(new_data)
                new_data[get_inf]=np.nan
                row[col+col_add] = new_data
            return row

        kwargs = {'colnorm':colnorm, 'colnames':colnames, 'colkeys':colkeys, 'colkeys_exclude':colkeys_exclude, 'other_path':other_path}
        df = df.apply(_norm, axis=1, **kwargs)
        return df

    def _remove_outliers(self, df, colnames=[], colkeys=[], colkeys_exclude=[], z_tol=2):
        '''
        '''
        # update columns to be normalized
        colnames=copy.copy(colnames)
        if len(colkeys)>0:
            columns = row.index.values
            for col in columns:
                if all([colkey in col for colkey in colkeys]) and not any([temp in col for temp in colkeys_exclude]):
                    colnames.append(col)
        # print colnames
        coladd='_remove_outliers'
        for col in colnames:
            series = df[col]
            keep = copy.copy(series)
            na = ~series.isna()
            keep[~na] = False
            keep[na] =  np.abs(stats.zscore(series[na])) < z_tol 
            df[col+coladd] = np.nan
            df.ix[keep, col+coladd] = df[col][keep] 

        return df

    def _regress_out(self, df, colregress, colnames=[], colkeys=[], colkeys_exclude=[]):
        '''
        '''
        # update columns to be normalized
        colnames=copy.copy(colnames)
        if len(colkeys)>0:
            columns = row.index.values
            for col in columns:
                if all([colkey in col for colkey in colkeys]) and not any([temp in col for temp in colkeys_exclude]):
                    colnames.append(col)

        coladd = '_regressout_'+colregress
        # pdb.set_trace()

        
        x_series = df[colregress]
        nax = ~x_series.isna()
        for col in colnames:
            df[col+coladd]=np.nan
            y_series = df[col]
            nay = ~y_series.isna()
            y = y_series[nax&nay].values
            x = x_series[nax&nay].values
            # check for missing values and remove rows
            # print col
            # print x
            # print y
            reg  = stats.linregress(x, y)
            # print reg
            y_fit = reg[0]*x + reg[1]
            # print y_fit
            # print y-y_fit
            df.ix[nax&nay,col+coladd]=y-y_fit
            # print df[col+coladd]

        return df

    def _combine_paths(self, df, colnames=[], colkeys=[], colkeys_exclude=[],):
        '''
        '''
        # update columns to be normalized
        colnames=copy.copy(colnames)
        if len(colkeys)>0:
            columns = row.index.values
            for col in columns:
                if all([colkey in col for colkey in colkeys]) and not any([temp in col for temp in colkeys_exclude]):
                    colnames.append(col)

        # get list of columns to be normalized
        def _combine_paths(row, colnorm=colnorm, colnames=colnames, colkeys=colkeys, colkeys_exclude=colkeys_exclude):
            ''' normalize data in colnames columns based on data in colnorm column
            '''
            col_add = '_combinedpaths'
            current_path = row['path']
            filename = row['filename']
            other_path_name = df[(df.filename==filename) & (df.path!=current_path)].name
            for col in colnames:
                row[col+coladd] = row[col] + df.loc[other_path_name, col]
            return row

        kwargs = {'colnorm':colnorm, 'colnames':colnames, 'colkeys':colkeys, 'colkeys_exclude':colkeys_exclude}
        df = df.apply(_combine_paths, axis=1, **kwargs)
        return df

class Stats:
    '''
    '''
    def _pairwise_ttests(self, df_sorted, variable, array_funcs=[], array_func_kws=[]):
        '''
        '''
        # stats

        data={}
        for tracekey in df_sorted.keys():
            # get series from df sorted
            trace_series = df_sorted[tracekey][variable]

            # convert to array
            data[tracekey] = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1, array_funcs=array_funcs, array_func_kws=array_func_kws)#*1000

            # FIXME how to apply array functions here
            if type(data[tracekey])==np.ndarray and data[tracekey].shape[0]>0:
                print tracekey, data[tracekey].shape
                for i, array_func in enumerate(array_funcs):
                    data[tracekey]= array_func(data[tracekey], **array_func_kws[i])

        # get pairwise combinations of traces
        combos = itertools.combinations(data.keys(), 2)
        ttests = {}
        for combo in combos:
            # print combo[0], combo[1]
            # print data[combo[0]]
            # print data[combo[1]]
            ttests[combo] = stats.ttest_ind(data[combo[0]], data[combo[1]])

        return ttests


    def _linregress(self, df_sorted, x_variable, y_variable, array_funcs_x=[], array_func_kws_x=[], array_funcs_y=[], array_func_kws_y=[]):
        '''
        '''
        regressions={}
        data_x={}
        data_y={}
        for tracekey in df_sorted:
            trace_series_x = df_sorted[tracekey][x_variable]
            trace_series_y = df_sorted[tracekey][y_variable]

            data_x[tracekey] = functions._2array(trace_series_x, remove_nans=True, remove_nans_axis=1,)
            data_y[tracekey] = functions._2array(trace_series_y, remove_nans=True, remove_nans_axis=1,)

            # apply array functions
            for i, array_func in enumerate(array_funcs_x):
                data_x[tracekey]= array_func(data_x[tracekey], **array_func_kws[i])
            for i, array_func in enumerate(array_funcs_y):
                data_y[tracekey]= array_func(data_y[tracekey], **array_func_kws[i])

            slope, intercept, r_value, p_value, std_err = stats.linregress(x=data_x[tracekey], y=data_y[tracekey])

            regressions[tracekey]['x_variable'] = x_variable
            regressions[tracekey]['y_variable'] = y_variable
            regressions[tracekey]['slope'] = slope
            regressions[tracekey]['intercept'] = intercept
            regressions[tracekey]['r_value'] = r_value
            regressions[tracekey]['p_value'] = p_value
            regressions[tracekey]['std_err'] = std_err
            
        return regressions

    def _cca(self, df_sorted, x_variables, y_variables):
        '''
        '''
        x_data={}
        y_data={}
        cca={}
        transformed={}
        for tracekey in df_sorted.keys():
            x_data[tracekey] = []
            for x_i, x_var in enumerate(x_variables):

                # get series from df sorted
                trace_series = df_sorted[tracekey][x_var]

                x_data[tracekey].append(functions._2array(trace_series, remove_nans=True, remove_nans_axis=1))

            x_data[tracekey] = np.array(x_data[tracekey]).squeeze().T
            y_data[tracekey] = []
            for y_i, y_var in enumerate(y_variables):

                # get series from df sorted
                trace_series = df_sorted[tracekey][x_var]
                y_data[tracekey].append(functions._2array(trace_series, remove_nans=True, remove_nans_axis=1))
            y_data[tracekey] = np.array(y_data[tracekey]).squeeze().T
            if x_data[tracekey].shape[0]>0:
                cca[tracekey] = CCA()
                cca[tracekey].fit(x_data[tracekey], y_data[tracekey])
                x_c, y_c = cca[tracekey].transform(x_data[tracekey], y_data[tracekey])
                transformed[tracekey]=[x_c, y_c]

        return cca, transformed

    def _anova_ind(self, df_sorted, variable):
        '''
        '''
        data={}
        for tracekey in df_sorted.keys():
            # get series from df sorted
            trace_series = df_sorted[tracekey][variable]

            # convert to array
            data[tracekey] = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1)#*1000

        # get pairwise combinations of traces

        combos = itertools.combinations(data.keys(), 2)
        ttests = {}
        for combo in combos:
            ttests[combo] = stats.ttest_ind(data[combo[0]], data[combo[1]])

# class FormatFig:
#     '''
#     '''
#     def __init__(self, ):
#         '''
#         '''
#         pass

#     def _standard_figformat(self, figures, axes, figdf, **kwargs):
#         '''
#         '''
        
#         # set yticks
#         #--------------
#         figures, axes = FormatFig()._set_yticks(figures=figures, axes=axes, figdf=figdf)
#         # scale ticklabels
#         #-------------------
#         figures, axes = FormatFig()._scale_ticklabels(figures=figures, axes=axes, figdf=figdf)
#         # set ticklabel decimals
#         #-----------------------
#         figures, axes = FormatFig()._set_ticklabel_decimals(figures=figures, axes=axes, figdf=figdf)
#         # set fontsizes
#         #---------------
#         figures, axes = FormatFig()._set_fontsizes(figures=figures, axes=axes, figdf=figdf)
#         # set tight layout
#         #-----------------
#         plt.tight_layout()

#         return figures, axes

#     def _set_xticks(self, figures, axes, figdf, tick_max=10,**kwargs):
#         '''
#         '''
#         print 'setting ticks'
#         # get ylim and xlim across all figures
#         #-------------------------------------
#         xlim={}
#         ylim={}
#         xlims=[]
#         ylims=[]
#         # iterate over figures
#         for axkey, ax in axes.iteritems():
#             # get ticks
#             yticks = ax.get_yticks()
#             xticks = ax.get_xticks()
#             # get updated lims
#             xlim[axkey] = _to_1sigfig(ax.get_xlim())
#             ylim[axkey] = _to_1sigfig(ax.get_ylim())
#             # print ylim
#             xlims.append(copy.copy(xlim[axkey]))
#             ylims.append(copy.copy(ylim[axkey]))
#         # find x and y lims across all figures in group
#         xlim_all = [min([temp[0] for temp in xlims]), max([temp[1] for temp in xlims])]
#         ylim_all = [min([temp[0] for temp in ylims]), max([temp[1] for temp in ylims])]

#         # iterate over figures
#         for axkey, ax in axes.iteritems():
#             # get ticks and limits
#             #----------------------
#             yticks = ax.get_yticks()
#             xticks = ax.get_xticks()
#             # ylim = ax.get_ylim()
#             # xlim = ax.get_xlim()
#             # get scale factors
#             #--------------------
#             if 'fig_yscale' in figdf:
#                 yscale = figdf.loc[axkey].fig_yscale.values[0]
#             else:
#                 yscale=1
#             if 'fig_xscale' in figdf:
#                 xscale = figdf.loc[axkey].fig_xscale.values[0]
#             else:
#                 xscale=1
#             # get x and y lims
#             ylim_current = list(ax.get_ylim())
#             xlim_current = list(ax.get_xlim())
#             # set ylim across all figures
#             #----------------------------
#             if all(figdf.fig_ylim_all):
#                 xlim_current = xlim_all
#                 ylim_current = ylim_all
#             if 'fig_ymin' in figdf.keys():
#                 ylim_current[0] = figdf.loc[axkey].fig_ymin.unique()[0]/yscale
#             if 'fig_xmin' in figdf.keys():
#                 xlim_current[0] = figdf.loc[axkey].fig_xmin.unique()[0]/xscale
#             if 'fig_ymax' in figdf.keys():
#                 ylim_current[1] = figdf.loc[axkey].fig_ymax.unique()[0]/yscale
#             if 'fig_xmax' in figdf.keys():
#                 xlim_current[1] = figdf.loc[axkey].fig_xmax.unique()[0]/xscale

#             ax.set_ylim(ylim_current)
#             ax.set_xlim(xlim_current)

#             # set x and y ticks
#             #---------------------------------------------------------------
#             print 'setting ticks'
#             # get current lims and ticks
#             xlim[axkey] = copy.copy(list(ax.get_xlim()))
#             ylim[axkey] = copy.copy(list(ax.get_ylim()))
#             # xticks = ax.get_xticks()
#             # yticks = ax.get_yticks()
#             xticks = xscale*np.array(ax.get_xticks())
#             yticks = yscale*np.array(ax.get_yticks())
#             xlim_scaled = xscale*np.array(xlim[axkey])
#             ylim_scaled = yscale*np.array(ylim[axkey])
#             nyticks=5
#             dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             nxticks=5
#             dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             # print 'ylim', ylim_scaled
#             if 'fig_dyticks' in figdf:
#                 dyticks = figdf.loc[axkey].fig_dyticks.unique()[0]
#                 nyticks = len(np.arange(ylim_scaled[0], ylim_scaled[1], dyticks))
#             elif 'fig_nyticks' in figdf:
#                 nyticks = figdf.loc[axkey].fig_nyticks.unique()[0]
#                 dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             # else:
#             #     nyticks=5
#             #     dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks

#             if nyticks>tick_max:
#                 nyticks=tick_max
#                 dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             if 'fig_ytick_assert' in figdf:
#                 ytick_assert = figdf.loc[axkey].fig_ytick_assert.unique()[0]
#             else:
#                 ytick_assert = ylim_scaled[0]
#             # print ylim_scaled
#             # print ytick_assert
#             yticks_new_1 = np.flip(np.arange(ytick_assert, ylim_scaled[0], -dyticks))
#             # print yticks_new_1
#             yticks_new_2 = np.arange(ytick_assert, ylim_scaled[1], dyticks)
#             yticks_new = np.append(yticks_new_1, yticks_new_2)

#             if 'fig_dxticks' in figdf:
#                 dxticks = figdf.loc[axkey].fig_dxticks.unique()[0]
#                 nxticks = len(np.arange(xlim_scaled[0], xlim_scaled[1], dxticks))
#             elif 'fig_nxticks' in figdf:
#                 nxticks = figdf.loc[axkey].fig_nxticks.unique()[0]
#                 dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             # else:
#             #     nxticks=5
#             #     dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             if nxticks>tick_max:
#                 nxticks=tick_max
#                 dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             if 'fig_xtick_assert' in figdf:
#                 xtick_assert = figdf.loc[axkey].fig_xtick_assert.unique()[0]
#             else:
#                 xtick_assert = xlim_scaled[0]
#                 xtick_assert = _to_1sigfig(xtick_assert)
#             xticks_new_1 = np.flip(np.arange(xtick_assert, xlim_scaled[0], -dxticks))
#             xticks_new_2 = np.arange(xtick_assert, xlim_scaled[1], dxticks)
#             xticks_new = np.append(xticks_new_1, xticks_new_2)
#             print xticks_new_1, xticks_new_2

#             if 'fig_ytick_round' in figdf:
#                 decimals = figdf.loc[axkey].fig_ytick_round.unique()[0]
#                 yticks_new = np.round(yticks_new, decimals=decimals)

#             if 'fig_xtick_round' in figdf:
#                 decimals = figdf.loc[axkey].fig_xtick_round.unique()[0]
#                 xticks_new = np.round(xticks_new, decimals=decimals)

#             if 'fig_xticks' in figdf:
#                 xticks_new = figdf.fig_xticks.values[0]
#             if 'fig_yticks' in figdf:
#                 yticks_new = figdf.fig_yticks.values[0]

#             if 'fig_set_xscale' in figdf:
#                 ax.set_xscale(figdf.fig_set_xscale.values[0])
#             print 'yticks_new',yticks_new
#             print 'xticks_new',xticks_new



#             # ax.set_yticks(yticks_new/yscale)
#             ax.set_xticks(xticks_new/xscale)
#         return figures, axes

#     def _set_yticks(self, figures, axes, figdf, tick_max=10,**kwargs):
#         '''
#         '''
#         print 'setting ticks'
#         # get ylim and xlim across all figures
#         #-------------------------------------
#         xlim={}
#         ylim={}
#         xlims=[]
#         ylims=[]
#         # iterate over figures
#         for axkey, ax in axes.iteritems():
#             # get ticks
#             yticks = ax.get_yticks()
#             xticks = ax.get_xticks()
#             # get updated lims
#             xlim[axkey] = _to_1sigfig(ax.get_xlim())
#             ylim[axkey] = _to_1sigfig(ax.get_ylim())
#             # print ylim
#             xlims.append(copy.copy(xlim[axkey]))
#             ylims.append(copy.copy(ylim[axkey]))
#         # find x and y lims across all figures in group
#         xlim_all = [min([temp[0] for temp in xlims]), max([temp[1] for temp in xlims])]
#         ylim_all = [min([temp[0] for temp in ylims]), max([temp[1] for temp in ylims])]

#         # iterate over figures
#         for axkey, ax in axes.iteritems():
#             # get ticks and limits
#             #----------------------
#             yticks = ax.get_yticks()
#             xticks = ax.get_xticks()
#             # ylim = ax.get_ylim()
#             # xlim = ax.get_xlim()
#             # get scale factors
#             #--------------------
#             if 'fig_yscale' in figdf:
#                 yscale = figdf.loc[axkey].fig_yscale.values[0]
#             else:
#                 yscale=1
#             if 'fig_xscale' in figdf:
#                 xscale = figdf.loc[axkey].fig_xscale.values[0]
#             else:
#                 xscale=1
#             # get x and y lims
#             ylim_current = list(ax.get_ylim())
#             xlim_current = list(ax.get_xlim())
#             # set ylim across all figures
#             #----------------------------
#             if all(figdf.fig_ylim_all):
#                 xlim_current = xlim_all
#                 ylim_current = ylim_all
#             if 'fig_ymin' in figdf.keys():
#                 ylim_current[0] = figdf.loc[axkey].fig_ymin.unique()[0]/yscale
#             if 'fig_xmin' in figdf.keys():
#                 xlim_current[0] = figdf.loc[axkey].fig_xmin.unique()[0]/xscale
#             if 'fig_ymax' in figdf.keys():
#                 ylim_current[1] = figdf.loc[axkey].fig_ymax.unique()[0]/yscale
#             if 'fig_xmax' in figdf.keys():
#                 xlim_current[1] = figdf.loc[axkey].fig_xmax.unique()[0]/xscale

#             ax.set_ylim(ylim_current)
#             ax.set_xlim(xlim_current)

#             # set x and y ticks
#             #---------------------------------------------------------------
#             print 'setting ticks'
#             # get current lims and ticks
#             xlim[axkey] = copy.copy(list(ax.get_xlim()))
#             ylim[axkey] = copy.copy(list(ax.get_ylim()))
#             # xticks = ax.get_xticks()
#             # yticks = ax.get_yticks()
#             xticks = xscale*np.array(ax.get_xticks())
#             yticks = yscale*np.array(ax.get_yticks())
#             xlim_scaled = xscale*np.array(xlim[axkey])
#             ylim_scaled = yscale*np.array(ylim[axkey])
#             nyticks=5
#             dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             nxticks=5
#             dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             # print 'ylim', ylim_scaled
#             if 'fig_dyticks' in figdf:
#                 dyticks = figdf.loc[axkey].fig_dyticks.unique()[0]
#                 nyticks = len(np.arange(ylim_scaled[0], ylim_scaled[1], dyticks))
#             elif 'fig_nyticks' in figdf:
#                 nyticks = figdf.loc[axkey].fig_nyticks.unique()[0]
#                 dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             # else:
#             #     nyticks=5
#             #     dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks

#             if nyticks>tick_max:
#                 nyticks=tick_max
#                 dyticks = float(abs(ylim_scaled[1]-ylim_scaled[0]))/nyticks
#             if 'fig_ytick_assert' in figdf:
#                 ytick_assert = figdf.loc[axkey].fig_ytick_assert.unique()[0]
#             else:
#                 ytick_assert = ylim_scaled[0]
#             # print ylim_scaled
#             # print ytick_assert
#             yticks_new_1 = np.flip(np.arange(ytick_assert, ylim_scaled[0], -dyticks))
#             # print yticks_new_1
#             yticks_new_2 = np.arange(ytick_assert, ylim_scaled[1], dyticks)
#             yticks_new = np.append(yticks_new_1, yticks_new_2)

#             if 'fig_dxticks' in figdf:
#                 dxticks = figdf.loc[axkey].fig_dxticks.unique()[0]
#                 nxticks = len(np.arange(xlim_scaled[0], xlim_scaled[1], dxticks))
#             elif 'fig_nxticks' in figdf:
#                 nxticks = figdf.loc[axkey].fig_nxticks.unique()[0]
#                 dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             # else:
#             #     nxticks=5
#             #     dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             if nxticks>tick_max:
#                 nxticks=tick_max
#                 dxticks = float(abs(xlim_scaled[1]-xlim_scaled[0]))/nxticks
#             if 'fig_xtick_assert' in figdf:
#                 xtick_assert = figdf.loc[axkey].fig_xtick_assert.unique()[0]
#             else:
#                 xtick_assert = xlim_scaled[0]
#                 xtick_assert = _to_1sigfig(xtick_assert)
#             xticks_new_1 = np.flip(np.arange(xtick_assert, xlim_scaled[0], -dxticks))
#             xticks_new_2 = np.arange(xtick_assert, xlim_scaled[1], dxticks)
#             xticks_new = np.append(xticks_new_1, xticks_new_2)
#             print xticks_new_1, xticks_new_2

#             if 'fig_ytick_round' in figdf:
#                 decimals = figdf.loc[axkey].fig_ytick_round.unique()[0]
#                 yticks_new = np.round(yticks_new, decimals=decimals)

#             if 'fig_xtick_round' in figdf:
#                 decimals = figdf.loc[axkey].fig_xtick_round.unique()[0]
#                 xticks_new = np.round(xticks_new, decimals=decimals)

#             if 'fig_xticks' in figdf:
#                 xticks_new = figdf.fig_xticks.values[0]
#             if 'fig_yticks' in figdf:
#                 yticks_new = figdf.fig_yticks.values[0]

#             if 'fig_set_xscale' in figdf:
#                 ax.set_xscale(figdf.fig_set_xscale.values[0])
#             print 'yticks_new',yticks_new
#             print yticks_new/yscale
#             print 'xticks_new',xticks_new

#             ax.set_yticks(yticks_new/yscale)
#             # ax.set_xticks(xticks_new/xscale)
#         return figures, axes

#     def _set_ticklabel_decimals(self, figures, axes, figdf, **kwargs):
#         '''
#         '''
#         print 'setting tick decimals'
#         for axkey, ax in axes.iteritems():
#             # get ticks
#             yticks = ax.get_yticks()
#             xticks = ax.get_xticks()
#             print 'yticks',yticks
#             # set tick decimal places
#             #---------------------------------------------------------------
#             if 'fig_ytick_decimals' in figdf:
#                 dec = figdf.loc[axkey].fig_ytick_decimals.unique()[0]
#                 yticklabels = [tick.get_text()for tick in ax.get_yticklabels()]
#                 print 'yticklabels',yticklabels
#                 # check if tick labels are numeric
#                 for label in yticklabels:
#                     try:
#                         label_float = type(float(label))==float
#                     except ValueError:
#                         label_float=False
#                 # if ticklabels are numeric, scale them, otherwise leave them
#                 if label_float:
#                     yticklabels = ['%.{}f'.format(dec) % float(tick) for tick in yticklabels]
#                 ax.set_yticklabels(yticklabels)
#                 # print yticks
#                 # print [tick.get_text() for tick in ax.get_yticklabels()]
#                 # yticklabels = ['%.{}f'.format(dec) % float(tick.get_text()) for tick in ax.get_yticklabels()]
#                 # ax.set_yticklabels(yticklabels)
#             if 'fig_xtick_decimals' in figdf:
#                 dec = figdf.loc[axkey].fig_xtick_decimals.unique()[0]
#                 xticklabels = [tick.get_text()for tick in ax.get_xticklabels()]
#                 # check if tick labels are numeric
#                 for label in xticklabels:
#                     try:
#                         label_float = type(float(label))==float
#                     except ValueError:
#                         label_float=False
#                 # if ticklabels are numeric, scale them, otherwise leave them
#                 if label_float:
#                     xticklabels = ['%.{}f'.format(dec) % float(tick) for tick in xticklabels]
#                 ax.set_xticklabels(xticklabels)
#         return figures, axes

#     def _scale_ticklabels(self, figures, axes, figdf, **kwargs):
#         '''
#         '''
#         print 'scaling axes'
#         for axkey, ax in axes.iteritems():
#             # get ticks
#             yticks = ax.get_yticks()
#             ax.set_yticklabels(yticks)
#             xticks = ax.get_xticks()
#             print 'yticks',yticks
#             #--------------------------------------
#             # yticks
#             #-------------------------------------
#             if 'fig_yscale' in figdf:
#                 print 'yscale factor found'
#                 yscale = figdf.loc[axkey].fig_yscale.values[0]
#             else:
#                 yscale=1
#             # apply scaling factor
#             yticks = yscale*yticks
#             print 'yticks',yticks
#             # get current ticklabels
#             yticklabels = [tick.get_text()for tick in ax.get_yticklabels()]
#             print 'yticklabels', yticklabels
#             # check if tick labels are numeric
#             for label in yticklabels:
#                 try:
#                     label_float = type(float(label))==float
#                 except ValueError:
#                     label_float=False
#             # if ticklabels are numeric, scale them, otherwise leave them alone
#             if label_float:
#                 # update tick decimal places
#                 #-----------------------------
#                 if 'fig_ytick_decimals' in figdf:
#                     # get decimal places
#                     dec = figdf.loc[axkey].fig_ytick_decimals.unique()[0]
#                     # get ticklabels with adjusted decimals
#                     yticklabels = ['%.{}f'.format(dec) % tick for tick in yticks]
#                 # set ticklabels
#                 print 'yticklabels', yticklabels
#                 ax.set_yticklabels(yticklabels)
#             #------------------------------------------
#             # xticks
#             #------------------------------------------
#             if 'fig_xscale' in figdf:
#                 # get scale factor
#                 xscale = figdf.loc[axkey].fig_xscale.values[0]
#             else:
#                 xscale=1
#             # scale ticklabels
#             xticks = xscale*xticks
#             xticklabels = [tick.get_text()for tick in ax.get_xticklabels()]
#             # check if tick labels are numeric
#             for label in xticklabels:
#                 try:
#                     label_float = type(float(label))==float
#                 except ValueError:
#                     label_float=False
#             # if ticklabels are numeric, scale them, otherwise leave them
#             if label_float:
#                 # update tick decimal places
#                 #----------------------------
#                 if 'fig_xtick_decimals' in figdf:
#                     # get decimal places
#                     dec = figdf.loc[axkey].fig_xtick_decimals.unique()[0]
#                     # get ticklabels with adjusted decimal places
#                     xticklabels = ['%.{}f'.format(dec) % tick for tick in xticks]
#                 # set ticklabels
#                 ax.set_xticklabels(xticklabels)

#         return figures, axes

#     def _set_fontsizes(self, figures, axes, figdf, **kwargs):
#         '''
#         '''
#         print 'setting axes properties'
#         # iterate through figures
#         for axkey, ax in axes.iteritems():
#             # set ticklabel fontweight and size
#             #-----------------------------------
#             print 'setting ticklabels'
#             # ytick labels
#             for label in ax.get_xticklabels():
#                 # fontweight
#                 label.set_fontweight(figdf.loc[axkey].fig_xtick_fontweight.values[0])
#                 # fonstize
#                 label.set_fontsize(figdf.loc[axkey].fig_xtick_fontsize.values[0])
#             # ytick labels
#             for label in ax.get_yticklabels():
#                 print 'yticklabel', label
#                 # fontweight
#                 label.set_fontweight(figdf.loc[axkey].fig_ytick_fontweight.values[0])
#                 # fontsize
#                 label.set_fontsize(figdf.loc[axkey].fig_ytick_fontsize.values[0])

#             # turn off axes box
#             #-----------------------------------
#             # turn off top and right axes lines
#             if all(figdf.loc[axkey].fig_boxoff):
#                 ax.spines['right'].set_visible(False)
#                 ax.spines['top'].set_visible(False)
#             # turn off all axes lines
#             if 'fig_axesoff' in figdf.keys() and all(figdf.loc[axkey].fig_axesoff):
#                 ax.set_axis_off()

#             # set axes linewidth and tick position
#             #--------------------------------------
#             ax.spines['left'].set_linewidth(figdf.loc[axkey].fig_axes_linewidth.unique()[0])
#             ax.spines['bottom'].set_linewidth(figdf.loc[axkey].fig_axes_linewidth.unique()[0])
#             ax.xaxis.set_ticks_position('bottom')
#             ax.yaxis.set_ticks_position('left')

#             # set axes labels
#             #----------------
#             ax.set_xlabel(figdf.loc[axkey].fig_xlabel.values[0], fontsize=figdf.loc[axkey]['fig_xlabel_fontsize'].values[0], fontweight=figdf.loc[axkey].fig_xlabel_fontweight.values[0])
#             ax.set_ylabel(figdf.loc[axkey].fig_ylabel.values[0], fontsize=figdf.loc[axkey]['fig_ylabel_fontsize'].values[0], fontweight=figdf.loc[axkey].fig_ylabel_fontweight.values[0])

#             # set tight layout
#             #-------------------
#             if all(figdf.loc[axkey].fig_tight_layout):
#                 plt.figure(figures[axkey].number)
#                 plt.tight_layout()

#         return figures, axes
#############################################################################
#
#############################################################################



# # def _trace_mean(df_sorted, figdf, variable, **kwargs):
#     '''FIXME add docs
#     '''
#     # FIXME add kwargs to alter figure details
#     # create figure groupings (all conditions that will go on the same figure)
#     fig={}
#     ax={}
#     n_subgroups={}
#     n_traces={}
#     xlim={}
#     ylim={}
#     # set figdf to hierarchical index (figure, subgroup, trace)
#     figdf = figdf.reset_index().set_index(['figure','subgroup','trace'])
#     # get list of all figure names
#     figures = figdf.index.get_level_values('figure').unique().values
#     # iterate over figures
#     for figkey in figures:
#         # create figure, passing params as **kwargs
#         fig[figkey], ax[figkey] = plt.subplots()
#         # get subgroups list
#         subgroups = figdf.loc[figkey].index.get_level_values('subgroup').unique().values
#         # subgroups = figdf[figdf.figure==figkey].subgroup.unique()
#         # number of subgroup in figure
#         n_subgroups[figkey] = len(subgroups) 
#         n_traces[figkey]={}
#         # iterate over subgroups of traces
#         for subkey in subgroups:
#             traces = figdf.loc[(figkey, subkey)].index.get_level_values('trace').unique().values
#             # FIXME distribute subgroup padrameters to each trace in the subgroup, with priority to trace parameters
#             n_traces[figkey][subkey]=len(traces)

#             # iterate over traces
#             for tracekey in traces:
#                 params = figdf.loc[(figkey,subkey, tracekey)]
#                 # get series from df sorted
#                 if tracekey in df_sorted:
#                     trace_series = df_sorted[tracekey][variable]
#                     # convert to array
#                     data_array = functions._2array(trace_series, remove_nans=True, remove_nans_axis=1)#*1000

#                     if 'fig_yscale' in figdf.loc[figkey]:
#                         print 'scaling y'
#                         yscale = figdf.loc[figkey].fig_yscale.unique()[0]
#                         data_array=data_array*yscale
#                     # change data units to percent
#                     if 'fig_topercent' in figdf.loc[figkey] and all(figdf.loc[figkey].fig_topercent):
#                         print 'converting to percent'
#                         data_array = 100.*(data_array-1)

#                     if data_array.shape[0]!=0:
#                         # scale y values
                        
#                         if len(data_array.shape)==1:
#                             # mean across slices
#                             data_mean = data_array
#                             #std across slices
#                             data_std = 0
#                             # sem across slices
#                             data_sem = 0
#                         else:
#                             # get stats
#                             # mean across slices
#                             data_mean = np.mean(data_array, axis=0)
#                             #std across slices
#                             data_std = np.std(data_array, axis=0)
#                             # sem across slices
#                             data_sem = stats.sem(data_array, axis=0)
#                         # time vector
#                         t = np.arange(len(data_mean))#
#                         # line plot with shaded error
#                         if figdf.loc[(figkey,subkey,tracekey)].error_style=='shade':
#                             ax[figkey].plot(t, data_mean, color=params.trace_color, linewidth=params.trace_linewidth)
#                             # print params.error_color
#                             plt.fill_between(t, data_mean-data_sem, data_mean+data_sem, color=params.error_color, alpha=params.error_alpha)
#                         # error bar plot
#                         elif figdf.loc[(figkey,subkey,tracekey)].error_style=='bar':
#                             ax[figkey].errorbar(t, data_mean, yerr=data_sem, color=params.trace_color, 
#                                 marker=params.trace_marker,  
#                                 markersize=params.markersize, 
#                                 elinewidth=params.error_linewidth, 
#                                 linewidth=params.trace_linewidth, 
#                                 markerfacecolor=params.trace_color, 
#                                 ecolor=params.error_color)
#         # get x and y limits based data
#         xlim[figkey] = ax[figkey].get_xlim()
#         ylim[figkey] = ax[figkey].get_ylim()

#     fig, ax = figsetup._format_figures(fig=fig, ax=ax, figdf=figdf, xlim=xlim, ylim=ylim)

#     plt.show(block=False)

#     return fig, ax
