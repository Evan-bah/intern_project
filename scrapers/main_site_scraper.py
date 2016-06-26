from selenium import webdriver
from bs4 import BeautifulSoup
import time


def scrape_profile(username):
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
    driver.get('https://www.instagram.com/%s/' %username)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    follow = soup.find('button')['class']
    driver.find_element_by_css_selector('.' + '.'.join(follow)).click()
    time.sleep(1)
    login = BeautifulSoup(driver.page_source).find('button')
    button = '.' + '.'.join(login['class'])
    driver.find_element_by_css_selector(button).click()
    soup = BeautifulSoup(driver.page_source)
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(text(), 'followers')]")[0].click()


    element_to_hover_over = driver.find_elements_by_xpath("//*[contains(text(), 'Follow')]")[0]
    hover = ActionChains(webdriver).move_to_element(element_to_hover_over)

    height = 4000
    for _ in range(1000):
        query = 'jQuery("div").filter((i, div) => jQuery(div).css("overflow-y") == "scroll")[0].scrollTop = %s' %height
        driver.execute_script(query)
        time.sleep(.5)
        height += 4000
