# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    chromedriver_path = '../chromedriver_win32/chromedriver.exe'
    browser = Browser('chrome', executable_path=chromedriver_path, headless=True)

    #Set news title and paragraph variables (This function will return two values).
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# ## Hemispheres

def hemispheres(browser):

    # Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create a list to hold the images and titles
    hemisphere_image_urls = []

    # Parse the resulting html with soup
    html = browser.html
    hemisph_soup = soup(html, 'html.parser')

    #Write code to retrieve the image urls and titles for each hemisphere
    hemisph_div_item = hemisph_soup.find_all('div', class_='item')

    hemisph_div_item_paths = []

    for div_item in hemisph_div_item:
        hemisph_path = div_item.find('a')['href']
        hemisph_div_item_paths.append(hemisph_path)

    astropedia_url = 'https://astrogeology.usgs.gov'
    hemispheres = {}

    for path in hemisph_div_item_paths:
        hemisph_url = astropedia_url + path
        
        # Use browser to visit the URL
        browser.visit(hemisph_url)
        
        # Parse the resulting html with soup
        html = browser.html
        download_soup = soup(html, 'html.parser')
        
        try:
            #Find the title inside an h2 tag with a class of 'title'
            title = download_soup.find('h2', class_='title').get_text()
            
            #Find the image url (href) inside a li tag
            img_url = download_soup.find('li').a['href']
        
        except AttributeError:
            title = None
            img_url = None

        # Store data in a dictionary
        hemispheres = {
            'img_url': img_url,
            'title': title
        }
        #Append the dictionary to the list
        hemisphere_image_urls.append(hemispheres)    

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())