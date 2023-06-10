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


# plot_show_fall('../datasets/raw_data_sien.csv', [3, 4, 13, 14, 16, 24, 25])
# plot_show_fall('../datasets/raw_data_tim.csv', [9, 10, 11, 19, 22, 23])


# ffrom PIL import Image, ImageDraw

# Load the image
pic = Image.open("../plots/cutoff_fall_marker/gyro_fall_entrynum4.png")

# Get the image dimensions
image_width, image_height = pic.size

# Convert the desired length to pixels (assuming a standard DPI value of 96)
cm_to_pixels = lambda cm: int(cm * 96 / 2.54)
line_length_cm = 16 # Desired length of the line in cm
line_length_pixels = cm_to_pixels(line_length_cm)

# Calculate the line coordinates
x = 960  # X-coordinate of the vertical line
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
pic.save("../plots/cutoff_fall_marker/MARKER_gyro_fall_entrynum4.png")
