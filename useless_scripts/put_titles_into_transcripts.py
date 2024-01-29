import time
import feedparser
import json
import os.path
import re

dt=time.time()

YOUR_PATREON_RSS=""

directory = os.fsencode("F:\Code\podaboutlist\\testfolder")

fileList = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    fileList.append(filename)


d = feedparser.parse('https://anchor.fm/s/da4e26b0/podcast/rss')

print("Loaded RSS (took %ss)" % str(time.time()-dt))
dt=time.time()

for i in d.entries:
    
    dirty = i.title
    clean = re.sub(r"[^(A-z0-9)]", "", dirty)
    
    clean = re.sub(r"[()]", "", clean)
    clean+=".json"
    if "teaser" in i.title.lower() or "unlocked" in i.title.lower():
        #print("Skipped episode \"%s\": Teaser for or unlocked premium episode." % clean)
        continue
    success = False
    for j in fileList:
        if clean==j:
            success=True
            filename = os.path.join(os.fsdecode(directory), j)
            raw_data = None
            with open(filename, 'r+', encoding='utf-8') as json_file:
                raw_data = json.load(json_file)
                raw_data.insert(0, {"episode_title": i.title})
                print(raw_data[0]["episode_title"])
                json_file.seek(0)
                json.dump(raw_data, json_file)
            #print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            #input()
    if not success:
        print(" Couldnt find  \"%s\": " % clean)
        #input()


d = feedparser.parse(YOUR_PATREON_RSS)

for i in d.entries:
    
    dirty = i.title
    clean = re.sub(r"[^(A-z0-9)]", "", dirty)
    
    clean = re.sub(r"[()]", "", clean)
    clean+=".json"
    success = False
    for j in fileList:
        if clean==j:
            success=True
            filename = os.path.join(os.fsdecode(directory), j)
            raw_data = None
            with open(filename, 'r+', encoding='utf-8') as json_file:
                raw_data = json.load(json_file)
                raw_data.insert(0, {"episode_title": i.title})
                print(raw_data[0]["episode_title"])
                json_file.seek(0)
                json.dump(raw_data, json_file)
            #print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
            #input()
    if not success:
        print(" Couldnt find  \"%s\": " % clean)
        #input()