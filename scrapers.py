import time
import ssl


from selenium import webdriver
from bs4 import BeautifulSoup
from urllib2 import urlopen


def pikore_tag_scraper(tag, num_scrolls):

    BASE_URL = "http://www.pikore.com/tag/" + tag
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get(BASE_URL)
    time.sleep(1) # Let the user actually see something!

    for i in range(1, num_scrolls):
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(1)

    html_source = driver.page_source

    return html_source


def scrape_pictaram(page_url, pages=1, print_progress=False):
    new_balance = []

    def user_name_scraper(image_url):

        data = urlopen(image_url).read()
        soup = BeautifulSoup(data, 'html.parser')
        user_names = soup.findAll(class_='user-name')
        user_name_list = []

        for name in user_names:
             user_name_list.append(name.text.strip())

        return user_name_list[1:]

    while pages > 0:
       
        if print_progress:
            print(pages)

        info = urlopen(page_url).read()
 
 
        soup = BeautifulSoup(info, 'html.parser')
        clearfix = soup.find_all(class_='clearfix')
 
        for box in clearfix:
            value = {}
            try:
                image_link = box.find(class_='content-image image').a['href']
                if print_progress:
                    print(image_link)
                value['image-link'] =  image_link
                value['last_100_likes'] = user_name_scraper(image_link)
                value['content-image'] = box.find(class_='content-image image').img['src']
                value['content'] = box.find(class_='content').text.strip()
                value['comments'] = box.find(class_='comments').text.strip()
                value['likes'] = box.find(class_='like').text.strip()
                new_balance.append(value)
            except:
                pass

        pages -= 1
        page_url = soup.find(class_='next-cont').a['href']
   
    return new_balance
