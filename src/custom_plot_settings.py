import matplotlib.pyplot as plt
import matplotlib as mpl

def custom_plot_settings(result_names: list[str]):
    """Accepts a list of string that contains the current result names.
    Outputs a custom color based in the result names.

    Args:
        result_names (list[str]): Result names

    Returns:
        matplotlib.colors.ListedColormap: Custom Colormap.
    """
    color_dict = {"1st Try Success" : "#ABEBC6", "2nd Try Success" : "#AED6F1", "3rd Try Success" : "#E6B0AA", "Failed" : "#D2B4DE"}
    
    colors = []
    
    for result_name in result_names:
        if result_name in color_dict.keys():
            colors.append(color_dict[result_name])
    
    custom_colors = plt.cm.colors.ListedColormap(colors) # type: ignore

    mpl.rcParams["figure.dpi"] = 150
    mpl.rcParams["figure.figsize"] = (10, 10)
    mpl.rcParams["font.size"] = 14
    
    return custom_colors

if __name__ == "__main__":
    # Just a test case.
    result_names = ["1st Try Success", "2nd Try Success", "3rd Try Success", "Failed"]
    custom_colors = custom_plot_settings(result_names)