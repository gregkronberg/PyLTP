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
import sys
sys.path.insert(0, 'F:\Google Drive\Work\GitHub\DCS-LTP-2')
import analysis

# use figsetup.LoadNSortDF to load data
# use figsetup.BuildFigDF to setup figure parameters
# use plots module to create plots

# directory and filename
#--------------------------
group_directory = 'Variables/'
figure_directory = 'Figures/'
dpi=350

# load sorted data
#-----------------------------
loadnsortdf =  figsetup.LoadNSortDF()
buildfigdf = figsetup.BuildFigDF()

# conditions to sort slices by
#--------------------------------------
conditions=['induction_pattern_0_slopes',
        'induction_pattern_other_0_slopes', 
        'induction_location_0_slopes', 
        'field_polarity_0_slopes',
        'field_mag_0_slopes']

# load group data
#----------------------------------------------
def _load_variables():
    # load and merge data for 1path and 2path experiments (includes asif and mahima data; can be sorted by 'experimenter' column)
    #--------------------------------------------------
    df_sorted, df_all = loadnsortdf._slopes_spikes_all(conditions=conditions)
    
    # get baseline io data
    #----------------------
    df_all = functions.ApplyDF()._get_io(df=df_all, max_idx_col='baseline_max_idx', colnames=['slopes', 'data_probe_hilbert_sum', 'area_probe_iir_band_5_50'], )
    df_all = functions.ApplyDF()._normalize_column(df=df_all, colnames=['data_ind_hilbert_smooth'], colnorm='data_probe_hilbert_sum_io_max' )
    df_all = functions.ApplyDF()._normalize_column(df=df_all, colnames=['slopes_ind'], colnorm='slopes_io_max' )
    df_all = functions.ApplyDF()._normalize_column(df=df_all, colnames=['area_ind_burst_iir_band_5_50'], colnorm='area_probe_iir_band_5_50_io_max' )

    # reset index
    #-------------------------------
    df_all=df_all.reset_index()
    return df_sorted, df_all

df_sorted, df_all  = _load_variables()
df_all_mahima = df_all[df_all.experimenter=='mahima']

#############################################################################
# dose response
#############################################################################
def _dose_response_mahima(df, buildfigdf):
    '''
    '''
    figdf = buildfigdf._dose_response_ltp_final_mahima()
    variable = 'ltp_final'
    figtype = '_'.join(['dose_response_mahima', variable, ''])
    # set axes labels
    #------------------
    figdf['fig_ylabel']='Norm. fEPSP slope'
    figdf['fig_xlabel']='Electric field (V/m)'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=-6
    figdf['fig_xmax']=21
    figdf['fig_dxticks']=5
    figdf['fig_ymin']=1.3
    figdf['fig_ymax']=1.81
    figdf['fig_dyticks']=.1
    figdf['fig_ytick_decimals']=1
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    drop=[]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # convert cathodal field magnitudes to negative values

    # set df_all index to match figdf
    #---------------------------------
    # df = df.reset_index()
    for index, row in df.iterrows():
        if row.field_polarity_0_slopes=='cathodal':
            if '-' not in row.field_mag_0_slopes:
                print row.field_mag_0_slopes
                df.at[index, 'field_mag_0_slopes']='-'+row.field_mag_0_slopes
    df=df.set_index(['field_polarity_0_slopes', 'field_mag_0_slopes'])
    # create plots
    #-------------------------------------------------
    array_funcs=[np.mean]
    array_func_kws=[{}]
    error_funcs=[stats.sem]
    error_func_kws=[{}]
    figs, ax = analysis.PlotFuncs()._var2var_func(df=df, figdf=figdf, x_variable='field_mag_0_slopes', variable='ltp_final', figformat='standard', array_funcs=array_funcs, array_func_kws=array_func_kws,
        error_funcs=error_funcs, error_func_kws=error_func_kws)

    # reset df_all index
    df=df.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)


_dose_response_mahima(df_all_mahima, buildfigdf)

#############################################################################
# dose response, show individual points
#############################################################################
def _dose_response_individual_points_mahima(df, buildfigdf):
    '''
    '''
    figdf = buildfigdf._dose_response_individual_points_mahima()
    variable = 'ltp_final'
    figtype = '_'.join(['dose_response_individual_points_mahima', variable, ''])
    # set axes labels
    #------------------
    figdf['fig_ylabel']='Norm. fEPSP slope'
    figdf['fig_xlabel']='Electric field (V/m)'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=-6
    figdf['fig_xmax']=21
    figdf['fig_dxticks']=5
    figdf['fig_ymin']=0.7
    figdf['fig_ymax']=2.31
    figdf['fig_dyticks']=.3
    figdf['fig_ytick_decimals']=1
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    drop=[]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # convert cathodal field magnitudes to negative values
    #--------------------------------------------

    # set df_all index to match figdf
    #---------------------------------
    # if type(df.index)!=pd.RangeIndex:
    #     print type(df.index)
    #     df = df.reset_index()
    for index, row in df.iterrows():
        if row.field_polarity_0_slopes=='cathodal':
            if '-' not in row.field_mag_0_slopes:
                print '-'+row.field_mag_0_slopes
                df.at[index, 'field_mag_0_slopes']='-'+row.field_mag_0_slopes
    df=df.set_index(['field_polarity_0_slopes',])

    # create plots
    #-------------------------------------------------
    # array functions
    array_funcs_x=[]
    array_func_kws_x=[{}]
    array_funcs_y=[]
    array_func_kws_y=[{}]

    variables = ['field_mag_0_slopes', 'ltp_final']
    # plot
    #--------------------------------------------------
    figs, axes = analysis.PlotFuncs()._var2var_corr(df=df, figdf=figdf, variables=variables, array_funcs_x=array_funcs_x,array_func_kws_x=array_func_kws_x,array_funcs_y=array_funcs_y,array_func_kws_y=array_func_kws_y)


    # reset df_all index
    df=df.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)


