# ----------------------------------------------------------------------------------------------------
# Imports:
# ----------------------------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import pandas as pd
import re

# ----------------------------------------------------------------------------------------------------
# RGB Values to be used as a reference in filtering the scraped results.
# ----------------------------------------------------------------------------------------------------
'''
                        RGB Values:
Success - 1st attempt - 171, 235, 198   -   Green   -   "background: rgb(171, 235, 198);    -   #ABEBC6"
Success - 2nd attempt - 174, 214, 241   -   Blue    -   "background: rgb(174, 214, 241);    -   #AED6F1"
Success - 3rd attempt - 230, 176, 170   -   Red     -   "background: rgb(230, 176, 170);    -   #E6B0AA"
Failed                - 210, 180, 222   -   Purple  -   "background: rgb(210, 180, 222);    -   #D2B4DE"
'''

# ----------------------------------------------------------------------------------------------------
# Collection of functions used by main.
# ----------------------------------------------------------------------------------------------------
def result_scraper_selenium(table: list) -> list:
    """This function scrapes the cells with color in each raw table.

    Args:
        table (list): A list containing raw tables.

    Returns:
        list: A list consisting of cells with color in it.
    """
    data_table_selenium = []

    for per_table in table:
        rows = per_table.find_elements(By.TAG_NAME, "tr")
        for per_row in rows:
            cells = per_row.find_elements(By.TAG_NAME, "td")
            for per_cell in cells:
                attri_value = per_cell.get_attribute("style")
                data_table_selenium.append(attri_value)
    
    return data_table_selenium

def results_cleaner(table: list) -> pd.DataFrame:
    """This cleans the data of the scraped by selenium. Creates a list with proper results names in it.
       Don't know if I will be using all the columns that I've made here. But its better to make many
       different columns than going back here to update my code.

    Args:
        table (list): The table ouput by result_scraper_selenium

    Returns:
        pd.DataFrame: A dataframe -> cleaned data for the results.
    """
    detailed_result_selenium = []
    general_result_selenium = []
    result_as_int_selenium = []
    
    for per_row in table:
        if per_row == "background: rgb(171, 235, 198);":
            detailed_result_selenium.append("1st Try Success")
            general_result_selenium.append("Success")
            result_as_int_selenium.append("1")
            continue
        if per_row == "background: rgb(174, 214, 241);":
            detailed_result_selenium.append("2nd Try Success")
            general_result_selenium.append("Success")
            result_as_int_selenium.append("2")
            continue
        if per_row == "background: rgb(230, 176, 170);":
            detailed_result_selenium.append("3rd Try Success")
            general_result_selenium.append("Success")
            result_as_int_selenium.append("3")
            continue
        if per_row == "background: rgb(210, 180, 222);":
            detailed_result_selenium.append("Failed")
            general_result_selenium.append("Failed")
            result_as_int_selenium.append("0")
            continue

    df_results = pd.DataFrame()
    df_results["Detailed Result"] = detailed_result_selenium
    df_results["General Result"] = general_result_selenium
    df_results["Result as Number"] = result_as_int_selenium
    
    return df_results

def string_formatter(text: str) -> str:
    """This removes the "Notes" / "HyperLink" in the text

    Args:
        text (str): Any text in the table. 

    Returns:
        str: Formatted string.
    """
    pattern = r"\[[a-z]{1,2}\]"
    
    handler = re.findall(pattern, text)
    if handler:
        text_list = list(text)
        filtered_list = []
        for per_char in text_list:
            if per_char == "[":
                break
            else:
                filtered_list.append(per_char)
        filtered_text = "".join(filtered_list).strip()
        return filtered_text
    else:
        return text

def month_extractor(text: str) -> str:
    """This function just retrieves the Date in the "Air Date" column. Might be useful
    in the data visualization.

    Args:
        text (str): Text in the "Air Date" column.

    Returns:
        str: Month in String format. To be inserted in the new column named "Month".
    """
    text_list = list(text)
    handler = []
    
    for per_char in text_list:
        if per_char.isalpha():
            handler.append(per_char)
    
    month = "".join(handler).strip()
    return month

