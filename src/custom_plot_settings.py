import matplotlib.pyplot as plt
import matplotlib as mpl

def custom_plot_settings():
    custom_colors = plt.cm.colors.ListedColormap( # type: ignore
        ["#ABEBC6", "#AED6F1", "#E6B0AA", "#D2B4DE"]
        )

    mpl.rcParams["figure.dpi"] = 150
    mpl.rcParams["figure.figsize"] = (10, 10)
    mpl.rcParams["font.size"] = 14
    
    return custom_colors