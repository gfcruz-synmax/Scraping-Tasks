#Imports (Undetected Chromedriver, Selenium, BeautifulSoup, Time, Random, RegEx, CSV, OrderedDict, Pandas)
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import re
import csv
from collections import OrderedDict
import pandas as pd

#Set up Undetected Chromedriver
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

#Actual get request
url = "https://www.tiktok.com/@bongbong.marcos"
driver.get(url)

#Scroll down with randomized, humanlike pauses to avoid captcha interruption
time.sleep(random.uniform(6, 10))
scroll_pause_time = random.uniform(3, 5)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scroll_pause_time = random.uniform(3, 5)  # Randomize scroll pause time

#Parse page with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

#Extract all non-video information:
title = soup.find("h1", {"data-e2e":"user-title"}).get_text()
subtitle = soup.find("h2", {"data-e2e":"user-subtitle"}).get_text()
following_count = soup.find("strong", {"data-e2e":"following-count"}).get_text()
following = soup.find("span", {"data-e2e":"following"}).get_text()
followers_count = soup.find("strong", {"data-e2e":"followers-count"}).get_text()
followers = soup.find("span", {"data-e2e":"followers"}).get_text()
likes_count = soup.find("strong", {"data-e2e":"likes-count"}).get_text()
likes = soup.find("span", {"data-e2e":"likes"}).get_text()
user_bio = soup.find("h2", {"data-e2e":"user-bio"}).get_text()
user_bio = user_bio[:-2] #this removes the "PH" character that cannot be written onto the CSV file
user_link = soup.find("a", {"data-e2e":"user-link"}).get_text()
videos_header = soup.select("p", {"class":"css-12nr5wl-PPlaylistTitle eo04fh21"})[1] #there are 2 instances of this class in the code so it is necessary to get the 2nd instance only using select
videos_header = re.sub("<.*?>","",str(videos_header)) #this strips unnecessary text via regex

'''
#Comment out non-video data that do not need to be displayed, and then create a list of only the useful non-video information for ease of tabulation.
nonvideo=[]
nonvideo.append(title)
nonvideo.append(subtitle)
nonvideo.append(following_count)
#nonvideo.append(following)
nonvideo.append(followers_count)
#nonvideo.append(followers)
nonvideo.append(likes_count)
#nonvideo.append(likes)
nonvideo.append(user_bio)
nonvideo.append(user_link)
#nonvideo.append(videos_header)

#Also prepare a list of column names of non-video data
nonvideocol=["Username","Full Name","Following Count","Followers Count","Likes Count","Bio","Bio Link/s"]

#Write nonvideo results to pandas dataframe
df=pd.DataFrame([nonvideo],columns=nonvideocol)
'''

#Extract video URLs and convert them into a pandas series
video_elements = soup.find_all('a', href=True)
video_urls = [video['href'] for video in video_elements if '/video/' in video['href']]
video_urls = list(OrderedDict.fromkeys(video_urls)) #this removes duplicates
#video_urls = pd.Series(video_urls, name="Video URLs")

#Add video links as a new column to the existing pandas dataframe
#df=pd.concat([df, video_urls], axis=1)

#Create a dictionary containing all needed information and generate DataFrame
data = {"Username": title, "Full Name": subtitle, "Following Count": following_count, "Followers Count": followers_count, "Likes Count": likes_count, "Bio": user_bio, "Bio Link/s": user_link, "Video URLs": video_urls}
df = pd.DataFrame(data)

#Finally write pandas to CSV
df.to_csv('results3.csv')

#End
driver.quit()