import time

from bs4 import BeautifulSoup
from selenium import webdriver


def pikore_tag_scraper(tag, num_scrolls):

    BASE_URL = "http://www.pikore.com/tag/" + tag
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get(BASE_URL);
    time.sleep(1) # Let the user actually see something!

    for i in range(1, num_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    items = soup.findAll(class_="item")
    page_data = []

    for item in items:
        try:
            description = item.find(class_='desc').text.strip()
            if tag in description:
                username = item.find(class_='username').text.strip()
                likes = item.find(class_='item-meta').find(class_='likes-number').text.strip()
                comments = item.find(class_='item-meta').find(class_='comments-number').text.strip()

                item_data = {'username'    : username,
                             'likes'       : likes,
                             'comments'    : comments,
                             'description' : description,
                             'search_tag'  : tag}

                page_data.append(item_data)

        except AttributeError:
            pass

    return page_data
