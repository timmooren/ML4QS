import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


def plot_show_fall(file, fall_numbers):

    df = pd.read_csv(file)
    df["Time (s)"] = pd.to_datetime(df["Time (s)"], unit="s")
    groups = df.groupby("entry_num")

    for group, data in groups:

        if group in fall_numbers:
            
            last_20_sec = data.tail(100)
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.plot(last_20_sec["Time (s)"], last_20_sec['Y (m/s^2)'])
            ax.set_xlabel('Time')
            ax.set_ylabel('Acceleration on the Y-axis (m/s^2)')
            ax.set_title('Number {}'.format(group))

        
            plt.savefig(f"../plots/cutoff_fall_marker/gyro_fall_entrynum{group}.png")


def draw_line(image, save_name, line_length, line_coordinate):
    """ produced with chatgpt: draw line to see the falling point """ 

    # Load the image
    pic = Image.open(image)

    # Get the image dimensions
    image_width, image_height = pic.size

    # Convert the desired length to pixels (assuming a standard DPI value of 96)
    cm_to_pixels = lambda cm: int(cm * 96 / 2.54)
    line_length_cm =  line_length# Desired length of the line in cm
    line_length_pixels = cm_to_pixels(line_length_cm)

    # Calculate the line coordinates
    x = line_coordinate  # X-coordinate of the vertical line
    half_line_length_pixels = line_length_pixels / 2
    start_point = (x, int(image_height / 2 - half_line_length_pixels))  # Top point of the line
    end_point = (x, int(image_height / 2 + half_line_length_pixels))  # Bottom point of the line

    # Create a drawing object
    draw = ImageDraw.Draw(pic)

    # Specify the line color
    line_color = (255, 0, 0)  # Red color in RGB format

    # Draw the line on the image
    draw.line([start_point, end_point], fill=line_color, width=2)

    # Display the modified image
    pic.show()

    # Save the modified image
    pic.save(save_name)

def remove_fall_byindex(csv_file, index_list, save_to):

    """index_list: give indices of the rows that need to be dropped (+1 included)"""

    df = pd.read_csv(csv_file)

    for set in index_list:
        
        df.drop(range(set[0], set[1]), inplace = True)

    df.to_csv(save_to, index = False)

# def remove_fall_bytime()





### Run the following lines to plot the data of the falls 
# plot_show_fall('../datasets/raw_data_sien.csv', [3, 4, 13, 14, 16, 24, 25])
# plot_show_fall('../datasets/raw_data_tim.csv', [9, 10, 11, 19, 22, 23])


### Run for the following line to drop certain indices
# remove falls siens first dataset
remove_fall_byindex("../datasets/data_sien_time_change.csv", [[6624, 6631],[1544, 1554], [4714, 4727], [2951, 2970], [10457, 10466], [3837, 3846], [8035, 8047]], "../datasets/cut_data/cut_data_sien.csv")
remove_fall_byindex("../datasets/data_tim_time_change.csv", [[2365, 2380],[1598, 1604], [468, 482], [4848, 4863], [7185, 7198], [7642, 7667]], "../datasets/cut_data/cut_data_tim.csv")


### Run the following line to draw a line in a plot and save 
# draw_line("../plots/cutoff_fall_marker/gyro_fall_entrynum4.png", "../plots/cutoff_fall_marker/MARKER_gyro_fall_entrynum4.png", 16, 960)
