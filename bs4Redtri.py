# coding: utf-8

# In[ ]:

# weekend requires week number in URL http://redtri.com/events/seattle/2016/10/weekend/5/

from math import ceil
from datetime import date, timedelta

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))


# In[ ]:

# weekend requires week number in URL http://redtri.com/events/seattle/2016/10/weekend/5/
# there is an easier way to get this: scrape the URL from the page http://redtri.com/events/seattle/

def weekend_url():
    today = date.today()
    weekNumber = week_of_month(today)
    yearNumber = today.year
    monthNumber = today.month

    url = 'http://redtri.com/events/seattle/' + str(yearNumber) + '/' + str(monthNumber) + '/weekend/' + str(weekNumber)
    return url


# In[ ]:

# todays date e.g. http://redtri.com/events/seattle/2016/10/26/

def today_url():
    today = date.today()
    dayNumber = today.day
    yearNumber = today.year
    monthNumber = today.month

    url = 'http://redtri.com/events/seattle/' + str(yearNumber) + '/' + str(monthNumber) + '/' + str(dayNumber)
    return url


# In[ ]:

# tomorrow's date e.g. http://redtri.com/events/seattle/2016/10/26/

def tomorrow_url():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    dayNumber = tomorrow.day
    yearNumber = tomorrow.year
    monthNumber = tomorrow.month

    url = 'http://redtri.com/events/seattle/' + str(yearNumber) + '/' + str(monthNumber) + '/' + str(dayNumber)
    return url


# In[ ]:

# Ask user what dates he wants

choice = input('What events in Seattle do you want to see? [1] Today, [2] Tomorrow, [3] This weekend? ')

if choice == "1":
    url = today_url()
elif choice == "2":
    url = tomorrow_url()
elif choice == "3":
    url = weekend_url()
else:
    print("You're naughty! That was not a valid choice!") # add a loop here


# In[ ]:

import requests
import bs4

url = 'http://www.redtri.com/events/seattle/'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')


# In[ ]:

# get URL for the events

segment = soup.find_all("div", {"class": "event container"})

link = []
for i in segment:
    link.append(i.find("a").get("href"))


# In[ ]:

# get names of the events

title = soup.find_all("h2")[1:]

name = []
for i in title:
    name.append(i.get_text())


# In[ ]:

when = soup.find_all("p", {"class": "when"})

date = []
for i in when:
    temp = i.find("span", {"class": "event-content"})
    date.append(temp.get_text())


# In[ ]:

where = soup.find_all("p", {"class": "where"})

location = []
for i in where:
    temp = i.find("span", {"class": "event-content"})
    location.append(temp.get_text())


# In[ ]:

ages = soup.find_all("p", {"class": "ages"})

age = []
for i in ages:
    temp = i.find("span", {"class": "event-content"})
    age.append(temp.get_text())



# In[ ]:

cost = soup.find_all("p", {"class": "cost"})

price = []
for i in cost:
    temp = i.find("span", {"class": "event-content"})
    price.append(temp.get_text())


# In[ ]:

prose = soup.find_all("div", {"class": "prose hidden-xs"})

shortDescription = []
for i in prose:
    temp = i.get_text()
    shortDescription.append(temp.lstrip().rstrip('read more'))


# In[ ]:

# get image

segment = soup.find_all("div", {"class": "event container"})

image = []
for i in segment:
    image.append(i.find("img").get("src"))


# In[ ]:

# get full description of event and URL for more info
# used CSS selectors here. Used Chrome extension SelectorGadget to find unique CSS selectors.

import string
import re

longDescription = []
moreInfo = []

for i in link:
    res = requests.get(i)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    temp = soup.select(".prose p")
    tempDescription = []
    for t in temp:
        tempDescription.append(t.get_text())
    longDescription.append("".join(tempDescription))

    temp2 = soup.select(".more-info a:nth-of-type(1)")
    for t in temp2:
        moreInfo.append(t.get("href"))


# In[ ]:

import os, csv
os.chdir("c:/Users/guygi/DropBox/AppSheet")

total = len(name)

with open("redtri.csv", "w", newline='', encoding='utf-8') as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["name", "image", "date", "short", "long", "location", "age", "price", "URL", "more info"])
    for i in range(total):
#        print('DEBUG: ', name[i], image[i], date[i], shortDescription[i], longDescription[i], location[i], age[i], price[i], link[i], moreInfo[i])
        writer.writerow([name[i], image[i], date[i], shortDescription[i], longDescription[i], location[i], age[i], price[i], link[i], moreInfo[i]])


print()
print('Done!')
