import pandas as pd
from datetime import datetime

data = {
    'number': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'time': [
        datetime(1970, 1, 1, 0, 0, 5, 624264750),
        datetime(1970, 1, 1, 0, 0, 10, 624264750),
        datetime(1970, 1, 1, 0, 0, 1, 624264750),
        datetime(1970, 1, 1, 0, 0, 3, 624264750),
        datetime(1970, 1, 1, 0, 0, 40, 624264750),
        datetime(1970, 1, 1, 0, 0, 1, 624264750),
        datetime(1970, 1, 1, 0, 0, 3, 624264750),
        datetime(1970, 1, 1, 0, 0, 3, 624264750),
        datetime(1970, 1, 1, 0, 0, 3, 624264750)
    ]
}

df = pd.DataFrame(data)

comparison_time = datetime(1970, 1, 1, 0, 0, 3, 624264750)

# Select the desired number
selected_number = 2

# Filter the dataframe by the selected number and the time threshold
filtered_df = df[(df['number'] == selected_number) & (df['time'] > comparison_time)]

# Get the index of the first row from the filtered dataframe
first_row_index = filtered_df.index[0]

print(first_row_index)
