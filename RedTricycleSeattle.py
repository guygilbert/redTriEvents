
# coding: utf-8

# In[1]:

#! python3

# ideas:
# create spreadsheet or Google Sheet so that I can asterisk events in AppSheet
# translate age into numbers
# add day of week as string


# In[2]:

from datetime import date, timedelta
import requests
import bs4
import string
import re
import os
import csv


# In[3]:

import logging
logging.disable(logging.CRITICAL) #comment this line to stop logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
logging.debug('Start of program')


# In[4]:

# create URL for todays date + delta days in format 'http://redtri.com/events/seattle/2016/10/26/'

def date_url(delta):
    today = date.today()
    selectDate = today + timedelta(days=delta)
    monthNumber = selectDate.month
    dayNumber = selectDate.day
    yearNumber = selectDate.year
    url = 'http://redtri.com/events/seattle/' + str(yearNumber) + '/' + str(monthNumber) + '/' + str(dayNumber)
    dateString = str('{:02d}'.format(monthNumber)) + '/' + str('{:02d}'.format(dayNumber)) + '/' + str('{:04d}'.format(yearNumber))
    return url, dateString


# In[5]:

def make_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup


# In[6]:

# get URL for the events

def make_link(soup):
    segment = soup.find_all("div", {"class": "event container"})
    link = []
    for i in segment:
        link.append(i.find("a").get("href"))
    return link


# In[7]:

# get names of the events

def make_name(soup):
    title = soup.select(".col-xs-8 h2 a")
    name = []
    for i in title:
        name.append(i.get_text())
    return name


# In[8]:

def make_period(soup):
    when = soup.find_all("p", {"class": "when"})
    period = []
    for i in when:
        temp = i.find("span", {"class": "event-content"})
        period.append(temp.get_text())
    return period


# In[9]:

def make_location(soup):
    where = soup.find_all("p", {"class": "where"})
    location = []
    for i in where:
        temp = i.find("span", {"class": "event-content"})
        location.append(temp.get_text())
    return location


# In[10]:

def make_age(soup):
    ages = soup.find_all("p", {"class": "ages"})
    age = []
    for i in ages:
        temp = i.find("span", {"class": "event-content"})
        age.append(temp.get_text())
    return age


# In[11]:

def make_price(soup):
    cost = soup.find_all("p", {"class": "cost"})
    price = []
    for i in cost:
        temp = i.find("span", {"class": "event-content"})
        price.append(temp.get_text())
    return price


# In[12]:

def make_shortDescription(soup):
    prose = soup.find_all("div", {"class": "prose hidden-xs"})
    shortDescription = []
    for i in prose:
        temp = i.get_text()
        shortDescription.append(temp.lstrip().rstrip('read more'))
    return shortDescription


# In[13]:

# get image

def make_image(soup):
    segment = soup.find_all("div", {"class": "event container"})
    image = []
    for i in segment:
        #logging.debug(i.find("img").get("src"))
        image.append(i.find("img").get("src"))
    return image


# In[14]:

# get full description of event and URL for more info
# used CSS selectors here. Used Chrome extension SelectorGadget to find unique CSS selectors.

def make_details(link):
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
        if temp2 == []: #in case there is no "more info" field
            moreInfo.append('http://www.google.com') 
        else:
            for t in temp2:
                moreInfo.append(t.get("href"))

    return longDescription, moreInfo


# In[15]:

def append_to_csv(name, image, eventDate, date, shortDescription, longDescription, location, age, price, link, moreInfo):
    os.chdir("c:/Users/guygi/DropBox/AppSheet")
    total = len(link)
    with open("redtri.csv", "a", newline='', encoding='utf-8') as toAppend:
        writer = csv.writer(toAppend, delimiter=",")
        for c in range(total):
            logging.debug(c)
            logging.debug(name[c]) 
            logging.debug(image[c]) 
            logging.debug(period[c]) 
            logging.debug(shortDescription[c]) 
            logging.debug(longDescription[c]) 
            logging.debug(location[c]) 
            logging.debug(age[c]) 
            logging.debug(price[c]) 
            logging.debug(link[c]) 
            logging.debug(moreInfo[c])

            writer.writerow([name[c], image[c], eventDate, period[c], shortDescription[c], longDescription[c], location[c], age[c], price[c], link[c], moreInfo[c]])

    print('Done with ' + eventDate + '!')


# In[16]:

os.chdir("c:/Users/guygi/DropBox/AppSheet")

with open("redtri.csv", "w", newline='', encoding='utf-8') as toWrite:
    writer = csv.writer(toWrite, delimiter=",")
    writer.writerow(["name", "image", "date", "period", "short", "long", "location", "age", "price", "URL", "more info"])


# In[17]:

# get URL's for next 7 days

for i in range(0,7):
    url, eventDate = date_url(i)
    soup = make_soup(url)
    link = make_link(soup)
    name = make_name(soup)
    period = make_period(soup)
    location = make_location(soup)
    age = make_age(soup)
    price = make_price(soup)
    shortDescription = make_shortDescription(soup)
    image = make_image(soup)
    longDescription, moreInfo = make_details(link)
    append_to_csv(name, image, eventDate, period, shortDescription, longDescription, location, age, price, link, moreInfo)

print()
print('All Done!!!')

