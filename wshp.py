# This is my first attempt at a web scraper project in Python. I am extracting data from IMDB's list of top rated movies.
# The list is sorted by user ratings.
#_Packages used: Beautiful Soup 4, requests

import re
from bs4 import BeautifulSoup
import requests

# Downloading IMDB's list of top rated movies
link = 'https://www.imdb.com/chart/top'
responses = requests.get(link)
soup_var = BeautifulSoup(responses.text, 'lxml') # Processing HTML and saving it to a txt file

# Getting table data from the url
movies = soup_var.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup_var.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup_var.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup_var.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup_var.select('td.ratingColumn strong')]

wshp = []

# Next, storing each item and putting them into a list
for index in range(0, len(movies)):
    # Factor movies into place, title, year
    movie_str = movies[index].get_text()
    movie = (' '.join(movie_str.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_str).group(1)
    place = movie[:len(str(index))-(len(movie))]
    data = {"movie_title": movie_title,
            "year": year,
            "place": place,
            "star_cast": crew[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    wshp.append(data)

for item in wshp:
    print(item['place'], '-', item['movie_title'], '('+item['year']+') -', 'Starring:', item['star_cast'])


