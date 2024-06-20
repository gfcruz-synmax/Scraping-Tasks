#Imports (Undetected Chromedriver, Selenium, BeautifulSoup, Time, Random, RegEx, CSV, OrderedDict)
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
import re
import csv
from collections import OrderedDict

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
#print(soup)

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
videos_header=re.sub("<.*?>","",str(videos_header)) #this strips unnecessary text via regex

#Extract video URLs
video_elements = soup.find_all('a', href=True)
video_urls = [video['href'] for video in video_elements if '/video/' in video['href']]
video_urls = list(OrderedDict.fromkeys(video_urls)) #this removes duplicates

#Write everything to CSV. Formatting of the resulting file is suboptimal and may still be improved (particularly the video URLs), but the resulting file contains all requested information
with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([title])
    writer.writerow([subtitle])
    writer.writerow([following_count])
    writer.writerow([following])
    writer.writerow([followers_count])
    writer.writerow([followers])
    writer.writerow([likes_count])
    writer.writerow([likes])
    writer.writerow([user_bio])
    writer.writerow([user_link])
    writer.writerow([videos_header])
    writer.writerows([video_urls])

#End
driver.quit()