from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(news_url)

    time.sleep(1)

    # Scrape page into Soup
    soup = BeautifulSoup(response.text, 'html')

    # Get the average temps
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='rollover_description_inner').text


    
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    main_url = 'https://www.jpl.nasa.gov'

    partial_url = soup.find('article',['style']).replace('background-image: url(','').replace(');','')[1:-1]

    featured_image_url = main_url+partial_url
    
    
    
    facts_url = 'https://space-facts.com/mars/'

    mars_tables = pd.read_html(facts_url)
    mars_table_df = mars_tables[0]
    mars_table_df.set_index(0, inplace=True)
    mars_table_df.index.names = [None]
    mars_table_df.columns = ['']
    
    html_table = mars_table_df.to_html()
    html_table = html_table.replace('\n','')
    
    
    
    
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # BONUS: Find the src for the sloth image
    relative_image_path = soup.find_all('img')[2]["src"]
    sloth_img = url + relative_image_path

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
