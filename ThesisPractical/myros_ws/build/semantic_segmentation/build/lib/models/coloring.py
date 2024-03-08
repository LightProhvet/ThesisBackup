import colorsys


# Function to generate RGB colors from HSV values
def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


# Generate a list of 200 RGB colors with better distinctiveness
rgb_colors_200_better = [hsv_to_rgb(i / 200, 1.0, 1.0) for i in range(200)]


rgb_colors_20 = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (128, 0, 0),      # Maroon
    (0, 128, 0),      # Olive
    (0, 0, 128),      # Navy
    (128, 128, 0),    # Olive Green
    (128, 0, 128),    # Purple
    (0, 128, 128),    # Teal
    (128, 128, 128),  # Gray
    (192, 192, 192),  # Silver
    (128, 64, 0),     # Brown
    (255, 165, 0),    # Orange
    (0, 128, 64),     # Dark Green
    (255, 140, 105),  # Salmon
    (255, 192, 203),  # Pink
    (75, 0, 130),     # Indigo
]

# colormap = [({key: colormap},{item: colormap}) for key, item in a.items()]
# i = 0
# colordict = {}
# for key, item in classes.items():
#     colormap = rgb_colors_20[i]
#     i += 1
#     colordict[key] = colormap
#     colordict[item] = colormap
