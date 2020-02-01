# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# Import dependencies
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #slide_elem.find("div", class_="content_title")

        # Use the parent element to find the first "a" tag and save it as "news_title"
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        #news_p

    except AttributeError:
        return None, None
        
    return news_title, news_p 

#### Featured Images

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that. Can use Splinter to find elements using text.
browser.is_element_present_by_text('more info', wait_time=1) # Use browser.links.find_by_partial_text instead
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

def featured_image(browser):

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        #img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    #img_url

    return img_url 

#### Fact table

def mars_facts():
    # Add try/except for error handling 
    try:
        # Scrape entire table with Pandas’ .read_html() function and put into DataFrame.
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    # Convert our DataFrame back into HTML-ready code using the .to_html() function
    return df.to_html()

# End the automated browsing session
#browser.quit()




