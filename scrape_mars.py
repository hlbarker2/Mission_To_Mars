#!/usr/bin/env python
# coding: utf-8

# Mission to Mars

# Dependencies
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    #Create dictionary to hold scraped data
    mars_data = {}
    
    #Nasa Mars News
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    time.sleep(5)
    # Create HTML object
    nasa_html = browser.html
    # Parse HTML with BeautifulSoup
    nasa_soup = bs(nasa_html, "html.parser")
    # Collect the latest News Title
    news_title = nasa_soup.find('div', class_="content_title").text.strip()
    # Collect the latest Paragraph text
    news_p = nasa_soup.find('div', class_="article_teaser_body").text.strip()
    #Add title and text to dictionary
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(5)
    # Use Splinter to locate image url
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(10)
    browser.click_link_by_partial_text("more info")
    # Create HTML object
    jpl_html = browser.html
    # Parse HTML with BeautifulSoup
    jpl_soup = bs(jpl_html, "html.parser")
    # Find image url
    image_path = jpl_soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path
    #Add url to dictionary
    mars_data['featured_image_url'] = featured_image_url

    # Mars Weather
    # URL of page to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(5)
    # Create HTML object
    weather_html = browser.html
    # Parse HTML with BeautifulSoup
    weather_soup = bs(weather_html, "html.parser")
    # Scrape the latest Mars weather tweet
    mars_weather = weather_soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    mars_data['mars_weather'] = mars_weather

    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    # Scrape tabular data
    tables = pd.read_html(facts_url)
    tables[0]
    # Convert to DataFrame
    facts_df = tables[0]
    facts_df.columns = ['Fact', 'Value']
    facts_df.set_index('Fact', inplace=True)
    # Convert to HTML table string
    facts_html_table = facts_df.to_html()
    facts_html_table = facts_html_table.replace('\n', '')
    mars_data['facts_html_table'] = facts_html_table

    # Mars Hemispheres
    # URL of page to be scraped
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    time.sleep(5)
    # Create HTML object
    usgs_html = browser.html
    # Parse HTML with BeautifulSoup
    usgs_soup = bs(usgs_html, "html.parser")
    #Create dictionaries to hold data
    hemisphere_dict = {"title": [] , "img_url": []}
    hemisphere_img_urls = []
    #Use loop to get title, img_url
    results = usgs_soup.find_all("h3")
    for result in results:
        title = result.text
        browser.visit(usgs_url)
        browser.click_link_by_partial_text(title)
        time.sleep(10)
        img_url = browser.find_link_by_partial_href("download")["href"]
        hemisphere_dict = {"title": title, "img_url": img_url} 
        hemisphere_img_urls.append(hemisphere_dict)
        mars_data['hemisphere_img_urls'] = hemisphere_img_urls

    return mars_data