import os
import json
from pinecone import Pinecone, PodSpec

YOUR_API_KEY="API_KEY"

pc = Pinecone(api_key=YOUR_API_KEY)

index = pc.Index("podcast", "https://podcast-1uwwj7r.svc.gcp-starter.pinecone.io")

transcript_directory = os.fsencode("F:/Code/podaboutlist/v2/transcripts_embeddings")
metadata_directory = os.fsencode("F:/Code/podaboutlist/v2/transcripts_metadata")
id=1

for file in os.listdir(transcript_directory):
    transcript_filename = os.path.join(os.fsdecode(transcript_directory), os.fsdecode(file))
    metadata_filename = os.path.join(os.fsdecode(metadata_directory), os.fsdecode(file))

    title=""
    link=""
    date=""
    transcript_id=""

    with open(metadata_filename, 'r', encoding='utf-8') as metadata_file:
        metadata = json.load(metadata_file)      
        title=metadata["title"]
        link=metadata["link"]
        date=str(metadata["published"])
        transcript_id=metadata["id"]

    upsert_data=[]

    with open(transcript_filename, 'r', encoding='utf-8') as transcript_file:
        transcript = json.load(transcript_file)

        for i in transcript:
            id+=1
            upsert_data.append({
                "id":str(id),
                "values":i["embedding"],
                "metadata":{"unique_id": str(id), "transcript_id": transcript_id, "title":title, "link":link, "date":date, "text": i["text"], "start": i["start"], "end": i["end"]}
            })

    index.upsert(vectors=upsert_data)
    print("done with file: " + transcript_filename)

