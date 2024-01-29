import time
import feedparser
import json
import os.path
import requests
import re

script_dir = os.path.dirname(__file__)
metadata_folder = os.path.join(script_dir, "metadata")
audio_folder = os.path.join(script_dir, "audio")
YOUR_PATREON_ACCESS =""

if not os.path.exists(metadata_folder):
    os.makedirs(metadata_folder)
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

normal_feed = feedparser.parse('https://anchor.fm/s/da4e26b0/podcast/rss')
premium_feed = feedparser.parse(YOUR_PATREON_ACCESS)

def fetch_from_feed(feed, premium=False):
    dt=time.time()
    for i in feed.entries:
        if not premium and ("teaser" in i.title.lower() or "unlocked" in i.title.lower()): # skip these for the normal feed
            continue
        title = i.title
        
        file_name = re.sub(r"[^A-Za-z0-9]", "", title)  # only latin letters for filename

        audio_file = os.path.join(audio_folder, file_name+".mp3") 
        if not os.path.isfile(audio_file): # skip already downloaded episodes
            link_to_file = i.links[1].href
            response = requests.get(link_to_file)
            response.raise_for_status()
            with open(audio_file, 'wb') as file:
                file.write(response.content)

        metadata_file = os.path.join(metadata_folder, file_name+".json") 
        if not os.path.isfile(metadata_file): # skip already generated metadata
            metadata = {
                "title" : i.title,
                "link" : i.link,
                "published" : i.published
            }
            with open(metadata_file, 'w') as file:
                json.dump(metadata, file)

        print("Fetched episode \"%s\" (took %ss)" % (title, str(time.time()-dt)))
        dt=time.time()

fetch_from_feed(normal_feed)
fetch_from_feed(premium_feed, True)