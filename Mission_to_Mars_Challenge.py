# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
chromedriver_path = '../chromedriver_win32/chromedriver.exe'
executable_path = {'executable_path': chromedriver_path}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide') #slide_elem is the parent element

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('http://space-facts.com/mars/')[0]
df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()


# ### Mars Weather

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# Parse the resulting html with soup
html = browser.html
hemisph_soup = soup(html, 'html.parser')

# 3. Write code to retrieve the image urls and titles for each hemisphere.
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
    
    #Find the title inside an h2 tag with a class of 'title'
    title = download_soup.find('h2', class_='title').get_text()
    
    #Find the image url (href) inside a li tag
    img_url = download_soup.find('li').a['href']
    
    # Store data in a dictionary
    hemispheres = {
        'img_url': img_url,
        'title': title
    }
    #Append the dictionary to the list
    hemisphere_image_urls.append(hemispheres)    

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()