import os
import json

src_directory = os.fsencode("F:/Code/podaboutlist/display_transcripts_backup")
target_directory = "F:/Code/podaboutlist/display_transcripts"

chunk_size=300

for file in os.listdir(src_directory):
    filename = os.path.join(os.fsdecode(src_directory), os.fsdecode(file))
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        title=data["title"]
        content = data["content"]
        new_content = []
        i=0
        while i < len(content):
            curText = content[i]["text"]
            curTime = content[i]["start"]
            while len(curText)<chunk_size:
                if not i+1>=len(content) and len(curText+content[i+1]["text"])<chunk_size:
                    if curText[len(curText)-1]==' ' or content[i+1]["text"][0]==' ':
                        curText+=content[i+1]["text"]
                    else:
                        curText+=" " + content[i+1]["text"]
                    i+=1
                else:
                    break
            new_content.append({"text":curText, "start": curTime})
            i+=1
        
        with open(os.path.join(target_directory, os.fsdecode(file)), 'w', encoding='utf-8') as json_file: 
            json.dump({"title":title, "content":new_content}, json_file)
            print("done")



            