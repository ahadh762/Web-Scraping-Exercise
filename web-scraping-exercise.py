import csv
from bs4 import BeautifulSoup
import requests
from requests import HTTPError


def getHTML(url): # Function makes a get request for a URL
    try:
        response = requests.get(url)
        return response
    except HTTPError as e:
    # Need to check if the error is an 404, 503, 500, 403 etc.
        error_code = e.response.status_code
        print(error_code)


# response = requests.get("http://books.toscrape.com/")
# print(response) # Returns Response [200] Status Code: Success!

# print(response.status_code)

titles_list = []
prices_list = []
ratings_list = []

for page in range(1,51):
    
    URL = 'https://books.toscrape.com/catalogue/page-'
    URL = URL + str(page) + '.html'

    html = getHTML(URL)

    soup = BeautifulSoup(html.content,"lxml")

    # Scrape Titles
    
    title_soup = soup.find_all(href = True, title = True)

    # print(title_soup[0]['href']) It is a list of dictionaries so you have to give list index and dictionary key
    for i in range(len(title_soup)):
        titles_list.append(title_soup[i]["title"])


    # Scrape Prices
    
    for price in soup.find_all('p', class_ = "price_color"):
        prices_list.append(price.text)


    # Scrape Ratings

    rating_soup = soup.findAll('p', {'class':['star-rating One', 'star-rating Two','star-rating Three','star-rating Four','star-rating Five']})
    # print(rating_soup[0]["class"][1]) List of dictionaries with two values
    # List position, key = 'class', second value from key
    for i in range(len(rating_soup)):
        rating = rating_soup[i]["class"][1]
        if rating == 'One':
            ratings_list.append(1)
        elif rating == 'Two':
            ratings_list.append(2)
        elif rating == 'Three':
            ratings_list.append(3)
        elif rating == 'Four':
            ratings_list.append(4)
        else:
            ratings_list.append(5)


# Write data to csv file

with open('scraped-data.csv','w') as file:
    write = csv.writer(file)
    write.writerow(["Book Title, Price, Star Rating (out of 5)"])
    
    for i in range(len(titles_list)):
        write.writerow((titles_list[i], prices_list[i], ratings_list[i]))
    file.close()