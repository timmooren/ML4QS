import pandas as pd
import random
import json


def create_snippets(df, snippet_length, freq):
    df = df.reset_index(drop=True)
    final_data = pd.DataFrame(columns=list(df.columns) + ["snippet"])
    groups = df.groupby("entry_num")

    # extract last 20 seconds snippet and random snippet per group
    for group_key, group in groups:
        ## last 20 seconds:

        # obtain last datapoint per group and snippet time interval
        last_sec = group["Time (s)"].iloc[-1]
        # print(last_sec)
        snippet_start = last_sec - snippet_length
        # print(snippet_start)

        # obtain the indices of the last 20 seconds
        mask = group["Time (s)"] > snippet_start
        df_20sec = group[mask]
        # indices = list(group.loc[mask].index)
        # print(len(df_20sec))

        # # add snippet to final dataset
        # df_20sec = group.loc[indices]
        df_20sec["snippet"] = "last_seconds"
        final_data = pd.concat([final_data, df_20sec], axis=0)

        ## random snippet:
        if group_key not in [39, 45]:

            # obtain possible indices for the random snippet
            indices = group.index[:-200].tolist()

            # obtain indices random snippet
            rand_start = random.choice(indices)
            rand_end = rand_start + (snippet_length * freq)

            random_20sec = group.loc[rand_start : rand_end - 1]
            # print(len(random_20sec))

            random_20sec.loc[:, "snippet"] = "random_snippet"
            random_20sec.loc[:, "fall_top"] = 0
            final_data = pd.concat([final_data, random_20sec], axis=0)

    final_data = final_data.reset_index(drop=True)

    return final_data


def change_climb_ID(df):
    df["climb_id"] = (
        df["entry_num"].astype(str)
        + "."
        + df["snippet"].replace({"last_seconds": "1", "random_snippet": "2"})
    )
    df = df.drop(columns=["entry_num", "snippet"])

    return df

    
def add_heart_rate(df):
    '''adds heart-rate data to processed dataframe (df with snippets)'''
    df_copy = df.copy()

    with open('heartrate/heart_rate-2023-06-07 copy.json', 'r') as f1: 
        hr_json1 = json.load(f1)
    with open('heartrate/heart_rate-2023-06-14 copy.json', 'r') as f2: 
        hr_json2 = json.load(f2)

    # put datetime & heart-rate values in a list 
    hr_data = [] 
    for heart_entry in (hr_json1 + hr_json2):
        dt = heart_entry['dateTime']
        hr = heart_entry['value']['bpm']
        hr_data.append((dt, hr))

    # prep fitbit datetimes 
    fitbit_datetimes = [x[0] for x in hr_data]
    fitbit_datetimes = pd.to_datetime(fitbit_datetimes)
    # prep fitbit heartreates 
    fitbit_heart_rates = [x[1] for x in hr_data]
    # prep datetime formats 
    df_copy['datetime'] = pd.to_datetime(df_copy['datetime'])
    df_copy['datetime'] = df_copy['datetime'].dt.tz_localize(None)

    mapping_dict = {}
    # iterates through each snippet 
    for group_name, group_data in df_copy.groupby("climb_id"):
        # gets all fitbit datetimes within snippet time interval 
        start_time = group_data.iloc[0]['datetime']
        end_time = group_data.iloc[-1]['datetime']
        fitbit_snippet_datetimes = fitbit_datetimes[(fitbit_datetimes >= start_time) & (fitbit_datetimes <= end_time)]
        # match each fitbit datetime to nearest datetime in the processed dataframe 
        for fitbit_dt in fitbit_snippet_datetimes:
            # datetime matching 
            closest_index = abs(df_copy['datetime'] - fitbit_dt).idxmin()
            data_closest_dt = df_copy.loc[closest_index, 'datetime']
            # get corresponding heart rate values & save mapping 
            hr_idx = fitbit_datetimes.get_loc(fitbit_dt)
            mapping_dict[data_closest_dt] = fitbit_heart_rates[hr_idx] 
    
    # Add new column by using HR to datetime mapping 
    df_copy['heart-rate'] = df_copy['datetime'].map(mapping_dict)

    # linear interpolation 
    df_copy['heart-rate'] = df_copy.groupby('climb_id', group_keys=False)['heart-rate'].apply(lambda x: x.interpolate(limit_direction='both'))

    return df_copy

def aggregate_rf(df):
    """aggregates rows grouped by climb ID for random forest model"""

    df_copy = df.copy()
    aggregation_method = {}
    sum_vars = ["Time (s)", "distance"]
    max_vars = ["climb_id", "name_climber", "num_attempt", "fall_top"]

    # maps variable to aggregation method
    for var in df_copy.columns:
        if var in sum_vars:
            aggregation_method[var] = "sum"
        elif var in max_vars:
            aggregation_method[
                var
            ] = "max"  # for categorical objects (same for every id)
        else:
            aggregation_method[var] = "mean"

    agg_df = df_copy.groupby("climb_id").agg(aggregation_method)

    return agg_df
