


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

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
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_data(browser)
    }
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    


    
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


    # use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

    
def mars_facts():
    #add try/except for error handling
    try:
        #use the 'read_html' to scrape the facts into a dataframe  
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #assign the columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #convert the dataframe into html format, add bootstrap

    return df.to_html()


def hemisphere_data(browser):
    #Create a list to hold the images and titles.
    hemisphere_image_urls = []

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    html_soup = soup(html, "html.parser")
    links = browser.find_by_css('a.product-item img')

    for item in range(len(links)):
        hemispheres = {}
        browser.find_by_css("a.product-item img")[item].click()
        mars_hem = browser.links.find_by_text("Sample").first
        hemispheres["img_url"] = mars_hem["href"]
        hemispheres["title"]=browser.find_by_css("h2.title").text
    
        hemisphere_image_urls.append(hemispheres)
    
        browser.back()
    return(hemisphere_image_urls)

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())