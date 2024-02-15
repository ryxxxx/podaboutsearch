import os
import srt
import voyageai
import time
import json
from pathlib import Path
from datetime import timedelta

vo = voyageai.Client(api_key="API_KEY")

max_token_count = 400
max_overlap_token_count = 150

def serialize_datetime(obj):
    if isinstance(obj, timedelta): 
        return obj.total_seconds()
    raise TypeError ("Type %s not serializable" % type(obj))

def generate_chunks(srt_file):
    srt_data = srt.parse(srt_file)
    srt_list = []
    for i in srt_data:
        token_count = vo.count_tokens([i.content+" "])
        srt_list.append({
            "text":i.content + " ",
            "start":i.start,
            "end":i.end,
            "token_count":token_count
            })
    
    chunks = []

    current_chunk = {
            "text":"",
            "start":None,
            "end":None,
            "token_count":0
            }
    last_chunk_lines = []
    current_chunk_lines = []

    i=0
    while i < len(srt_list):
        current_line = srt_list[i]
        
        #chunk is full
        if current_chunk["token_count"] + current_line["token_count"]>max_token_count:
            #add overlap with last chunk
            overlap_last_chunk =""
            temp_token_count=0
            for j in range(len(last_chunk_lines)-1, 0, -1):
                if temp_token_count + last_chunk_lines[j]["token_count"] > max_overlap_token_count:
                    break
                overlap_last_chunk = last_chunk_lines[j]["text"] + overlap_last_chunk
                temp_token_count += last_chunk_lines[j]["token_count"]
            current_chunk["text"] = overlap_last_chunk + current_chunk["text"]
            current_chunk["token_count"] += temp_token_count

            last_chunk_lines = current_chunk_lines
            current_chunk_lines = []

            #add overlap with next chunk
            overlap_next_chunk=""
            temp_token_count=0
            k = 0
            while i+k < len(srt_list) and temp_token_count+srt_list[i+k]["token_count"]<max_overlap_token_count:
                overlap_next_chunk += srt_list[i+k]["text"]
                temp_token_count += srt_list[i+k]["token_count"]
                k+=1
            current_chunk["text"] += overlap_next_chunk
            current_chunk["token_count"] += temp_token_count

            chunks.append(current_chunk)
            current_chunk = {
                "text":"",
                "start":None,
                "end":None,
                "token_count":0
            }
            continue

        current_chunk["text"] += current_line["text"]
        current_chunk["token_count"] += current_line["token_count"]
        if current_chunk["start"] == None:
            current_chunk["start"] = current_line["start"]
        current_chunk["end"] = current_line["end"]

        current_chunk_lines.append(current_line)
        i+=1
    
    #final chunk

    overlap_last_chunk =""
    temp_token_count=0
    for j in range(len(last_chunk_lines)-1, 0, -1):
        if temp_token_count + last_chunk_lines[j]["token_count"] > max_overlap_token_count:
            break
        overlap_last_chunk = last_chunk_lines[j]["text"] + overlap_last_chunk
        temp_token_count += last_chunk_lines[j]["token_count"]
    current_chunk["text"] = overlap_last_chunk + current_chunk["text"]
    current_chunk["token_count"] += temp_token_count
    chunks.append(current_chunk)

    return chunks


def generate_embeddings(chunks):
    texts = []
    for i in chunks:
        texts.append(i["text"])
    result = vo.embed(texts, model="voyage-2", input_type="document")
    time.sleep(0.3)
    for i in range(len(chunks)):
        chunks[i]["embedding"]=result.embeddings[i]
    return chunks

transcript_directory = os.fsencode("F:/Code/podaboutlist/v2/transcripts_raw")
embeddings_directory = os.fsencode("F:/Code/podaboutlist/v2/transcripts_embeddings")        

for file in os.listdir(transcript_directory):
    srt_filename = os.path.join(os.fsdecode(transcript_directory), os.fsdecode(file))
    with open(srt_filename, 'r', encoding='utf-8') as srt_file:
        chunks = generate_chunks(srt_file)
        chunks_with_embeddings = generate_embeddings(chunks)
        
        json_filename=os.path.join(os.fsdecode(embeddings_directory), Path(srt_filename).stem + ".json")
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(chunks, json_file, default=serialize_datetime)
    print("done with " + srt_filename)
