import chromadb

client = chromadb.PersistentClient(path="F:/Code/podaboutlist/chroma_save")

from chromadb.utils import embedding_functions

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="thenlper/gte-large")

collection = client.get_or_create_collection(name="podaboutlist", embedding_function=sentence_transformer_ef)


while True:

    query = input("looking for an episode?")

    if query=="exit":
        break

    embedded_query = sentence_transformer_ef([query])

    result = collection.query(query_embeddings=embedded_query, n_results=15)

    for i in range(15):
        print(result["documents"][0][i])
        
        print(result["metadatas"][0][i])
        
        #print(result["distances"][0][i])
        print("---")
'''


import os
import json

directory = os.fsencode("F:\Code\podaboutlist\\testfolder")    

id=1

for file in os.listdir(directory):
    filename = os.path.join(os.fsdecode(directory), os.fsdecode(file))
    
    ids=[]
    embeddings=[]
    documents=[]
    metadatas=[]

    title=""
    with open(filename, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data:
            if title=="":
                title=i["episode_title"]
                continue
            for j in i["embeddings"]:
                embeddings.append(j)
                documents.append(title)
                metadatas.append({"start": i["start"], "end" : i["end"], "text": i["text"]})
                ids.append("id"+str(id))
                id+=1
    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print("done with file: " + filename)

'''