import time
import ssl

from bs4 import BeautifulSoup
from urllib2 import urlopen


def pictaram_last_100_likes(image_url):

    data = urlopen(image_url).read()
    soup = BeautifulSoup(data, 'html.parser')
    user_names = soup.findAll(class_='user-name')
    user_name_list = []

    for name in user_names:
         user_name_list.append(name.text.strip())

    return user_name_list[1:]


def first_pictaram_search_result(username):
	BASE_SEARCH_URL = 'http://www.pictaram.com/search?query='

	search_url = BASE_SEARCH_URL + username
    html_search_source = urlopen(search_url).read()

    soup = BeautifulSoup(html_search_source)
    user_page_url = soup.find(class_='user-name')['href']

    return user_page_url


def scrape_pictaram_by_username(username, pages=1, print_progress=False):

	user_page_url = first_pictaram_search_result(username)

    user_post_data = []

    while pages > 0:
       
        if print_progress:
            print(pages)

        user_page = urlopen(user_page_url).read()

        soup = BeautifulSoup(user_page, 'html.parser')
        clearfix = soup.find_all(class_='clearfix')
 
        for box in clearfix:
            value = {}
            try:
                image_link = box.find(class_='content-image image').a['href']
                if print_progress:
                    print(image_link)
                value['image-link'] =  image_link
                value['last_100_likes'] = pictaram_last_100_likes(image_link)
                value['content-image'] = box.find(class_='content-image image').img['src']
                value['content'] = box.find(class_='content').text.strip()
                value['comments'] = box.find(class_='comments').text.strip()
                value['likes'] = box.find(class_='like').text.strip()
                user_post_data.append(value)
            except TypeError, AttributeError:
                pass

        pages -= 1

        try:
            page_url = soup.find(class_='next-cont').a['href']
        except TypeError, AttributeError:
            return user_post_data

    return user_post_data