def tables_scraper_pandas(table: list[pd.DataFrame]) -> pd.DataFrame:
    """After the pandas scraped the tables, this function will add two new columns
       that might be useful for the next step -> "Month" and "Year"
       This function also formats the texts by calling to another functions.

    Args:
        table (list[pd.DataFrame]): Dataframe consisting of tables scraped by Pandas.

    Returns:
        pd.DataFrame: Returns a semi-cleaned data. Will still output as RAW data.
    """
    consolidated_tables_pandas = pd.DataFrame()
    consolidated_tables_pandas["Year"] = [] # Adding two new column that might be useful for the next steps.
    consolidated_tables_pandas["Month"] = []

    year = 2018
    # Iterating through each table:
    for per_table in table:
        cleaned_table = []
        # Iterating through each row of the table. Applying the two functions above to this function.
        for _, row in per_table.iterrows():
            current_row = row.copy()
            
            current_episode = str(current_row["Ep."])
            filtered_episode = string_formatter(current_episode)
            current_row["Ep."] = filtered_episode
            
            current_date = str(current_row["Air Date"])
            filtered_date = string_formatter(current_date)
            current_row["Air Date"] = f"{filtered_date}, {year}"
            
            month = month_extractor(filtered_date)
            current_row["Month"] = month
            
            current_row["Year"] = str(year)
            
            current_song = str(current_row["Song Questions[b] + Snack Time Game[c]"])
            filtered_song = string_formatter(current_song)
            current_row["Song Questions[b] + Snack Time Game[c]"] = filtered_song
            
            cleaned_table.append(current_row.to_dict())
        year += 1
        cleaned_df = pd.DataFrame(cleaned_table)
        consolidated_tables_pandas = pd.concat([consolidated_tables_pandas, cleaned_df], axis=0)

    consolidated_tables_pandas = consolidated_tables_pandas.drop(
        ["Featured Market", "Dressing Theme Concept", "Guest(s)"], axis=1
        ).rename(
            columns={"Ep." : "Episode #", "Song Questions[b] + Snack Time Game[c]" : "Song Questions + Snack Time Game"}
            )

    columns_inorder = ["Episode #", "Song Questions + Snack Time Game", "Air Date", "Month", "Year"]
    df_arranged_columns = consolidated_tables_pandas[columns_inorder].copy()
    return df_arranged_columns

# ----------------------------------------------------------------------------------------------------
# Main function:
# ----------------------------------------------------------------------------------------------------
def main() -> None:
    """
    Main function of the file. This uses both selenium and pandas to scrape the results and tables from
    the webpage respectively. After that, another function will clean the data gathered by selenium. For
    the data gathered by the pandas, it will be semi-cleaned only. Will only be adding some new columns
    -> "Month" and "Year" that might be useful for the next step, and remove some "Notes" / "HyperLink" 
    in the text for each cell of the table.
    """
    # ----------------------------------------------------------------------------------------------------
    # Scraping Results using Selenium.
    # ----------------------------------------------------------------------------------------------------
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    page_url = "https://en.wikipedia.org/wiki/List_of_DoReMi_Market_episodes"

    driver.get(page_url)
    # Wait for 3 seconds to make sure that the webpage has been load properly.
    time.sleep(3)

    all_tables_selenium = driver.find_elements(by="xpath", value="//div[contains(@class, \"hidden-content mw-collapsible-content\")]")
    # This function get color values from td tag of the HTML:
    data_table_selenium = result_scraper_selenium(all_tables_selenium)

    driver.quit()

    # This function cleans the raw result gathered using Selenium.
    df_results = results_cleaner(data_table_selenium)
    df_results.to_csv("../data/cleaned/cleaned_result.csv", index=False)

    # ----------------------------------------------------------------------------------------------------
    # Gathering the tables and the texts using Pandas.
    # ----------------------------------------------------------------------------------------------------
    all_tables_pandas = pd.read_html(page_url)
    # Throwing the first one since its a table that is not needed.
    selected_tables = all_tables_pandas[1:].copy()

    df_tables_pandas = tables_scraper_pandas(selected_tables)

    df_tables_pandas.to_csv("../data/raw/raw_tables.csv", index=False)

if __name__ == "__main__":
    main()


"""
As of April 05, 2024, there's 308 episodes.
"""