_dose_response_individual_points_mahima(df_all_mahima, buildfigdf)

#############################################################################
# dose response, show individual points and connect with same date
#############################################################################
def _dose_response_individual_points_mahima_connect(df, buildfigdf):
    '''
    '''
    figdf = buildfigdf._dose_response_individual_points_mahima_connect()
    variable = 'ltp_final'
    figtype = '_'.join(['dose_response_individual_points_mahima', variable, ''])
    # set axes labels
    #------------------
    figdf['fig_ylabel']='Norm. fEPSP slope'
    figdf['fig_xlabel']='Electric field (V/m)'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=-6
    figdf['fig_xmax']=21
    figdf['fig_dxticks']=5
    figdf['fig_ymin']=0.7
    figdf['fig_ymax']=2.31
    figdf['fig_dyticks']=.3
    figdf['fig_ytick_decimals']=1
    figdf['trace_markersize']=20
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    drop=[]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # convert cathodal field magnitudes to negative values
    #--------------------------------------------

    # set df_all index to match figdf
    #---------------------------------
    # if type(df.index)!=pd.RangeIndex:
    #     print type(df.index)
    #     df = df.reset_index()
    for index, row in df.iterrows():
        if row.field_polarity_0_slopes=='cathodal':
            if '-' not in row.field_mag_0_slopes:
                print '-'+row.field_mag_0_slopes
                df.at[index, 'field_mag_0_slopes']='-'+row.field_mag_0_slopes
    df=df.set_index(['field_polarity_0_slopes',])

    # create plots
    #-------------------------------------------------
    # array functions
    array_funcs_x=[]
    array_func_kws_x=[{}]
    array_funcs_y=[]
    array_func_kws_y=[{}]

    variables = ['field_mag_0_slopes', 'ltp_final']
    x_variable = 'field_mag_0_slopes'
    y_variable = 'ltp_final'
    connect_variable = 'date_slopes'
    # plot
    #--------------------------------------------------
    figs, axes = analysis.PlotFuncs()._var2var_corr_connect(df=df, figdf=figdf, x_variable=x_variable, y_variable=y_variable, connect_variable=connect_variable, array_funcs_x=array_funcs_x,array_func_kws_x=array_func_kws_x,array_funcs_y=array_funcs_y,array_func_kws_y=array_func_kws_y)


    # reset df_all index
    df=df.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)


_dose_response_individual_points_mahima_connect(df_all_mahima, buildfigdf)


#############################################################################
# spiking during induction
    
#############################################################################
# probe slopes over time
#############################################################################
def _slopes_probe_traces(df_all, buildfigdf):
    # variable to plot
    variable = 'slopes_norm_aligned_0'
    # filename prefix for saving figures
    figtype = 'slopes_probe_'

    figdf = buildfigdf._slopes_probe()
    # figdf['fig_ylim_all']=False
    # figdf['fig_ylabel_fontsize']=25
    # figdf['fig_xlabel_fontsize']=25
    figdf['fig_ylabel']='Norm. fEPSP slope'
    figdf['fig_xmax']=81
    figdf['fig_ymin']=0.9
    figdf['fig_ymax']=1.8
    # print figdf.index.values
    figdf.at[('weak unpaired',slice(None),slice(None)), 'fig_ymax']=2.61
    figdf.at[('strong unpaired',slice(None),slice(None)), 'fig_ymax']=2.41
    figdf.at[('paired',slice(None),slice(None)), 'fig_ymax']=2.61
    figdf.at[('apical TBS 1path ac 20 Vm',slice(None),slice(None)), 'fig_ymax']=2.01
    figdf.at[('apical TBS 1path 20 Vm',slice(None),slice(None)), 'fig_ymax']=1.71

    print figdf.fig_ymax

    df_all=df_all.reset_index().set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ])
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable, df_sorted=df_sorted)
    df_all=df_all.reset_index()

    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
# _slopes_probe_traces(df_all, buildfigdf)

