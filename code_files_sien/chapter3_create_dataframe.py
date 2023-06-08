import pandas as pd
import os

def file_to_df(filepath, files, test = True):

    """
    Combine the data of the files per folder (e.g. Gyroscope.csv, Linear Accelerometer.csv in folder ../climb_data_phyphox/sien/climb_phy_5_sien)
    Returns df with all the data
    the if-else statement can be deleted when completely sure the function works, its just to not have to fill in all the info
    """

    # initiate empty df as final df
    final = pd.DataFrame(columns = ["entry_num", "name_climber", "grading", "num_attempt", "fall_top", "climbers_rating"])
    
    # combine data from selected files into the final dataframe
    for file in files:
        df_data = pd.read_csv(f"{filepath}/{file}")
        final = pd.concat([df_data, final], axis=1)

    # for now there is this test so not all the info needs to be written yet
    # enter the climb number for indexing
    if test:
        final["entry_num"] = input("what is the entry nummer? (num) ")

    # enter all the other data
    else:
        final["name_climber"] = input("name climber? (no caps) ")
        final["grading"] = input("official grading? (num+no_cap_letter) ")
        final["num_attempt"] = input("how manyth time climbing? (num) ")
        final["fall_top"] = input("fall (1) or top (0)?")
        final["climbers_rating"] = input("easy/medium/hard? (no caps)")

    # set the climb number as (multi?)index
    final = final.set_index("entry_num")
    
    
    ### TODO: preferably this:
    # final = final.reset_index() might want to keep the original index too! 
    # so multi-index would be best

    return final
                          

def list_df_files(filepath, filenames, fillin_df, all_files = True):

    """
    Takes a filepath to a folder of a climber with the containing e.g. gyroscope data (e.g. "../climb_data_phyphox/sien"),
    filenames of data that needs to be collected, an empty or previously generated dataframe (empty in the beginning, 
    but previously made csv files with all this data can be used too if we climb more during this project), and an option to
    only add a selection of files or all of them in that folder.
    Returns a csv file, saved with all the data necessary for analysis
    """

    # only if all files in the folder need to be processed
    if all_files:

        # create a list of folders (e.g. folder climb_phy_5_sien)
        list_folder = [folder for folder in os.listdir(filepath)]
        list_folder.remove(".DS_Store")

        # search through folders for the necessary files ("Gyroscope.csv", "Linear Accelerometer.csv")
        for folder in list_folder:

            # print the folder to know which data needs to be filled in
            print(folder)
            
            # create a df of the files and add it to the final (fill-in) df
            current_filepath = f"{filepath}/{folder}"
            df = file_to_df(filepath = current_filepath, files = filenames, test= True)
            fillin_df = pd.concat([fillin_df, df])
            

    #### TODO: if only selection of files
    #### TODO: still need to save to csv

    return fillin_df


df = pd.DataFrame()
# print(file_to_df("../climb_data_phyphox/sien/climb_phy_5_sien", ["Gyroscope.csv", "Linear Accelerometer.csv"], test = True))
print(list_df_files(filepath = "../climb_data_phyphox/sien", filenames = ["Gyroscope.csv", "Linear Accelerometer.csv"], fillin_df = df))

