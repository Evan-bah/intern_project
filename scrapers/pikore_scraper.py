import time
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from urllib2 import urlopen


def extract_hash_tags(text):
    return re.findall(r"#(\w+)", text)

def convert_to_timestamp(posted_time):
    from datetime import timedelta, datetime

    posted_time = posted_time.replace('about', '')
    
    def get_time_data(instagram_timestring, time_format):
        time_string = ' %s' %(time_format)
        return int(posted_time.replace(' ago', '').replace(time_string, ''))

    if 'minute ' in posted_time:
        return datetime.now().strftime('%Y/%m/%d %T')
    if 'minutes' in posted_time:
        minutes_ago = get_time_data(posted_time, 'minutes')
        return (datetime.now() - timedelta(minutes=minutes_ago)).strftime('%Y/%m/%d %T')
    if 'hour ' in posted_time:
        return (datetime.now() - timedelta(hours=1)).strftime('%Y/%m/%d %T')
    if 'hours ' in posted_time:
        hours_ago = get_time_data(posted_time, 'hours')
        return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y/%m/%d %T')
    if 'day ' in posted_time:
        return (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d %T')
    if 'days ' in posted_time:
        days_ago = get_time_data(posted_time, 'days')
        return (datetime.now() - timedelta(days=days_ago)).strftime('%Y/%m/%d %T')


def pikore_content_scraper(query, num_scrolls, username=True):

    def pikore_url_generator(query, username=True):
        if username:
            return 'http://www.pikore.com/' + query
        return 'http://www.pikore.com/tag/' + query

    def get_post_content(post_link):
        full_link = 'http://www.pikore.com' + post_link
        html_source = urlopen(full_link).read()
        soup = BeautifulSoup(html_source, 'html.parser')
        return soup.find(class_='desc').text

    base_url = pikore_url_generator(query, username)
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get(base_url);
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
            username = item.find(class_='username').text.strip()
            likes = item.find(class_='item-meta').find(class_='likes-number').text.strip()
            comments = item.find(class_='item-meta').find(class_='comments-number').text.strip()
            time_posted = convert_to_timestamp(item.find(class_='posted').text)
            image_link = item.img['src']
            post_link = item.find(class_='image-wrapper').a['href']
            description = get_post_content(post_link)

            item_data = {'username'    : username,
                         'likes'       : likes,
                         'comments'    : comments,
                         'description' : description,
                         'hash_tags'   : extract_hash_tags(description),
                         'time_posted' : time_posted,
                         'image_link'  : image_link}

            page_data.append(item_data)

        except AttributeError:
            pass

    return page_data