#############################################################################
# slopes, burst area, spikes traces during induction
#############################################################################
# slopes
#========================================================================
def _induction_slopes(df_all, buildfigdf):
    
    figdf = buildfigdf._induction_variables()
    variable = 'slopes_ind_norm'
    figtype = '_'.join(['ind_trace', variable, ''])
    # set axes labels
    #------------------
    if 'norm' in variable:
        figdf['fig_ylabel']='Norm. fEPSP slope'
    else:
        figdf['fig_ylabel']='fEPSP slope (V/s)'
    figdf['fig_xlabel']='Pulses'

    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=0
    figdf['fig_xmax']=61
    figdf['fig_ymin']=-0.21
    figdf['fig_ymax']=1.21
    figdf['fig_ylim_all']=False
    figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    figdf['fig_dyticks']=.2
    figdf['fig_dxticks']=10
    # drop figdf values
    drop = ['fig_nyticks',]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # update figdf for specific trace conditions
    #------------------------------------
    figdf = figdf.reset_index().set_index('trace')
    # change xlims for weak5hz
    i = figdf.index.str[0]=='weak5Hz'
    figdf.loc[i, 'fig_xmax']=15
    figdf.loc[i, 'fig_dxticks']=5
    # change ylims for apical
    i = figdf.index.str[2]=='apical'
    figdf.loc[i, 'fig_ymax']=1
    # reset index
    figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # set df_all index to match figdf
    #---------------------------------
    df_all=df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ])

    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)

    # reset df_all index
    df_all=df_all.reset_index()

     # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# _induction_slopes(df_all, buildfigdf)
# area
#========================================================================
def _induction_area(df_all, buildfigdf):
    figdf = buildfigdf._induction_variables()
    variable = 'area_ind_burst_iir_band_5_50_norm'
    figtype = '_'.join(['ind_trace', variable, ''])
    # set axes labels
    #------------------
    if 'norm' in variable:
        figdf['fig_ylabel']='Norm. burst area'
    else:
        figdf['fig_ylabel']='Burst area (mv*us)'
    figdf['fig_ylabel_fontsize']=25
    figdf['fig_xlabel_fontsize']=25
    figdf['fig_xlabel']='Bursts'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=0
    figdf['fig_xmax']=16
    figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=2.
    figdf['fig_xtick_assert']=0.
    figdf['fig_nyticks']=5
    figdf['fig_dyticks']=4.
    figdf['fig_ymin']=4.
    figdf['fig_ymax']=18.
    figdf['fig_ytick_round']=1
    figdf['fig_dxticks']=5
    drop = []
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    figdf = figdf.reset_index().set_index('trace')
    i = figdf.index.str[0]=='weak5Hz'
    figdf.loc[i, 'fig_xmax']=15
    figdf.loc[i, 'fig_dxticks']=5
    figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # set df_all index to match figdf
    #---------------------------------
    df_all=df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ])

    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    # reset df_all index
    df_all=df_all.reset_index()
     # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# _induction_area(df_all, buildfigdf)

# spikes firstpulse normalized
#========================================================================
def _induction_spikes_firstpulse_norm(df_all, buildfigdf):
    figdf = buildfigdf._induction_variables()
    variable = 'data_ind_hilbert_sum_firstpulse_norm'
    figtype = '_'.join(['ind_trace', variable, ''])
    # set axes labels
    #------------------
    if 'norm' in variable:
        figdf['fig_ylabel']='Norm. pop. spike'
    else:
        figdf['fig_ylabel']='High frequency power (mv^2)'
    figdf['fig_ylabel_fontsize']=25
    figdf['fig_xlabel_fontsize']=25
    figdf['fig_xlabel']='Bursts'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=0
    figdf['fig_xmax']=16
    figdf['fig_ylim_all']=False
    figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    figdf['fig_nyticks']=5
    figdf['fig_ytick_round']=1
    figdf['fig_dxticks']=5
    # figdf['fig_dyticks']=.5
    drop = []
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    figdf = figdf.reset_index().set_index('trace')
    i = figdf.index.str[0]=='weak5Hz'
    figdf.loc[i, 'fig_xmax']=15
    figdf.loc[i, 'fig_dxticks']=5
    i = figdf.index.str[2]=='apical'
    figdf.loc[i, 'fig_xmax']=16
    figdf.loc[i, 'fig_dxticks']=5
    figdf.loc[i, 'fig_ymin']=0.4
    figdf.loc[i, 'fig_ymax']=2.01
    figdf.loc[i, 'fig_dyticks']=.5
    i = figdf.index.str[2]=='basal'
    figdf.loc[i, 'fig_xmax']=16
    figdf.loc[i, 'fig_dxticks']=5
    figdf.loc[i, 'fig_ymin']=0.8
    figdf.loc[i, 'fig_ymax']=6.01
    figdf.loc[i, 'fig_dyticks']=1.
    figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # set df_all index to match figdf
    #---------------------------------
    df_all=df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ])
    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    # reset df_all index
    df_all=df_all.reset_index()

    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# spikes all normalized
