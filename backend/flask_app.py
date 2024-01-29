# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import torch
torch.set_num_threads(1)

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('thenlper/gte-small')

import requests
import json

'''
@app.route('/embed/', methods=['GET'])
@cross_origin()
def embed_query():
    query = request.args.get('arg')
    embeddings = model.encode([query]).tolist()
    return jsonify(embeddings[0])

@app.route('/query/', methods=['GET'])
@cross_origin()
def query_transcripts():
    query = request.args.get('arg')

    url = "https://podaboutlist-1uwwj7r.svc.gcp-starter.pinecone.io/query"
    headers = {
        "Api-Key":"PINECONE_API_KEY",
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "topK": 10,
        "vector": query,
        "includeValues": "false",
        "includeMetadata": "true"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
'''

@app.route('/query', methods=['GET'])
@cross_origin()
def test():
    query = request.args.get('arg')
    embeddings = model.encode([query]).tolist()

    url = "https://podaboutlist-1uwwj7r.svc.gcp-starter.pinecone.io/query"
    headers = {
        "Api-Key":"PINECONE_API_KEY",
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "topK": 10,
        "vector": embeddings[0],
        "includeValues": "false",
        "includeMetadata": "true"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


import re
import os

@app.route('/transcript', methods=['GET'])
@cross_origin()
def get_transcript():
    transcript_name = request.args.get('arg')
    transcript_name = re.sub(r"[^(A-z0-9)]", "", transcript_name)
    transcript_name = re.sub(r"[()]", "", transcript_name)
    transcript_name = "public/display_transcripts/" + transcript_name + ".json"
    my_dir = os.path.dirname(__file__)
    file_location = os.path.join(my_dir, transcript_name)
    if os.path.isfile(file_location):
        json_data=None
        with open(file_location, 'r', encoding='utf-8') as json_file:
            json_data=json.load(json_file)
        return json_data
    else:
        return json.dumps({"Error": transcript_name})