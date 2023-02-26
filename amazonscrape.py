import requests
import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=firefox_options)

def get_review(links):
    full_dict = dict()
    for brand in links:
        brand_dict = dict()
        for category in links[brand]:
            category_dict = dict()
            print(category)
            for URL in links[brand][category]:
                driver.get(URL)
                time.sleep(1)
                product_name = driver.find_element(By.CLASS_NAME, 'a-size-large').text
                print(product_name)
                review_list = []

                while True:
                    print(driver.current_url)
                    page = driver.page_source
                    time.sleep(1)
                    soup = BeautifulSoup(page, 'html.parser')
                    reviews = soup.find_all('span', class_='review-text-content')
                    for review in reviews:
                        for stuff in review.contents:
                            text = stuff.get_text()
                            if text != '\n':
                                review_list.append(stuff.get_text())
                    print(len(review_list))
                    if len(review_list) >= 50:
                        break
                    try:
                        driver.find_element(By.XPATH, '//li[@class="a-last"]/a').click()
                    except:
                        print('No more pages')
                        break

                for text in review_list:
                    print(text)
                category_dict[product_name] = review_list
            brand_dict[category] = category_dict
        full_dict[brand] = brand_dict
    with open("reviews.json", "w") as ff:
        json.dump(full_dict, ff, indent=2)
    return full_dict

with open('urls.json') as f:
    URLS = json.load(f)
full_dict = get_review(URLS)
print(full_dict)


