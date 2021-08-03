from splinter import Browser
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit first URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    headlines = soup.find_all('div', class_='content_title')
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    headlines_list = []
    paragraph_list = []

    for category in headlines:
        title = category.text.strip()
        headlines_list.append(title)

    for category in paragraphs:
        para = category.text.strip()
        paragraph_list.append(para)

    #Getting info from URL 2:
    url_2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_2)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    featured_image = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + featured_image)

    # Getting the HTML table
    import pandas as pd
    url_3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_3)
    df = tables[1]
    new_df = df[['Mars - Earth Comparison', 'Mars']]
    new_df.rename(columns = {'Mars - Earth Comparison': ' Mars Facts', 'Mars':'Measurements'}, inplace=True)
    table_string = new_df.to_html()

    # Last URL info
    url_4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_4)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    sidebar = soup.find_all('a', class_='itemLink product-item')
    new = soup.find_all('h3')
    new_sidebar = []
    new_sidebar = (sidebar[0], sidebar[2], sidebar[4], sidebar[6])

    hemisphere_image_urls = []

    for category in range(4):
        title = new[category].text
        image = new_sidebar[category]['href']
        browser.visit(f'https://astrogeology.usgs.gov{image}')
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        hemisphere = soup.find('img', class_='wide-image')['src']
        hemi_list = f'https://astrogeology.usgs.gov{hemisphere}'
        title_image_dict = {"title": title, "img_url":hemi_list}
        hemisphere_image_urls.append(title_image_dict)
        browser.back()

    mars_data = {
        'headlines': headlines_list,
        'paragraphs': paragraph_list,
        'featured_image': featured_image_url,
        'html_info': table_string,
        'hemi_images': hemisphere_image_urls
    }




    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
