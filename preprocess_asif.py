# analyze asif data
import numpy as np
import glob
import pandas as pd
import functions
import pickle
from collections import OrderedDict

dc_directory = 'Asif TBS DCS/'
ac_directory = 'Asif TBS ACS/'
induction_info_filename = 'tbsindex.csv'
group_df_directory = 'Variables/'
group_df_filename = 'slopes_df_asif.pkl'

# list all files
dc_files = glob.glob(dc_directory+'*')
ac_files = glob.glob(ac_directory+'*')
all_files = dc_files+ac_files

# load induction info
induction_info = pd.read_csv(induction_info_filename)
# print induction_info

def _loadtextdata(textfile, splitkey='\r\n'):
    '''
    '''
    listy=[]
    for stringy in textfile.split(splitkey):
        # print stringy
        try:
            vally = float(stringy.split('-')[-1])
        except:
            continue
        listy.append(vally)

    return np.array(listy)

# iterate over files
group_df=pd.DataFrame()
# print dc_files
for file_i, file in enumerate(all_files):

    name  = file.split('\\')[-1]
    comments = name.split('.txt')[0].split('_')
    date = comments[0]
    # remove letters from date
    date = int(''.join([s for s in date if s.isdigit()]))
    # name  = file.split('\\')[-1]
    induction_pattern = 'TBS'
    induction_patter_other='nostim'

    # load each text file
    with open(file, 'rb') as textfile:
        textdata = textfile.read()

    slopes = _loadtextdata(textfile=textdata)

    # print slopes

    # print name, induction_info[induction_info.filename==name].tbsindex
    # get induction index subtract 1 for python style zero-indexing 
    ind_idx = induction_info[induction_info.filename==name].tbsindex.values[0]

    # print comments
    if 'an' in comments:
        polarity='anodal'
    elif 'ca' in comments:
        polarity='cathodal'
    elif 'Ctrl' in comments or 'ctrl' in comments:
        polarity='control'
    elif 'trough' in comments:
        polarity='trough'
    elif 'peak' in comments:
        polarity='peak'
    else:
        polarity='control'


    if file in dc_files:
        field_waveform = 'dc'
    elif file in ac_files:
        field_waveform = 'ac'

    # get field magnitude
    if not any(['Vm' in com for com in comments]):
        field_magnitude = '0'
    else:
        for com in comments:
            if 'Vm' in com:
                # print com.split('V')[0]
                field_magnitude = com.split('V')[0]
        
    # print slopes.shape
    slopes_smooth = functions._remove_outliers(time_series=slopes, ind_idx=[ind_idx], time_window=5, std_tol=3, include_ind=False)

    # print ind_idx.values
    slopes_baseline_mean = np.mean(slopes_smooth[ind_idx-20:ind_idx])

    slopes_norm = slopes_smooth/slopes_baseline_mean

    print ind_idx, slopes_norm.shape
    print ind_idx+60 > slopes_norm.shape

    slopes_norm_aligned = [slopes_norm[ind_idx-20:ind_idx+60]]

    ltp_final = np.mean(slopes_norm[ind_idx+50:ind_idx+60])

    path='path1'
    induction_location_0 = 'apical'
    experimenter='asif'
    remove=False

    current_dict = {
    'comments':[comments],
    'date':[date],
    'name':[name],
    'induction_pattern_0':[induction_pattern],
    'induction_pattern_other_0':[induction_patter_other],
    'slopes':[slopes],
    'ind_idx':[ind_idx],
    'field_mag_0':[field_magnitude],
    'field_polarity_0':[polarity],
    'path':[path],
    'field_waveform':[field_waveform],
    'slopes_smooth':[slopes_smooth],
    'slopes_norm':[slopes_norm],
    'ltp_final':[ltp_final],
    'slopes_norm_aligned_0':[slopes_norm_aligned],
    'induction_location_0':[induction_location_0],
    'experimenter':[experimenter],
    'remove':remove
    }

    current_df = pd.DataFrame(current_dict)

    if ind_idx+60 <= slopes_norm.shape:
        group_df = group_df.append(current_df, ignore_index=True)

group_df.to_pickle(group_df_directory+group_df_filename)

conditions = ['field_polarity_0','induction_pattern_0','induction_pattern_other_0']

constraints_spec = OrderedDict([
    ('date', {
        ('TBS','weak5Hz'):['>=',20181113],#20181113
        ('TBS','nostim'): ['>=',20181210],#20181210
        ('weak5Hz', 'nostim'):['>',20180920]#20180920
        })
    ]) 
# constraint applied to all conditions. this gets overwritten by specific constraints
constraints_all = OrderedDict([
    ])

df_sorted = functions._sortdf(df=group_df, conditions=conditions, constraints_all=constraints_all, constraints_spec=constraints_spec)

figures_any = True
figures = [('anodal','cathodal', 'control'), ('peak','trough','control')]
titles=OrderedDict(zip(figures,
    ['DC', 'AC']
    ))

colors = {'anodal':(1,0,.5), 'control':'k', 'cathodal':(0,1,1), 'peak':(0,1,1), 'trough':(1,0,.5)}
markers = {'TBS':'.'}

functions._plot_timeseries(df_sorted=df_sorted, figures=figures, variable='slopes_norm_aligned', colors=colors, markers=markers, titles=titles, mean=True, figures_any=figures_any)


