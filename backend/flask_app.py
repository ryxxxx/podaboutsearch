from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests
import json
import voyageai
import os
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import select

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
SQLALCHEMY_DATABASE_URI = "URI_HERE"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Base(DeclarativeBase):
    pass

class TranscriptChunk(Base):
    __tablename__ = "transcripts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(4096))


@app.route('/v2search/', methods=['GET'])
@cross_origin()
def v2_search():
    query = request.args.get('arg')

    literals = re.findall('"([^"]*)"', query)
    literal_results=[]

    if len(literals)>0:
        stmt = select(TranscriptChunk).where(TranscriptChunk.content.ilike("%"+literals[0]+"%"))
        i=1
        while i<len(literals):
            stmt = stmt.where(TranscriptChunk.content.ilike("%"+literals[i]+"%"))
            i+=1
        for id in db.session.scalars(stmt):
            literal_results.append(str(id.id))

    embeddings = vo.embed([query], model="voyage-2", input_type="query")

    url = "https://podcast-1uwwj7r.svc.gcp-starter.pinecone.io/query"
    headers = {
        "Api-Key":"API_HERE",
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "topK": 20,
        "vector": embeddings.embeddings[0],
        "includeValues": "false",
        "includeMetadata": "true",
        "filter": {
            "unique_id": {"$in": literal_results}
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

@app.route('/transcript/', methods=['GET'])
@cross_origin()
def transcript():
    transcript_name = request.args.get('arg')
    transcript_name = re.sub(r"[^A-z0-9]", "", transcript_name)
    transcript_name = "transcripts/" + transcript_name + ".json"
    my_dir = os.path.dirname(__file__)
    file_location = os.path.join(my_dir, transcript_name)
    if os.path.isfile(file_location):
        json_data=None
        with open(file_location, 'r', encoding='utf-8') as json_file:
            json_data=json.load(json_file)
        return json_data
    else:
        return json.dumps({"File does not exist: ": file_location})

@app.route('/transcript_list/', methods=['GET'])
@cross_origin()
def transcript_list():
    my_dir = os.path.dirname(__file__)
    file_location = os.path.join(my_dir, "transcript_list.json")
    json_data=None
    with open(file_location, 'r', encoding='utf-8') as json_file:
        json_data=json.load(json_file)
    return json_data
