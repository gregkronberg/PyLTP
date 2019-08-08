from scipy import signal
import numpy as np
import functions 
import glob
import pickle
import pandas as pd
import copy
import pdb

# timeseries
class VtraceFuncs:


    def __init__(self,):
        '''
        '''
        pass
        # self._process()

    def _get_vtrace(self, preprocessed, df=[], keep=[], **kwargs):# timing='data_probe', location='apical', data_type='data', **kwargs):
        '''
        '''
        # get data_type, timings, locations and assert that they are lists (will be iterated below)
        data_types = kwargs['data_type']
        if type(data_types)!=list:
            data_types = [data_types]
        timings=kwargs['timing']
        if type(timings)!=list:
            timings = [timings]
        locations=kwargs['location']
        if type(locations)!=list:
            locations = [locations]
        # index of voltage values to normalize each voltage trace to
        # if 'norm_idx' in kwargs:
        #     norm_idx=kwargs['norm_idx']
        # else:
        #     norm_idx=0
        # preprocessed data
        pre=preprocessed
        # preallocate
        
        
        vtrace={}
        # iterate over timings (e.g. 'data_probe', 'data_induction')
        for timing in timings:
            print pre[timing].keys()
            # if all keyword in locations, add all locations in the current slice. otherwise check for matches between the listed locations and the current slice
            if 'all' in locations:
                locations = list(set(pre[timing].keys()))
            else:
                # check for reccording locations in the current slice
                locations = list(set(locations) & set(pre[timing].keys()))
            print locations
            # iterate over recording locations ('apical', 'basal', 'soma')
            for location in locations:
                # iterate over data types
                for data_type in data_types:
                    data={}
                    data_aligned_0={}
                    if 'norm_idx' in kwargs and 'hilbert' not in data_type:
                        norm_idx=copy.copy(kwargs['norm_idx'])
                    else:
                        norm_idx=25
                    # iterate over bipolar stimulus pathways
                    for path in pre[timing][location]:
                        # print timing, location, data_type, path
                        # print sorted(pre[timing][location][path].keys())
                        # process induction traces
                        if 'induction' in timing:
                            # list with entry for each induction
                            data[path]=[]
                            # iterate over inductons
                            for induction_data in pre[timing][location][path][data_type]:
                                # print induction_data.shape
                                # if there is induction data
                                if len(induction_data)>0:
                                    if 'hilbert' in data_type:
                                        data[path].append(induction_data)
                                    if len(induction_data.shape)==2:
                                        # normalize induction traces
                                        data[path].append(induction_data - induction_data[norm_idx, :])
                                    elif len(induction_data.shape)==1:
                                        # normalize induction traces
                                        data[path].append(induction_data - induction_data[norm_idx])
                                # if no induction data, append empty array
                                else:
                                    data[path].append(induction_data)


                        # process probe traces
                        elif 'probe' in timing:
                            if 'sortby' in data_type:
                                data_type_probe = data_type.split('_sortby')[0]
                            else:
                                data_type_probe=data_type
                            # normalize data
                            data[path] = pre[timing][location][path][data_type_probe] - pre[timing][location][path][data_type_probe][norm_idx,:]
                            # get induction index
                            ind_idx_0 = pre['ind_idx'][path][0]
                            # indices to align data on
                            idx = range(ind_idx_0-20, ind_idx_0) + range(ind_idx_0+1, ind_idx_0+61) 
                            # data aligned to first dinduction
                            data_aligned_0[path] = data[path][:,idx]
                
                    # create dictionary key (to become df column) that reflects timing, type, location
                    data_key = timing+'_'+data_type+'_'+location
                    # print data_key
                    # update data dictionary
                    vtrace[data_key] = copy.deepcopy(data)
                    # if 'hilbert' in data_key:
                    #     pdb.set_trace()
                    #     print vtrace[data_key]
                    # add aligned data for probe traces
                    if 'probe' in timing:
                        vtrace[data_key+'_data_aligned_0']=copy.deepcopy(data_aligned_0)

        print sorted(vtrace.keys())
        # convert to df
        vtrace_df = functions._postdict2df(postdict=vtrace, pre=pre)
        # for key in vtrace_df:
        #     print key
        #     if 'hilbert' in key:
        #         pdb.set_trace()
        #         print vtrace_df[key][1]

        print vtrace_df.name

        return vtrace_df

class Vtrace:
    def __init__(self,):

        pass

    def _process(self, directory='Variables/', filename='vtrace_df.pkl', pre_directory='Preprocessed Data/', **kwargs):
        '''
        '''
        # FIXME allow for passing multiple locations and datatypes
        tracefuncs = VtraceFuncs()
        funclist = [tracefuncs._get_vtrace]
        kwlist = [
        {
        'timing':['data_probe','data_induction'],
        'location':['apical','basal','perforant','soma'],
        # 'data_type':['data_sortby_burst','data_filt_iir_high_5_sortby_burst','data_filt_iir_band_5_50_sortby_burst', 'data_filt_iir_high_600_sortby_burst'],
        'data_type':[],
        'norm_idx':17
        }]
        if 'kwlist' in kwargs:
            for kw_i, kw in enumerate(kwlist):
                kwlist[kw_i].update(kwargs['kwlist'][kw_i])
        rerun=[tracefuncs._get_vtrace]
        keep=[]
        self.group_df = functions._load_group_data(directory, filename, df=True)
        self.group_df = functions._process_new_data_df(group_df= self.group_df, preprocessed_directory= pre_directory, search_string= '.pkl', functions= funclist, kwlist= kwlist, rerun= rerun, keep= keep)
        # pdb.set_trace()
        # print self.group_df.data_induction_data_filt_iir_band_300_1000_hilbert_sortby_burst_apical[:10]
        self.group_df.to_pickle(directory+filename)

# datatypes = ['data_sortby_burst','data_filt_iir_high_5_sortby_burst','data_filt_iir_band_5_50_sortby_burst', 'data_filt_iir_high_300_sortby_burst']
# datatypes = [ 'data_filt_iir_high_300_sortby_burst']
datatypes = ['data_filt_iir_high_300_sortby_pulse']

for datatype in datatypes:
    kwlist=[{'data_type':[datatype]}]
    vtrace = Vtrace()
    vtrace._process(pre_directory='Preprocessed Data/', filename='vtrace_df_'+datatype+'.pkl', kwlist=kwlist)

    vtrace1 = Vtrace()
    vtrace1._process(pre_directory='Preprocessed Data 1Path/', filename='vtrace_df_1path_'+datatype+'.pkl', kwlist=kwlist)

# vtrace_1path = Vtrace()
# vtrace_1path._process(pre_directory='Preprocessed Data 1Path/', filename='vtrace_df_1path.pkl')

# vtrace = Vtrace()
# vtrace._process(pre_directory='Preprocessed Data/', filename='vtrace_df.pkl')

if __name__=='__main__':

    df = Vtrace().group_df