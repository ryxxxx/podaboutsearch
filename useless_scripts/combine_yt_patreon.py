import os
import re
import json
from pathlib import Path

title_directory = os.fsencode("F:/Code/podaboutlist/testfolder")
source_directory = os.fsencode("F:/Code/podaboutlist/json_transcripts")
yt_directory = os.fsencode("F:/Code/podaboutlist/json_transcripts_yt")
target_directory = os.fsencode("F:/Code/podaboutlist/display_transcripts")

yt_eps_found = {}

for file in os.listdir(source_directory):
    filename = os.fsdecode(file)

    filename = Path(filename).stem
    #print(filename)
    filename=re.sub(r"[^(A-z)]", "", filename) + ".json"
    check_path = os.path.join(os.fsdecode(yt_directory), filename)

    if os.path.isfile(check_path):
        yt_eps_found[os.fsdecode(file)] = filename
    else:
        check_path = os.path.join(os.fsdecode(yt_directory), filename[2:])
        if os.path.isfile(check_path):
            yt_eps_found[os.fsdecode(file)] = filename[2:]
        else:
            check_path = os.path.join(os.fsdecode(yt_directory), "unlocked"+filename)
            if os.path.isfile(check_path):
                yt_eps_found[os.fsdecode(file)] = "unlocked"+filename
            else:
                for i in range(5, len(filename)):
                    check_path = os.path.join(os.fsdecode(yt_directory), filename[:-i]+".json")
                    if os.path.isfile(check_path):
                        yt_eps_found[os.fsdecode(file)] = filename[:-i]+".json"

    #else:
        #print("failure")
    #print("____________")
    #print("")
                        


for file in os.listdir(title_directory):
    filename = os.fsdecode(file)
    
    
    episode_title=""
    episode_content=[]

    with open(os.path.join(os.fsdecode(title_directory), filename), 'r', encoding='utf-8') as json_file:
        raw_data = json.load(json_file)
        episode_title = raw_data[0]["episode_title"]

    transcript_filename=filename
    which_dir=source_directory
    yt_ep_tst= yt_eps_found.get(filename)
    if yt_ep_tst!=None:
        transcript_filename=yt_ep_tst
        which_dir=yt_directory

    with open(os.path.join(os.fsdecode(which_dir), transcript_filename), 'r', encoding='utf-8') as json_file:
        raw_data = json.load(json_file)
        for i in raw_data:
            episode_content.append({"start": i["start"], "text":i["text"]})

    with open(os.path.join(os.fsdecode(target_directory), filename), 'w', encoding='utf-8') as json_file:
        json.dump({"title": episode_title, "content": episode_content}, json_file)

    #with open(os.path.join(os.fsdecode(target_directory), rss),"w", encoding="utf-8") as new_file:
