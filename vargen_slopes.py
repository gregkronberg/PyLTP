'''
'''
import numpy as np
import scipy.io as io
from scipy import stats
from scipy import signal
import pandas as pd
import glob
import copy
import os
import matplotlib.pyplot as plt
import pickle
import itertools
import tkSimpleDialog as tk
from datetime import datetime
import functions
import inspect
import pdb

class SlopeFuncs:
    '''
    '''
    def __init__(self):
        '''
        '''
        pass

    def _get_epsp_area_df(self, pre, df=[], keep=[], **kwargs):
        '''
        '''
        print 'adding epsp area'
        # check for filtered data to use in calculating area
        if 'filter_name' in kwargs:
            data_type_ind = 'data_filt_'+kwargs['filter_name']+'_sortby_pulse'
            data_type_ind_burst = 'data_filt_'+kwargs['filter_name']+'_sortby_burst'
            data_type_probe = 'data_filt_'+kwargs['filter_name']
            column_name_ind = 'area_ind_'+kwargs['filter_name']
            column_name_ind_burst = 'area_ind_burst_'+kwargs['filter_name']
            column_name_probe = 'area_probe_'+kwargs['filter_name']
        else:
            data_type_ind = 'data'+'_sortby_pulse'
            data_type_ind_burst = 'data'+'_sortby_burst'
            data_type_probe= 'data' 
            column_name_ind = 'area_ind'
            column_name_ind_burst = 'area_ind_burst'
            column_name_probe = 'area_probe'
            kwargs['filter_name']=''

        # time window to take area in
        t0 = 23 # samples
        t1 = 100
        # create for for masking bipolar locations in burst data
        pulses=4
        burst_temp_array = np.concatenate([np.arange(t0)+(t1*b) for b in range(pulses)])
        burst_mask_array = np.ones(t1*pulses)
        burst_mask_array[burst_temp_array]=0
        burst_mask_array = burst_mask_array.astype(bool)
        # preallocate variables to be stored as df columns
        area_ind={}
        area_ind_burst={}
        area_probe={}
        area_probe_smooth={}
        area_baseline_mean={}
        area_probe_norm={}
        area_ind_smooth={}
        area_ind_norm={}
        area_ind_norm_mean={}
        area_ind_mean={}
        area_ind_burst_smooth={}
        area_ind_burst_norm={}
        area_ind_burst_norm_mean={}
        area_ind_burst_mean={}
        t_area={}
        area_filter={}
        ind_idx={}
        # get dendritic location
        rec_locs = ['apical', 'basal', 'perforant']
        slope_loc = list(set(pre['data_probe'].keys()) & set(rec_locs))[0] 

        for path_key, path in pre['data_probe'][slope_loc].iteritems():

            if pre['induction_info'][0][path_key]['protocol']=='nostim':
                pulses=0
                burst_temp_array=np.array([])
                burst_mask_array=np.array([])
            else:
                # print pre['induction_info'][0][path_key]
                pulses=pre['induction_info'][0][path_key]['input_params']['pulses']
                burst_temp_array = np.concatenate([np.arange(t0)+(t1*b) for b in range(pulses)])
                burst_mask_array = np.ones(t1*pulses)
                burst_mask_array[burst_temp_array]=0
                burst_mask_array = burst_mask_array.astype(bool)

            # continue
            # if there is data to be kept from group_df
            if type(df) == pd.DataFrame and not df.empty:
                # get locations of the current slice and path in the group_df
                df_locs = df[(df.name==pre['slice_info']['name']) & (df.path==path_key)].index.values
            # induction index (matched to current path indices)
            ind_idx[path_key] = path['ind_idx']
            data_probe = path[data_type_probe]
            data_ind =  pre['data_induction'][slope_loc][path_key][data_type_ind]
            data_ind_burst =  pre['data_induction'][slope_loc][path_key][data_type_ind_burst]
            # area under probe epsp's
            area_probe[path_key] = np.sum(np.abs(data_probe[t0:t1,:]-data_probe[t0,:]),axis=0)
            # remove outliers
            area_probe_smooth[path_key] = functions._remove_outliers(
                time_series=area_probe[path_key],
                ind_idx=ind_idx[path_key],
                time_window=5,
                std_tol=2,
                include_ind=False)

            # get baseline mean
            # print ind_idx[path_key]
            area_baseline_mean[path_key] = np.mean(area_probe_smooth[path_key][ind_idx[path_key][0]-20:ind_idx[path_key][0]])
            # normalize to baseline mean
            area_probe_norm[path_key] = area_probe_smooth[path_key]/area_baseline_mean[path_key]
            # if there is induction data for the current pathway
            if data_ind[0].shape[1]>0:
                # get area under each induction pulse
                area_ind[path_key] = np.sum(np.abs(data_ind[0][t0:t1,:]-data_ind[0][t0,0]), axis=0)
                # create mask for ignoring bipolar pulses
                area_ind_burst[path_key] = np.sum(np.abs(data_ind_burst[0][burst_mask_array,:]-data_ind_burst[0][t0,:]), axis=0)
                # plt.figure()
                # plt.plot(data_ind_burst[0], 'k')
                # plt.plot(data_ind_burst[0][burst_mask_array,:], 'r')
                # plt.show()

                # remove oultiers
                area_ind_smooth[path_key] = functions._remove_outliers(
                    time_series=area_ind[path_key],
                    ind_idx=[0],
                    time_window=5,
                    std_tol=2,
                    include_ind=False)
                area_ind_burst_smooth[path_key] = functions._remove_outliers(
                    time_series=area_ind_burst[path_key],
                    ind_idx=[0],
                    time_window=5,
                    std_tol=2,
                    include_ind=False)
                # normalize to baseline mean
                area_ind_norm[path_key] = area_ind_smooth[path_key]/area_baseline_mean[path_key]
                area_ind_burst_norm[path_key] = area_ind_burst_smooth[path_key]/area_baseline_mean[path_key]

                area_ind_norm_mean[path_key] = np.mean(area_ind_norm[path_key])
                area_ind_burst_norm_mean[path_key] = np.mean(area_ind_burst_norm[path_key])

                area_ind_mean[path_key] = np.mean(area_ind_smooth[path_key])
                area_ind_burst_mean[path_key] = np.mean(area_ind_burst_smooth[path_key])
            # if no induction data for the current path, store empty lists
            else:
                area_ind[path_key]=np.nan
                area_ind_smooth[path_key]=np.nan
                area_ind_norm[path_key]=np.nan
                area_ind_norm_mean[path_key]=np.nan
                area_ind_mean[path_key]=np.nan
                area_ind_burst[path_key]=np.nan
                area_ind_burst_smooth[path_key]=np.nan
                area_ind_burst_norm[path_key]=np.nan
                area_ind_burst_norm_mean[path_key]=np.nan
                area_ind_burst_mean[path_key]=np.nan
            # store time window that area was taken during 
            t_area[path_key] = [t0,t1]
            # store name of the filter that was used
            area_filter[path_key] = kwargs['filter_name']

        # temporary dictionary to be converted to dataframe
        epsp_area = {
        column_name_ind:area_ind,
        column_name_ind_burst:area_ind_burst,
        column_name_probe:area_probe,
        column_name_probe+'_baseline_mean':area_baseline_mean,
        column_name_probe+'_norm':area_probe_norm,
        column_name_probe+'_smooth':area_probe_smooth,
        column_name_ind+'_smooth':area_ind_smooth,
        column_name_ind+'_norm':area_ind_norm,
        column_name_ind+'_norm_mean':area_ind_norm_mean,
        column_name_ind+'_mean':area_ind_mean,
        column_name_ind_burst+'_smooth':area_ind_burst_smooth,
        column_name_ind_burst+'_norm':area_ind_burst_norm,
        column_name_ind_burst+'_norm_mean':area_ind_burst_norm_mean,
        column_name_ind_burst+'_mean':area_ind_burst_mean,
        't_area':t_area,
        'area_filter':area_filter,
        }

        # convert to df
        epsp_area_df = functions._postdict2df(postdict=epsp_area, pre=pre)

        # print'epsp area keys:', sorted(epsp_area_df.keys())

        
        return epsp_area_df

    def _get_slopes_df(self, pre, df=[], keep=[], **kwargs):
        '''
        '''
        ind_data_type = 'data'+'_sortby_pulse'

        slopes={}
        slopes_smooth={}
        slopes_norm={}
        slopes_ind={}
        slopes_ind_smooth={}
        slopes_ind_norm={}
        ind_idx={}
        baseline={}
        t_slope={}

        # get dendritic location
        rec_locs = ['apical', 'basal', 'perforant',]
        print pre['data_probe'].keys()
        # print pre['data_probe'].keys()
        # print set(pre['data_probe'].keys()), set(rec_locs)
        # print set(pre['data_probe'].keys()) 
        # print set(rec_locs)
        slope_loc = list(set(pre['data_probe'].keys()) & set(rec_locs))[0] 
        # iterate over paths
        for path_key, path in pre['data_probe'][slope_loc].iteritems():
            # if there is data to be kept from group_df
            if type(df) == pd.DataFrame and not df.empty:
                # get locations of the current slice and path in the group_df
                df_locs = df[(df.name==pre['slice_info']['name']) & (df.path==path_key)].index.values[0]
            # if keeping t_slope, get t_slope value from 
            if 't_slope' in keep and not df.empty:
                # print df_locs
                t_slope[path_key] = df.t_slope[df_locs]

            elif 't_slope' in kwargs:
                t_slope[path_key] = kwargs['t_slope']
            # otherwise plot traces for each pathway and select t_slope using ginput
            else:
                plt.figure()
                plt.plot(pre['data_probe']['apical'][path_key]['data'])
                plt.xlim([0,100])
                plt.ylim([-.008,0.001])
                clicks = plt.ginput(n=2, show_clicks=True)
                plt.close()
                t_slope[path_key] = sorted(list(zip(*clicks)[0]))
            # induction index (matched to current path indices)
            ind_idx[path_key] = path['ind_idx']
            # array of voltage values to take slope of
            print pre['slice_info']['name'], t_slope[path_key]
            slope_array = path['data'][int(round(t_slope[path_key][0])):int(round(t_slope[path_key][1])),:]
            if '20160926' in pre['slice_info']['name']:
                plt.figure()
                plt.plot(slope_array)
                plt.show(block=False)
            # take average slope in the time window specified by t_slope
            slopes[path_key] = np.mean(np.diff(slope_array, axis=0),axis=0)
            if '20160926' in pre['slice_info']['name']:
                plt.figure()
                plt.plot(slopes[path_key])
                plt.show(block=False)
            # remove individual probe outliers
            slopes_smooth[path_key] = functions._remove_outliers(time_series=slopes[path_key], 
                ind_idx=ind_idx[path_key],
                time_window=5,
                std_tol=2,
                include_ind=False)
            # slopes_smooth[path_key] = self._remove_probe_outliers(slopes=slopes[path_key], ind_idx=ind_idx, time_window=5, std_tol=3)
            # get baseline average to normalize slopes
            baseline[path_key] = np.mean(slopes_smooth[path_key][ind_idx[path_key][0]-20:ind_idx[path_key][0]])
            # normalized slopes for current path
            slopes_norm[path_key] = slopes_smooth[path_key]/baseline[path_key]
            # raw induction data
            data_ind =  pre['data_induction'][slope_loc][path_key][ind_data_type][0]
            # get slopes during induction
            slopes_ind[path_key] = np.mean( np.diff( data_ind[int(t_slope[path_key][0]):int(t_slope[path_key][1]), :], axis=0), axis=0)
            # remove outliers
            slopes_ind_smooth[path_key] = functions._remove_outliers(time_series=slopes_ind[path_key], 
                ind_idx=ind_idx[path_key],
                time_window=5,
                std_tol=2,
                include_ind=False)
            
            slopes_ind_norm[path_key] = slopes_ind[path_key]/baseline[path_key]

        slopes = {
        'slopes':slopes,
        'slopes_smooth':slopes_smooth,
        'slopes_baseline_mean':baseline,
        'slopes_norm':slopes_norm,
        'slopes_ind':slopes_ind,
        'slopes_ind_smooth':slopes_ind_smooth,
        'slopes_ind_norm':slopes_ind_norm,
        'ind_idx':ind_idx,
        't_slope':t_slope
        }

        # convert to dataframe (includes conditions dictionary)
        slopes_df = functions._postdict2df(postdict=slopes, pre=pre)

        return slopes_df

    def _get_baseline_max_idx(self, pre, df=[], keep=[], **kwargs):
        '''
        '''
        baseline_max_idx={}
        baseline_io={}
        baseline_io_norm={}

        for path in pre['path_blocks']:
            # print 'empty?',df.empty
            # if there is data to be kept from group_df
            if type(df) == pd.DataFrame and not df.empty:
                # get locations of the current slice and path in the group_df
                df_locs = df[(df.name==pre['slice_info']['name']) & (df.path==path)].index.values[0]

                # get slopes and baseline max idx from df
                #-----------------------------------------
                slopes = df.slopes[df_locs]
                baseline_max_idx_temp = df.baseline_max_idx[df_locs]

                # if baseline max idx has not been found
                #---------------------------------------
                if np.isnan(baseline_max_idx_temp):
                    # pdb.set_trace()
                    # show slopes
                    #------------
                    plt.figure()
                    plt.plot(slopes)
                    plt.show(block=False)
                    # dialogue box to manually enter index
                    #-------------------------------------
                    app_window=tk.Tk()
                    idx_str = tk.askstring('Input','baseline max index (enter \'none\' if unknown )',parent=app_window)
                    app_window.destroy()
                    plt.close()

                    try:
                        idx_int = int(idx_str)
                    except ValueError:
                        idx_int = np.nan

                    baseline_max_idx[path] = idx_int

                else:
                    baseline_max_idx[path] = baseline_max_idx_temp

            if not np.isnan(baseline_max_idx[path]):
                slope_max = slopes[baseline_max_idx[path]]
                baseline_io[path] = slopes[:baseline_max_idx[path]+1]
                baseline_io_norm[path] = slopes[:baseline_max_idx[path]+1]/slope_max
            else:
                baseline_io[path] = np.nan
                baseline_io_norm[path] = np.nan

        idx_dict = {
        'baseline_max_idx':baseline_max_idx,
        'slopes_io':baseline_io,
        # 'slopes_io_norm'
        }

        idx_df = functions._postdict2df(postdict=idx_dict, pre=pre)

        return idx_df

    def _remove_exp_fit(self, group_df, ):
        '''
        '''
        # if no files have been processed for removal yet
        if 'exp_fit_remove' not in group_df:
            # create a column to mark files for removal. nan indicates that the trace has not been processed yet
            group_df['exp_fit_remove']=None
        if 'exp_fit_coeff' not in group_df:
            group_df['exp_fit_coeff']=None
        if 'exp_fit' not in group_df:
            group_df['exp_fit']=None
        if 'exp_fit_error' not in group_df:
            group_df['exp_fit_error']=None

        idx = range(22,80)
        param_range = [-8E-3, 0]
        error_threshold = 8
        for i in group_df.index:
            slopes = group_df.loc[i, 'slopes_norm_aligned_0']
            if type(slopes)==float and np.isnan(slopes):
                continue
            # print any(np.isnan(group_df.loc[i, 'slopes_norm_aligned_0']))
            # slopes = group_df.loc[i, 'slopes_norm_aligned_0']
            # if type(slopes)==list or type(slopes)==np.ndarray:
            #     if any(np.isnan(slopes)):
            #         continue
            # elif np.isnan(slopes):
            #     continue
            x = np.array(range(len(idx)))
            
            y = slopes[0][idx]

            fit_coeff = functions.exp_fit(x,y)
            exp_fit = fit_coeff[0]*np.exp(fit_coeff[1]*x)
            exp_fit_error = np.sum(np.abs(exp_fit-y))/np.mean(y)

            group_df.at[i, 'exp_fit_coeff']=fit_coeff
            group_df.at[i, 'exp_fit']=exp_fit
            group_df.at[i, 'exp_fit_error']=exp_fit_error

            if param_range[0] < fit_coeff[1] < param_range[1]:
                group_df.at[i, 'exp_fit_remove'] = False
            elif exp_fit_error<error_threshold:
                group_df.at[i, 'exp_fit_remove'] = False
            else:
                group_df.at[i, 'exp_fit_remove'] = True

        return group_df

    def _remove_bad_slices(self, group_df, query=[], process_all=False):
        '''remove slices that show drift.  plot each trace and click below 1 to flag for removal

        ==Args==
        -group_df : group dataframe 
        -query : query string for group_df to only process traces that meet the specified condition. for example 'date > 20181012'
        -process_all : if False, only traces that have a nan in the remove column will be processed.  if true, all traces that match the query will be processed
        
        ==Out==
        -group_df : group dataframe
       
        ==Updates==
        -group_df : columns 'remove', 'remove_reason', and 'remove_date' are updated
                ~remove : column of boolean values marking a trace to be removed.  if nan, the trace hasn't been processed yet
                ~remove_reason : reason for removing the slice (e.g. 'drift'). if slice is not removed, the reason is automatically set to 'keep'
                ~remove_date : date and time that the trace was processed for removal

        ==Comments==
        -traces that have not been processed for removal yet are marked with a nan value

        '''
        # if no files have been processed for removal yet
        if 'remove' not in group_df:
            # create a column to mark files for removal. nan indicates that the trace has not been processed yet
            group_df['remove']=np.nan

        if 'remove_reason' not in group_df:
            group_df['remove_reason']=np.nan
        if 'remove_date' not in group_df:
            group_df['remove_date']=np.nan

        # parameters for plot
        ymin = 0.8
        ymax = 3
        grid_spacing = 0.1

        def _plot_and_remove(df_source, df_target, process_all=False, ylim=[0.8,3], grid_spacing=0.1, copy_from_source=False):
            '''
            ==Args==
            -df_source : dataframe that traces are drawn from.  this assumes that the rows indices, match that of the target dataframe. from example df_source can be the result of a query that maintains the original row indices from the original dataframe
            -df_target : dataframe that contains all data in which removal flags are to be stored
            -process_all : if false, only unprocessed (nan in remove column) are processed. if true, all traces are processed for removal
            -ylim : y limits for plot to decide rejection
            -grid_spacing : grid_spacing for plot to decide rejection 

            ==Out==
            -df_target : dataframe to be updated with traces flagged for 
            removal

            ==Update==
            -df_target : dataframe with updated 'remove' column.  traces that are marked for removal have a 1 in this column
            '''
            if copy_from_source:
                df_target[['remove','remove_reason','remove_date']] = df_source[['remove','remove_reason','remove_date']]

            else:
                # iterate over traces
                for trace_i, trace in  enumerate(df_source.slopes_norm):

                    # get corresponding index in the target dataframe
                    target_index = df_source.index[trace_i]

                    # if only processing new traces and the current trace is not new, pass
                    if not process_all and not pd.isnull(df_source.remove.iloc[trace_i]):
                        continue

                    # if the current trace is new or all traces are being processed
                    else:

                        # plot trace, click below 1 to mark trace for rejection
                        plt.figure()
                        plt.plot(trace)
                        print 'induction block:', df_source.induction_block_0.iloc[trace_i]
                        plt.axvline(x=df_source.induction_block_0.iloc[trace_i], color='black')
                        plt.ylim(ylim)
                        plt.yticks(np.arange(ylim[0],ylim[1], grid_spacing))
                        plt.grid()
                        plt.title('click below 1 to reject')
                        clicks = plt.ginput(n=1, show_clicks=True)
                        plt.close()
                        t_clicks = sorted(list(zip(*clicks)[1]))

                        # if clicked below 1, mark trace for removal
                        if min(t_clicks)<1:

                            # mark trace for removal
                            df_target.remove[target_index] = True
                            
                            # dialogue box for removal reason
                            app_window=tk.Tk()
                            reason = tk.askstring('Input','reason for rejection',parent=app_window)
                            df_target.remove_reason[target_index] = reason
                            
                            # store date and time of removal
                            df_target.remove_date[target_index] = str(datetime.now())

                        # if clicked above 1, mark trace for keeping
                        else:
                            df_target.remove[target_index] = False
                            df_target.remove_reason[target_index] = 'keep'
                            df_target.remove_date[target_index] = str(datetime.now())

            return df_target

        if query:
            df_source = group_df.query(query)
        else:
            df_source = group_df

        group_df = _plot_and_remove(df_source=df_source, df_target=group_df, process_all=process_all)

        # after each trace, save the result
        # group_df.to_pickle(self.directory+self.filename)

        return group_df

    def _align_and_measure_ltp(self, group_df):
        ''' create columns with normalized slopes that are aligned to the induction block and the final amount of ltp
        ==Args==
        -group_df : group dataframe. must contain columns 'induction_block_0', 'slopes_norm'

        ==Out==
        -group_df : group dataframe. new columns: 'slopes_norm_aligned_0' and 'ltp_final'

        ==Update==
        -group_df.slopes_norm_aligned_0 : normalized slopes are aligned to the first induction block, so that each entry is an array of length 80 (the first 20 samples are pre-indction, the last 60 samples are post-induction)
        -group_df.ltp_final : mean of the last ten normalized slopes (min 51-60) for each trace

        ==Comments==
        '''
        def _get_aligned_data(row):
            '''for each row align slopes data to the induction block
            ==Args==
            -row : row in a pandas dataframe
            ==Out==
            -aligned_data :  a list, where the first element is the aligned slopes
            ==Comments==
            -when fed to the apply function in pandas, a series is returned, where each entry contains the corresponding aligned data
            '''
            # print 'induction block 0:', row['induction_block_0']
            # get indices to align data
            indices = range(int(row['induction_block_0'])-20, int(row['induction_block_0'])) + range(int(row['induction_block_0']), int(row['induction_block_0'])+60)
            # get aligned data
            aligned_data = [row['slopes_norm'][indices]]
            return aligned_data

        def _get_ltp_final(row):
            '''
            '''
            ltp_final = np.mean(row.slopes_norm_aligned_0[0][-10:])
            return ltp_final

        group_df['slopes_norm_aligned_0'] = group_df.apply(lambda row: _get_aligned_data(row), axis=1)

        group_df['ltp_final'] = group_df.apply(lambda row: _get_ltp_final(row), axis=1)



        return group_df

