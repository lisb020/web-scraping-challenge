import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import time



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # Scrape the nasa news
    #-----------------------
    # Setup splinter
    # URL of page to be scraped
    urlnasa = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser = init_browser()
    #open browser page
    browser.visit(urlnasa)
    page = browser.html
    time.sleep(1)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(page, 'html.parser')
    print(soup.prettify())
    browser.quit()
    # find first/latest article
    title_results = soup.find('div', class_='list_text').find('div', class_='content_title').text
    teaser_results = soup.find('div', class_='article_teaser_body').text
    
    #scraping Mars facts table
    #________________________
    urlfact = "https://space-facts.com/mars/"
    facttable = pd.read_html(urlfact)
    df = facttable[0]
    html_table = df.to_html()

    #scraping images
    #---------------
    urlpic = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Setup splinter
    browser = init_browser()
    #set up list
    hemisphere_image_urls = []

    #list of hemispheres to click through on website
    Hemispheres = ["Cerberus", "Schiaparelli","Syrtis","Valles"]

    #loop through list of hemispheres to click on each one on the website
    for hemisphere in Hemispheres:
        #restart on the initial browser page
        browser.visit(urlpic)

        time.sleep(1)
        #click on hemisphere link
        browser.links.find_by_partial_text(hemisphere).click()

        time.sleep(1)
        #get the html
        page = browser.html
        soup_page = BeautifulSoup(page, 'html.parser')
        #find the title and link in the html
        pictitle = soup_page.find('h2', class_="title").text
        piclink = soup_page.find('div', class_='downloads').li.a["href"]
        
        #put in dictionary
        hemisphere_dict = {
            "title":pictitle,
            "img_url":piclink
        }
        #append to list
        hemisphere_image_urls.append(hemisphere_dict)

    browser.quit()

    return hemisphere_image_urls