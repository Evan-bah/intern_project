from selenium import webdriver
from bs4 import BeautifulSoup
import time


def scrape_profile(username, num_scrolls, print_status=True):
    driver = webdriver.Chrome()
    driver.get('http://www.instagram.com')
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    button_class = str('.' + '.'.join(soup.button['class']))
    driver.find_element_by_css_selector(button_class).click()

    login = driver.find_element_by_class_name('inputtext')
    login.send_keys('robkellybah@gmail.com')
    password = driver.find_element_by_id('pass')
    password.send_keys('BoozAllen')
    submit = driver.find_element_by_id('loginbutton')
    submit.click()

    driver.get('https://www.instagram.com/{}/'.format(username))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    follow = soup.find('button')['class']
    driver.find_element_by_css_selector('.' + '.'.join(follow)).click()
    time.sleep(1)

    login = BeautifulSoup(driver.page_source, 'html.parser').find('button')
    button = '.' + '.'.join(login['class'])
    driver.find_element_by_css_selector(button).click()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(text(), 'followers')]")[0].click()

    element_to_hover_over = driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")[0]
    hover = webdriver.ActionChains(webdriver).move_to_element(element_to_hover_over)

    height = 4000
    for _ in range(num_scrolls):
        if num_scrolls % 200 == 0 & print_status:
            print(num_scrolls)
        query = 'jQuery("div").filter((i, div) => jQuery(div).css("overflow-y") == "scroll")[0].scrollTop = %s' %height
        driver.execute_script(query)
        time.sleep(.5)
        height += 4000

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    followers_lis = soup.findAll('li')
    followers_class = str(followers_lis[30]['class'][0])

    followers = soup.findAll(class_=followers_class)
    follower_list = []
    for follower in followers:
        follower_list.append(follower.a['href'][1:-1])

    return follower_list


scrape_profile('newbalance', 100)