#========================================================================
def _induction_spikes_norm(df_all, buildfigdf):
    figdf = buildfigdf._induction_variables()
    variable = 'data_ind_hilbert_sum_norm'
    figtype = '_'.join(['ind_trace', variable, ''])
    conditions = ['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ]
    # set axes labels
    #------------------
    if 'norm' in variable:
        figdf['fig_ylabel']='Norm. pop. spike'
    else:
        figdf['fig_ylabel']='High frequency power (mv^2)'
    figdf['fig_ylabel_fontsize']=25
    figdf['fig_xlabel_fontsize']=25
    figdf['fig_xlabel']='Bursts'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=0
    figdf['fig_xmax']=61
    figdf['fig_ylim_all']=False
    figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    figdf['fig_nyticks']=5
    figdf['fig_ytick_round']=1
    figdf['fig_dxticks']=10
    figdf['fig_xlabel']='Pulses'
    # figdf['fig_dyticks']=.5
    drop = []
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    figdf = figdf.reset_index().set_index('trace')
    i = figdf.index.str[0]=='weak5Hz'
    figdf.loc[i, 'fig_xmax']=15
    figdf.loc[i, 'fig_dxticks']=5
    i = figdf.index.str[2]=='apical'
    figdf.loc[i, 'fig_xmax']=61
    figdf.loc[i, 'fig_dxticks']=10
    figdf.loc[i, 'fig_ymin']=0.4
    figdf.loc[i, 'fig_ymax']=2.01
    figdf.loc[i, 'fig_dyticks']=.5
    i = figdf.index.str[2]=='basal'
    figdf.loc[i, 'fig_xmax']=61
    figdf.loc[i, 'fig_dxticks']=10
    figdf.loc[i, 'fig_ymin']=0.4
    figdf.loc[i, 'fig_ymax']=5.01
    figdf.loc[i, 'fig_dyticks']=1.
    figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # set df_all index to match figdf
    #---------------------------------
    df_all=df_all.set_index(conditions)
    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    # reset df_all index
    df_all=df_all.reset_index()

    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

    # stats
    #-------------------------------------------------------
    stats_dict=functions._build_ttest_dict(df=df_all, figdf=figdf, variable='data_ind_hilbert_sum_firstpulse_norm_mean', conditions=conditions)

    stats_df = functions._build_timeseries_anova_df(df_all, array_column=variable, columns=conditions)

    return stats_dict, stats_df

# stats_dict, stats_df = _induction_spikes_norm(df_all, buildfigdf)
# spikes center of mass
#========================================================================
def _induction_spikes_centerofmass(df_all, buildfigdf):
    figdf = buildfigdf._induction_variables()
    variable = 'data_ind_hilbert_com'
    figtype = '_'.join(['ind_trace', variable, ''])
    # set axes labels
    #------------------
    figdf['fig_ylabel']='Spike time (ms)'
    figdf['fig_xlabel']='Bursts'
    # axes ticks and lims
    #---------------------
    # figdf['fig_xmin']=0
    # figdf['fig_xmax']=60
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    figdf['fig_nyticks']=5
    figdf['fig_dxticks']=5
    figdf['fig_dyticks']=2
    figdf['fig_ylim_all']=False

    # figdf['fig_ytick_round']=1
    # figdf['fig_dxticks']=5
    drop = ['fig_ymin',]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    # figdf = figdf.reset_index().set_index('trace')
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=15
    # figdf.loc[i, 'fig_dxticks']=5
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # set df_all index to match figdf
    #---------------------------------
    df_all=df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes', 'field_polarity_0_slopes','field_mag_0_slopes' ])
    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    # reset df_all index
    df_all=df_all.reset_index()
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# _induction_spikes_centerofmass(df_all, buildfigdf)

# fft of induction spikes
#========================================================================
run_figs=False
if run_figs:
    figdf = buildfigdf._induction_variables()
    variable = 'data_ind_hilbert_sum_norm_fft_angle'
    figtype = '_'.join(['ind_trace', variable, ''])
    # set axes labels
    #------------------
    if 'norm' in variable:
        figdf['fig_ylabel']='Normalized high frequency power'
    else:
        figdf['fig_ylabel']='High frequency power (mv^2)'
    figdf['fig_xlabel']='Bursts'
    # axes ticks and lims
    #---------------------
    figdf['fig_xmin']=0
    figdf['fig_xmax']=60
    figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    figdf['fig_xtick_assert']=0.
    figdf['fig_nyticks']=5
    figdf['fig_ytick_round']=1
    figdf['fig_dxticks']=5
    drop = ['fig_ymin', 'fig_dyticks',]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    figdf = figdf.reset_index().set_index('trace')
    i = figdf.index.str[0]=='weak5Hz'
    figdf.loc[i, 'fig_xmax']=15
    figdf.loc[i, 'fig_dxticks']=5
    figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])
    # create plots
    #-------------------------------------------------
    figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
