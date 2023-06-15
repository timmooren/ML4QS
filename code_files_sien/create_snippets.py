import pandas as pd
import random

def create_snippets(file, snippet_length, per_second):
    
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

        """eerdere manier"""
        mask = group["Time (s)"] <= random_snippet_max
        indices = list(group.loc[mask].index)

        rand_start = random.choice(indices)
        rand_end = rand_start + (snippet_length * per_second)
        
        
        random_20sec = group.loc[rand_start : rand_end-1]
        random_20sec["snippet"] = "random_snippet"
        random_20sec["fall_top"] = 0
        final_data = pd.concat([final_data, random_20sec], axis = 0)
        
        




    #     """Tims manier"""
    #     mask = group["Time (s)"] <= random_snippet_max
    #     group = group[mask]

    #     # set boundries of random snippet
    #     rand_start = random.choice(list(group["Time (s)"]))
    #     rand_end = rand_start + snippet_length

    #     # print(rand_start, rand_end)

    #     mask = (group["Time (s)"] >= rand_start) & (group["Time (s)"] <= rand_end)
    #     indices = list(group.loc[mask].index)
    #     random_20sec = group.loc[indices]
    #     random_20sec["snippet"] = "random_snippet"

    #     final_data = pd.concat([final_data, random_20sec], axis = 0)

    print(final_data[final_data['snippet'] == 'last_seconds'].shape[0])
    print(final_data[final_data['fall_top'] == 0].shape[0])

        # df.to_csv("../code_files_sien/datasets_for_me/completedf.csv", index = False)
    final_data.to_csv("../code_files_sien/datasets_for_me/someshit.csv", index = False)
        # # idk = group.loc[indices]
        # # print(idk)

        

    ### TODO: 
        # Noteer in de dataframe dat de 'last_sec" snipplet is en niet 'random_snipplet'

    ### TODO: 
        # add a random snippet per group (zorg ervoor dat je weet waar het laatste punt is waarvan je mag nemen (dus 20
        # sec voor het einde) en dan alles daarvoor mag je een random one kiezen en dan de volgende 20 sec nemen)
        # pick random index in the group 
        # Zorg dat de 'complete/fall' column nu in deze naar complete gaat omdat deze altijd gecompleet zijn
        ## check whether all the list( ) can also become sets

# create_snippets("../datasets/cut_data/cut_data_sien.csv", 20)
create_snippets("../datasets/cut_data/cut_data_sien.csv", 20, 5)

