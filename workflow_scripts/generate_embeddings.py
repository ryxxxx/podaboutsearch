import os
import requests
import json
import time

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('thenlper/gte-small')


def embed(texts):
    return model.encode(texts)

target_directory = os.fsencode("F:/Code/podaboutlist/just_texts")    
src_directory = target_directory


dt=time.time()
for file in os.listdir(src_directory):
    dt=time.time()
    filename = os.path.join(os.fsdecode(src_directory), os.fsdecode(file))
    maxStringLength=300
    chunkPercent=0.1
    prev=""
    next=""
    raw_data = None

    with open(filename, 'r+', encoding='utf-8') as json_file:
        raw_data = json.load(json_file)
        raw_text = raw_data["text"]
        chunks = []

        while raw_text!="":
            chunks.append(raw_text[:maxStringLength+int(maxStringLength*chunkPercent*2)])
            if(len(raw_text)>maxStringLength+int(maxStringLength*chunkPercent)):
                raw_text=raw_text[maxStringLength+int(maxStringLength*chunkPercent):]
            else:
                raw_text=""

        
        if raw_data.get("embeddings")==None:
            embeddings = embed(chunks).tolist()
            raw_data["embeddings"] = embeddings

        raw_data["text"] = chunks

        json_file.seek(0)
        json.dump(raw_data, json_file)

    print("Done with file " + filename + " in " + str(time.time()-dt) +  "s")














'''
    with open(filename, 'r', encoding='utf-8') as json_file:
        raw_data = json.load(json_file)
        for cur, next in zip(raw_data, raw_data[1:]+ [None]):
            if cur.get("embeddings"):
                continue
            text = cur["text"]
            if next!=None:
                afterChunk = next["text"][:int(len(next["text"])*chunkPercent)-len(next["text"])]
            else:
                afterChunk=""
            text = beforeChunk + text + afterChunk
            textsToEmbed = []

            while(len(text)>maxStringLength):
        
                substring = text[:maxStringLength-len(text)]
                text = text[maxStringLength:]

                afterChunk = text[:int(len(text)*chunkPercent)-len(text)]

                textsToEmbed.append(beforeChunk + substring + afterChunk)
                
                beforeChunk=substring[len(substring)-int(len(substring)*chunkPercent):]
          
            textsToEmbed.append(text)

            for i in textsToEmbed:
                if(len(i)>400):
                    print(i)

            embeddings = embed(textsToEmbed).tolist()

            cur["embeddings"] = embeddings

            beforeChunk=cur["text"][len(cur["text"])-int(len(cur["text"])*chunkPercent):]

    with open(os.path.join(os.fsdecode(target_directory), os.path.split(filename)[1]), 'w', encoding='utf-8') as json_file:
        json.dump(raw_data, json_file)
    
    print("Finished file \'%s\' in %ss"%(filename, str(time.time()-dt)))
'''