#############################################################################
# correlations between induction variables
#############################################################################
run_ind_corr=False
if run_ind_corr:
    # loadnsortdf =  figsetup.LoadNSortDF()
    # buildfigdf = figsetup.BuildFigDF()
    # df_sorted, df_all = loadnsortdf._slopes_spikes_all()
    figdf = buildfigdf._var2var_corr_all()

    # df_sorted, figdf = lns._slopes_spikes(paths= ['1path', '2path'], figdf_funcs=[figsetup.BuildFigDF()._var2var_corr,figsetup.BuildFigDF()._var2var_corr])
    # # print df_sorted.keys()anal

    # paths=[ '2path']
    variable_pairs =[
    # ('data_ind_hilbert_sum_firstpulse_mean_regressout_data_probe_hilbert_sum_baseline_mean','ltp_final_regressout_data_probe_hilbert_sum_baseline_mean'),
    # ('data_ind_hilbert_sum_norm_fft_angle','ltp_final'),
    # ('data_ind_hilbert_sum_secondpulse_norm_mean','ltp_final'),
    ('data_ind_hilbert_com','ltp_final'),
    # ('data_probe_hilbert_sum_baseline_mean','data_ind_hilbert_sum_firstpulse'),
    # ('data_probe_hilbert_sum_baseline_mean','ltp_final'),

    # ('area_ind_burst_iir_band_5_50_norm_mean','ltp_final'),
    # ('area_ind_burst_iir_band_5_50_smooth','ltp_final'),
    # ('area_ind_burst_iir_band_5_50_smooth','data_ind_hilbert_sum_firstpulse'),
    # ('area_ind_burst_iir_band_5_50_norm','data_ind_hilbert_sum_firstpulse_norm'),
    ]

    # # which burst to show inplot
    # burstns = ['first', 'last', 'mean']
    burstns=['mean']#['last','mean']

    # for path in df_sorted:
    for variable_pair in variable_pairs:
        for burstn in burstns:

            figtype='_'.join(['corr', variable_pair[0], variable_pair[1], str(burstn)])+'_'

            # array functions to pass to _bar method
            #--------------------------------------
            if burstn == 'first':
                array_func = plots.ArrayFunctions()._slice
                array_func_kw={'islice':0, 'axis':1}
            if burstn == 'last':
                array_func = plots.ArrayFunctions()._slice
                array_func_kw={'islice':-1, 'axis':1}
            if burstn == 'mean':
                array_func = plots.ArrayFunctions()._slice_mean
                array_func_kw={'islice':slice(None), 'axis':1}
            if type(burstn)==int:
                array_func = plots.ArrayFunctions()._slice
                array_func_kw={'islice':burstn, 'axis':1}
            if type(burstn)==slice:
                array_func = plots.ArrayFunctions()._slice_mean
                array_func_kw={'islice':burstn, 'axis':1}

            array_funcs_x = [array_func, np.abs,]
            array_func_kws_x = [array_func_kw, {}]
            # array_funcs_y = [array_func, np.abs]
            # array_func_kws_y = [array_func_kw, {}]
            # array_funcs_x = []
            # array_func_kws_x = []
            array_funcs_y = []
            array_func_kws_y = []

            # colregress = 'data_probe_hilbert_sum_baseline_mean'
            # colname1 = 'data_ind_hilbert_sum_firstpulse_mean'
            # colname2 = 'ltp_final'
            # # pass df functions to remove outliers
            # df_funcs = [plots.FrameFunctions()._regress_out]
            # df_func_kws = [{'colregress':colregress,'colnames':[colname1, colname2],}]

            # remove outliers
            # colname1 = 'data_ind_hilbert_sum_firstpulse_mean'
            # # pass df functions to remove outliers
            # df_funcs = [plots.FrameFunctions()._remove_outliers]
            # df_func_kws = [{'colnames':[colname1],'z_tol':2}]

            df_funcs=[]
            df_func_kws=[]

            # update figure aesthetics
            figdf['trace_markersize']=10
            figdf['fig_xlabel']='high frequency power'#variable_pair[0]
            figdf['fig_ylabel']='ltp_final'#variable_pair[1]
            figdf['fig_nyticks']=5
            figdf['fig_nxticks']=5
            figdf['fig_show_corrcoef']=True

            drop = ['fig_ymin', 'fig_dxticks','fig_xlim_all']
            for val in drop:
                if val in figdf:
                    figdf.drop(val, axis=1, inplace=True)
            # plot
            #-------------------------------------------------
            figs, axes = plots._var2var_corr(
                df_sorted=df_sorted, 
                figdf=figdf, 
                variables=variable_pair, 
                array_funcs_x=array_funcs_x, 
                array_func_kws_x=array_func_kws_x, 
                array_funcs_y=array_funcs_y, 
                array_func_kws_y=array_func_kws_y,
                df_funcs=df_funcs,
                df_func_kws=df_func_kws)
            # figs, axes = plots._bar(df_sorted=df_sorted[path], figdf=figdf[path], variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
            # save figures
            #--------------------------------------------------
            for fig_key, fig in figs.iteritems():
                fname = figure_directory+figtype+str(fig_key)+'.png'
                fig.savefig(fname, format='png', dpi=dpi)
