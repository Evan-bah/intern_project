import time

from selenium import webdriver


def pikore_tag_scraper(tag, num_scrolls):

    BASE_URL = "http://www.pikore.com/tag/" + tag
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get(BASE_URL)
    time.sleep(1) # Let the user actually see something!

    for i in range(1, num_scrolls):
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(1)

    html_source = driver.page_source

    #ADD STUFF

    stuff = html_source

    return stuff
