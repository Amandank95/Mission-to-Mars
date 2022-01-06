


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }


def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    #assign the title and summary to the variable
    slide_elem.find('div', class_='content_title')

    #use the parent element to find the first 'a' tag and save it as 'news title'
    news_title = slide_elem.find('div', class_='content_title').get_text()

    # use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    #add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #use the parent element to find the first 'a' tag and save it as 'news title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # Visit URL 
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        #find the image relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    #find the relative image URL
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel

    # use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url

    
def mars_facts():
    #add try/except for error handling
    try:
        #use the 'read_html' to scrape the facts into a dataframe  
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return none

    #assign the columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #convert the dataframe into html format, add bootstrap

    return df.to_html()







