from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape():
    
    mars_dict = {}
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    


    # Visit https://mars.nasa.gov
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(news_url)

    # Scrape page into Soup
    soup = BeautifulSoup(response.text, 'html')

    # Locate the latest news and summary paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    # Store news title and summary paragraph in mars dictionary
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    
    
    
    
    #images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    #browser.visit(images_url)
    
    # Scrape page into Soup
    #html = browser.html
    #soup = BeautifulSoup(html, 'html.parser')
    
    #main_url = 'https://www.jpl.nasa.gov'

    #partial_url = soup.find('article',['style']).replace('background-image: url(','').replace(');','')[1:-1]

    #featured_image_url = main_url+partial_url
    
    # Store link to featured image in mars dictionary
    #mars_dict['featured_image_url'] = featured_image_url
    
    
    
    
    # Visit https://space-facts.com/mars/
    facts_url = 'https://space-facts.com/mars/'

    # Scrape facts from html
    mars_tables = pd.read_html(facts_url)
    
    # Store facts data in dataframe
    mars_table_df = mars_tables[0]
    
    # Edit dataframe
    mars_table_df.set_index(0, inplace=True)
    mars_table_df.index.names = [None]
    mars_table_df.columns=['Mars']
    
    # Convert dataframe to html and edit
    html_table = mars_table_df.to_html()
    html_table = html_table.replace('\n','')
    
    # Store html fact data in mars dictionary
    mars_dict['html_table'] = html_table
    
    
    
    
    # Visit https://astogeology.usgs.gov for hemisphere images and titles
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    
    # Scrape page into Soup
    hemisphere_html = browser.html
    soup = BeautifulSoup(hemisphere_html, 'html.parser')
    
    # Locate link to hemisphere pages
    hemisphere_items = soup.find_all('div',class_='item')
    
    hemisphere_image_urls = []

    for h in hemisphere_items:
        
        #Scrape hemisphere title
        title = (h.find('h3').text).replace(' Enhanced','')
        
        # Navigate to hemisphere page
        browser.click_link_by_partial_text(title)
        
        # Scrape page into Soup
        soup = BeautifulSoup(browser.html, 'html.parser')

        # Locate tag for hemisphere images
        full_image = soup.find('a', text='Sample')

        # Scrape hemisphere href
        full_url = full_image['href']

        # Store hemisphere title and image href in dictionary
        hemisphere_image_urls.append({'title': title, 'img_url': full_url})

        # Navigate to previous page
        browser.back()

    # Quit browser
    browser.quit()
    
    # Store hemisphere data in mars dictionary
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls
    
    #Return results
    return mars_dict
