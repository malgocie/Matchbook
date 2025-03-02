# Matchbook - it's like Tinder but for books
This app was written during Code First Girls Intro to Python course. The code is far from perfect though I've learnt a lot along the way and I intend on working on it further.

The main idea was to create a book recommendation system that will work similarly to tinder algorythm - the user is creating a profile with their preferences and possibly their goodreads data. Based on both they would get a book recommended, "match" would save the book to the tbr list. During the course my time was very restricted so I had to compromise to meet the deadline and had to scratch some of the functionalities. This is a very lite version that still needs a lot of work to be done.

## First steps - downloading data and setup for IDE
Sadly Goodreads stoped sharing their API so I've downloaded Books_Dataset_GoodReads(May 2024) by Grimm using Kaggle API. I've also used multiple pips:
- zipfile and pathlib to manipulate the downloaded zip files
- numpy and pandas to manipulate data
- easugui to create a simple user interface

### Before starting please install Kaggle API
- Kaggle API info: https://www.kaggle.com/docs/api#getting-started-installation-&-authentication
- Kaggle API documentation https://github.com/Kaggle/kaggle-api

### Installing Kaggle
- the easiest way is using CLI tool > use command 'pip install kaggle' in the terminal
- you may need to do pip install --user kaggle on Mac/Linux
  
### Authentication
- go to the 'Account' tab of your user profile and select 'Create New Token'
- this will trigger the download of kaggle.json, a file containing your API credentials
- move the downloaded file to appropriate folder
  - Linux: $XDG_CONFIG_HOME/kaggle/kaggle.json (defaults to ~/.config/kaggle/kaggle.json). The path ~/.kaggle/kaggle.json which was used by older versions of the tool is also still supported.
  - Windows: C:\Users\<Windows-username>\.kaggle\kaggle.json - you can check the exact location, sans drive, with echo %HOMEPATH%.
  - Other: ~/.kaggle/kaggle.json

Before downloading the dataset change directory in Terminal to a directory with the python file using 'cd DirectoryPath' command

### Downloading the dataset
- info on downloading datasets from Kaggle: https://www.kaggle.com/docs/api#interacting-with-datasets
- dataset: https://www.kaggle.com/datasets/dk123891/books-dataset-goodreadsmay-2024
- to download the dataset use command > kaggle datasets download -d dk123891/books-dataset-goodreadsmay-2024

### Installing and importing required libraries
To run this app you need to install all required libraries via terminal, some of them may be already installed
```python
# Installing via console standard package for creating gui
!pip install easygui
# Importing required libraries
import pandas as pd
import zipfile as zf
from pathlib import Path
import json
import easygui as eg
import sys
import numpy as np
```
### Unziping dowloaded dataset 

```python
# Unzip downloaded dataset to project directory
with zf.ZipFile('books-dataset-goodreadsmay-2024.zip') as zip_ref:
    file_path = Path('Book_Details.csv')
    # Checking if the data set is already unzipped
    if not file_path.exists():
        zip_ref.extractall()
```
## App code

### Creating dataframes that will be used by the app
A user profile is a new dataframe created from the goodreads database by creating a subset of books that are meeting the user requirements - current version is based on intended age group of the books (i.e. young adult) and specific genres and tags chosen by the user

```python
# Creating DataFrame from csv file
books = pd.read_csv('/kaggle/input/books-dataset-goodreadsmay-2024/Book_Details.csv',index_col=0)

# Creating simpler DataFrame
book_genres = pd.DataFrame(books, columns= ['author', 'book_title', 'book_details', 'num pages', 'genres'])

# Creating a data subset of eligible books based on chosen tags and age groups
def tags_and_ages_mask(field):
    field_as_list = json.loads(field.replace("'", '"'))
    return (tags | ages).issubset(field_as_list)
```

### Defined functions

The app basically uses two deifned functions

- exit_msg() that creates gui for an exit message that allows the user to quit the app
- swipe() that allows the user to look fo the books

```python
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
```

## GUI and main loop - this is how the app runs

### Creating start menu GUI

```python
# Creating start menu GUI
menu_msg = "*** Matchbook ***\n\n""Where bookworms can find their match!"
menu_title = "Matchbook | It's like Tinder but for books!"
# Window with continue/cancel menu
menu = eg.ccbox(menu_msg,menu_title)
tags = {}
ages = {}
```
![image](https://github.com/user-attachments/assets/332a0e50-df29-4c6a-8123-88be812decfc)

### Main loop
```python
# Main loop of the app that allows the user to swipe the books or exit the app
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
```
![image](https://github.com/user-attachments/assets/979423f1-1f3d-4f8d-a063-5c1fbc9813a2)
![image](https://github.com/user-attachments/assets/aa298caa-535d-475a-8902-736be1fb541b)
Ok button will use the selected genres to create a filtered data frame and start the main loop

```python
# Creating filtered DataFrame of eligible books
eligible_books = book_genres[book_genres['genres'].apply(tags_and_ages_mask)]
row_number = eligible_books.shape[0]

# Main loop - using "continue" button is giving the user next recommendation
while True:
    swipe()
```

![image](https://github.com/user-attachments/assets/9cde7b61-aadf-45db-bbec-9635e1211224)
![image](https://github.com/user-attachments/assets/a5d3e1db-cdaa-4aff-9b16-b40ed608813e)
![image](https://github.com/user-attachments/assets/2a782ea1-e894-4e2b-8c76-a3ad009affaf)

Cancel button will brake the loop and display an exit window, ok button will exit the app

![image](https://github.com/user-attachments/assets/a0d130d2-cb47-4db2-a22a-4c9494cb1e3f)

## Things to come (someday)
- creating function writing "matched" books to a file
- importing user data from goodreads





