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

# directory and filename
group_directory = 'Variables/'
figure_directory = 'Figures/'
dpi=350

#============================================================================
# load two pathway data
#============================================================================
filename_spikes = 'spikes_df.pkl'
filename_slopes = 'slopes_df.pkl'
df_slopes = pd.read_pickle(group_directory+filename_slopes)
# load group data class object
df_spikes=pd.read_pickle(group_directory+filename_spikes)

df_merged = pd.merge(df_slopes, df_spikes, on=['name','path'], how='left', suffixes=['_slopes','_spikes'])

df_sorted = figsetup._sortdf_2path_spikes(df=df_merged)

#============================================================================
# load one path data
#============================================================================
filename_spikes_1path = 'spikes_df_1path.pkl'
filename_slopes_1path = 'slopes_df_1path.pkl'
df_slopes_1path = pd.read_pickle(group_directory+filename_slopes_1path)
# load group data class object
df_spikes_1path=pd.read_pickle(group_directory+filename_spikes_1path)

df_merged_1path = pd.merge(df_slopes_1path, df_spikes_1path, on=['name','path'], how='left', suffixes=['_slopes','_spikes'])

df_sorted_1path = figsetup._sortdf_1path_spikes(df=df_merged_1path)

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_2path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_'
# variable = 'data_ind_hilbert_sum_firstpulse_lastburst'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar, ttests = plots._bar(df_sorted=df_sorted, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_2path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_norm_'
# variable = 'data_ind_hilbert_sum_firstpulse_norm_lastburst'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar, ttests = plots._bar(df_sorted=df_sorted, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# setup df of figure parameters
#------------------------------
figdf_bar = figsetup._var2var_corr_1path()
figdf_bar.drop('fig_ymin', inplace=True, axis=1)
figdf_bar.drop('fig_xmin', inplace=True, axis=1)
figdf_bar['fig_xscale']=1000.
figdf_bar['trace_markersize']=30
figdf_bar['fig_xtick_decimals']=1
figdf_bar['fig_ytick_decimals']=1
figdf_bar['fig_xlim_all']=False
figdf_bar['fig_xmin']=0.
figdf_bar['fig_ylim_all']=False
figdf_bar.drop('fig_dyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_dxticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nxticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
figdf_bar['fig_ylabel']='% LTP'
figdf_bar['fig_xlabel']='Population spike (mV*us)'

figtype = 'corr_spikes_ind_firtpulse_lastburst_X_ltp_final_'
variables = ['data_ind_hilbert_sum_secondpulse_mean', 'ltp_final']
# plot and show
#-------------------------------------
figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted_1path, figdf=figdf_bar, variables=variables)

# save figures
#-----------------
for fig_key, fig in figs_bar.iteritems():
    fname = figure_directory+figtype+str(fig_key)+'.png'
    fig.savefig(fname, format='png', dpi=dpi)

figdf_bar = figsetup._var2var_corr_1path()
figdf_bar.drop('fig_ymin', inplace=True, axis=1)
figdf_bar.drop('fig_xmin', inplace=True, axis=1)
figdf_bar['fig_xscale']=1000.
figdf_bar['trace_markersize']=30
figdf_bar['fig_xtick_decimals']=1
figdf_bar['fig_ytick_decimals']=1
figdf_bar['fig_xlim_all']=False
figdf_bar['fig_xmin']=0.
figdf_bar['fig_ylim_all']=False
figdf_bar.drop('fig_dyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_dxticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nxticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
figdf_bar['fig_ylabel']='% LTP'
figdf_bar['fig_xlabel']='Population spike (mV*us)'

figtype = 'corr_spikes_ind_firtpulse_lastburst_X_ltp_final_'
variables = ['area_ind_burst_iir_band_5_50_mean', 'ltp_final']
# plot and show
#-------------------------------------
figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted_1path, figdf=figdf_bar, variables=variables)

# save figures
#-----------------
for fig_key, fig in figs_bar.iteritems():
    fname = figure_directory+figtype+str(fig_key)+'.png'
    fig.savefig(fname, format='png', dpi=dpi)


