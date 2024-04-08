# ----------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------
from custom_plot_settings import custom_plot_settings
from  datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ----------------------------------------------------------------------------------------------------
# Functions that are used by the main function.
# ----------------------------------------------------------------------------------------------------
def datetime_formatter() -> str:
    """A function used for naming output files.

    Returns:
        str: Returns the current time in String format already:\n\t\t"%H%M%S"
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%H%M%S")
    
    return formatted_datetime

def result_names_ordered_func(result_names: list) -> list[str]:
    """Makes the current list of result names to be in chronological order.

    Args:
        result_names (list): Raw list of results names. Might be unordered in some scenarios.

    Returns:
        list[str]: Chronological order of result names.
    """
    
    ordered_result_names: list = ["1st Try Success","2nd Try Success", "3rd Try Success", "Failed"]
    
    result_names_ordered: list = []
    
    for result in ordered_result_names:
        if result in result_names:
            result_names_ordered.append(result)
    
    return result_names_ordered

def plot_months_per_year(dataframe: pd.DataFrame) -> None:
    """Accepts a pandas dataframe and make plots of the months per year.

    Args:
        dataframe (pd.DataFrame): Data feed here must be the cleaned and merged data.
    """
    
    year_list = list(dataframe["Year"].unique())
    
    for per_year in year_list:
        # > Current datetime to be used for naming the saved plots.
        current_datetime = datetime_formatter()
        # Filtered dataframe base on the current year in the list.
        df_year = dataframe[dataframe["Year"] == per_year].copy()
        # A dataframe that will be use to handle the data of the inner for loop
        handler = pd.DataFrame()
        
        month_list = list(df_year["Month"].unique())
        # Just some rcParams setting to make the text bigger or smaller depending on how many months there is available.
        if len(month_list) > 6:
            mpl.rcParams["font.size"] = 14
        else:
            mpl.rcParams["font.size"] = 18
        # ----------------------------------------------------------------------------------------------------
        # This inner for loop is used to make the grouping of months in the filtered dataframe in order.
        # By default, if you used "groupby" to the whole dataframe, it will jumble the order of the months. 
        # This for loop ensures that the order the months is still in order while grouping it.
        # ----------------------------------------------------------------------------------------------------
        for per_month in month_list:
            df_months_inorder = df_year[df_year["Month"] == per_month]
            
            per_month_result = df_months_inorder.groupby(["Month", "Detailed Result"]).size().unstack()
            
            handler = pd.concat([handler, per_month_result], axis=0)
        # ----------------------------------------------------------------------------------------------------
        # > Reording the columns of the filtered -> grouped dataframe.
        # > Filling the NaN with "0" so that I could convert the Dtype to "int". This will prevent the values
        # to have decimals.
        # ----------------------------------------------------------------------------------------------------
        result_names = list(df_year["Detailed Result"].unique())
        result_names_ordered = result_names_ordered_func(result_names)
        
        df_results_per_month = handler[result_names_ordered].copy()
        df_results_per_month.fillna(0, inplace=True)
        df_results_per_month[result_names_ordered] = df_results_per_month[result_names_ordered].astype("int")
        # ----------------------------------------------------------------------------------------------------
        # > Applying the custom color settings based on how many Result names there is.
        # > Data plotting and other settings.
        # ----------------------------------------------------------------------------------------------------
        custom_colors = custom_plot_settings(result_names_ordered)
        ax = df_results_per_month.plot(kind="bar", stacked=True, colormap=custom_colors, rot=45)
        ax.grid(axis="y")
        plt.xlabel("Month", fontsize=18)
        plt.ylabel("Number of Occurrences", fontsize=18)
        plt.title(f"Consolidated results per Month\n(Year: {per_year})", fontsize=25)
        plt.legend(title="Result:", fontsize=12, bbox_to_anchor=(1, 1))
        # ----------------------------------------------------------------------------------------------------
        # This for loop gets the Results for each month, checks the value if its greater than 0. If it is, 
        # then it will be placed to the bar - centered. If its 0 or lower, then it will be just an empty string.
        # ----------------------------------------------------------------------------------------------------
        for c in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 0 else "" for v in c]
            
            ax.bar_label(c, labels=labels, label_type="center") # type: ignore
        # ----------------------------------------------------------------------------------------------------
        # Saves and show the plots.
        # ----------------------------------------------------------------------------------------------------
        # plt.savefig(f"../figures/Plot-Months-{per_year}.{current_datetime}.jpg",
        #             dpi=300,
        #             bbox_inches ="tight",
        #             pad_inches=0.5)
        plt.show()

def plot_years_per_month(dataframe: pd.DataFrame) -> None:
    """Accepts a pandas dataframe and make plots of the years per month.

    Args:
        dataframe (pd.DataFrame): Data feed here must be the cleaned and merged data.
    """
    
    # ----------------------------------------------------------------------------------------------------
    # > Getting the unique "Month" values (No repetition) to be loop and used as a filtering method to the 
    # dataframe.
    # ----------------------------------------------------------------------------------------------------
    month_list = ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"]

    for per_month in month_list:
        # > Current datetime to be used for naming the saved plots.
        current_datetime = datetime_formatter()
        # Filtered dataframe base on the current month in the list.
        df_current_month = dataframe[dataframe["Month"] == per_month]
        # A dataframe that will be use to handle the data of the inner for loop
        handler = pd.DataFrame()
        
        year_list = list(df_current_month["Year"].unique())
        # ----------------------------------------------------------------------------------------------------
        # This inner for loop is used to make the grouping of years in the filtered dataframe in order.
        # By default, if you used "groupby" to the whole dataframe, it will jumble the order of the years. 
        # This for loop ensures that the order the years is still in order while grouping it.
        # ----------------------------------------------------------------------------------------------------
        for per_year in year_list:
            df_year_inorder = df_current_month[df_current_month["Year"] == per_year]
            
            per_year_result = df_year_inorder.groupby(["Year", "Detailed Result"]).size().unstack()
            
            handler = pd.concat([handler, per_year_result], axis=0)
        # ----------------------------------------------------------------------------------------------------
        # > Reording the columns of the filtered -> grouped dataframe.
        # > Filling the NaN with "0" so that I could convert the Dtype to "int". This will prevent the values
        # to have decimals.
        # ----------------------------------------------------------------------------------------------------
        result_names = list(df_current_month["Detailed Result"].unique())
        result_names_ordered = result_names_ordered_func(result_names)
        
        df_results_per_year = handler[result_names_ordered].copy()
        df_results_per_year.fillna(0, inplace=True)
        df_results_per_year[result_names_ordered] = df_results_per_year[result_names_ordered].astype("int")
        # ----------------------------------------------------------------------------------------------------
        # Data plotting and settings.
        # ----------------------------------------------------------------------------------------------------
        custom_colors = custom_plot_settings(result_names_ordered)
        ax = df_results_per_year.plot(kind="bar", stacked=True, colormap=custom_colors, rot=45)
        ax.grid(axis="y")
        plt.xlabel("Year", fontsize=18)
        plt.ylabel("Number of Occurrences", fontsize=18)
        plt.title(f"Consolidated results per Year\n(Month: {per_month})", fontsize=25)
        plt.legend(title="Result:", fontsize=12, bbox_to_anchor=(1, 1))
        # ----------------------------------------------------------------------------------------------------
        # This for loop gets the Results for each month, checks the value if its greater than 0. If it is, 
        # then it will be placed to the bar - centered. If its 0 or lower, then it will be just an empty string.
        # ----------------------------------------------------------------------------------------------------
        for c in ax.containers:
            labels = [int(v.get_height()) if v.get_height() > 0 else "" for v in c]
            
            ax.bar_label(c, labels=labels, label_type="center") # type: ignore
        # ----------------------------------------------------------------------------------------------------
        # Saves and show the plots.
        # ----------------------------------------------------------------------------------------------------
        # plt.savefig(f"../figures/Plot-Years-{per_month}.{current_datetime}.jpg",
        #             dpi=300,
        #             bbox_inches ="tight",
        #             pad_inches=0.5)
        plt.show()

def plot_comparison_per_consolidated_year(dataframe: pd.DataFrame) -> None:
    """Accepts a pandas dataframe and make plots of the years.

    Args:
        dataframe (pd.DataFrame): Data feed here must be the cleaned and merged data.
    """
    
    # Current datetime to be used for naming the saved plots.
    current_datetime = datetime_formatter()
    # ----------------------------------------------------------------------------------------------------
    # This part of the code checks if the current iteration of the year has 12 months of data in it. If it
    # has, then it will be concatenated to the df_year which holds all the years with only 12 months in it.
    # ----------------------------------------------------------------------------------------------------
    year_list = list(dataframe["Year"].unique())
    df_year = pd.DataFrame()

    for year in year_list:
        df_current_year = dataframe[dataframe["Year"] == year]
        
        month_list = list(df_current_year["Month"].unique())
        
        if len(month_list) == 12:
            df_year = pd.concat([df_year, df_current_year], axis=0)
    # ----------------------------------------------------------------------------------------------------
    # This inner for loop is used to make the grouping of months in the filtered dataframe in order.
    # By default, if you used "groupby" to the whole dataframe, it will jumble the order of the months. 
    # This for loop ensures that the order the months is still in order while grouping it.
    # ----------------------------------------------------------------------------------------------------
    handler = pd.DataFrame()
    filtered_year_list = list(df_year["Year"].unique())

    for year in filtered_year_list:
        df_year_inorder = df_year[df_year["Year"] == year]
        
        per_year_result = df_year_inorder.groupby(["Year", "Detailed Result"]).size().unstack()
        
        handler = pd.concat([handler, per_year_result], axis=0)
    # ----------------------------------------------------------------------------------------------------
    # > Reording the columns of the filtered -> grouped dataframe.
    # > Filling the NaN with "0" so that I could convert the Dtype to "int". This will prevent the values
    # to have decimals.
    # ----------------------------------------------------------------------------------------------------
    result_names = list(df_year["Detailed Result"].unique())
    result_names_ordered = result_names_ordered_func(result_names)
    
    df_results_per_year = handler[result_names_ordered].copy()
    df_results_per_year.fillna(0, inplace=True)
    df_results_per_year[result_names_ordered] = df_results_per_year[result_names_ordered].astype("int")
    # ----------------------------------------------------------------------------------------------------
    # Data plotting and settings.
    # ----------------------------------------------------------------------------------------------------
    custom_colors = custom_plot_settings(result_names_ordered)
    ax = df_results_per_year.plot(kind="bar", stacked=True, colormap=custom_colors, rot=45)
    ax.grid(axis="y")
    plt.xlabel("Year", fontsize=18)
    plt.ylabel("Number of Occurrences", fontsize=18)
    plt.title(f"Consolidated results:\n{filtered_year_list[0]} to {filtered_year_list[-1]}", fontsize=25)
    plt.legend(title="Result:", fontsize=12, bbox_to_anchor=(1, 1))
    # ----------------------------------------------------------------------------------------------------
    # This for loop gets the Results for each year. Will be placed to the bar - centered.
    # ----------------------------------------------------------------------------------------------------
    for c in ax.containers:
        labels = [int(v.get_height()) for v in c]
        
        ax.bar_label(c, labels=labels, label_type="center") # type: ignore
    # ----------------------------------------------------------------------------------------------------
    # Saves and show the plot.
    # ----------------------------------------------------------------------------------------------------
    # plt.savefig(f"../figures/Plot-Consolidated-{filtered_year_list[0]}-to-{filtered_year_list[-1]}.{current_datetime}.jpg",
    #             dpi=300,
    #             bbox_inches ="tight",
    #             pad_inches=0.5)
    plt.show()

def plot_pie_consolidated_result_year(dataframe: pd.DataFrame) -> None:
    """
    Make a pie chart for the "Detailed Result" column of the dataframe.

    Args:
        dataframe (pd.DataFrame): Data feed here must be the cleaned and merged data.
    """
    # Current datetime to be used for naming the saved plots.
    current_datetime = datetime_formatter()
    # Making a copy of the dataframe with the column "Year" and "Detailed Result" only in it.
    df_year = dataframe[["Year", "Detailed Result"]].copy()
    # ----------------------------------------------------------------------------------------------------
    # Looping through each row and count the occurence of each result name
    # ----------------------------------------------------------------------------------------------------
    first_count: int = 0
    second_count: int = 0
    third_count: int = 0
    failed_count: int = 0
    
    for _, row in df_year.iterrows():
        current_row = row.copy()
        
        current_row_result = current_row["Detailed Result"]
        
        if current_row_result == "1st Try Success":
            first_count += 1
            continue
        
        if current_row_result == "2nd Try Success":
            second_count += 1
            continue
        
        if current_row_result == "3rd Try Success":
            third_count += 1
            continue
        
        if current_row_result == "Failed":
            failed_count += 1
            continue
    # Generating a ordered Result names in the case it is not.
    result_names = list(df_year["Detailed Result"].unique())
    result_names_ordered = result_names_ordered_func(result_names)
    # ----------------------------------------------------------------------------------------------------
    # Making a dataframe base of the ordered Result names and the count.
    # ----------------------------------------------------------------------------------------------------
    df_sum_result = pd.DataFrame()
    df_sum_result["Result"] = result_names_ordered
    df_sum_result["Count"] = [first_count, second_count, third_count, failed_count]
    # Setting the index to the "Result" column since "plot" doesn't take "int" as the index.
    df_sum_result = df_sum_result.set_index("Result")
    # ----------------------------------------------------------------------------------------------------
    # > Listing all the years. This is already in chronological order right from the start of the data 
    # scraping.
    # Applying custom color.
    # Plot settings.
    # ----------------------------------------------------------------------------------------------------
    filtered_year_list = list(df_year["Year"].unique())
    custom_cmap = custom_plot_settings(result_names_ordered)
    
    df_sum_result.plot(kind="pie", subplots=True, ylabel="", autopct='%1.1f%%', colormap=custom_cmap)
    plt.title(f"Results percentage:\n{filtered_year_list[0]} to {filtered_year_list[-1]}", fontsize=25)
    plt.legend(title="Result:", fontsize=16, loc="upper left", bbox_to_anchor=(-0.2, 1))
    # ----------------------------------------------------------------------------------------------------
    # Plot and saves it to the "figure" folder.
    # ----------------------------------------------------------------------------------------------------
    # plt.savefig(f"../figures/Plot-Result-Percentage-{filtered_year_list[0]}-to-{filtered_year_list[-1]}.{current_datetime}.jpg",
    #         dpi=300,
    #         bbox_inches ="tight",
    #         pad_inches=0.5)
    plt.show()

# ----------------------------------------------------------------------------------------------------
# Main function:
# ----------------------------------------------------------------------------------------------------
def main() -> None:
    """
    Main function for this file. Runs the functions that plots the data and saves it into "figures" folder.
    """
    df: pd.DataFrame = pd.read_csv("../data/merged/data_merged.csv")
    df = df.set_index("Episode #")
    
    plot_pie_consolidated_result_year(df)
    plot_comparison_per_consolidated_year(df)
    plot_months_per_year(df)
    plot_years_per_month(df)

if __name__ == "__main__":
    main()