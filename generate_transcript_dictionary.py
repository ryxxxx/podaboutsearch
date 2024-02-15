import os
import json
from datetime import datetime
from functools import cmp_to_key

metadata_dir = os.fsencode("F:/Code/podaboutlist/v2/transcripts_metadata")

episode_list = []

id=1

for file in os.listdir(metadata_dir):
    meta_filename = os.path.join(os.fsdecode(metadata_dir), os.fsdecode(file))
    if not os.path.isfile(os.path.join("F:/Code/podaboutlist/v2/transcripts_embeddings", os.fsdecode(file))):
        continue
    metadata = None
    with open(meta_filename, 'r', encoding='utf-8') as meta_file:
        metadata = json.load(meta_file)
        episode_list.append({
            "title": metadata["title"],
            "link": metadata["link"],
            "date": metadata["published"],
            "id" : id
        })
    metadata["id"]=id
    with open(meta_filename, 'w', encoding='utf-8') as meta_file:
        json.dump(metadata, meta_file)
    id+=1

sorted_episodes = sorted(episode_list, key=lambda t: datetime.strptime(t["date"], '%a, %d %b %Y %H:%M:%S %Z'),reverse=True)

with open("F:/Code/podaboutlist/v2/transcript_list.json", 'w', encoding='utf-8') as transcript_dict:
        json.dump({"transcripts": sorted_episodes}, transcript_dict)