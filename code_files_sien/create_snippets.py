import pandas as pd
import random

def create_snippets(file, snippet_length, per_second):
    
    """
    
    """
    df = pd.read_csv(file)
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

        # remove this snippet from the original dataset (to avoid double picking)
        group.drop(indices, inplace = True)
        
        ## random snippet:

        # set last possible initial snippet point
        random_snippet_max = snippet_start - snippet_length


        mask = group["Time (s)"] <= random_snippet_max
        indices = list(group.loc[mask].index)

        rand_start = random.choice(indices)
        rand_end = rand_start + (snippet_length * per_second)
        
        
        random_20sec = group.loc[rand_start : rand_end-1]
        random_20sec["snippet"] = "random_snippet"
        random_20sec["fall_top"] = 0
        final_data = pd.concat([final_data, random_20sec], axis = 0)
        

create_snippets("../datasets/cut_data/cut_data_sien.csv", 20, 5)