#============================================================================
# # induction area bar plots 2 path
# #============================================================================
# setup df of figure parameters
#------------------------------
figdf_bar = figsetup._var2var_corr_2path()
figdf_bar.drop('fig_ymin', inplace=True, axis=1)
figdf_bar.drop('fig_xmin', inplace=True, axis=1)
figdf_bar['fig_xscale']=1000.
figdf_bar['trace_markersize']=30
figdf_bar['fig_xtick_decimals']=1
figdf_bar['fig_ytick_decimals']=1
figdf_bar['fig_xlim_all']=False
figdf_bar['fig_xmin']=0.
figdf_bar['fig_ylim_all']=False
figdf_bar.drop('fig_dyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_dxticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nxticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
figdf_bar['fig_ylabel']='% LTP'
figdf_bar['fig_xlabel']='Population spike (mV*us)'

figtype = 'corr_spikes_ind_firtpulse_lastburst_X_ltp_final_'
variables = ['data_ind_hilbert_sum_secondpulse_mean', 'ltp_final']
# plot and show
#-------------------------------------
figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted, figdf=figdf_bar, variables=variables)

# save figures
#-----------------
for fig_key, fig in figs_bar.iteritems():
    fname = figure_directory+figtype+str(fig_key)+'.png'
    fig.savefig(fname, format='png', dpi=dpi)
# 

# setup df of figure parameters
#------------------------------
figdf_bar = figsetup._sbar_2path()
figdf_bar.drop('fig_ymin', inplace=True, axis=1)
figdf_bar.drop('fig_xmin', inplace=True, axis=1)
figdf_bar['fig_xscale']=1000.
figdf_bar['trace_markersize']=30
figdf_bar['fig_xtick_decimals']=1
figdf_bar['fig_ytick_decimals']=1
figdf_bar['fig_xlim_all']=False
figdf_bar['fig_xmin']=0.
figdf_bar['fig_ylim_all']=False
figdf_bar.drop('fig_dyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_dxticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nxticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
figdf_bar['fig_ylabel']='Population spike (mV*us) induction'
figdf_bar['fig_xlabel']='Population spike (mV*us) baseline'

figtype = 'corr_spikes_probe_hilbert_sum_baseline_mean_x_spikes_ind_firtpulse_lastburst'
variables = ['data_probe_hilbert_sum_baseline_mean','data_ind_hilbert_sum_firstpulse_mean']
# plot and show
#-------------------------------------
figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted, figdf=figdf_bar, variables=variables)

# save figures
#-----------------
for fig_key, fig in figs_bar.iteritems():
    fname = figure_directory+figtype+str(fig_key)+'.png'
    fig.savefig(fname, format='png', dpi=dpi)

# setup df of figure parameters
#------------------------------
figdf_bar = figsetup._sbar_2path()
figdf_bar.drop('fig_ymin', inplace=True, axis=1)
figdf_bar.drop('fig_xmin', inplace=True, axis=1)
figdf_bar['fig_xscale']=1000.
figdf_bar['trace_markersize']=30
figdf_bar['fig_xtick_decimals']=1
figdf_bar['fig_ytick_decimals']=1
figdf_bar['fig_xlim_all']=False
figdf_bar['fig_xmin']=0.
figdf_bar['fig_ylim_all']=False
figdf_bar.drop('fig_dyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nyticks', axis=1, inplace=True)
# figdf_bar.drop('fig_dxticks', axis=1, inplace=True)
# figdf_bar.drop('fig_nxticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
figdf_bar['fig_ylabel']='LTP'
figdf_bar['fig_xlabel']='baseline epsp area'

figtype = 'corr_spikes_probe_hilbert_sum_baseline_mean_x_spikes_ind_firtpulse_lastburst'
variables = ['area_probe_iir_band_5_50_baseline_mean','ltp_final']
# plot and show
#-------------------------------------
figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted, figdf=figdf_bar, variables=variables)

# save figures
#-----------------
for fig_key, fig in figs_bar.iteritems():
    fname = figure_directory+figtype+str(fig_key)+'.png'
    fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_1path()
# figdf_bar.drop('fig_ymin', inplace=True, axis=1)
# figdf_bar.drop('fig_xmin', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_norm_'
# variables = ['data_probe_hilbert_sum_baseline_mean', 'ltp_final']
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted_1path, figdf=figdf_bar, variables=variables)


# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_1path()
# figdf_bar.drop('fig_ymin', inplace=True, axis=1)
# figdf_bar.drop('fig_xmin', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_norm_'
# variables = ['area_ind_burst_iir_band_5_50_norm_mean','ltp_final']
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted_1path, figdf=figdf_bar, variables=variables)

