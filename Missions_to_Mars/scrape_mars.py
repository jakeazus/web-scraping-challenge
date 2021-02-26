import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
import time

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars


def mars_scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Retrieve page with the requests module
    # response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(browser.html, 'html.parser')

    results = soup.find('li', class_="slide")

    # scrape the title
    news_title = results.find('div', class_='content_title').text

    # scrape the paragraph text
    paragraph_text = results.find('div', class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(2)
    browser.links.find_by_partial_href('/images').click()
    time.sleep(2)
    soup = BeautifulSoup(browser.html, 'html.parser')

    featured_img = soup.find('a', class_="BaseButton")['href']
    try:
        url = 'https://space-facts.com/mars/'
        browser.visit(url)

        mars_facts = pd.read_html(url)
        mars_facts[0]

        mars_facts_table_df = mars_facts[0]
        mars_facts_table_df.columns = ['facts', 'values']
        mars_facts_table_df

        mars_html_table_string = mars_facts_table_df.to_html()
    except:
        mars_html_table_string = "<h3> website not found </h3>"
    try:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        soup = BeautifulSoup(browser.html, 'html.parser')

        results = soup.find_all('div', class_="item")

        # hemisphere section
        hemisphere_image_urls = []
        for result in results:
            hemisphere_dictionary = {}
            hemp_title = result.find('h3').text
            title_split = hemp_title.split(" ", 1)[0]
            browser.click_link_by_partial_text(title_split)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            image_url = soup.find('div', class_='downloads').find('a')['href']
            hemisphere_dictionary["title"] = hemp_title
            hemisphere_dictionary["img_url"] = image_url
            hemisphere_image_urls.append(hemisphere_dictionary)
    except:
        hemisphere_image_urls = []
    browser.quit()
    output = {"news_title": news_title,
    "featured_img": featured_img,
    "news_p": paragraph_text,
    "mars_facts": mars_html_table_string,
    "hemisphere_imgs_url":hemisphere_image_urls
    }
    return output