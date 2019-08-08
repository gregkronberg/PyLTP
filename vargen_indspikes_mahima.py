'''
'''
from scipy import signal
import numpy as np
import functions 
import glob
import pickle
import pandas as pd
# add docs to all functions
# write outline in readme file
# function to merge previous group datas
# analyze 

class SpikeFuncs:
    '''
    '''
    def __init__(self, ):
        '''
        '''
        pass

    def _get_induction_spikes_df(self, pre, df=[], keep=[], **kwargs):
        '''
        '''
        if 'filter_name' in kwargs:
            filter_name = kwargs['filter_name']
        channel=pre['data_induction'].keys()[0]
        path = pre['data_induction'][channel].keys()[0]
        # print data_induction[channel][path]['fs']
        fs = pre['data_induction'][channel][path]['fs'][0]
        t_window = [int(.003*fs), int(.007*fs)]#np.array([.002, .008])*fs
        data_ind={}
        data_ind_hilbert={}
        data_ind_hilbert_smooth={}
        data_ind_hilbert_sum={}
        data_ind_hilbert_sum_mean={}
        data_ind_hilbert_sum_norm={}
        data_ind_hilbert_com={}
        data_ind_hilbert_com_smooth={}
        data_ind_hilbert_com_mean={}

        # data_ind_hilbert_sum_norm_fft_abs={}
        # data_ind_hilbert_sum_norm_fft_angle={}

        data_ind_hilbert_sum_normsub={}
        data_ind_hilbert_sum_norm_mean={}
        data_ind_hilbert_sum_normsub_mean={}
        data_ind_hilbert_sum_normsub_max={}
        data_ind_hilbert_sum_normsub_var={}
        data_ind_hilbert_sum_firstpulse={}
        data_ind_hilbert_sum_secondpulse={}
        data_ind_hilbert_sum_thirdpulse={}
        data_ind_hilbert_sum_fourthpulse={}
        data_ind_hilbert_sum_allpulse={}

        data_ind_hilbert_sum_firstpulse_norm={}
        data_ind_hilbert_sum_secondpulse_norm={}
        data_ind_hilbert_sum_thirdpulse_norm={}
        data_ind_hilbert_sum_fourthpulse_norm={}
        data_ind_hilbert_sum_allpulse_norm={}

        data_ind_hilbert_sum_firstpulse_mean={}
        data_ind_hilbert_sum_secondpulse_mean={}
        data_ind_hilbert_sum_thirdpulse_mean={}
        data_ind_hilbert_sum_fourthpulse_mean={}
        data_ind_hilbert_sum_allpulse_mean={}

        data_ind_hilbert_sum_firstpulse_norm_mean={}
        data_ind_hilbert_sum_secondpulse_norm_mean={}
        data_ind_hilbert_sum_thirdpulse_norm_mean={}
        data_ind_hilbert_sum_fourthpulse_norm_mean={}
        data_ind_hilbert_sum_allpulse_norm_mean={}


        data_probe={}
        data_probe_hilbert={}
        data_probe_hilbert_smooth={}
        data_probe_hilbert_sum={}
        data_probe_hilbert_sum_baseline_mean={}
        data_probe_hilbert_norm={}
        data_probe_hilbert_smooth_other={}
        data_probe_hilbert_sum_other={}
        data_probe_hilbert_sum_baseline_mean_other={}
        data_probe_hilbert_smooth_combined={}
        data_probe_hilbert_sum_combined={}
        data_probe_hilbert_sum_baseline_mean_combined={}

        paths = pre['data_probe']['soma'].keys()
        # iterate over paths
        for path, data in pre['data_probe']['soma'].iteritems():

            # if there is data to be kept from group_df
            if type(df) == pd.DataFrame and not df.empty:
                # get locations of the current slice and path in the group_df
                df_locs = df[(df.name==pre['slice_info']['name']) & (df.path==path)].index.values[0]

            # FIXME allow for multiple inductions to be stored
            # print pre['ind_idx'][0]
            # get induction block 
            induction_block = pre['ind_idx'][path][0]
            data_ind[path] = pre['data_induction']['soma'][path]['data_filt_'+filter_name+'_sortby_pulse'][0]
            data_probe[path] = pre['data_probe']['soma'][path]['data_filt_'+filter_name]

            data_probe_hilbert[path] = pre['data_probe']['soma'][path]['data_filt_'+filter_name+'_hilbert']

            # data_probe_hilbert[path] = signal.hilbert(data_probe[path] - np.mean(data_probe[path], axis=0), axis=0)

            data_probe_hilbert_sum[path] = np.sum(np.abs(data_probe_hilbert[path][t_window,:]), axis=0)

            # remove outliers
            data_probe_hilbert_smooth[path] = functions._remove_outliers(time_series=data_probe_hilbert_sum[path], 
                ind_idx=pre['ind_idx'][path],
                time_window=5,
                std_tol=2,
                include_ind=False)

            data_probe_hilbert_sum_baseline_mean[path] = np.mean(data_probe_hilbert_smooth[path][induction_block-20:induction_block])

            data_probe_hilbert_norm[path] = data_probe_hilbert_smooth[path]/data_probe_hilbert_sum_baseline_mean[path]

            # check if there is induction data (no data if path is inactive during induction)
            # exclude slice on 20170117_1, where data in soma channel was saturated
            if data_ind[path].size!=0 and '20170117_1' not in pre['slice_info']['name']:

                data_ind_hilbert[path] = pre['data_induction']['soma'][path]['data_filt_'+filter_name+'_hilbert_sortby_pulse'][0]

                data_ind_hilbert_com[path] = functions._get_burst_spiketimes(data=data_ind_hilbert[path], t_window=t_window)

                data_ind_hilbert_com_smooth[path] = functions._remove_outliers(time_series=data_ind_hilbert_com[path], 
                ind_idx=[0],
                time_window=5,
                std_tol=3,
                include_ind=False)

                # data_ind_hilbert[path] = signal.hilbert(data_ind[path]-np.mean(data_ind[path]), axis=0)
                data_ind_hilbert_sum[path] = np.sum(np.abs(data_ind_hilbert[path][t_window,:]), axis=0)
                # remove outliers
                data_ind_hilbert_smooth[path] = functions._remove_outliers(time_series=data_ind_hilbert_sum[path], 
                ind_idx=[0],
                time_window=5,
                std_tol=3,
                include_ind=False)

                data_ind_hilbert_sum_norm[path] = data_ind_hilbert_smooth[path]/data_probe_hilbert_sum_baseline_mean[path]

                # data_ind_hilbert_sum_norm_fft_abs[path] = np.abs(np.fft.fft(data_ind_hilbert_sum_norm[path]))
                # data_ind_hilbert_sum_norm_fft_angle[path] = np.angle(np.fft.fft(data_ind_hilbert_sum_norm[path]))

                data_ind_hilbert_sum_normsub[path] = data_ind_hilbert_smooth[path]-data_probe_hilbert_sum_baseline_mean[path]


                if pre['induction_info'][0][path]['protocol']=='nostim':
                    pulses=0
                    data_ind_hilbert_sum_firstpulse[path] = np.nan
                    data_ind_hilbert_sum_secondpulse[path] = np.nan
                    data_ind_hilbert_sum_thirdpulse[path] = np.nan
                    data_ind_hilbert_sum_fourthpulse[path] = np.nan
                    data_ind_hilbert_sum_firstpulse_mean[path] = np.nan
                    data_ind_hilbert_sum_secondpulse_mean[path] = np.nan
                    data_ind_hilbert_sum_thirdpulse_mean[path] = np.nan
                    data_ind_hilbert_sum_fourthpulse_mean[path] = np.nan
                    data_ind_hilbert_sum_allpulse_mean[path] = np.nan
                    data_ind_hilbert_com[path]=np.nan

                    data_ind_hilbert_sum_firstpulse_norm[path] = np.nan
                    data_ind_hilbert_sum_secondpulse_norm[path] = np.nan
                    data_ind_hilbert_sum_thirdpulse_norm[path] = np.nan
                    data_ind_hilbert_sum_fourthpulse_norm[path] = np.nan
                    data_ind_hilbert_sum_allpulse_norm[path] = np.nan
                    data_ind_hilbert_sum_firstpulse_norm_mean[path] = np.nan
                    data_ind_hilbert_sum_secondpulse_norm_mean[path] = np.nan
                    data_ind_hilbert_sum_thirdpulse_norm_mean[path] = np.nan
                    data_ind_hilbert_sum_fourthpulse_norm_mean[path] = np.nan
                    data_ind_hilbert_sum_allpulse_norm_mean[path] = np.nan

                else:
                    # print pre['induction_info'][0][path_key]
                    pulses=pre['induction_info'][0][path]['input_params']['pulses']
                    bursts = pre['induction_info'][0][path]['input_params']['bursts']
                    mask1 = range(0, len(data_ind_hilbert_smooth[path]), pulses)
                    mask2 = range(1, len(data_ind_hilbert_smooth[path]), pulses)
                    mask3 = range(2, len(data_ind_hilbert_smooth[path]), pulses)
                    mask4 = range(3, len(data_ind_hilbert_smooth[path]), pulses)
                    data_ind_hilbert_sum_firstpulse[path] = data_ind_hilbert_smooth[path][mask1]
                    data_ind_hilbert_sum_secondpulse[path]= data_ind_hilbert_smooth[path][mask2]
                    data_ind_hilbert_sum_thirdpulse[path]=data_ind_hilbert_smooth[path][mask3]
                    data_ind_hilbert_sum_fourthpulse[path]=data_ind_hilbert_smooth[path][mask4]
                    data_ind_hilbert_sum_allpulse[path]=np.sum(np.reshape(data_ind_hilbert_smooth[path], (-1, bursts), order='F'), axis=0)

                    data_ind_hilbert_sum_firstpulse_norm[path] = data_ind_hilbert_sum_norm[path][mask1]
                    data_ind_hilbert_sum_secondpulse_norm[path]= data_ind_hilbert_sum_norm[path][mask2]
                    data_ind_hilbert_sum_thirdpulse_norm[path]=data_ind_hilbert_sum_norm[path][mask3]
                    data_ind_hilbert_sum_fourthpulse_norm[path]=data_ind_hilbert_sum_norm[path][mask4]
                    data_ind_hilbert_sum_allpulse_norm[path]= np.sum(np.reshape(data_ind_hilbert_sum_norm[path], (-1, bursts), order='F'), axis=0)

                data_ind_hilbert_sum_mean[path] = np.mean(data_ind_hilbert_smooth[path])
                data_ind_hilbert_sum_firstpulse_mean[path] = np.mean(data_ind_hilbert_sum_firstpulse[path])
                data_ind_hilbert_sum_secondpulse_mean[path] = np.mean(data_ind_hilbert_sum_secondpulse[path])
                data_ind_hilbert_sum_thirdpulse_mean[path] = np.mean(data_ind_hilbert_sum_thirdpulse[path])
                data_ind_hilbert_sum_fourthpulse_mean[path] = np.mean(data_ind_hilbert_sum_fourthpulse[path])
                data_ind_hilbert_sum_allpulse_mean[path] = np.mean(data_ind_hilbert_sum_allpulse[path])

                data_ind_hilbert_sum_firstpulse_norm_mean[path] = np.mean(data_ind_hilbert_sum_firstpulse_norm[path])
                data_ind_hilbert_sum_secondpulse_norm_mean[path] = np.mean(data_ind_hilbert_sum_secondpulse_norm[path])
                data_ind_hilbert_sum_thirdpulse_norm_mean[path] = np.mean(data_ind_hilbert_sum_thirdpulse_norm[path])
                data_ind_hilbert_sum_fourthpulse_norm_mean[path] = np.mean(data_ind_hilbert_sum_fourthpulse_norm[path])
                data_ind_hilbert_sum_allpulse_norm_mean[path] = np.mean(data_ind_hilbert_sum_allpulse_norm[path])

                data_ind_hilbert_sum_norm_mean[path] = np.mean(data_ind_hilbert_sum_norm[path])

                data_ind_hilbert_sum_normsub_mean[path] = np.mean(data_ind_hilbert_sum_normsub[path])

                data_ind_hilbert_sum_normsub_max[path] = np.max(data_ind_hilbert_sum_normsub[path])

                data_ind_hilbert_sum_normsub_var[path] = np.var(data_ind_hilbert_sum_normsub[path])

                data_ind_hilbert_com_mean[path]= np.mean(data_ind_hilbert_com_smooth[path])

            else:
                data_ind_hilbert[path] = np.nan
                data_ind_hilbert_sum[path] = np.nan
                data_ind_hilbert_smooth[path]=np.nan
                data_ind_hilbert_sum_mean[path] = np.nan
                data_ind_hilbert_sum_norm[path] = np.nan
                # data_ind_hilbert_sum_norm_fft_abs[path] = np.nan
                # data_ind_hilbert_sum_norm_fft_angle[path] = np.nan
                data_ind_hilbert_sum_normsub[path] = np.nan
                data_ind_hilbert_sum_norm_mean[path] = np.nan
                data_ind_hilbert_sum_normsub_mean[path] = np.nan
                data_ind_hilbert_sum_normsub_max[path] = np.nan
                data_ind_hilbert_sum_normsub_var[path] = np.nan
                data_ind_hilbert_sum_firstpulse[path] = np.nan
                data_ind_hilbert_sum_secondpulse[path] = np.nan
                data_ind_hilbert_sum_thirdpulse[path] = np.nan
                data_ind_hilbert_sum_fourthpulse[path] = np.nan
                data_ind_hilbert_sum_allpulse[path] = np.nan
                data_ind_hilbert_sum_firstpulse_mean[path] = np.nan
                data_ind_hilbert_sum_secondpulse_mean[path] = np.nan
                data_ind_hilbert_sum_thirdpulse_mean[path] = np.nan
                data_ind_hilbert_sum_fourthpulse_mean[path] = np.nan
                data_ind_hilbert_sum_allpulse_mean[path] = np.nan

                data_ind_hilbert_sum_firstpulse_norm[path] = np.nan
                data_ind_hilbert_sum_secondpulse_norm[path] = np.nan
                data_ind_hilbert_sum_thirdpulse_norm[path] = np.nan
                data_ind_hilbert_sum_fourthpulse_norm[path] = np.nan
                data_ind_hilbert_sum_allpulse_norm[path] = np.nan
                data_ind_hilbert_sum_firstpulse_norm_mean[path] = np.nan
                data_ind_hilbert_sum_secondpulse_norm_mean[path] = np.nan
                data_ind_hilbert_sum_thirdpulse_norm_mean[path] = np.nan
                data_ind_hilbert_sum_fourthpulse_norm_mean[path] = np.nan
                data_ind_hilbert_sum_allpulse_norm_mean[path] = np.nan

                data_ind_hilbert_com[path]=np.nan
                data_ind_hilbert_com_smooth[path]=np.nan
                data_ind_hilbert_com_mean[path]=np.nan
            

        # for each path store metrics from other path
        if len(paths)>1:

            for path in paths:
                path_other = [temp for temp in paths if temp!=path][0]
                data_probe_hilbert_sum_other[path] = data_probe_hilbert_sum[path_other]
                data_probe_hilbert_sum_baseline_mean_other[path] = data_probe_hilbert_sum_baseline_mean[path_other]
                data_probe_hilbert_smooth_other[path] = data_probe_hilbert_smooth[path_other]

                # data_probe_hilbert_sum_combined[path] = data_probe_hilbert_sum[path] + data_probe_hilbert_sum[path_other]
                data_probe_hilbert_sum_baseline_mean_combined[path] = data_probe_hilbert_sum_baseline_mean[path]+data_probe_hilbert_sum_baseline_mean[path_other]

        else:
            for path in paths:
                data_probe_hilbert_sum_other[path] = np.nan
                data_probe_hilbert_sum_baseline_mean_other[path] = np.nan
                data_probe_hilbert_smooth_other[path] = np.nan
                data_probe_hilbert_sum_baseline_mean_combined[path] = np.nan



        spikes = {
        'data_ind':data_ind,
        'data_ind_hilbert':data_ind_hilbert,
        'data_ind_hilbert_sum':data_ind_hilbert_sum,
        'data_ind_hilbert_smooth':data_ind_hilbert_smooth,
        'data_ind_hilbert_sum_mean':data_ind_hilbert_sum_mean,
        'data_ind_hilbert_sum_norm':data_ind_hilbert_sum_norm,
        'data_ind_hilbert_sum_normsub':data_ind_hilbert_sum_normsub,
        'data_ind_hilbert_sum_norm_mean':data_ind_hilbert_sum_norm_mean,
        'data_ind_hilbert_sum_normsub_mean':data_ind_hilbert_sum_normsub_mean,
        'data_ind_hilbert_com':data_ind_hilbert_com,
        'data_ind_hilbert_com_smooth':data_ind_hilbert_com_smooth,
        'data_ind_hilbert_com_mean':data_ind_hilbert_com_mean,
        'data_ind_hilbert_sum_firstpulse':data_ind_hilbert_sum_firstpulse,
        'data_ind_hilbert_sum_secondpulse':data_ind_hilbert_sum_secondpulse,
        'data_ind_hilbert_sum_thirdpulse':data_ind_hilbert_sum_thirdpulse,
        'data_ind_hilbert_sum_fourthpulse':data_ind_hilbert_sum_fourthpulse,
        'data_ind_hilbert_sum_allpulse':data_ind_hilbert_sum_allpulse,
        'data_ind_hilbert_sum_firstpulse_norm':data_ind_hilbert_sum_firstpulse_norm,
        'data_ind_hilbert_sum_secondpulse_norm':data_ind_hilbert_sum_secondpulse_norm,
        'data_ind_hilbert_sum_thirdpulse_norm':data_ind_hilbert_sum_thirdpulse_norm,
        'data_ind_hilbert_sum_fourthpulse_norm':data_ind_hilbert_sum_fourthpulse_norm,
        'data_ind_hilbert_sum_allpulse_norm':data_ind_hilbert_sum_allpulse_norm,
        'data_ind_hilbert_sum_firstpulse_mean':data_ind_hilbert_sum_firstpulse_mean,
        'data_ind_hilbert_sum_secondpulse_mean':data_ind_hilbert_sum_secondpulse_mean,
        'data_ind_hilbert_sum_thirdpulse_mean':data_ind_hilbert_sum_thirdpulse_mean,
        'data_ind_hilbert_sum_fourthpulse_mean':data_ind_hilbert_sum_fourthpulse_mean,
        'data_ind_hilbert_sum_allpulse_mean':data_ind_hilbert_sum_allpulse_mean,
        'data_ind_hilbert_sum_firstpulse_norm_mean':data_ind_hilbert_sum_firstpulse_norm_mean,
        'data_ind_hilbert_sum_secondpulse_norm_mean':data_ind_hilbert_sum_secondpulse_norm_mean,
        'data_ind_hilbert_sum_thirdpulse_norm_mean':data_ind_hilbert_sum_thirdpulse_norm_mean,
        'data_ind_hilbert_sum_fourthpulse_norm_mean':data_ind_hilbert_sum_fourthpulse_norm_mean,
        'data_ind_hilbert_sum_allpulse_norm_mean':data_ind_hilbert_sum_allpulse_norm_mean,

        'data_ind_hilbert_sum_normsub_max':data_ind_hilbert_sum_normsub_max,
        'data_ind_hilbert_sum_normsub_var':data_ind_hilbert_sum_normsub_var,
        'data_probe':data_probe,
        'data_probe_hilbert':data_probe_hilbert,
        'data_probe_hilbert_sum':data_probe_hilbert_sum,
        'data_probe_hilbert_smooth':data_probe_hilbert_smooth,
        'data_probe_hilbert_sum_baseline_mean':data_probe_hilbert_sum_baseline_mean,
        'data_probe_hilbert_norm':data_probe_hilbert_norm,
        'data_probe_hilbert_sum_other':data_probe_hilbert_sum_other,
        'data_probe_hilbert_smooth_other':data_probe_hilbert_smooth_other,
        'data_probe_hilbert_sum_baseline_mean_other':data_probe_hilbert_sum_baseline_mean_other,
        # 'data_probe_hilbert_sum_combined':data_probe_hilbert_sum_combined,
        # 'data_probe_hilbert_smooth_combined':data_probe_hilbert_smooth_combined,
        'data_probe_hilbert_sum_baseline_mean_combined':data_probe_hilbert_sum_baseline_mean_combined,

        }

        spikes_df = functions._postdict2df(postdict=spikes, pre=pre)

        return spikes_df

    def _load_group_data(self, directory='', filename='spikes_df.pkl', df=True):
        """ Load group data from folder
        
        ===Args===
        -directory : directory where group data is stored including /
        -filename : file name for group data file, including .pkl
                    -file_name cannot contain the string 'data', since this string is used t search for individual data files
        -df : boolean, if true group data is assumed to be a pandas dataframe, otherwise it is assumed to be a nested dictionary

        ===Out===
        -group_data  : if df is True, group_data will be a pandas dataframe.  if no group data is found in the directory an empty dataframe is returned.  if df is False, group_data is returned as a nested dictionary, and if no data is found an empty dictionary is returned

        ===Updates===
        -none

        ===Comments===
        """
        
        # all files in directory
        files = os.listdir(directory)

        # if data file already exists
        if filename in files:
            print 'group data found:', filename

            # if stored as dataframe
            if df:
                # load dataframe
                group_data=pd.read_pickle(directory+filename)
                print 'group data loaded'
            # if stored as dictionary
            else:
                # load dictionary
                with open(directory+filename, 'rb') as pkl_file:
                    group_data= pickle.load(pkl_file)
                print 'group data loaded'

        # otherwise create data structure
        else:
            print 'no group data found'
            
            # if dataframe
            if df:
                # create empty dataframe
                group_data = pd.DataFrame()
            # else if dicitonary
            else:
                group_data= {}

        return group_data 
    
    def _process_new_data_df(self, group_df, preprocessed_directory='Preprocessed Data/', search_string='.pkl', variables=['slopes','slopes_norm','slopes_smooth'], file_limit=2):
        ''' process new data and add to group

        ==Args==
        -group_df : pandas dataframe containing group data
        -directory : relative directory containing unprocessed data
        -search_string :  string to identify unprocessed data, typically ".mat"
        -variables : variables to be derived from unprocessed data (e.g. slopes or slopes_norm)

        ==Out==
        -group_df : pandas dataframe containing group data

        ==Update==
        
        ==Comments==
        
        '''
        # get list of all data files
        data_files = glob.glob(preprocessed_directory+'*'+search_string+'*')
        # remove directory and file extension
        data_filenames = [file.split('\\')[-1].split('.')[0] for file in data_files]

        # get list of processed data files
        if group_df.empty:
            processed_data_filenames = []
        else:
            processed_data_filenames = group_df.name

        # get list of new data files
        new_data_filenames = list(set(data_filenames)-set(processed_data_filenames))
        new_data_files = [data_files[file_i] for file_i, file in enumerate(data_filenames) if file in new_data_filenames]

        print 'total data files:', len(data_files) 
        print 'new data files:', len(new_data_files)

        # iterate over new files and update group_data structure
        #`````````````````````````````````````````````````````````````````
        print 'updating group data structure'
        # dictionary for temporary storage of individual simulation data

        spike_funcs = SpikeFuncs()
        filter_name = 'iir_highpass_1000'
        # iterate over new data files
        for file_i, file in enumerate(new_data_files):

            name = file.split('\\')[-1].split('.')[0]
            date = int(name[:8])

            # limit number of files processed at a time
            if file_limit and file_i>file_limit:
                continue
            else:

                # load data file
                with open(file, 'rb') as pkl_file:

                    pre = pickle.load(pkl_file)

                    if 'soma' in pre['comment_dict'].keys():
                        # print name
                        spikes = spike_funcs._get_induction_spikes(preprocessed=pre, filter_name=filter_name)

                        for path  in pre['path_blocks']:
                            current_dict = functions._build_conditions_dict(pre, path)

                            current_dict['filename']=[file]
                            current_dict['name']=[name]
                            current_dict['date']=[date]

                            print spikes['data_probe_hilbert_sum_baseline_mean'][path]
                            # iterate over variables to be stored (e.g. slopes, slopes_norm)
                            for key in spikes:

                                # get data from preprocessed structure
                                current_dict[key]=[spikes[key][path]]

                            for key in current_dict:
                                if type(current_dict[key])==list and len(current_dict[key])>1:
                                    current_dict[key] = [current_dict[key]]
                                # print key, len(current_dict[key])
                            # convert to dataframe    
                            current_df = pd.DataFrame(current_dict)

                            # add to group data
                            group_df = group_df.append(current_df, ignore_index=True)

        return group_df

