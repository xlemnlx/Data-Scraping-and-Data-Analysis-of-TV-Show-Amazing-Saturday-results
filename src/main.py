from data_gathering import main as data_gathering
from data_cleaning_merging import main as data_cleaning
from data_visualizations import main as data_visualization

def main():
    """
    This just runs all the files right after another to kind of automate the process.
    """
    data_gathering()
    data_cleaning()
    data_visualization()

if __name__ == "__main__":
    main()