#############################################################################
# histograms during induction
#############################################################################
run_figs=False
if run_figs:
    
    figdf = buildfigdf._induction_variables()
    variable = 'data_ind_hilbert_smooth_norm_data_probe_hilbert_sum_io_max'
    figtype = '_'.join(['hist', variable, ''])
    array_func = plots.ArrayFunctions()._slice
    array_func_kw={'islice':slice(0,None, 4), 'axis':1}
    array_funcs=[array_func]
    array_func_kws=[array_func_kw]
    figs, axes = plots._hist(df=df_all, figdf=figdf, variable=variable, array_funcs=array_funcs, array_func_kws=array_func_kws)
    # # set axes labels
    # #------------------
    # if 'norm' in variable:
    #     figdf['fig_ylabel']='Normalized fEPSP slope'
    # else:
    #     figdf['fig_ylabel']='fEPSP slope (V/s)'
    # figdf['fig_xlabel']='Pulses'

    # # axes ticks and lims
    # #---------------------
    # figdf['fig_xmin']=0
    # figdf['fig_xmax']=60
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    # figdf['fig_xtick_assert']=0.
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=10
    # drop = ['fig_ymin', 'fig_nyticks',]
    # for val in drop:
    #     if val in figdf:
    #         figdf.drop(val, axis=1, inplace=True)

    # # upate values for weak5Hz induction
    # #------------------------------------
    # figdf = figdf.reset_index().set_index('trace')
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=15
    # figdf.loc[i, 'fig_dxticks']=5
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # # create plots
    # #-------------------------------------------------
    # figs, axes = plots._trace_mean(df=df_all, figdf=figdf, variable=variable,)
    #  # save
    # #--------------------------------------------------
    # for fig_key, fig in figs.iteritems():
    #     fname = figure_directory+figtype+str(fig_key)+'.png'
    #     fig.savefig(fname, format='png', dpi=dpi)
#############################################################################
# input/output curves
#############################################################################
def _baseline_input_output(df_all=df_all, buildfigdf=buildfigdf):
    '''
    '''
    # prefix for saving figure
    #-----------------------------
    figtype='baseline_input_output_'
    # create figdf
    #--------------------
    figdf = buildfigdf._baseline_input_output()
    # upodate figdf
    #------------------------
    figdf['fig_ymin']=0
    figdf['fig_xmin']=0
    figdf['fig_ymax']=1.08
    figdf['fig_xmax']=1.08
    figdf['fig_dyticks']=.2
    figdf['fig_dxticks']=.2
    figdf['fig_ytick_decimals']=1
    figdf['fig_xtick_decimals']=1
    figdf['fig_ylabel']='Norm. pop spike'
    figdf['fig_xlabel']='Norm. fEPSP slope'
    # variables to plot
    #-----------------------
    variables = ['slopes_io_norm', 'data_probe_hilbert_sum_io_norm']
    # array functions
    #------------------------------------------
    array_funcs_x = [analysis.ArrayFunctions()._flatten]
    array_funcs_y = [analysis.ArrayFunctions()._flatten]
    array_func_kws_x = [{}]
    array_func_kws_y = [{}]
    # update df index
    #------------------------
    df_all=df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes', 'induction_location_0_slopes','field_polarity_0_slopes', 'field_mag_0_slopes' ])
    # plot
    #--------------------------------------------------
    figs, axes = analysis.PlotFuncs()._var2var_corr(df=df_all, figdf=figdf, variables=variables, array_funcs_x=array_funcs_x,array_func_kws_x=array_func_kws_x,array_funcs_y=array_funcs_y,array_func_kws_y=array_func_kws_y)
    # draw rectangle to indicate where baseline is chosen
    #------------------------------------------------------
    figs, axes = analysis.PlotFuncs()._draw_rectangle(fig=figs, ax=axes, figdf=figdf)
    # reset index
    #----------------------------
    df_all=df_all.reset_index()
    # save figure
    #------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# _baseline_input_output()
#############################################################################
# cca with burst area and spikes
#############################################################################
run_figs=False
if run_figs:
    # loadnsortdf =  figsetup.LoadNSortDF()
    # buildfigdf = figsetup.BuildFigDF()
    # df_sorted, df_all = loadnsortdf._slopes_spikes_all()
    figdf = buildfigdf._var2var_corr_all()

    # x_variables = ['data_ind_hilbert_sum_firstpulse_norm_lastburst', 'area_ind_burst_iir_band_5_50_norm_mean','data_ind_hilbert_sum_secondpulse_norm_mean','data_ind_hilbert_sum_norm_fft_angle_13th']
    # x_variables = ['data_ind_hilbert_sum_firstpulse_norm_lastburst', 'data_ind_hilbert_sum_secondpulse_norm_mean','data_ind_hilbert_sum_norm_fft_angle_13th','area_ind_burst_iir_band_5_50_norm_mean'
    # ]
    x_variables = ['area_ind_burst_iir_band_5_50_norm_mean', 'data_ind_hilbert_sum_allpulse_norm_mean',]# 'data_ind_hilbert_sum_allpulse_norm_firstburst',]#'data_ind_hilbert_sum_norm_fft_angle_13th']#'data_ind_hilbert_sum_firstpulse_norm_lastburst']#'data_ind_hilbert_sum_norm_fft_angle_13th','area_ind_burst_iir_band_5_50_norm_mean']
    # x_variables = ['data_ind_hilbert_sum_allpulse_norm_lastburst',]#'data_ind_hilbert_sum_norm_fft_angle_13th','area_ind_burst_iir_band_5_50_norm_mean']
    y_variables = ['ltp_final']

    figtypekeys = ['cca']+x_variables
    figtype='_'.join(figtypekeys)+'_'

    figdf['fig_show_corrcoef']=True
    figdf['fig_xlabel']='CCA transform'
    figdf['fig_ylabel']='LTP'
    figdf['trace_markersize']=25

    figdf = figdf.reset_index().set_index('trace')
     # upate values for weak5Hz induction
    #------------------------------------
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=2
    # figdf.loc[i, 'fig_xmin']=-1

    # i_basal = figdf.index.str[2]=='basal'
    # figdf.loc[i_basal, 'fig_xmax']=1
    # figdf.loc[i_basal, 'fig_xmin']=-1
    # figdf.loc[i_basal, 'fig_ymin']=-2

    # i_apical = figdf.index.str[2]=='apical'
    # figdf.loc[i_apical, 'fig_xmax']=4
    # figdf.loc[i_apical, 'fig_xmin']=-1
    # figdf.loc[i_apical, 'fig_ymin']=-2

    figs, axes = plots._cca(df_sorted=df_sorted, figdf=figdf, x_variables=x_variables, y_variables=y_variables)

    
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # save figures
            #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