class Slopes:
    '''
    '''
    def __init__(self, directory='Variables/', filename='slopes_df.pkl', pre_directory='Preprocessed Data/', **kwargs):
        '''
        '''
        self._process(directory=directory, filename=filename, pre_directory=pre_directory)
        
    def _process(self, directory='Variables/', filename='slopes_df.pkl', pre_directory='Preprocessed Data/', **kwargs):
        '''
        '''
        ############################################################
        # FIXME
        ############################################################
        self.slopefuncs = SlopeFuncs()
        df_funcs = functions.ApplyDF()
        funclist = [self.slopefuncs._get_slopes_df,self.slopefuncs._get_epsp_area_df]#,self.slopefuncs._get_baseline_max_idx]
        # funclist = [self.slopefuncs._get_baseline_max_idx]
        kwlist = [{}, {'filter_name':'iir_band_5_50'}]#, {}]
        # kwlist = [{}, {}] 
        # rerun = [self.slopefuncs._get_baseline_max_idx]
        rerun=[]
        keep = ['t_slope', 'remove', 'remove_reason', 'baseline_max_idx']
        self.directory=directory
        self.filename=filename
        self.group_df = functions._load_group_data(directory, filename, df=True)
        print self.group_df
        self.group_df = functions._process_new_data_df(group_df=self.group_df, preprocessed_directory=pre_directory, search_string='.pkl', functions=funclist, kwlist=kwlist, rerun=rerun, keep=keep, file_limit=5)
        # fix me, _remove_bad_slices to functions module
        
        self.group_df = self.slopefuncs._remove_bad_slices(self.group_df)

        self.group_df = self.slopefuncs._align_and_measure_ltp(self.group_df)
        self.group_df = self.slopefuncs._remove_exp_fit(group_df=self.group_df)
        self.group_df = df_funcs._get_io(df=self.group_df, max_idx_col='baseline_max_idx', colnames=['data_ind_hilbert_sum_norm'], slice_i=slice(40, None), unwrap=False)
        # add experimenter info
        #------------------------
        if 'asif' in filename:
            experimenter='asif'
        elif 'mahima' in filename:
            experimenter='mahima'
        else:
            experimenter = 'greg'
        self.group_df['experimenter']=experimenter
        self.group_df.to_pickle(directory+self.filename)

# FIXME compare removed slices to previous runs
# greg two pathway data
df = Slopes(filename='slopes_df.pkl', pre_directory='Preprocessed Data/').group_df
# greg 1 pathway data
#---------------------
df_1path = Slopes(filename='slopes_df_1path.pkl', pre_directory='Preprocessed Data 1Path/').group_df
# mahima data
#--------------
# df_mahima = Slopes(filename='slopes_df_mahima.pkl', pre_directory='Preprocessed Data Mahima/').group_df

if __name__=='__main__':

    df = Slopes().group_df
