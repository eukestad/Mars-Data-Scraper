# dependencies
import pandas as pd
import datetime as dt
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def get_soup(url):
    # Initialize Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit URL
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    return browser, soup

def mars_news():
    # set url
    nmn_url = 'https://redplanetscience.com/'
    
    # get soup
    browser, soup = get_soup(nmn_url)

    # Retrieve news element
    news = soup.find('div', id='news')

    # get all list dates
    list_dates = news.find_all('div', class_='list_date')

    maxdate = max([dt.datetime.strptime(ldate.text.strip(), '%B %d, %Y') for ldate in list_dates])

    # get articles
    articles = news.find_all('div', class_='list_text')

    for article in articles:
        list_date = article.select_one(".list_date").text.strip()

        if dt.datetime.strptime(list_date, '%B %d, %Y') == maxdate:
            newsa = article
            news_title = newsa.select_one(".content_title").text.strip()
            news_p = newsa.select_one(".article_teaser_body").text.strip()
            
    # prepare output
    news_dict = {'title':news_title,
                    'lead_in':news_p}

    browser.quit()

    return news_dict

def featured_img():
    # set url
    spcimages_url = 'https://spaceimages-mars.com/'

    # get soup
    browser, soup = get_soup(spcimages_url)

    featured_image = soup.find('img', class_='headerimage fade-in')

    featured_image_url = spcimages_url + featured_image['src']

    browser.quit()
    
    return featured_image_url

def mars_facts():
    mf_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mf_url)
    df = tables[0]

    df.columns = ['','Mars','Earth']
    df = df.iloc[1:]
    df.set_index('', inplace=True)

    facts = df.to_dict()

    return facts

def hemispheres():
    # set url
    hms_url = 'https://marshemispheres.com/'

    # get soup
    browser, soup = get_soup(hms_url)

    items = soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for item in items:
        hmsphere = {}
        name = item.h3.text
        link = item.a['href']

        # get full image
        try:
            browser.links.find_by_partial_text(name).click()
            
            html2 = browser.html
            imgsoup = BeautifulSoup(html2, 'html.parser')
            imgsoup
            img = imgsoup.find('img', class_="wide-image")
            
            hmsphere['title'] = name[:-9]
            hmsphere['img_url'] = hms_url + img['src']
            
        except:
            print("Could not get Image Link")   
            
        hemisphere_image_urls.append(hmsphere)    
        browser.back()
        
    browser.quit()

    return hemisphere_image_urls

def scrape():

    results = {}

    # get Mars News
    results['latest_news'] = mars_news()

    # get featured image
    results['featured_img'] = featured_img()

    # get Mars Facts
    results['mars_facts'] = mars_facts()

    # get hemispheres
    results['hemispheres'] = hemispheres()

    return results

# if __name__ == "__main__":
#     scrape()