# # save figures
# #-----------------
# # for fig_key, fig in figs_bar.iteritems():
# #     fname = figure_directory+figtype+str(fig_key)+'.png'
# #     fig.savefig(fname, format='png', dpi=dpi)
# # 

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_2path()
# figdf_bar.drop('fig_ymin', inplace=True, axis=1)
# figdf_bar.drop('fig_xmin', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_norm_'
# variables = ['area_ind_burst_iir_band_5_50_norm_mean','ltp_final']
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._var2var_corr(df_sorted=df_sorted, figdf=figdf_bar, variables=variables)

# # save figures
# #-----------------
# # for fig_key, fig in figs_bar.iteritems():
# #     fname = figure_directory+figtype+str(fig_key)+'.png'
# #     fig.savefig(fname, format='png', dpi=dpi)
# # 

# #===========================================================================
# # slope trace plots during induction
# #===========================================================================
# setup df of figure parameters
#------------------------------   
# figdf_strace = figsetup._strace_ind_2path_mean()
# figdf_strace['fig_xlim_all']=False
# figdf_strace['fig_ylim_all']=False
# figdf_strace['fig_yscale']=100.
# figdf_strace.drop('fig_dyticks', axis=1, inplace=True)
# figdf_strace.drop('fig_nyticks', axis=1, inplace=True)
# figdf_strace.drop('fig_ymin', axis=1, inplace=True)
# figdf_strace['fig_ylabel']='Spike area (mV*ms)'
# figdf_strace['fig_xlabel']='Burst number'
# # plot and show
# #-------------------------------------
# figtype='spikes_ind_trace_firstpulse_'
# variable = 'data_ind_hilbert_sum_firstpulse'
# figs_strace, axes_strace = plots._trace_mean(df_sorted=df_sorted, figdf=figdf_strace, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_strace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #===========================================================================
# # slope trace plots during induction
# #===========================================================================
# # setup df of figure parameters
# #------------------------------   
# figdf_strace1 = figsetup._strace_ind_1path_mean()
# figdf_strace1['fig_xlim_all']=False
# figdf_strace1['fig_ylim_all']=False
# figdf_strace1['fig_yscale']=100.
# figdf_strace1['fig_ylabel']='Spike area (mV*ms)'
# figdf_strace1['fig_xlabel']='Burst number'
# print sorted(figdf_strace1.keys())
# # figdf_strace.drop('fig_dyticks', axis=1, inplace=True)

# # figdf_strace.drop('fig_ymin', axis=1, inplace=True)
# # plot and show
# #-------------------------------------
# figtype='spikes_ind_trace_firstpulse_1path_'
# variable = 'data_ind_hilbert_sum_firstpulse'
# figs_strace, axes_strace = plots._trace_mean(df_sorted=df_sorted_1path, figdf=figdf_strace1, variable=variable)
# # save figures
# #-----------------
# for fig_key, fig in figs_strace.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

#============================================================================
# # induction area bar plots 1 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_1path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_firtpulse_lastburst_1path'
# variable = 'data_ind_hilbert_sum_firstpulse_lastburst'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar, ttests = plots._bar(df_sorted=df_sorted_1path, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_2path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_secondpulse_lastburst_'
# variable = 'data_ind_hilbert_sum_secondpulse_lastburst'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._bar(df_sorted=df_sorted, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 1 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_1path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_secondpulse_lastburst_1path'
# variable = 'data_ind_hilbert_sum_secondpulse_lastburst'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._bar(df_sorted=df_sorted_1path, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 2 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_2path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_norm_mean_'
# variable = 'data_ind_hilbert_sum_norm_mean'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._bar(df_sorted=df_sorted, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

# #============================================================================
# # induction area bar plots 1 path
# #============================================================================
# # setup df of figure parameters
# #------------------------------
# figdf_bar = figsetup._sbar_1path()
# figdf_bar['fig_ylabel']='Soma high frequency power'
# figdf_bar['fig_topercent']=False
# figdf_bar['fig_ymin']=0
# figdf_bar.drop('fig_dyticks', inplace=True, axis=1)

# figtype = 'spikes_ind_bar_norm_mean_1path_'
# variable = 'data_ind_hilbert_sum_norm_mean'
# # plot and show
# #-------------------------------------
# figs_bar, axes_bar = plots._bar(df_sorted=df_sorted_1path, figdf=figdf_bar, variable=variable)

# # save figures
# #-----------------
# for fig_key, fig in figs_bar.iteritems():
#     fname = figure_directory+figtype+str(fig_key)+'.png'
#     fig.savefig(fname, format='png', dpi=dpi)

