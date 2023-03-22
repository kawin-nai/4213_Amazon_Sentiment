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


# TODO: plot correlation between sentiment score and actual ratings

def get_review(links):
    full_dict = dict()
    for brand in links:
        brand_dict = dict()
        for category in links[brand]:
            category_list = []
            print(category)
            for URL in links[brand][category]:
                product_dict = dict()
                driver.get(URL)
                time.sleep(1)
                product_name = driver.find_element(By.CLASS_NAME, 'a-size-large').text
                product_rating = float(driver.find_element(By.CSS_SELECTOR, '.a-size-medium.a-color-base').text.split(' ')[0])
                print(product_name)
                review_list = []

                while True:
                    print(driver.current_url)
                    page = driver.page_source
                    time.sleep(1)
                    get_review_list(page, review_list)
                    if len(review_list) >= 50:
                        break
                    try:
                        driver.find_element(By.XPATH, '//li[@class="a-last"]/a').click()
                    except:
                        print('No more pages')
                        break

                for text in review_list:
                    print(text)
                product_dict["name"] = product_name
                product_dict["rating"] = product_rating
                product_dict["reviews"] = review_list
                category_list.append(product_dict)
            brand_dict[category] = category_list
        full_dict[brand] = brand_dict
    with open("reviews_extracted.json", "w") as ff:
        json.dump(full_dict, ff, indent=2)
    return full_dict


def get_review_list(page, review_list):
    soup = BeautifulSoup(page, 'html.parser')
    reviews = soup.find_all('span', class_='review-text-content')
    for review in reviews:
        for stuff in review.contents:
            text = stuff.get_text()
            if text != '\n':
                review_list.append(stuff.get_text())
    print(len(review_list))


def main():
    with open('urls.json') as f:
        URLS = json.load(f)
    full_dict = get_review(URLS)
    print(full_dict)


if __name__ == '__main__':
    main()
