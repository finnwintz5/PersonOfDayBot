from keep_alive import keep_alive
import tweepy
from bs4 import BeautifulSoup
import requests
import time
import random

# INITIALIZE ACCESS
API_KEY = 'api key here'
API_KEY_SECRET = 'secret api key here'

BEARER_TOKEN = 'bearer token here'

ACCESS_TOKEN = 'access token here'
ACCESS_TOKEN_SECRET = 'secret access token here'


def getClient():
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=API_KEY,
                           consumer_secret=API_KEY_SECRET,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)
    return client


client = getClient()

url = "https://www.biography.com/people"
bio_url = "https://www.biography.com"
repeat_count = 0
tweeted_people = []

def get_person(content, i):
    html_block = str(content[i])
    temp_name = html_block.split('role="heading">', 1)
    person = temp_name[1].split('</h2>')[0]
    return person


def get_url(content, i):  # i is the index to begin loop at
    # First five are not characters.
    html_block = str(content[i])  # List of divs -> str
    temp_path = html_block.split('href="', 1)  # Single out the url
    path = temp_path[1].split('" onclick=', 1)[0]
    people_url = bio_url + path  # Full path
    return people_url


keep_alive()
time.sleep(28800)
# INFINITE LOOP
while True:
  # handles case where all people on main page have been previously tweeted
  if repeat_count>24:
    tweet_text = "Today's person of the day is YOU! 😄 That's it for @personofday bot!"
    client.create_tweet(text=tweet_text)
    break
  web_stuff = requests.get(url)
  html = web_stuff.text
  soup = BeautifulSoup(html, "html.parser")
  people_content = soup.find_all("phoenix-ellipsis", class_="m-ellipsis m-card--header")
  people_length = len(people_content)
  rand_int = random.randint(0, people_length - 1)
  p_name = get_person(people_content, rand_int)
  p_url = get_url(people_content, rand_int)
  if p_name not in tweeted_people:
    repeat_count = 0
    # tweet this randomly selected person and wait until tomorrow
    tweet_text = "Today's person of the day is " + p_name + "! 😄 " + p_url
    client.create_tweet(text=tweet_text)
    tweeted_people.append(p_name)
    time.sleep(86400)
  else:
    # if person has already been tweeted, try again (until repeat_count > 24)
    repeat_count += 1