class Spikes:
    '''
    '''
    def __init__(self, directory='Variables/', filename='spikes_df.pkl', 
        pre_directory='Preprocessed Data/', file_limit=[]):
        '''
        '''
        self._process(directory=directory, filename=filename, pre_directory=pre_directory)
        # self.directory=directory
        # self.filename=filename
        # spike_funcs = SpikeFuncs()
        # self.group_df=functions._load_group_data(directory=directory, filename=filename, df=True)
        # self.group_df = spike_funcs._process_new_data_df(group_df=self.group_df, file_limit=file_limit)
        # self.group_df.to_pickle(directory+filename)

    def _process(self, directory='Variables/', filename='spikes_df.pkl', pre_directory='Preprocessed Data/', **kwargs):
        '''
        '''
        ############################################################
        # FIXME
        ############################################################
        self.spikefuncs = SpikeFuncs()
        funclist = [self.spikefuncs._get_induction_spikes_df]
        kwlist = [{'filter_name':'iir_high_300'}] 
        rerun= []#[self.spikefuncs._get_induction_spikes_df]#[self.spikefuncs._get_induction_spikes_df]
        # rerun=[]
        keep = ['remove', 'exp_fit_remove']
        # filename_temp = 'slopes_df_temp.pkl'
        self.directory=directory
        self.filename=filename
        self.filename_temp = 'spikes_df_temp.pkl'
        self.group_df = functions._load_group_data(directory, filename, df=True)
        self.group_df = functions._process_new_data_df(group_df=self.group_df, preprocessed_directory=pre_directory, search_string='.pkl', functions=funclist, kwlist=kwlist, rerun=rerun, keep=keep)
        
        df_funcs = functions.ApplyDF()
        colnames= ['data_ind_hilbert_smooth']
        colkeys=['data','ind','hilbert','sum',]
        colkeys_exclude=['mean', 'max', 'var', 'lastburst', 'firstburst']
        colnorm='data_probe_hilbert_sum_baseline_mean'
        # print df_spikes.data_ind_hilbert_smooth
        # self.group_df = df_funcs._normalize_column(df=self.group_df, colnames=colnames, colnorm=colnorm)
        # apply functions row wise to df
        #--------------------------------
        # self.group_df = df_funcs._last_burst(df=self.group_df, colnames=colnames, colkeys=colkeys, colkeys_exclude=colkeys_exclude)
        # self.group_df = df_funcs._first_burst(df=self.group_df, colnames=colnames, colkeys=colkeys, colkeys_exclude=colkeys_exclude)
        # self.group_df = df_funcs._fft(df=self.group_df, colnames=['data_ind_hilbert_sum_norm'], slice_i=slice(40, None), unwrap=False)
        # self.group_df = df_funcs._get_nth(df=self.group_df, colnames=['data_ind_hilbert_sum_norm_fft_angle'], n=13)
        self.group_df.to_pickle(directory+self.filename)

# df = Spikes(pre_directory='Preprocessed Data/', filename='spikes_df.pkl').group_df

# df = Spikes(pre_directory='Preprocessed Data 1Path/', filename='spikes_df_1path.pkl').group_df

df = Spikes(pre_directory='Preprocessed Data Mahima/', filename='spikes_df_mahima.pkl').group_df

if __name__=='__main__':

    df = Spikes().group_df