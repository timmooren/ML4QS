import pandas as pd
import random

def create_snippets(df, snippet_length, freq):

    df = df.reset_index(drop = True)
    final_data = pd.DataFrame(columns = list(df.columns)+["snippet"])
    groups = df.groupby("entry_num")
    

    # extract last 20 seconds snippet and random snippet per group
    for _, group in groups:
        
        ## last 20 seconds:

        # obtain last datapoint per group and snippet time interval
        last_sec = group['Time (s)'].iloc[-1]
        snippet_start = last_sec - snippet_length

        # obtain the indices of the last 20 seconds 
        mask = group["Time (s)"] > snippet_start
        indices = list(group.loc[mask].index)

        # add snippet to final dataset
        df_20sec = group.loc[indices]
        df_20sec["snippet"] = "last_seconds"
        final_data = pd.concat([final_data, df_20sec], axis = 0)
        
        ## random snippet:

        # obtain possible indices for the random snippet
        indices = group.index[:-200].tolist()

        # obtain indices random snippet
        rand_start = random.choice(indices)
        rand_end = rand_start + (snippet_length * freq)

        random_20sec = group.loc[rand_start : rand_end]

        random_20sec.loc[:, "snippet"] = "random_snippet"
        random_20sec.loc[:, "fall_top"] = 0
        final_data = pd.concat([final_data, random_20sec], axis = 0)
    
    final_data = final_data.reset_index(drop = True)

    return final_data

def change_climb_ID(df):

    df['climb_id'] = df['entry_num'].astype(str) + '.' + df['snippet'].replace({"last_seconds": "1", "random_snippet": "2"})
    df = df.drop(columns = ['entry_num', 'snippet'])

    return df