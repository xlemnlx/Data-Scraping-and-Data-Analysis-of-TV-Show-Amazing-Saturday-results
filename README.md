# Data Analysis of results for the TV Game Show "Amazing Saturday"

## Table of contents:
<a id="table-of-contents"></a>

1. [About the TV Game Show - Amazing Saturday](#heading-1)
2. [About the project](#heading-2)
3. [How the data was gathered?](#heading-3)
4. [Main plot and conclusion statement](#heading-4)
5. [Other plots example from different plot types](#heading-5)
6. [Project Structure](#heading-6)

<a id="heading-1"></a>

## [About the TV Game Show - Amazing Saturday](#table-of-contents)

It is a Korean TV Show, wherein fix casts will be playing as a whole team to guess song lyrics. They can eat delicious food as a prize if they successfully guess the correct lyrics of the song that they are guessing. Each episode contains two rounds of song lyrics guessing and a "Snack Time Game" in between the rounds. Each round, the team has three tries to guess the song. Every time they get the wrong answer, Haetnim, a well-known mukbang YouTube streamer in Korea, will eat a portion of the food. If they don't manage to successfully guess the lyrics by their third try, it is considered a failure, and Haetnmin will eat what is left in the food. 
[Wikipedia](https://en.wikipedia.org/wiki/DoReMi_Market)

<a id="heading-2"></a>

## [About the project](#table-of-contents)

This personal project of mine serves as an experience in data scraping and data analysis. I scraped this Wikipedia [webpage](https://en.wikipedia.org/wiki/List_of_DoReMi_Market_episodes), which contains the results for each round in each episode and also the data that I need for this project to make the data plots and data analysis.

This project only uses four external packages: Selenium, Webdriver-Manager, Pandas, and Matplotlib. Selenium, Webdriver-Manager, and Pandas are used to scrape data from the Wikipedia page. Pandas, again, are used to manage, manipulate, and clean the data from the dataframe. While the Matplotlib is used to make plots based on the cleaned and merged data that Selenium and Pandas scraped.

As of March 6, 2024, there's currently 308 episodes. So the data that I have in here is for episodes 1 to 308.

<a id="heading-3"></a>

## [How the data was gathered?](#table-of-contents)

I used Selenium in Python and Pandas. Selenium was used to scrape the Results - Colored cell of the tables for each year. While Pandas was used to scrape all the text in the table for each year.

<a id="heading-4"></a>

## [Main plot and conclusion statement](#table-of-contents)

<figure>
    <center><img src="/figures/Plot-Consolidated-2019-to-2023.154419.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results per year</figcaption></center>
</figure>

The reason why this plot doesn't have the results for years 2018 and 2024 is because those years don't have data for the whole year - 12 months. I code the function that plots this to consider only those years with a whole year of data so that all data interpretation will be based on data with a whole year of data only.

With this plot, we can see that the whole team is mostly and more likely to guess the correct lyrics by their second try. Their success on their first try is also not that bad. As for their third try and failing the round, we can say that they are more likely to fail if they are already in their third try than actually successfully guessing the lyrics. These will further be strengthen with the other plots from the other functions that I made.

<a id="heading-5"></a>

#### [Other plots example from different plot types](#table-of-contents)

<figure>
    <center><img src="/figures/Plot-Months-2018.155440.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results per month. Year: 2018</figcaption></center>
</figure>

<figure>
    <center><img src="/figures/Plot-Months-2023.155445.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results per month. Year: 2023</figcaption></center>
</figure>

<figure>
    <center><img src="/figures/Plot-Months-2024.155446.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results per month. Year: 2024</figcaption></center>
</figure>

This plots are from a function that sums the results per month in each year. There are other plot that I didn't include here since its going to take a lot of space. The statement I made earlier still holds true, as we can see here. While the month of April from 2018 has a lot of success in their thrid try, it is because its their launch month. And the "Snack Time Game" segment between the two round still hasn't been implemented in that Month. Instead, they have three rounds of song lyrics guessing game.

<figure>
    <center><img src="/figures/Plot-Years-August.155956.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results each year. Month: August</figcaption></center>
</figure>

<figure>
    <center><img src="/figures/Plot-Years-February.155952.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results each year. Month: February</figcaption></center>
</figure>

<figure>
    <center><img src="/figures/Plot-Years-May.155954.jpg", width="900", height="900"></center>
    <center><figcaption>Summation of results each year. Month: May</figcaption></center>
</figure>

This is the final function. This function plots each month with data from different years. In these plots, we can see how the whole team performed through the years in the same month. As for the other plots,they are located in the "figures" folder of this project.

<a id="heading-6"></a>

## [Project Structure](#table-of-contents)

```
├── README.md                  <- This README. Top level README.
├── data
│   ├── merged                 <- Merged data from two cleaned data.
│   ├── cleaned                <- Cleaned data.
│   └── raw                    <- The original, immutable data dump.
│
│
├── figures                    <- This is where the plots are saved. 
│
│
├── notebooks                  <- Jupyter notebooks. 
│   ├── data_gathering.ipynb           <- Jupyter Notebook version of the "data_gathering.py". With some Markdown for added explanations.
│   │   
│   ├── data_cleaning_merging.ipynb    <- Jupyter Notebook version of the "data_data_cleaning_merging.py". With some Markdown for added explanations.
│   │   
│   ├── data_visualization.ipynb       <- Jupyter Notebook version of the "data_visualization.py". With some Markdown for added explanations.
│
│
├── src                        <- Source codes use in this project.
│   ├── __init__.py                    <- Makes src a Python module.
│   │
│   ├── main.py                        <- Main script that runs the three "data" py files one after another.
│   │   
│   ├── data_gathering.py              <- Script that scrape the data from the Wikipedia using Selenium and Pandas.
│   │   
│   ├── data_cleaning_merging.py       <- Script to cleaning the raw data and merging dataframes.
│   │   
│   ├── data_visualization.py          <- Script that plots the data from a cleaned and merged data.
│   │   
│   ├── custom_plot_settings.py        <- A custom plot setting of mine.
│   
```

## Thank you for visiting!