#############################################################################
# bar plots during induction
#############################################################################
# epsp area (last burst)
#-------------------------------
def _bar_epsp_area_1path_last(df_all, buildfigdf):
    path='1path'
    figdf = buildfigdf._induction_bar(path=path)
    variable = 'area_ind_burst_iir_band_5_50_norm'
    figtype = '_'.join(['ind_bar_last', variable, ''])
    # set axes labels
    #------------------
    # if 'norm' in variable:
    #     figdf['fig_ylabel']='Normalized fEPSP slope'
    # else:
    #     figdf['fig_ylabel']='fEPSP slope (V/s)'
    # figdf['fig_xlabel']='Pulses'

    # # axes ticks and lims
    # #---------------------
    figdf['fig_ylabel']='Norm. burst area'
    figdf['fig_ymin']=4
    figdf['fig_ymax']=14
    figdf['fig_dyticks']=2
    figdf['fig_ytick_decimals']=0
    # figdf['fig_xmax']=60
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    # figdf['fig_xtick_assert']=0.
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=10
    # drop = ['fig_ymin', 'fig_nyticks',]
    # for val in drop:
    #     if val in figdf:
    #         figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    # figdf = figdf.reset_index().set_index('trace')
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=15
    # figdf.loc[i, 'fig_dxticks']=5
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # array functions
    #------------------------------------
    arrayfuncs = [plots.ArrayFunctions()._last]
    arrayfunckws = [{}]

    # ensure that df indices match figdf
    #------------------------------------
    # df_all = df_all.set_index(['field_polarity_0_slopes', 'induction_location_0_slopes', 'field_mag_0_slopes'])
    # df_all=df_all.reset_index()
    df_all = df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes','induction_location_0_slopes','field_polarity_0_slopes' , 'field_mag_0_slopes'])
    # create plots
    #-------------------------------------------------
    figs, axes = plots.PlotFuncs()._bar(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # reset index
    #-------------------
    df_all = df_all.reset_index()
     # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
# _bar_epsp_area_1path_last(df_all, buildfigdf)

# hilbert spikes firstpulse (last burst)
#-------------------------------
def _bar_spikes_1path_last(df_all, buildfigdf):
    path='1path'
    figdf = buildfigdf._induction_bar(path=path)
    variable = 'data_ind_hilbert_sum_firstpulse_norm'
    figtype = '_'.join(['ind_bar_last', variable, ''])
    # set axes labels
    #------------------
    # if 'norm' in variable:
    #     figdf['fig_ylabel']='Normalized fEPSP slope'
    # else:
    #     figdf['fig_ylabel']='fEPSP slope (V/s)'
    # figdf['fig_xlabel']='Pulses'

    # # axes ticks and lims
    # #---------------------
    figdf['fig_ylabel']='Norm. pop spike'
    figdf['fig_ymin']=0.5
    figdf['fig_ymax']=2.
    figdf['fig_dyticks']=.5
    figdf['fig_ytick_decimals']=1
    for key in figdf.index.values:
        if 'basal' in key[0]:
            figdf.at[key, 'fig_ymin']=.5
            figdf.at[key, 'fig_ymax']=5.2
            figdf.at[key, 'fig_dyticks']=.5
    # figdf['fig_ylim_all']=False
    # figdf['fig_ytick_assert']=1.
    # figdf['fig_xtick_assert']=0.
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=10
    # drop = ['fig_ymin', 'fig_nyticks',]
    # for val in drop:
    #     if val in figdf:
    #         figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    # figdf = figdf.reset_index().set_index('trace')
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=15
    # figdf.loc[i, 'fig_dxticks']=5
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # array functions
    #------------------------------------
    arrayfuncs = [plots.ArrayFunctions()._last]
    arrayfunckws = [{}]

    # ensure that df indices match figdf
    #------------------------------------
    df_all = df_all.set_index(['name'])
    # df_all.at['20170616_1_TBS_anodal_20Vm_basal_none_rig1','data_ind_hilbert_sum_firstpulse_norm']=np.nan
    df_all=df_all.reset_index()
    # df_all = df_all.reset_index()
    # df_all = df_all.set_index(['field_polarity_0_slopes', 'induction_location_0_slopes', 'field_mag_0_slopes'])
    df_all = df_all.set_index(['induction_pattern_0_slopes','induction_pattern_other_0_slopes','induction_location_0_slopes','field_polarity_0_slopes' , 'field_mag_0_slopes'])
    # create plots
    #-------------------------------------------------
    figs, axes = plots.PlotFuncs()._bar(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # figs, axes = plots.PlotFuncs()._bar_with_points(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # reset index
    #-------------------
    df_all = df_all.reset_index()
     # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
# _bar_spikes_1path_last(df_all, buildfigdf)

# ltp final
#--------------------------------
def _ltp_final(df_all=df_all, buildfigdf=buildfigdf):
    '''
    '''
    path='1path'
    figdf = buildfigdf._induction_bar(path=path)
    variable = 'ltp_final'
    figtype = '_'.join(['ltp_final', variable, ''])

    # array functions
    #------------------------------------
    arrayfuncs = []#[plots.ArrayFunctions()._last]
    arrayfunckws = []#[{}]

    df_all=df_all.set_index(['field_polarity_0_slopes', 'induction_pattern_0_slopes', 'induction_pattern_other_0_slopes' ])

    figs, axes = analysis.PlotFuncs()._bar(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
# _ltp_final()

# ltp final
#--------------------------------
def _ltp_final_1path(df_all=df_all, buildfigdf=buildfigdf):
    '''
    '''
    path='1path'
    figdf = buildfigdf._induction_bar(path=path)
    variable = 'ltp_final'
    figtype = '_'.join(['ltp_final', variable, ''])

    # array functions
    #------------------------------------
    arrayfuncs = []#[plots.ArrayFunctions()._last]
    arrayfunckws = []#[{}]

    for key in figdf.index.values:
        if 'basal' in key[0]:
            print key
            figdf.at[key, 'fig_ymin']=1.3
            print figdf.at[key, 'fig_ymin']
            figdf.at[key, 'fig_ymax']=1.91
            figdf.at[key, 'fig_dyticks']=.1

    print figdf.fig_ymax
    df_all=df_all.set_index(['induction_pattern_0_slopes', 'induction_pattern_other_0_slopes','induction_location_0_slopes', 'field_polarity_0_slopes', 'field_mag_0_slopes',  ])

    figs, axes = analysis.PlotFuncs()._bar(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)
# _ltp_final_1path()

# ltp final
#-------------------------------
def _ltp_final_2path(df_all, buildfigdf):

    path='2path'
    figdf = buildfigdf._ltp_bar_2path_2()
    variable = 'ltp_final'
    figtype = '_'.join(['ltp_final', variable, ''])
    # set axes labels
    #------------------
    # if 'norm' in variable:
    #     figdf['fig_ylabel']='Normalized fEPSP slope'
    # else:
    #     figdf['fig_ylabel']='fEPSP slope (V/s)'
    # figdf['fig_xlabel']='Pulses'

    # # axes ticks and lims
    # #---------------------
    figdf['fig_ylabel']='Norm. fEPSP slope'
    figdf['fig_ymin']=.95
    # figdf['fig_dyticks']=.5
    figdf['fig_ytick_decimals']=1
    # figdf['fig_xmax']=60
    # figdf['fig_ylim_all']=False
    figdf['fig_ytick_assert']=1.
    # figdf['fig_xtick_assert']=0.
    # figdf['fig_dyticks']=.2
    # figdf['fig_dxticks']=10
    drop = ['fig_ymax',]
    for val in drop:
        if val in figdf:
            figdf.drop(val, axis=1, inplace=True)

    # upate values for weak5Hz induction
    #------------------------------------
    # figdf = figdf.reset_index().set_index('trace')
    # i = figdf.index.str[0]=='weak5Hz'
    # figdf.loc[i, 'fig_xmax']=15
    # figdf.loc[i, 'fig_dxticks']=5
    # figdf=figdf.reset_index().set_index(['figure','subgroup','trace'])

    # array functions
    #------------------------------------
    arrayfuncs = []#[plots.ArrayFunctions()._last]
    arrayfunckws = []#[{}]

    # ensure that df indices match figdf
    #------------------------------------
    df_all = df_all.reset_index().set_index(['field_polarity_0_slopes','induction_pattern_0_slopes', 'induction_pattern_other_0_slopes',])
    # create plots
    #-------------------------------------------------
    figs, axes = plots.PlotFuncs()._bar(df=df_all, figdf=figdf, variable=variable, array_funcs=arrayfuncs, array_func_kws=arrayfunckws)
    # reset index
    #-------------------
    # df_all = df_all.reset_index()
     # save
    #--------------------------------------------------
    for fig_key, fig in figs.iteritems():
        fname = figure_directory+figtype+str(fig_key)+'.png'
        fig.savefig(fname, format='png', dpi=dpi)

# _ltp_final_2path(df_all, buildfigdf)
