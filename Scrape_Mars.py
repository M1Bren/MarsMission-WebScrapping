# Define all the functions for scrapping and organizing data for the MarsFLASK.py application.
# This data should be saved in MongoDB.

# import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs4
import pandas as pd
import time

# Direct Path to Chromedriver (Opens Website in Google Chrome)
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

# Define the scrape() function, which will combine all of the data previously scrapped
def scrape():
    info_dict = {}
    marsNews = marsNews()
    info_dict["Mars_Headline"] = marsNews[0]
    info_dict["Mars_Paragraph"] = marsNews[1]
    info_dict["Mars_Image"] = marsImage()
    info_dict["Mars_Weather"] = marsWeather()
    info_dict["Mars_Facts"] = marsFacts()
    info_dict["Mars_Hemispheres"] = marsHemipsheres()

    return info_dict

# NASA Mars News
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs4(html, "html.parser")
    title = soup.find("div", class_="content_title").text
    paragraph = soup.find("div", class_="article_teaser_body").text
    marsNews = [title, paragraph]

    return marsNews

# JPL Mars Space Images - Curiosity at Glen Etive
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs4(html, "html.parser")
    image = soup.find("img", alt="Curiosity at Glen Etive")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    return featured_image_url

# Mars Weather Tweet
def marsWeather():
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    soup = bs4(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    return mars_weather

# Mars Facts - Space Facts
def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_facts = pd.read_html(facts_url)
    mars_facts = pd.DataFrame(mars_facts[0])
    mars_facts.columns = ["Description", "Value"]
    mars_facts = mars_facts.set_index("Description")
    marsFacts_HTML = mars_facts.to_html(header = True, index = True)

    return marsFacts_HTML

# Mars Hemispheres Photos
def marsHemipsheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs4(html, "html.parser")
    hemisphere_image_urls = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs4(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
    return hemisphere_image_urls
