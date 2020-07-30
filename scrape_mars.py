from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time

def scrape():
    #initialize chrome driver
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path,headless = True)

    #Create empty dictionary to store all data in
    mars_dict = {}
    
    #Scrape data from Nasa News Page
    try:
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)
        browser.links.find_by_partial_text('Next')

        html = browser.html
        # Create a Beautiful Soup object
        soup = bs(html,'html.parser')
        
        #collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
        news_title = soup.find_all('li',class_='slide')[0].find(class_='content_title').text
        news_p = soup.find_all('li',class_='slide')[0].text

        mars_dict['news_title'] = news_title
        mars_dict['news_p'] = news_p
    except: 
        print(f"Could not pull data from {url}")
    
    #Scrape feautured mars image 
    try:
        pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(pic_url)

        #click on the 'full image' button to view featured image
        browser.find_by_id('full_image').click()
        time.sleep(4)
        pic = browser.html

        # Create a Beautiful Soup object
        soup = bs(pic,'html.parser')

        featured_image_url = "https://www.jpl.nasa.gov" + soup.find_all('img',class_='fancybox-image')[0]['src']

        mars_dict['featured_image_url'] = featured_image_url
    except: 
        print(f"Could not pull data from {pic_url}")
        
    #Scrape the latest weather data from Mars Weather twitter account 
    try:
        twit_url= "https://twitter.com/marswxreport?lang=en"
        browser.visit(twit_url)

        browser.links.find_by_partial_text('Next')

        twit = browser.html

        soup_twit = bs(twit,'html.parser')

        weather = soup_twit.find('article',class_="css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-o7ynqc r-6416eg").text
        mars_weather = weather.strip().replace('Mars Weather@MarsWxReport·9hInSight ','')

        mars_dict['mars_weather'] = mars_weather
    except: 
        print(f"Could not pull data from {twit_url}")
    
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    try: 
        url3 = "https://space-facts.com/mars/"

        table = pd.read_html(url3)
        df = table[0]
        df.columns = ['Description','Value']
        df.set_index('Description', inplace=True)
    
        #Use Pandas to convert the data to a HTML table string.
        html_table =df.to_html()
        #Get rid of new line symbols
        new_table = html_table.replace('\n', '')
        new_table

        mars_dict['html_table'] = new_table
    except: 
        print(f"Could not pull data from {url3}")
     
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the 
    #hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    try:
        url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url4)
        browser.links.find_by_partial_text('Next')

        hem = browser.html

        soup_hem = bs(hem,'html.parser')

        #Create empty dictionary of lists
        hem_dict = []
        data = soup_hem.find_all('div',class_="description")

        for item in data:
            highres_url = f"https://astrogeology.usgs.gov{item.find('a')['href']}"
            highres = browser.visit(highres_url)
            highres = browser.html
    
            soup_highres = bs(highres,'html.parser')
    
            highres_img = soup_highres.find_all('div',class_='downloads')[0].find('a')['href']
    
            title = item.find('h3').text
            hem_dict.append({"title": title, "img_url": highres_img})
        mars_dict['hemisphere_image_urls']=hem_dict
    except:
        print(f"Could not pull data from {url4}")
              
           
    return mars_dict

        
        