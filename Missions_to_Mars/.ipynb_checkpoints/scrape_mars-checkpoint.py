from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    
    mars_dict = {}
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    


    # Visit visitcostarica.herokuapp.com
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(news_url)

    # Scrape page into Soup
    soup = BeautifulSoup(response.text, 'html')

    # Get the average temps
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    
    
    
    
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    main_url = 'https://www.jpl.nasa.gov'

    partial_url = soup.find('article',['style']).replace('background-image: url(','').replace(');','')[1:-1]

    featured_image_url = main_url+partial_url
    
    mars_dict['featured_image_url'] = featured_image_url
    
    
    
    
    
    facts_url = 'https://space-facts.com/mars/'

    mars_tables = pd.read_html(facts_url)
    mars_table_df = mars_tables[0]
    mars_table_df.set_index(0, inplace=True)
    mars_table_df.index.names = [None]
    mars_table_df.columns = ['']
    
    html_table = mars_table_df.to_html()
    html_table = html_table.replace('\n','')
    
    mars_dict['html_table'] = html_table
    
    
    
    
    
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    
    hemisphere_html = browser.html
    soup = BeautifulSoup(hemisphere_html, 'html.parser')
    
    hemisphere_items = soup.find_all('div',class_='item')
    
    hemisphere_image_urls = []

    for h in hemisphere_items:
        title = (h.find('h3').text).replace(' Enhanced','')

        browser.click_link_by_partial_text(title)

        soup = BeautifulSoup(browser.html, 'html.parser')

        full = soup.find('a', text='Sample')

        img_url = full['href']

        hemisphere_image_urls.append({'title': title, 'img_url': img_url})

        browser.back()

    browser.quit()
    
    mars_dict['hemisphere_image_urls'] = hemisphere_images_url
    
    
    return mars_dict
