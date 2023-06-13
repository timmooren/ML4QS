import pandas as pd

def create_snippets(file, snippet_length):
    
    df = pd.read_csv(file)
    final_data = pd.DataFrame(columns = list(df.columns)+["snippet"])
    groups = df.groupby("entry_num")

    # extract last 20 seconds snippet
    for _, group in groups:
        
        # obtain last datapoint per group and obtain snippet
        last_sec = group['Time (s)'].iloc[-1]
        snippet_start = last_sec - snippet_length

        # obtain the indices of the last 20 seconds 
        mask = group["Time (s)"] > snippet_start
        indices = list(group.loc[mask].index)

        # add snippet to final dataset
        df_20sec = group.loc[indices]
        final_data["snippet"] = "last_seconds"
        final_data = pd.concat([final_data, df_20sec], axis=0)

        # remove this snippet from the original dataset (to avoid double picking)
        df.drop(indices, inplace = True)

        print(final_data)

    ### TODO: 
        # Noteer in de dataframe dat de 'last_sec" snipplet is en niet 'random_snipplet'

    ### TODO: 
        # add a random snippet per group (zorg ervoor dat je weet waar het laatste punt is waarvan je mag nemen (dus 20
        # sec voor het einde) en dan alles daarvoor mag je een random one kiezen en dan de volgende 20 sec nemen)
        # pick random index in the group 
        # Zorg dat de 'complete/fall' column nu in deze naar complete gaat omdat deze altijd gecompleet zijn


# create_snippets("../datasets/cut_data/cut_data_sien.csv", 20)
create_snippets("../datasets/raw_data_sien.csv", 20)