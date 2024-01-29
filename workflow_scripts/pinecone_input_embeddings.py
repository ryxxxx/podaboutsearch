'''
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
import os
import json

CLUSTER_ENDPOINT="https://in03-2ef085b7f87df23.api.gcp-us-west1.zillizcloud.com" # Set your cluster endpoint
TOKEN="f65037110893afe48bc3c7f6fec8e1aeb66f2ad32ef1e93dc701bcb229c07f66e243c61d070e454101e4b40f5fb8040fc13cbb5a" # Set your token
COLLECTION_NAME="podaboutlist_transcripts" # Set your collection name

# Initialize a MilvusClient instance
# Replace uri and token with your own
connections.connect(
    alias='default',
    uri="https://in03-2ef085b7f87df23.api.gcp-us-west1.zillizcloud.com", # Cluster endpoint obtained from the console
    token="f65037110893afe48bc3c7f6fec8e1aeb66f2ad32ef1e93dc701bcb229c07f66e243c61d070e454101e4b40f5fb8040fc13cbb5a" # API key or a colon-separated cluster username and password
)

# 1. Define fields
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),   
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1024)
]

# 2. Build the schema
schema = CollectionSchema(
    fields,
    description="Schema for podaboutlist transcripts",
    enable_dynamic_field=False
)

# 3. Create collection
collection = Collection(
    name=COLLECTION_NAME, 
    description="Podaboutlist transcripts",
    schema=schema
)
'''
import os
import json
from pinecone import Pinecone, PodSpec

YOUR_API_KEY=""

pc = Pinecone(api_key=YOUR_API_KEY)

pc.create_index(
  name="podaboutlist",
  dimension=384,
  metric="cosine",
  spec=PodSpec(
    environment="gcp-starter"
  )
)

index = pc.Index("pod-index")

#prepare data
directory = os.fsencode("F:/Code/podaboutlist/just_texts")    
id=1

for file in os.listdir(directory):
    filename = os.path.join(os.fsdecode(directory), os.fsdecode(file))
    
    data=[]

    with open(filename, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

        assert len(json_data["text"]) == len(json_data["embeddings"])
        for i in range(len(json_data["text"])):
            id+=1
            data.append({
                "id":str(id),
                "values":json_data["embeddings"][i],
                "metadata":{"title": json_data["title"], "text": json_data["text"][i]}
            })

    index.upsert(vectors=data)
    print("done with file: " + filename)

