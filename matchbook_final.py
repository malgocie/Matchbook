# Matchbook - it's like Tinder but for books!

# Before starting please install Kaggle API
# Kaggle API info: https://www.kaggle.com/docs/api#getting-started-installation-&-authentication
# Kaggle API documentation https://github.com/Kaggle/kaggle-api

# Install Kaggle
    # the easiest way is using CLI tool > use command 'pip install kaggle' in the terminal
    # you may need to do pip install --user kaggle on Mac/Linux
# Authentication
    # go to the 'Account' tab of your user profile and select 'Create New Token'
    # this will trigger the download of kaggle.json, a file containing your API credentials
    # move the downloaded file to appropriate folder
        # Linux: $XDG_CONFIG_HOME/kaggle/kaggle.json (defaults to ~/.config/kaggle/kaggle.json). The path ~/.kaggle/kaggle.json which was used by older versions of the tool is also still supported.
        # Windows: C:\Users\<Windows-username>\.kaggle\kaggle.json - you can check the exact location, sans drive, with echo %HOMEPATH%.
        # Other: ~/.kaggle/kaggle.json

# Before downloading the dataset change directory in Terminal to a directory with the python file using 'cd DirectoryPath' command

# Downloading the dataset
    # info on downloading datasets from Kaggle: https://www.kaggle.com/docs/api#interacting-with-datasets
    # dataset: https://www.kaggle.com/datasets/dk123891/books-dataset-goodreadsmay-2024
    # to download the dataset use command > kaggle datasets download -d dk123891/books-dataset-goodreadsmay-2024

# To run this app you need to install all required libraries via terminal, some of them may be already installed

# Importing required libraries
import pandas as pd
import zipfile as zf
from pathlib import Path
import json
import easygui as eg
import sys
import numpy as np
888

# Unzip downloaded dataset to project directory
with zf.ZipFile('books-dataset-goodreadsmay-2024.zip') as zip_ref:
    file_path = Path('Book_Details.csv')
    # Checking if the data set is already unzipped
    if not file_path.exists():
        zip_ref.extractall()

# Creating DataFrame from csv file
books = pd.read_csv('Book_Details.csv')

# Creating simpler DataFrame
book_genres = pd.DataFrame(books, columns= ['author', 'book_title', 'book_details', 'num pages', 'genres'])

# Creating a data subset of eligible books based on chosen tags and age groups
def tags_and_ages_mask(field):
    field_as_list = json.loads(field.replace("'", '"'))
    return (tags | ages).issubset(field_as_list)

# Creating an exit window that will be called upon using cancel buttons
def exit_msg():
    message = "*** Have a nice read! ***"
    title = "Matchbook | It's like Tinder but for books!"
    msg = eg.msgbox(message, title)
    if msg:
        sys.exit()

# Main function showing random book based on chosen tags and age groups with GUI
def swipe():
    # Calling random row from a filtered DataFrame
    chosen_idx = np.random.choice(row_number, replace=True, size=1)
    book_rec = eligible_books.iloc[chosen_idx]
    book_title = book_rec['book_title']
    author = book_rec['author']
    rtitle = book_title + " by " + author
    #choices = ['Add to TBR', 'Continue swiping', 'Exit']
    output = eg.ccbox(rtitle, title = "Matchbook | It's like Tinder but for books!")
    if not output:
        exit_msg()

# Creating start menu GUI
menu_msg = "*** Matchbook ***\n\n""Where bookworms can find their match!"
menu_title = "Matchbook | It's like Tinder but for books!"
# Window with continue/cancel menu
menu = eg.ccbox(menu_msg,menu_title)
tags = {}
ages = {}

# What happens when chosing continue
if menu:
    # Window with age groups options
    q_ages = "\nPlease select your favourite age groups:\n***\n"
    t_ages = "Matchbook | It's like Tinder but for books!"
    list_ages = ["Young Adult", "Adult", "Middle Grade", "Childrens", "New Adult"]
    ages_l = eg.multchoicebox(q_ages, t_ages, list_ages)

    if ages_l:
        # Window with genres/tags options
        q_tags = "\nPlease select your favourite genres/tags:\n***\n"
        t_tags = "Matchbook | It's like Tinder but for books!"
        list_tags = ["Contemporary", "Fantasy", "Gothic", "Historical", "Horror", "Literary Fiction", "Memoir", "Mythology", "Mystery", "Nonfiction", "Poetry", "Political", "Romance", "Science Fiction", "Thriller"]
        tags_l = eg.multchoicebox(q_tags, t_tags, list_tags)

        if tags_l:
            tags = set(tags_l)
            ages = set(ages_l)
        else:
            exit_msg()
    else:
        exit_msg()
else:
    exit_msg()

# Creating filtered DataFrame
eligible_books = book_genres[book_genres['genres'].apply(tags_and_ages_mask)]
row_number = eligible_books.shape[0]

while True:
    swipe()