import numpy as np 
import pandas as pd
import re
from pathlib import Path 

def combine_start_dfs(df1, df2, df3, df4):
    '''concatenates start dataframes from sien & tim'''
    return pd.concat([df1.copy(), df2.copy(), df3.copy(), df4.copy()])


def drop_climber_rating(df):
    '''removes climber rating variable'''
    df_copy = df.copy()
    return df_copy.drop(columns=['climbers_rating'])


def add_datetime(df):
    '''
    adds datetime variable to df by interplating start & end datetime from phyphox metadata. 
    @phyphox_dir: encompassing directory of phyphox data files
    '''
    df_copy = df.copy()
    phyphox_dir = Path('climb_data_phyphox') # relative path 

    # subdirectories 
    subdir_sien = phyphox_dir.joinpath('sien')
    subdir_tim = phyphox_dir.joinpath('tim')

    # -- generate mapping from climb ID to start/end datetimes -- 
    datetime_dict = {}
    # get start & end datetimes for each climb entry 
    for climber in (subdir_sien, subdir_tim):
        # dirs for each climb 
        for climb_dir in climber.iterdir():
            if climb_dir.name == '.DS_Store': continue 
            # get climb entry number
            entry_num = int(re.findall(r'\d+', climb_dir.name)[0])
            # metadata dir 
            metadir = climb_dir.joinpath('meta')
            # open time file 
            with open(metadir.joinpath('time.csv'), 'r') as datetime_file:
                # put start & end time into dict 
                datetime_df = pd.read_csv(datetime_file)
                start_time, end_time = datetime_df['system time text'][0], datetime_df['system time text'][1]
                datetime_dict[entry_num] = (start_time, end_time)

    # -- generate mapping from climb ID to datetime sequences -- 
    datetime_sequence_dict = {}
    for group_name, group_data in df_copy.groupby('entry_num'):
        # create & save datetime sequence for each climb entry 
        start_datetime, end_datetime = pd.to_datetime(datetime_dict[group_name][0]), pd.to_datetime(datetime_dict[group_name][1])
        datetime_range = pd.date_range(start=start_datetime, end=end_datetime, periods=len(group_data))
        datetime_sequence_dict[group_name] = datetime_range

    # inits null datetime var
    if not 'datetime' in df_copy:
        df_copy.insert(1, 'datetime', float('nan'))

    # fills in datetime sequences 
    for entry_id in df_copy['entry_num'].unique():
        mask = df_copy['entry_num'] == entry_id
        df_copy.loc[mask, 'datetime'] = datetime_sequence_dict[entry_id]

    return df_copy


def add_heartrate(df):
    '''
    adds heartrate data from fitbit to dataframe
    '''
    # TODO: need data from eva or sien or idk how we get it. 
    # TODO: decide on interpolation method 
    pass 


def cut_fall(df):
    '''
    removes falls from the dataframe. fall cutoffs were determined manually. 
    @cut_lst: list of list containing climb ID & cutoff point (in seconds) 
    '''
    df_copy = df.copy()
    cut_lst = [
        [3, 153.2797517], [4, 189.9308711], [13, 68.81188696], [14, 99.74502792], [16, 123.9687483], [25, 174.5428594], [24, 282.813116], #sien
        [33, 486.73], [35, 164.48], [36, 116.27], [37, 516.16], [44, 155.21], [45, 33.35], [47, 115.98], #sien2
        [9, 153.0813127],[10, 224.6286238], [11, 94.31351708], [19, 153.0707448], [22, 60.91507088], [23, 89.37636454], #tim 
        [28, 84.07], [30, 41.37], [31, 159.29], [38, 111.05], [39, 23.91], [41, 76.6] #tim2

               ]
    
    for item in cut_lst:
        # climb ID & cut times
        entry_num = item[0]
        cut_time = item[1]
        # get indices & drop 
        idx = list(df.index[(df["entry_num"] == entry_num) & (df["Time (s)"] >= cut_time)])
        df_copy = df_copy.drop(idx)

    return df_copy



        

    
    




