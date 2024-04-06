# ----------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------
import pandas as pd
import re

# ----------------------------------------------------------------------------------------------------
# Functions that are used by the main function.
# ----------------------------------------------------------------------------------------------------
def song_catcher(text: str) -> bool:
    """Accepts a string and determines if its a song or not based on the format "String - String".

    Args:
        text (str): A string to be determine if its a song or not.

    Returns:
        bool: True -> It is a song.\n\t\tFalse -> Not a song.
    """
    pattern = r"[a-zA-Z0-9`~!@#$%^&*)(=+_\}{';:.>,<?/-Â] - [a-zA-Z0-9`~!@#$%^&*)(=+_\}{';:.>,<?/-Â]|[a-zA-Z0-9`~!@#$%^&*)(=+_\}{';:.>,<?/-Â] -[a-zA-Z0-9`~!@#$%^&*)(=+_\}{';:.>,<?/-Â]"
    is_it_a_song = False
    
    matched = re.findall(pattern, text)
    if matched:
        is_it_a_song = True
        return is_it_a_song
    else:
        return is_it_a_song

def song_remover(text: str) -> bool:
    """Accepts a string and determines if its a song to be 
    remove or not since not all song has a result in it.

    Args:
        text (str): A string to be determine if its to be remove or not.

    Returns:
        bool: True -> Remove the song.\n\t\tFalse -> Don't remove the song.
    """
    # This list contains the songs with no Result in it.
    song_list = [
        "Jin (BTS) - Super Tuna",
        "Badkiz - Ear Attack",
        "DJ DOC - Let's Go to the Beach",
        "BTS - Airplane pt.2",
        "Deux - We Are",
        "TXT - New Rules",
        "Turbo - Only Seventeen",
        "Lee Seung-yoon - Some Some Some",
        "TBA - TBA"
    ]
    
    remove_song = False
    
    if text in song_list:
        remove_song = True
        return remove_song
    
    return remove_song

# ----------------------------------------------------------------------------------------------------
# Main function:
# ----------------------------------------------------------------------------------------------------
def main() -> None:
    """
    Main function of the file. Loads the csv as dataframe then determines each row in "Song" if its a song.
    Outputs a file that is cleaned -> filtered data wherein all the data are just songs with results in it.
    """
    df_results = pd.read_csv("../data/cleaned/cleaned_result.csv")
    df_tables = pd.read_csv("../data/raw/raw_tables.csv")

    songs_handler = []

    for _, row in df_tables.iterrows():
        current_row = row.copy()
        current_song = str(current_row["Song Questions + Snack Time Game"])
        
        remove_song = song_remover(current_song)
        if remove_song is True:
            continue
        
        is_it_a_song = song_catcher(current_song)
        if is_it_a_song is True:
            songs_handler.append(current_row.to_dict())

    df_table_songs = pd.DataFrame(songs_handler)

    df_merged = pd.concat([df_table_songs, df_results], axis=1)
    columns_inorder = ["Episode #", "Song Questions + Snack Time Game", "Air Date", "Month", "Year", "Detailed Result", "General Result", "Result as Number"]
    df_merged[columns_inorder] = df_merged[columns_inorder].astype("object")

    df_table_songs.to_csv("../data/cleaned/cleaned_tables.csv", index=False)
    df_merged.to_csv("../data/merged/data_merged.csv", index=False)

if __name__ == "__main__":
    main()


"""
The above code works. I just want to insert here the problems that I've faced while solving those:

This are the list that are "uncatched" because of their format:
62	-	Apink - %% (Eung Eung)
64	-	Bolbbalgan4 - #First Love
155	-	H.O.T. - Warrior's Descendant
181	-	S.E.S. - Twilight Zone
183	-	CL - +HWA+
214	-	H.O.T. - Delight
268	-	S.E.S. - Rock'N Country
-> How did I solved this?
    -> I just update my pattern used for RegEx.
    -> Also, "Apink - %% (Eung Eung)" is "Apink -Â %% (Eung Eung)" in the raw data. I've also added this to the pattern used for RegEx.

This are the list of songs that needs to be removed since there is no result in these songs:
200	-	Jin (BTS) - Super Tuna
207	-	Badkiz - Ear Attack
224	-	DJ DOC - Let's Go to the Beach
244	-	BTS - Airplane pt.2
245	-	Deux - We Are
258	-	TXT - New Rules
261	-	Turbo - Only Seventeen
300	-	Lee Seung-yoon - Some Some Some
-> How did I solved this?
    -> Created a function, put this in a list. Then for loop.
"""